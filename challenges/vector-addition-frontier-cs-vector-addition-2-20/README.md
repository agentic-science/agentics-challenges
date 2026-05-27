# Vector Addition 2^20 Throughput

Optimize a Triton kernel for element-wise `float32` vector addition on a medium GPU workload.

The submitted ZIP project provides `solution.py` with the Frontier-CS `Solution.solve(spec_path)` interface. The trusted Agentics coexecuted-evaluator calls `solve`, materializes the returned `code` or `program_path` artifact, imports the artifact's `add(x, y)` function inside a PyTorch/Triton environment produced by `validation_setup` or `official_evaluation_setup`, checks correctness, times it against CPU and PyTorch GPU baselines, and writes `result.json`.

## Provenance

This challenge is migrated from Frontier-CS:

- `research/problems/vector_addition/2_20`
- Original title: Vector Addition Problem - Medium Vectors (2^20)
- Original shape: Triton/PyTorch benchmark expecting `Solution.solve(spec_path)` to return a Python artifact that defines `add(x, y)`.

This PoC intentionally uses `coexecuted_benchmark`: participant code and the trusted coexecuted-evaluator run in the same evaluator-image container. The evaluator setup phase installs uv-managed CPython 3.12 under `/setup`, then creates a `/setup` uv project environment with PyTorch installed from the explicit CUDA 13.0 PyTorch index and Triton installed through uv's project workflow. It intentionally avoids `uv pip`.

## Files

- `v1/spec.json` declares the coexecuted GPU challenge bundle and setup phases.
- `v1/statement.md` is the submitter-facing statement.
- `v1/coexecuted-evaluator/setup.py` creates the PyTorch/Triton environment under `/setup`.
- `v1/coexecuted-evaluator/run.py` calls the source-style `Solution.solve(spec_path)` interface and benchmarks the submitted `add(x, y)`.
- `v1/public/README.md` documents the public validation configuration.
- `v1/resources/` contains the source submission spec and resource files.

Official benchmark configuration is uploaded as a private asset overlay and is not committed.
