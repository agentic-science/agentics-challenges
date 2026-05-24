from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = {
    "n": 1_048_576,
    "validation_samples": 3,
    "official_samples": 5,
    "warmups": 2,
}


HARNESS_SOURCE = r'''
#include <algorithm>
#include <cmath>
#include <cuda_runtime.h>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "/workspace/solution.cu"

__global__ void agentics_reference_vector_add_kernel(
    const float* x,
    const float* y,
    float* out,
    int n
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        out[idx] = x[idx] + y[idx];
    }
}

int fail(const std::string& message) {
    std::cerr << message << std::endl;
    return 2;
}

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = (call); \
        if (err != cudaSuccess) { \
            std::ostringstream oss; \
            oss << "CUDA failure at " << __FILE__ << ":" << __LINE__ << ": " \
                << cudaGetErrorString(err); \
            return fail(oss.str()); \
        } \
    } while (0)

template <typename Kernel>
float median_time_ms(Kernel kernel, int samples, int warmups) {
    for (int i = 0; i < warmups; ++i) {
        kernel();
    }
    CUDA_CHECK(cudaDeviceSynchronize());

    std::vector<float> timings;
    timings.reserve(samples);
    cudaEvent_t start;
    cudaEvent_t stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    for (int i = 0; i < samples; ++i) {
        CUDA_CHECK(cudaEventRecord(start));
        kernel();
        CUDA_CHECK(cudaEventRecord(stop));
        CUDA_CHECK(cudaEventSynchronize(stop));
        float elapsed_ms = 0.0f;
        CUDA_CHECK(cudaEventElapsedTime(&elapsed_ms, start, stop));
        timings.push_back(elapsed_ms);
    }

    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    std::sort(timings.begin(), timings.end());
    return timings[timings.size() / 2];
}

int main(int argc, char** argv) {
    if (argc != 4) {
        return fail("usage: vector_bench <n> <samples> <warmups>");
    }

    const int n = std::stoi(argv[1]);
    const int samples = std::stoi(argv[2]);
    const int warmups = std::stoi(argv[3]);
    if (n <= 0 || samples <= 0 || warmups < 0) {
        return fail("n and samples must be positive; warmups must be non-negative");
    }

    std::vector<float> h_x(n);
    std::vector<float> h_y(n);
    std::vector<float> h_out(n, 0.0f);
    for (int i = 0; i < n; ++i) {
        h_x[i] = static_cast<float>((i % 1009) - 503) * 0.001f;
        h_y[i] = static_cast<float>(((i * 17) % 997) - 491) * 0.002f;
    }

    float* d_x = nullptr;
    float* d_y = nullptr;
    float* d_out = nullptr;
    const size_t bytes = static_cast<size_t>(n) * sizeof(float);
    CUDA_CHECK(cudaMalloc(&d_x, bytes));
    CUDA_CHECK(cudaMalloc(&d_y, bytes));
    CUDA_CHECK(cudaMalloc(&d_out, bytes));
    CUDA_CHECK(cudaMemcpy(d_x, h_x.data(), bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_y, h_y.data(), bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemset(d_out, 0, bytes));

    const int threads = 256;
    const int blocks = (n + threads - 1) / threads;

    auto custom_kernel = [&]() {
        vector_add_kernel<<<blocks, threads>>>(d_x, d_y, d_out, n);
    };
    auto reference_kernel = [&]() {
        agentics_reference_vector_add_kernel<<<blocks, threads>>>(d_x, d_y, d_out, n);
    };

    custom_kernel();
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    CUDA_CHECK(cudaMemcpy(h_out.data(), d_out, bytes, cudaMemcpyDeviceToHost));

    double max_abs_error = 0.0;
    for (int i = 0; i < n; ++i) {
        const double expected = static_cast<double>(h_x[i] + h_y[i]);
        const double actual = static_cast<double>(h_out[i]);
        max_abs_error = std::max(max_abs_error, std::abs(actual - expected));
    }
    const bool correct = max_abs_error <= 1.0e-5;

    float custom_ms = 0.0f;
    float reference_ms = 0.0f;
    if (correct) {
        custom_ms = median_time_ms(custom_kernel, samples, warmups);
        CUDA_CHECK(cudaGetLastError());
        reference_ms = median_time_ms(reference_kernel, samples, warmups);
        CUDA_CHECK(cudaGetLastError());
    }

    CUDA_CHECK(cudaFree(d_x));
    CUDA_CHECK(cudaFree(d_y));
    CUDA_CHECK(cudaFree(d_out));

    const double moved_bytes = static_cast<double>(n) * 3.0 * sizeof(float);
    const double custom_bandwidth = custom_ms > 0.0f
        ? moved_bytes / (static_cast<double>(custom_ms) / 1000.0) / 1.0e9
        : 0.0;
    const double reference_bandwidth = reference_ms > 0.0f
        ? moved_bytes / (static_cast<double>(reference_ms) / 1000.0) / 1.0e9
        : 0.0;
    const double speedup = reference_bandwidth > 0.0
        ? custom_bandwidth / reference_bandwidth
        : 0.0;

    std::cout << std::fixed << std::setprecision(8)
              << "{"
              << "\"correct\":" << (correct ? "true" : "false") << ","
              << "\"n\":" << n << ","
              << "\"samples\":" << samples << ","
              << "\"warmups\":" << warmups << ","
              << "\"custom_ms\":" << custom_ms << ","
              << "\"reference_ms\":" << reference_ms << ","
              << "\"custom_bandwidth_gbps\":" << custom_bandwidth << ","
              << "\"reference_bandwidth_gbps\":" << reference_bandwidth << ","
              << "\"speedup_vs_reference\":" << speedup << ","
              << "\"max_abs_error\":" << max_abs_error
              << "}" << std::endl;
    return 0;
}
'''


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

    try:
        run_benchmark(args, output_path)
    except Exception as exc:  # noqa: BLE001 - result.json should explain harness failures.
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics={
                "custom_bandwidth_gbps": 0.0,
                "reference_bandwidth_gbps": 0.0,
                "speedup_vs_reference": 0.0,
                "max_abs_error": 0.0,
            },
            message=f"benchmark error: {exc}",
        )
    return 0


