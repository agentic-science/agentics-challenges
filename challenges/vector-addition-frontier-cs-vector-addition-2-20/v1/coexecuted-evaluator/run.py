from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


DEFAULT_CONFIG = {
    "n": 1_048_576,
    "validation_samples": 3,
    "official_samples": 5,
    "warmups": 5,
    "gpu_warmups": 5,
    "seed": 1337,
}

ENV_PROJECT_DIR = "pytorch-triton-env"
ENV_ACTIVE = "AGENTICS_VECTOR_ADDITION_ENV_ACTIVE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--workspace-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", required=True, choices=["validation", "official"])
    parser.add_argument("--target", required=True)
    parser.add_argument("--setup-dir")
    args = parser.parse_args()

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_runtime_cache(output_path.parent)
    reexec_with_setup_python(args)

    try:
        run_benchmark(args, output_path)
    except Exception as exc:  # noqa: BLE001 - result.json should explain evaluator failures.
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics=zero_metrics(),
            message=f"benchmark error: {exc}",
        )
    return 0


def configure_runtime_cache(output_root: Path) -> None:
    tmp_root = output_root / "tmp"
    tmp_root.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HOME", str(output_root))
    os.environ.setdefault("TMPDIR", str(tmp_root))
    os.environ.setdefault("XDG_CACHE_HOME", str(tmp_root / "cache"))
    os.environ.setdefault("TRITON_CACHE_DIR", str(tmp_root / "triton-cache"))
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")


def reexec_with_setup_python(args: argparse.Namespace) -> None:
    if os.environ.get(ENV_ACTIVE) == "1":
        return
    if not args.setup_dir:
        raise RuntimeError("coexecuted-evaluator requires --setup-dir with the PyTorch/Triton environment")
    venv_python = Path(args.setup_dir) / ENV_PROJECT_DIR / ".venv" / "bin" / "python"
    if not venv_python.is_file():
        raise RuntimeError(f"setup environment is missing Python at {venv_python}")
    env = os.environ.copy()
    env[ENV_ACTIVE] = "1"
    os.execve(str(venv_python), [str(venv_python), *sys.argv], env)


def run_benchmark(args: argparse.Namespace, output_path: Path) -> None:
    challenge_dir = Path(args.challenge_dir)
    workspace_dir = Path(args.workspace_dir)
    config = load_config(challenge_dir, args.mode)

    solution_path = workspace_dir / "solution.py"
    if not solution_path.is_file():
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics=zero_metrics(),
            message="missing solution.py at the submitted project root",
        )
        return

    add_func = load_add_function(solution_path, output_path.parent / "tmp")
    raw = evaluate_vector_addition(add_func, config, args.mode)
    correct = bool(raw["correct"])
    score = finite_float(raw["score"]) if correct else 0.0
    metrics = {
        "custom_bandwidth_gbps": finite_float(raw["custom_bandwidth_gbps"]),
        "pytorch_bandwidth_gbps": finite_float(raw["pytorch_bandwidth_gbps"]),
        "cpu_bandwidth_gbps": finite_float(raw["cpu_bandwidth_gbps"]),
        "speedup_vs_pytorch": finite_float(raw["speedup_vs_pytorch"]),
        "custom_vs_cpu": finite_float(raw["custom_vs_cpu"]),
        "pytorch_vs_cpu": finite_float(raw["pytorch_vs_cpu"]),
        "max_abs_error": finite_float(raw["max_abs_error"]),
    }
    write_result(
        output_path,
        mode=args.mode,
        score=score,
        correct=correct,
        metrics=metrics,
        message="ok" if correct else "incorrect output",
    )


def load_add_function(solution_path: Path, tmp_dir: Path) -> Callable[[Any, Any], Any]:
    module = import_module_from_path(solution_path, "agentics_submitted_solution")
    if hasattr(module, "add"):
        return module.add

    if not hasattr(module, "Solution"):
        raise ValueError("solution.py must define add(x, y) or a Frontier-compatible Solution class")
    solution = module.Solution()
    if not hasattr(solution, "solve"):
        raise ValueError("Solution class must define solve()")
    artifact = solution.solve(None)
    artifact_path = materialize_artifact(artifact, solution_path.parent, tmp_dir)
    return load_add_from_artifact(artifact_path, solution_path.parent, tmp_dir)


