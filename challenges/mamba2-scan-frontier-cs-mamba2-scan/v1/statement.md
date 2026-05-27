# Mamba2 Scan Optimization

Submit a ZIP project containing `solution.py` with:

```python
class Solution:
    def solve(self, spec_path: str | None = None) -> dict:
        ...
```

Return either `{"code": "..."}` or `{"program_path": "path/to/kernel.py"}`. The materialized module must define:

```python
def chunk_scan(X, A, B, chunk: int = 128, BD: int = 128):
    ...
```

The function receives CUDA `torch.float16` tensors `X`, `A`, and `B` of shape `(L, D)` and must return the scan output for:

```text
y_t = a_t * y_{t-1} + b_t * x_t
```

The source benchmark checks numerical correctness against its PyTorch GPU baseline using `rtol=1e-2` and `atol=5e-3`. Any failed correctness row receives score 0. Official source-scale shapes are `L = 2048, 4096`, `D = 512`, `chunk = 128`, and `BD = 128`; public validation uses a much smaller smoke shape.

The source score compares geometric mean answer time with the GPU baseline. A 1x GPU-baseline implementation receives 0 points; a 200x speedup receives 100 points by linear interpolation, with the public primary metric `score`.

This challenge uses `coexecuted_benchmark` with `acknowledge_danger: true` because the trusted evaluator imports or executes participant Python from `/workspace` and runs CUDA code in the evaluator container. External network access is disabled during evaluation.