def run_benchmark(args: argparse.Namespace, output_path: Path) -> None:
    challenge_dir = Path(args.challenge_dir)
    workspace_dir = Path(args.workspace_dir)
    config = load_config(challenge_dir, args.mode)
    n = positive_int(config.get("n", DEFAULT_CONFIG["n"]), "n")
    warmups = non_negative_int(config.get("warmups", DEFAULT_CONFIG["warmups"]), "warmups")
    sample_key = "validation_samples" if args.mode == "validation" else "official_samples"
    samples = positive_int(config.get(sample_key, DEFAULT_CONFIG[sample_key]), sample_key)

    solution_path = workspace_dir / "solution.cu"
    if not solution_path.is_file():
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics={
                "custom_bandwidth_gbps": 0.0,
                "reference_bandwidth_gbps": 0.0,
                "speedup_vs_reference": 0.0,
                "max_abs_error": 0.0,
            },
            message="missing solution.cu at the submitted project root",
        )
        return

    tmp_dir = output_path.parent / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    harness_path = tmp_dir / "vector_bench.cu"
    binary_path = tmp_dir / "vector_bench"
    harness_path.write_text(HARNESS_SOURCE)

    compile_cmd = [
        "nvcc",
        "-O3",
        "--std=c++17",
        "-arch=native",
        "-lineinfo",
        "-o",
        str(binary_path),
        str(harness_path),
    ]
    compile_result = subprocess.run(
        compile_cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if compile_result.returncode != 0:
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics={
                "custom_bandwidth_gbps": 0.0,
                "reference_bandwidth_gbps": 0.0,
                "speedup_vs_reference": 0.0,
                "max_abs_error": 0.0,
            },
            message="nvcc compilation failed",
            logs=[trim_log(compile_result.stderr or compile_result.stdout)],
        )
        return

    bench_result = subprocess.run(
        [str(binary_path), str(n), str(samples), str(warmups)],
        check=False,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if bench_result.returncode != 0:
        write_result(
            output_path,
            mode=args.mode,
            score=0.0,
            correct=False,
            metrics={
                "custom_bandwidth_gbps": 0.0,
                "reference_bandwidth_gbps": 0.0,
                "speedup_vs_reference": 0.0,
                "max_abs_error": 0.0,
            },
            message="benchmark binary failed",
            logs=[trim_log(bench_result.stderr or bench_result.stdout)],
        )
        return

    raw = parse_json_from_stdout(bench_result.stdout)
    correct = bool(raw.get("correct"))
    metrics = {
        "custom_bandwidth_gbps": finite_float(raw.get("custom_bandwidth_gbps", 0.0)),
        "reference_bandwidth_gbps": finite_float(raw.get("reference_bandwidth_gbps", 0.0)),
        "speedup_vs_reference": finite_float(raw.get("speedup_vs_reference", 0.0)),
        "max_abs_error": finite_float(raw.get("max_abs_error", 0.0)),
    }
    speedup = metrics["speedup_vs_reference"] if correct else 0.0
    score = max(0.0, min(100.0, 50.0 * speedup))
    write_result(
        output_path,
        mode=args.mode,
        score=score,
        correct=correct,
        metrics=metrics,
        message="ok" if correct else "incorrect output",
    )


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
    logs: list[str] | None = None,
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
            {
                "metric_name": "custom_bandwidth_gbps",
                "value": finite_float(metrics["custom_bandwidth_gbps"]),
            },
            {
                "metric_name": "reference_bandwidth_gbps",
                "value": finite_float(metrics["reference_bandwidth_gbps"]),
            },
            {
                "metric_name": "speedup_vs_reference",
                "value": finite_float(metrics["speedup_vs_reference"]),
            },
            {"metric_name": "max_abs_error", "value": finite_float(metrics["max_abs_error"])},
        ],
        summary_key: {
            "score": score,
            "passed": 1 if passed else 0,
            "total": 1,
        },
        "logs": logs or [],
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


def parse_json_from_stdout(stdout: str) -> dict[str, Any]:
    start = stdout.rfind("{")
    end = stdout.rfind("}")
    if start < 0 or end <= start:
        raise RuntimeError("benchmark did not print JSON")
    payload = json.loads(stdout[start : end + 1])
    if not isinstance(payload, dict):
        raise RuntimeError("benchmark JSON must be an object")
    return payload


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


def trim_log(value: str, limit: int = 4000) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[:limit] + "\n[truncated]"


if __name__ == "__main__":
    raise SystemExit(main())