def materialize_artifact(artifact: Any, solution_dir: Path, tmp_dir: Path) -> Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    if isinstance(artifact, dict):
        artifact_path = tmp_dir / "solution-artifact.json"
        artifact_path.write_text(json.dumps(artifact))
        return artifact_path
    if isinstance(artifact, str):
        candidate = solution_dir / artifact
        if len(artifact) < 4096 and "\n" not in artifact and candidate.is_file():
            artifact_path = tmp_dir / "solution-artifact.json"
            artifact_path.write_text(json.dumps({"program_path": str(candidate)}))
            return artifact_path
        code_path = tmp_dir / "submitted_add.py"
        code_path.write_text(artifact)
        artifact_path = tmp_dir / "solution-artifact.json"
        artifact_path.write_text(json.dumps({"program_path": str(code_path)}))
        return artifact_path
    raise TypeError(f"Solution.solve() returned unsupported artifact type {type(artifact)!r}")


def load_add_from_artifact(artifact_path: Path, solution_dir: Path, tmp_dir: Path) -> Callable[[Any, Any], Any]:
    artifact = json.loads(artifact_path.read_text())
    if not isinstance(artifact, dict):
        raise ValueError("solution artifact must be a JSON object")
    if "code" in artifact:
        code_path = tmp_dir / "submitted_add.py"
        code_path.write_text(str(artifact["code"]))
        module = import_module_from_path(code_path, "agentics_submitted_add")
    elif "program_path" in artifact:
        program_path = Path(str(artifact["program_path"]))
        if not program_path.is_absolute():
            program_path = solution_dir / program_path
        module = import_module_from_path(program_path, "agentics_submitted_add")
    else:
        raise ValueError("solution artifact must contain code or program_path")
    if not hasattr(module, "add"):
        raise ValueError("submitted program must define add(x, y)")
    return module.add


def import_module_from_path(path: Path, module_name: str) -> ModuleType:
    if not path.is_file():
        raise FileNotFoundError(f"Python module not found: {path}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"failed to load Python module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def evaluate_vector_addition(
    add_func: Callable[[Any, Any], Any],
    config: dict[str, Any],
    mode: str,
) -> dict[str, float | bool]:
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available")
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)

    n = positive_int(config.get("n", DEFAULT_CONFIG["n"]), "n")
    warmups = non_negative_int(config.get("warmups", DEFAULT_CONFIG["warmups"]), "warmups")
    gpu_warmups = non_negative_int(config.get("gpu_warmups", DEFAULT_CONFIG["gpu_warmups"]), "gpu_warmups")
    seed = positive_int(config.get("seed", DEFAULT_CONFIG["seed"]), "seed")
    sample_key = "validation_samples" if mode == "validation" else "official_samples"
    samples = positive_int(config.get(sample_key, DEFAULT_CONFIG[sample_key]), sample_key)

    warmup_gpu(torch, device, gpu_warmups)

    pytorch_ms = []
    cpu_ms = []
    custom_ms = []
    correctness = []
    max_abs_error = 0.0
    for sample_idx in range(samples):
        torch.manual_seed(seed + sample_idx)
        torch.cuda.manual_seed_all(seed + sample_idx)
        x = torch.rand(n, device=device, dtype=torch.float32)
        y = torch.rand(n, device=device, dtype=torch.float32)
        x_cpu = x.detach().cpu()
        y_cpu = y.detach().cpu()

        expected = x + y
        actual = add_func(x, y)
        if not torch.is_tensor(actual):
            raise TypeError("add(x, y) must return a torch.Tensor")
        torch.cuda.synchronize()
        sample_error = float(torch.max(torch.abs(expected - actual)).detach().cpu())
        max_abs_error = max(max_abs_error, sample_error)
        correctness.append(bool(torch.allclose(expected, actual, rtol=1e-5, atol=1e-8)))

        pytorch_ms.append(time_cuda_ms(torch, lambda: x + y, warmups))
        cpu_ms.append(time_cpu_ms(lambda: x_cpu + y_cpu, warmups))
        custom_ms.append(time_cuda_ms(torch, lambda: add_func(x, y), warmups))

    pytorch_bandwidth = bandwidth_gbps(n, median(pytorch_ms))
    cpu_bandwidth = bandwidth_gbps(n, median(cpu_ms))
    custom_bandwidth = bandwidth_gbps(n, median(custom_ms))
    speedup_vs_pytorch = safe_ratio(custom_bandwidth, pytorch_bandwidth)
    custom_vs_cpu = safe_ratio(custom_bandwidth, cpu_bandwidth)
    pytorch_vs_cpu = safe_ratio(pytorch_bandwidth, cpu_bandwidth)
    target = max(2.0 * pytorch_vs_cpu, 1.0 + 1e-12)
    score = max(0.0, min(100.0, ((custom_vs_cpu - 1.0) / (target - 1.0)) * 100.0))
    correct = all(correctness)

    return {
        "correct": correct,
        "score": score if correct else 0.0,
        "custom_bandwidth_gbps": custom_bandwidth if correct else 0.0,
        "pytorch_bandwidth_gbps": pytorch_bandwidth,
        "cpu_bandwidth_gbps": cpu_bandwidth,
        "speedup_vs_pytorch": speedup_vs_pytorch if correct else 0.0,
        "custom_vs_cpu": custom_vs_cpu if correct else 0.0,
        "pytorch_vs_cpu": pytorch_vs_cpu,
        "max_abs_error": max_abs_error,
    }


