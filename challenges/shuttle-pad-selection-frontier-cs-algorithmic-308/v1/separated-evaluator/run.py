from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

PARTIAL_EXIT_CODE = 7
POINTS_RE = re.compile(r"\bpoints\s+([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score a migrated Frontier-CS Testlib checker challenge")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    try:
        payload = load_json(path)
    except Exception:
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return payload if isinstance(payload, dict) else {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}


def clamp01(value: float) -> float:
    if not math.isfinite(value):
        return 0.0
    return max(0.0, min(1.0, value))


def text_from_run(run: dict[str, Any], challenge_dir: Path, text_key: str, path_key: str) -> str:
    value = run.get(text_key)
    if isinstance(value, str):
        return value
    path = run.get(path_key)
    if isinstance(path, str):
        return (challenge_dir / path).read_text(encoding="utf-8")
    return ""


def compile_checker(challenge_dir: Path, work_dir: Path) -> Path:
    evaluator_dir = challenge_dir / "separated-evaluator"
    source = evaluator_dir / "chk.cc"
    binary = work_dir / "checker"
    compiler = shutil.which("g++") or shutil.which("c++")
    if compiler is None:
        raise RuntimeError("trusted evaluator image does not provide g++ or c++")
    command = [
        compiler,
        "-std=c++17",
        "-O2",
        "-pipe",
        f"-I{evaluator_dir}",
        str(source),
        "-o",
        str(binary),
    ]
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"checker compilation failed: {details[:2000]}")
    return binary


def checker_points(result: subprocess.CompletedProcess[str]) -> tuple[float, str]:
    combined = "\n".join(part for part in [result.stderr, result.stdout] if part)
    match = POINTS_RE.search(combined)
    if match:
        return clamp01(float(match.group(1))), combined.strip()
    if result.returncode == 0:
        return 1.0, combined.strip() or "accepted"
    return 0.0, combined.strip() or f"checker exited with code {result.returncode}"


def score_run(
    run: dict[str, Any],
    checker: Path,
    challenge_dir: Path,
    solution_runs_dir: Path,
    scratch_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    run_name = str(run["run_name"])
    run_dir = solution_runs_dir / run_name
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0) or 0)
    base: dict[str, Any] = {"case_name": run_name, "wall_time_ms": wall_time_ms}

    if metadata.get("timed_out") is True:
        return {**base, "status": "error", "score": 0.0, "message": "solution timed out"}, [f"{run_name}: solution timed out"]
    if metadata.get("exit_code", 0) != 0:
        return {**base, "status": "error", "score": 0.0, "message": f"solution exited with code {metadata.get('exit_code')}"}, [f"{run_name}: nonzero solution exit"]

    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return {**base, "status": "error", "score": 0.0, "message": "missing stdout.txt"}, [f"{run_name}: missing stdout.txt"]

    case_dir = scratch_dir / run_name
    case_dir.mkdir(parents=True, exist_ok=True)
    input_path = case_dir / "input.txt"
    answer_path = case_dir / "answer.txt"
    input_path.write_text(text_from_run(run, challenge_dir, "stdin_text", "input_path"), encoding="utf-8")
    answer_path.write_text(text_from_run(run, challenge_dir, "answer_text", "answer_path"), encoding="utf-8")

    try:
        result = subprocess.run(
            [str(checker), str(input_path), str(stdout_path), str(answer_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        return {**base, "status": "failed", "score": 0.0, "message": "checker timed out"}, [f"{run_name}: checker timed out"]

    ratio, message = checker_points(result)
    score = round(100.0 * ratio, 6)
    if result.returncode in (0, PARTIAL_EXIT_CODE):
        status = "passed"
        log = f"{run_name}: score={score}; {message[:500]}"
    else:
        status = "failed"
        score = 0.0
        ratio = 0.0
        log = f"{run_name}: checker rejected output: {message[:500]}"
    return {
        **base,
        "status": status,
        "score": score,
        "ratio": round(ratio, 8),
        "checker_exit_code": result.returncode,
        "message": message[:1000],
    }, [log]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    valid = sum(1 for result in results if result.get("status") == "passed")
    score = round(sum(float(result.get("score", 0.0)) for result in results) / total, 6) if total else 0.0
    return {"score": score, "valid_cases": valid, "total_cases": total, "passed": valid, "total": total}


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    runs = load_json(Path(args.runs_file))["runs"]
    results: list[dict[str, Any]] = []
    logs: list[str] = []

    with tempfile.TemporaryDirectory(prefix="frontier-checker-") as tmp:
        tmp_path = Path(tmp)
        try:
            checker = compile_checker(challenge_dir, tmp_path)
        except Exception as error:
            payload = {
                "status": "failed",
                "mode": args.mode,
                "aggregate_metrics": [
                    {"metric_name": "score", "value": 0.0},
                    {"metric_name": "valid_cases", "value": 0},
                    {"metric_name": "total_cases", "value": len(runs)},
                ],
                "run_metrics": [],
                "public_results": [] if args.mode == "official" else [],
                "logs": [str(error)],
            }
            Path(args.output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return 0

        scratch = tmp_path / "cases"
        scratch.mkdir()
        for run in runs:
            result, run_logs = score_run(run, checker, challenge_dir, Path(args.solution_runs_dir), scratch)
            results.append(result)
            logs.extend(run_logs)

    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["valid_cases"] == summary["total_cases"] and summary["total_cases"] > 0 else "failed",
        "mode": args.mode,
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_cases", "value": summary["total_cases"]},
        ],
        "run_metrics": [
            {"run_name": result["case_name"], "metrics": [{"metric_name": "score", "value": result.get("score", 0.0)}]}
            for result in results
        ],
        "public_results": results if args.mode == "validation" else [],
        "logs": logs,
    }
    payload["validation_summary" if args.mode == "validation" else "official_summary"] = summary
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
