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
    parser = argparse.ArgumentParser(description="Agentics coexecuted evaluator wrapper")
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
    config = load_mode_config(challenge_dir, args.mode)
    declared_metrics = declared_metric_names(challenge_dir)
    logs: list[str] = []
    try:
        with captured_logs(logs):
            result = dispatch(config, challenge_dir, workspace_dir, output_path.parent, args.mode)
    except Exception as exc:  # noqa: BLE001 - result.json must explain evaluator failures.
        result = {"status": "error", "score": 0.0, "score_unbounded": 0.0, "runs_successfully": 0.0, "error": str(exc)}
    write_agentics_result(output_path, args.mode, result, logs, declared_metrics)
    return 0


def configure_runtime_cache(output_root: Path) -> None:
    tmp_root = output_root / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HOME", str(output_root))
    os.environ.setdefault("TMPDIR", str(tmp_root))
    os.environ.setdefault("XDG_CACHE_HOME", str(tmp_root / "cache"))
    os.environ.setdefault("TRITON_CACHE_DIR", str(tmp_root / "triton-cache"))
    os.environ.setdefault("AGENTICS_EVALUATOR_OUTPUT_DIR", str(output_root))
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
    if not path.is_file():
        raise RuntimeError(f"missing {mode} config at {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("mode config must be a JSON object")
    return payload


def declared_metric_names(challenge_dir: Path) -> set[str]:
    payload = json.loads((challenge_dir / "spec.json").read_text(encoding="utf-8"))
    metrics = payload.get("metric_schema", {}).get("metrics", [])
    if not isinstance(metrics, list):
        return set()
    names: set[str] = set()
    for metric in metrics:
        if isinstance(metric, dict) and isinstance(metric.get("name"), str):
            names.add(metric["name"])
    return names


@contextlib.contextmanager
def captured_logs(logs: list[str]):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        yield
    text = (stdout.getvalue() + "\n" + stderr.getvalue()).strip()
    if text:
        logs.append(truncate(text))


def dispatch(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path, output_dir: Path, mode: str) -> dict[str, Any]:
    runner = config.get("runner")
    if runner == "frontier_python_evaluate":
        return run_frontier_python_evaluate(config, challenge_dir, workspace_dir, output_dir)
    if runner == "sql_fuzzer":
        return run_sql_fuzzer(config, challenge_dir, workspace_dir, output_dir)
    if runner == "imagenet_pareto":
        return run_imagenet(config, challenge_dir, workspace_dir)
    if runner == "llm_router":
        return run_llm_router(config, challenge_dir, workspace_dir)
    if runner == "llm_sql":
        return run_llm_sql(config, challenge_dir, workspace_dir, output_dir)
    if runner == "symbolic_regression":
        return run_symbolic(config, challenge_dir, workspace_dir)
    if runner == "vdb_pareto":
        return run_vdb(config, challenge_dir, workspace_dir)
    if runner == "nbody":
        return run_nbody(config, challenge_dir, workspace_dir)
    raise RuntimeError(f"unsupported runner {runner!r}")


def import_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"failed to import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_frontier_python_evaluate(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path, output_dir: Path) -> dict[str, Any]:
    sys.path.insert(0, str(challenge_dir / "resources"))
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_source_evaluator")
    apply_benchmark_override(source, config)
    solution_path = workspace_dir / "solution.py"
    spec_path = challenge_dir / str(config.get("submission_spec_path", "resources/submission_spec.json"))
    cwd = Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chdir(output_dir)
        return source.evaluate(solution_path, spec_path)
    finally:
        os.chdir(cwd)


def apply_benchmark_override(source: Any, config: dict[str, Any]) -> None:
    override = config.get("benchmark_override")
    if not override:
        return
    if override == "vector_sizes":
        sizes = [int(value) for value in config.get("sizes", [])]
        if sizes:
            source._determine_large_test_sizes = lambda: sizes
        if "num_samples" in config:
            source.NUM_VECTOR_SAMPLES = int(config["num_samples"])
        if "gpu_warmups" in config:
            source.GPU_WARMUP_ITERS = int(config["gpu_warmups"])
        if "inner_warmups" in config:
            source.INNER_ADD_WARMUP_ITERS = int(config["inner_warmups"])
        return

    import benchmark  # type: ignore

    if override == "gemm_shapes":
        shapes = [tuple(item) for item in config["shapes"]]
        baseline = source.baseline_matmul
        def run_benchmark(answer, baseline_matmul=baseline, print_output=False):
            rows = [benchmark._bench_pair(int(m), int(n), int(k), answer, baseline_matmul) for m, n, k in shapes]
            return summarize_rows(rows)
        source.run_benchmark = run_benchmark
        return

    if override == "quant_dot_shapes":
        shapes = [tuple(item) for item in config["shapes"]]
        baseline = source.baseline_quant_dot
        def run_benchmark(answer, baseline_fn=baseline, print_output=False):
            rows = [benchmark._bench_pair(int(m), int(n), answer, baseline_fn) for m, n in shapes]
            return summarize_rows(rows)
        source.run_benchmark = run_benchmark
        return

    if override == "qknorm_shapes":
        shapes = [tuple(item) for item in config["shapes"]]
        baseline = source.baseline_qknorm
        def run_benchmark(answer, baseline_fn=baseline, print_output=False):
            rows = [benchmark._bench_pair(int(b), int(kv), int(qo), int(hd), answer, baseline_fn) for b, kv, qo, hd in shapes]
            return summarize_rows(rows)
        source.run_benchmark = run_benchmark
        return

    raise RuntimeError(f"unknown benchmark override {override}")


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    speedups: list[float] = []
    for row in rows:
        answer = finite(row.get("answer_ms", 0.0))
        baseline = finite(row.get("baseline_ms", row.get("gpu_baseline_ms", 0.0)))
        if answer > 0 and baseline > 0:
            speedups.append(baseline / answer)
    if speedups:
        arith = sum(speedups) / len(speedups)
        geo = math.exp(sum(math.log(max(value, 1e-12)) for value in speedups) / len(speedups))
        median = sorted(speedups)[len(speedups) // 2]
    else:
        arith = geo = median = 0.0
    return {
        "rows": rows,
        "arithmetic_mean_speedup": arith,
        "geometric_mean_speedup": geo,
        "median_speedup": median,
        "pass_all": all(bool(row.get("close_passed")) for row in rows),
    }


def run_sql_fuzzer(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path, output_dir: Path) -> dict[str, Any]:
    sys.path.insert(0, str(challenge_dir / "resources"))
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_sql_fuzzer_evaluator")
    solution_path = workspace_dir / "solution.py"
    module = source.load_solution_module(solution_path)
    solution = module.Solution()
    artifact = solution.solve(str(challenge_dir / "resources"))
    cwd = Path.cwd()
    try:
        os.chdir(output_dir)
        artifact_path = source.materialize_artifact(artifact, solution_path)
        fuzz = source.load_fuzzer_from_artifact(artifact_path)
        result = source.evaluate_fuzzer(fuzz, challenge_dir / "resources", time_budget=float(config.get("time_budget_sec", 1.0)))
    finally:
        os.chdir(cwd)
    return {"status": "success", "runs_successfully": 1.0, **result}


def run_imagenet(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_imagenet_evaluator")
    for name, value in config.get("sample_overrides", {}).items():
        if hasattr(source, name):
            setattr(source, name, int(value))
    module = source.load_solution_module(workspace_dir / "solution.py")
    cls = getattr(module, "Solution")
    evaluator = source.Evaluator()
    return evaluator.evaluate(cls())


def run_llm_router(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_llm_router_evaluator")
    evaluator = source.Evaluator(str(challenge_dir))
    evaluator.trace_files = [str(challenge_dir / path) for path in config.get("datasets", [])]
    return evaluator.evaluate(str(workspace_dir / "solution.py"))


def run_llm_sql(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path, output_dir: Path) -> dict[str, Any]:
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_llm_sql_evaluator")
    evaluator = source.Evaluator(str(challenge_dir))
    evaluator.trace_files = [str(challenge_dir / path) for path in config.get("datasets", [])]
    if "col_merges" in config:
        evaluator.col_merges = config["col_merges"]
    cache_dir = output_dir / "tmp"
    cache_dir.mkdir(parents=True, exist_ok=True)
    evaluator.baseline_cache_file = str(cache_dir / "baseline_cache.json")
    return evaluator.evaluate(str(workspace_dir / "solution.py"))


def run_symbolic(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_symbolic_evaluator")
    refs = source.load_reference_metrics(challenge_dir / config["reference_path"])
    data_dir = challenge_dir / config["data_dir"]
    data_files = sorted(data_dir.glob("*.csv"))
    datasets = {path.name: path for path in data_files if path.name in refs}
    if not datasets:
        raise RuntimeError("no symbolic regression datasets matched reference metrics")
    module = source.load_solution_module(workspace_dir / "solution.py")
    by_dataset = source.evaluate(module, datasets, refs)
    scores = [float(entry["score"]) for entry in by_dataset.values()]
    scores_unbounded = [float(entry["score_unbounded"]) for entry in by_dataset.values()]
    mse_values = [float(entry["mse"]) for entry in by_dataset.values()]
    return {
        "status": "success",
        "runs_successfully": 1.0,
        "score": sum(scores) / len(scores),
        "score_unbounded": sum(scores_unbounded) / len(scores_unbounded),
        "metrics": {
            "mean_mse": sum(mse_values) / len(mse_values),
            "num_datasets": len(by_dataset),
        },
    }


def run_vdb(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    blocked = config.get("blocked_reason")
    if blocked:
        raise RuntimeError(str(blocked))
    source = import_module(challenge_dir / "source-evaluator.py", "frontier_vdb_evaluator")
    module = source.load_solution_module(workspace_dir / "solution.py")
    index_class = source.find_solution_class(module)
    if config.get("dataset") == "synthetic":
        import numpy as np
        rng = np.random.default_rng(int(config.get("seed", 2026)))
        dim = int(config.get("dim", 16))
        base = int(config.get("base_vectors", 128))
        queries = int(config.get("queries", 16))
        xb = rng.normal(size=(base, dim)).astype("float32")
        xq = rng.normal(size=(queries, dim)).astype("float32")
        distances = ((xq[:, None, :] - xb[None, :, :]) ** 2).sum(axis=2)
        gt = np.argsort(distances, axis=1)[:, :1].astype("int64")
        index = index_class(dim)
        index.add(xb)
        metrics = source.evaluate_index(index, xq, gt, int(config.get("k", 1)))
        score = source.compute_score(metrics)
        unbounded_cfg = dict(source.SCORE_CONFIG)
        unbounded_cfg["scoring"] = dict(unbounded_cfg["scoring"])
        unbounded_cfg["scoring"]["max_score"] = float("inf")
        unbounded_cfg["scoring"]["min_score"] = float("-inf")
        score_unbounded = source.compute_score(metrics, unbounded_cfg)
        return {"status": "success", "runs_successfully": 1.0, "score": score, "score_unbounded": score_unbounded, "metrics": metrics}
    return source.evaluate(workspace_dir / "solution.py", k=int(config.get("k", 1)))


def run_nbody(config: dict[str, Any], challenge_dir: Path, workspace_dir: Path) -> dict[str, Any]:
    common = import_module(challenge_dir / "nbody-common/evaluator_common.py", "frontier_nbody_common")
    cfg = common.VariantConfig(
        num_particles=int(config["num_particles"]),
        num_iterations=int(config["num_iterations"]),
        space_size=float(config["space_size"]),
        num_runs=int(config["num_runs"]),
        min_speedup=float(config["min_speedup"]),
        max_speedup=float(config["max_speedup"]),
    )
    return common.evaluate(workspace_dir / "solution.cpp", challenge_dir / "nbody-common", cfg)


def write_agentics_result(output_path: Path, mode: str, result: dict[str, Any], logs: list[str], declared_metrics: set[str]) -> None:
    score = finite(result.get("score", 0.0))
    score_unbounded = finite(result.get("score_unbounded", score))
    error = result.get("error")
    pass_all = result.get("pass_all")
    runs_successfully = finite(result.get("runs_successfully", 1.0))
    correct = bool(result.get("correct", True))
    passed = error is None and runs_successfully > 0 and correct and (pass_all is not False)
    metrics = collect_metrics(result, score, score_unbounded, passed, declared_metrics)
    summary_key = "validation_summary" if mode == "validation" else "official_summary"
    payload: dict[str, Any] = {
        "status": "passed" if passed else "failed",
        "mode": mode,
        "aggregate_metrics": metrics,
        summary_key: {"score": score, "passed": 1 if passed else 0, "total": 1},
        "logs": [truncate(item) for item in logs[:4]],
    }
    if error is not None:
        payload["logs"].append(truncate(str(error)))
    if mode == "validation":
        payload["public_results"] = [{"case_name": "public-validation", "status": payload["status"], "score": score, "message": truncate(str(error or "ok"), 500)}]
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def collect_metrics(result: dict[str, Any], score: float, score_unbounded: float, passed: bool, declared_metrics: set[str]) -> list[dict[str, float | str]]:
    values: dict[str, float] = {}

    def set_declared(name: str, value: float) -> None:
        if name in declared_metrics:
            values[name] = value

    set_declared("score", score)
    set_declared("score_unbounded", score_unbounded)
    set_declared("runs_successfully", finite(result.get("runs_successfully", 1.0)))
    set_declared("correctness", 1.0 if passed else 0.0)

    def add(name: str, value: Any) -> None:
        if name in {"score", "score_unbounded", "runs_successfully", "correctness"} or name not in declared_metrics:
            return
        if isinstance(value, bool):
            values[name] = 1.0 if value else 0.0
        elif isinstance(value, (int, float)) and math.isfinite(float(value)):
            values[name] = float(value)
    for key, value in result.items():
        if key in {"metrics", "by_dataset", "stdout", "stderr"}:
            continue
        add(key, value)
    nested = result.get("metrics")
    if isinstance(nested, dict):
        for key, value in nested.items():
            if isinstance(value, dict):
                continue
            add(key, value)
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