def warmup_gpu(torch: Any, device: Any, iters: int) -> None:
    if iters <= 0:
        return
    n = 1 << 20
    x = torch.rand(n, device=device, dtype=torch.float32)
    y = torch.rand(n, device=device, dtype=torch.float32)
    for _ in range(iters):
        _ = x + y
    torch.cuda.synchronize()


def time_cuda_ms(torch: Any, fn: Callable[[], Any], warmups: int) -> float:
    for _ in range(warmups):
        _ = fn()
    torch.cuda.synchronize()
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    _ = fn()
    end.record()
    end.synchronize()
    return finite_float(start.elapsed_time(end))


def time_cpu_ms(fn: Callable[[], Any], warmups: int) -> float:
    for _ in range(warmups):
        _ = fn()
    start = time.perf_counter()
    _ = fn()
    return finite_float((time.perf_counter() - start) * 1000.0)


def load_config(challenge_dir: Path, mode: str) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    private_config_path = challenge_dir / "private-benchmark" / "config.json"
    if mode == "validation":
        if private_config_path.exists():
            raise RuntimeError("validation benchmark unexpectedly received private config")
        return config
    if not private_config_path.is_file():
        raise RuntimeError("official benchmark requires private-benchmark/config.json")
    private_config = json.loads(private_config_path.read_text())
    if not isinstance(private_config, dict):
        raise RuntimeError("private benchmark config must be a JSON object")
    config.update(private_config)
    return config


def write_result(
    output_path: Path,
    *,
    mode: str,
    score: float,
    correct: bool,
    metrics: dict[str, float],
    message: str,
) -> None:
    score = finite_float(score)
    passed = bool(correct) and score > 0.0
    summary_key = "validation_summary" if mode == "validation" else "official_summary"
    payload: dict[str, Any] = {
        "status": "passed" if passed else "failed",
        "mode": mode,
        "rank_score": score,
        "aggregate_metrics": [
            {"metric_name": "score", "value": score},
            {"metric_name": "correctness", "value": 1.0 if correct else 0.0},
            {"metric_name": "custom_bandwidth_gbps", "value": finite_float(metrics["custom_bandwidth_gbps"])},
            {"metric_name": "pytorch_bandwidth_gbps", "value": finite_float(metrics["pytorch_bandwidth_gbps"])},
            {"metric_name": "cpu_bandwidth_gbps", "value": finite_float(metrics["cpu_bandwidth_gbps"])},
            {"metric_name": "speedup_vs_pytorch", "value": finite_float(metrics["speedup_vs_pytorch"])},
            {"metric_name": "custom_vs_cpu", "value": finite_float(metrics["custom_vs_cpu"])},
            {"metric_name": "pytorch_vs_cpu", "value": finite_float(metrics["pytorch_vs_cpu"])},
            {"metric_name": "max_abs_error", "value": finite_float(metrics["max_abs_error"])},
        ],
        summary_key: {
            "score": score,
            "passed": 1 if passed else 0,
            "total": 1,
        },
        "logs": [],
    }
    if mode == "validation":
        payload["public_results"] = [
            {
                "case_name": "vector-addition-public",
                "status": "passed" if passed else "failed",
                "score": score,
                "message": message,
            }
        ]
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def zero_metrics() -> dict[str, float]:
    return {
        "custom_bandwidth_gbps": 0.0,
        "pytorch_bandwidth_gbps": 0.0,
        "cpu_bandwidth_gbps": 0.0,
        "speedup_vs_pytorch": 0.0,
        "custom_vs_cpu": 0.0,
        "pytorch_vs_cpu": 0.0,
        "max_abs_error": 0.0,
    }


def median(values: list[float]) -> float:
    ordered = sorted(finite_float(value) for value in values)
    if not ordered:
        return 0.0
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def bandwidth_gbps(n: int, elapsed_ms: float) -> float:
    if elapsed_ms <= 0.0:
        return 0.0
    return finite_float((3.0 * float(n) * 4.0 * 1.0e-9) / (elapsed_ms * 1.0e-3))


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0.0:
        return 0.0
    return finite_float(numerator / denominator)


def positive_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise RuntimeError(f"{field} must be a positive integer")
    return value


def non_negative_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise RuntimeError(f"{field} must be a non-negative integer")
    return value


def finite_float(value: Any) -> float:
    number = float(value)
    if not math.isfinite(number):
        return 0.0
    return number


if __name__ == "__main__":
    raise SystemExit(main())
