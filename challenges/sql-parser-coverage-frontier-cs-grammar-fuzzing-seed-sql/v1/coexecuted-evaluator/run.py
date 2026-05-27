from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

ENV_PROJECT_DIR = "evaluator-env"
ENV_ACTIVE = "AGENTICS_EVALUATOR_ENV_ACTIVE"
MAX_LOG_CHARS = 4000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agentics wrapper for the Frontier-CS SQL seed coverage evaluator")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--workspace-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--setup-dir")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_runtime_cache(output_path.parent)
    maybe_reexec_with_setup_python(args)

    challenge_dir = Path(args.challenge_dir).resolve()
    workspace_dir = Path(args.workspace_dir).resolve()
    declared_metrics = declared_metric_names(challenge_dir)
    logs: list[str] = []
    try:
        config = load_mode_config(challenge_dir, args.mode)
        with captured_logs(logs):
            result = run_source_evaluator(config, challenge_dir, workspace_dir)
    except Exception as exc:  # noqa: BLE001 - result.json must explain evaluator failures.
        error = str(exc) if args.mode == "validation" else "official evaluation failed"
        result = {"score": 0.0, "runs_successfully": 0.0, "error": error}
    write_agentics_result(output_path, args.mode, result, logs, declared_metrics)
    return 0


def configure_runtime_cache(output_root: Path) -> None:
    tmp_root = output_root / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HOME", str(output_root))
    os.environ.setdefault("TMPDIR", str(tmp_root))
    os.environ.setdefault("XDG_CACHE_HOME", str(tmp_root / "cache"))
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")


def maybe_reexec_with_setup_python(args: argparse.Namespace) -> None:
    if os.environ.get(ENV_ACTIVE) == "1" or not args.setup_dir:
        return
    venv_python = Path(args.setup_dir) / ENV_PROJECT_DIR / ".venv" / "bin" / "python"
    if not venv_python.is_file():
        return
    env = os.environ.copy()
    env[ENV_ACTIVE] = "1"
    os.execve(str(venv_python), [str(venv_python), *sys.argv], env)


def load_mode_config(challenge_dir: Path, mode: str) -> dict[str, Any]:
    path = challenge_dir / ("public/config.json" if mode == "validation" else "private-benchmark/config.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("mode config must be a JSON object")
    return payload


def declared_metric_names(challenge_dir: Path) -> set[str]:
    payload = json.loads((challenge_dir / "spec.json").read_text(encoding="utf-8"))
    metrics = payload.get("metric_schema", {}).get("metrics", [])
    return {metric["name"] for metric in metrics if isinstance(metric, dict) and isinstance(metric.get("name"), str)}


@contextlib.contextmanager
def captured_logs(logs: list[str]):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        yield
    text = (stdout.getvalue() + "\n" + stderr.getvalue()).strip()
    if text:
        logs.append(truncate(text))


def import_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"failed to import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_source_evaluator(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_sql_seed_evaluator")
    evaluator = source.Evaluator(str(challenge_dir))
    evaluator.time_budget_seconds = float(config.get("time_budget_sec", evaluator.time_budget_seconds))
    return evaluator.evaluate(str(workspace_dir / "solution.py"))


def write_agentics_result(output_path: Path, mode: str, result: dict[str, Any], logs: list[str], declared_metrics: set[str]) -> None:
    score = finite(result.get("score", 0.0))
    error = result.get("error")
    runs_successfully = finite(result.get("runs_successfully", 1.0))
    passed = error is None and runs_successfully > 0
    metrics = collect_metrics(result, score, passed, declared_metrics)
    summary_key = "validation_summary" if mode == "validation" else "official_summary"
    payload: dict[str, Any] = {
        "status": "passed" if passed else "failed",
        "mode": mode,
        "rank_score": score,
        "aggregate_metrics": metrics,
        summary_key: {"score": score, "passed": 1 if passed else 0, "total": 1},
        "logs": [truncate(item) for item in logs[:4]],
    }
    if error is not None:
        payload["logs"].append(truncate(str(error)))
    if mode == "validation":
        payload["public_results"] = [
            {
                "case_name": "public-validation",
                "status": payload["status"],
                "score": score,
                "message": truncate(str(error or "ok"), 500),
            }
        ]
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def collect_metrics(result: dict[str, Any], score: float, passed: bool, declared_metrics: set[str]) -> list[dict[str, float | str]]:
    values: dict[str, float] = {}
    for name, value in {
        "score": score,
        "runs_successfully": finite(result.get("runs_successfully", 1.0)),
        "correctness": 1.0 if passed else 0.0,
    }.items():
        if name in declared_metrics:
            values[name] = value
    for key, value in result.items():
        if key in values or key in {"error", "traceback"} or key not in declared_metrics:
            continue
        if isinstance(value, bool):
            values[key] = 1.0 if value else 0.0
        elif isinstance(value, (int, float)) and math.isfinite(float(value)):
            values[key] = float(value)
    return [{"metric_name": key, "value": value} for key, value in values.items()]


def finite(value: Any) -> float:
    try:
        number = float(value)
    except Exception:
        return 0.0
    return number if math.isfinite(number) else 0.0


def truncate(value: str, limit: int = MAX_LOG_CHARS) -> str:
    value = value.replace("\x00", "")
    if len(value) <= limit:
        return value
    return value[:limit] + "... [truncated]"


if __name__ == "__main__":
    raise SystemExit(main())
