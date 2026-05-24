# Vector Addition Throughput

Optimize a CUDA kernel for element-wise `float32` vector addition on a medium GPU workload.

The submitted ZIP project provides `solution.cu` with a `vector_add_kernel` implementation. The trusted Agentics benchmark harness compiles the participant source inside the evaluator container, checks correctness, times the custom kernel against a reference CUDA kernel, and writes `result.json`.

## Provenance

This challenge is migrated from Frontier-CS:

- `research/problems/vector_addition/2_20`
- Original title: Vector Addition Problem - Medium Vectors (2^20)
- Original shape: Triton/PyTorch benchmark expecting a Python `add(x, y)` function.

This PoC intentionally uses `coexecuted_benchmark`: participant code and the trusted benchmark harness run in the same evaluator-image container. The current Agentics CUDA image has `nvcc` but does not include PyTorch or Triton, so this first migration adapts the participant interface to CUDA C++ while preserving the vector-addition workload, CUDA target, throughput scoring, and weaker trust boundary that the Agentics mode is meant to exercise.

## Files

- `v1/spec.json` declares the co-executed GPU challenge bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/benchmark/run.py` compiles and runs the trusted CUDA benchmark harness.
- `v1/public/README.md` documents the public validation configuration.

Official benchmark configuration is uploaded as a private asset overlay and is not committed.
