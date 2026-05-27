# Vector Addition 2^20 Throughput

Write a Triton implementation of element-wise vector addition for two contiguous `float32` CUDA tensors of length `1048576`.

Your submitted ZIP project must include `solution.py` at the project root. The file must define a `Solution` class with the Frontier-CS `solve(spec_path)` interface:

```python
class Solution:
    def solve(self, spec_path: str | None = None) -> dict:
        return {"program_path": "kernel.py"}
```

The returned artifact must contain either `{"code": "..."}` or `{"program_path": "..."}`. The referenced module must define:

```python
import torch
import triton
import triton.language as tl

def add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    ...
```

`add` receives two CUDA tensors with the same shape and must return a CUDA tensor containing `x + y`. The evaluator calls `Solution.solve(spec_path)`, materializes the returned artifact, and imports `add` inside a PyTorch/Triton environment created during the coexecuted-evaluator setup phase.

## Scoring

Correctness is required. Incorrect output receives score 0.

The primary metric is `score`, a 0 to 100 throughput score normalized against CPU and PyTorch GPU baselines:

```text
target = max(2 * pytorch_bandwidth_gbps / cpu_bandwidth_gbps, 1)
score = clamp(((custom_bandwidth_gbps / cpu_bandwidth_gbps - 1) / (target - 1)) * 100, 0, 100)
```

## Constraints

- Public validation uses a tiny deterministic vector length. Official scoring uses the source 2^20 vector length.
- Inputs are contiguous CUDA `float32` tensors.
- Correctness uses `torch.allclose` with `rtol=1e-5` and `atol=1e-8`.
- Do not rely on network access or external services at evaluation time.
- The evaluator setup phase installs uv-managed CPython 3.12, PyTorch, and Triton with `uv sync`; your run-time code should only import packages available in that environment or files included in your ZIP project.

## Coexecuted-Evaluator Boundary

This challenge uses `coexecuted_benchmark`, so the trusted coexecuted-evaluator imports participant code from `/workspace` inside the evaluator container. Official private benchmark configuration shares that container with participant code. The private asset contains no secrets.
