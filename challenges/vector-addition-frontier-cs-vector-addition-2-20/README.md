# Vector Addition Throughput

Optimize a Triton kernel for element-wise `float32` vector addition on a medium GPU workload.

The submitted ZIP project provides `solution.py` with an `add(x, y)` function. The trusted Agentics coexecuted-evaluator imports the participant function inside a PyTorch/Triton environment produced by `validation_setup` or `official_evaluation_setup`, checks correctness, times it against CPU and PyTorch GPU baselines, and writes `result.json`.

## Provenance

This challenge is migrated from Frontier-CS:

- `research/problems/vector_addition/2_20`
- Original title: Vector Addition Problem - Medium Vectors (2^20)
- Original shape: Triton/PyTorch benchmark expecting a Python `add(x, y)` function.

This PoC intentionally uses `coexecuted_benchmark`: participant code and the trusted coexecuted-evaluator run in the same evaluator-image container. The evaluator setup phase installs uv-managed CPython 3.12 under `/setup`, then creates a `/setup` uv project environment with PyTorch installed from the explicit CUDA 13.0 PyTorch index and Triton installed through uv's project workflow. It intentionally avoids `uv pip`.

## Files

- `v1/spec.json` declares the coexecuted GPU challenge bundle and setup phases.
- `v1/statement.md` is the submitter-facing statement.
- `v1/coexecuted-evaluator/setup.py` creates the PyTorch/Triton environment under `/setup`.
- `v1/coexecuted-evaluator/run.py` imports and benchmarks the submitted `add(x, y)`.
- `v1/public/README.md` documents the public validation configuration.

Official benchmark configuration is uploaded as a private asset overlay and is not committed.
