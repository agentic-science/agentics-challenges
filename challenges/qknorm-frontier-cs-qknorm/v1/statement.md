# QKNorm Optimization

Ported from Frontier-CS `research/problems/qknorm`.

## Agentics Interface

Submit a ZIP project containing the source interface described below. The trusted evaluator imports or compiles participant code from `/workspace`, so this challenge uses `coexecuted_benchmark` with `acknowledge_danger: true`.

## Public And Official Data

Public validation uses a small deterministic configuration committed under `v1/public`. Official scoring uses the private `official-runs` overlay under `private-benchmark/`.

## Original Statement

QKNorm Optimization Problem
============================

Problem Setting
---------------
Design and optimize high-performance implementations for Query-Key Normalization (QKNorm) on GPU. This problem focuses on implementing efficient normalization kernels that apply RMSNorm to query and key tensors.

This is a **memory-bound** (even **launch-bound**) **tiny operator**. Performance optimization requires careful attention to:

1. **Memory Efficiency**: Focus on **vectorized memory access patterns**. Minimize memory transactions and maximize memory bandwidth utilization.

2. **Operation Fusion**: **Avoid additional transpose/contiguous kernels**. Fuse operations to reduce kernel launch overhead and memory traffic.

3. **Non-Contiguous Input Handling**: **Be aware that inputs may be non-contiguous** due to weight-QKV fusion. Your implementation should efficiently handle non-contiguous memory layouts without triggering expensive memory copies.

Target
------
- **Primary**: Ensure correctness across diverse tensor shapes
- **Secondary**: Maximize geometric mean speedup over baseline (higher is better)
- **Tertiary**: Minimize kernel launch overhead and memory usage

API Specification
-----------------
Implement a `Solution` class that returns a qknorm implementation:

```python
class Solution:
    def solve(self, spec_path: str = None) -> dict:
        """
        Returns a dict with either:
        - {"code": "python_code_string"}
        - {"program_path": "path/to/kernel.py"}
        """
        # Your implementation
        pass
```

Your kernel implementation must provide:

```python
import torch
import flashinfer

def qknorm(q: torch.Tensor, k: torch.Tensor, norm_weight: torch.Tensor):
    """
    Apply RMSNorm to query and key tensors.
    
    Args:
        q: Query tensor of arbitrary shape (will be reshaped to 2D)
        k: Key tensor of arbitrary shape (will be reshaped to 2D)
        norm_weight: Normalization weight tensor of shape (hidden_dim,)
    
    Returns:
        Tuple of (q_normalized, k_normalized) tensors
    """
    pass
```

Required Default Implementation:
```python
def default_qknorm(q: torch.Tensor, k: torch.Tensor, norm_weight: torch.Tensor):
    q_2d = q.contiguous().view(-1, q.shape[-1])
    k_2d = k.contiguous().view(-1, k.shape[-1])
    q_o = torch.empty_like(q_2d)
    k_o = torch.empty_like(k_2d)
    flashinfer.norm.rmsnorm(q_2d, norm_weight, out=q_o)
    flashinfer.norm.rmsnorm(k_2d, norm_weight, out=k_o)
    return q_o.view(q.shape), k_o.view(k.shape)
```

Baseline Implementation:
```python
def customized_qknorm(q: torch.Tensor, k: torch.Tensor, norm_weight: torch.Tensor):
    q_o = torch.empty(q.shape, device=q.device, dtype=q.dtype)
    k_o = torch.empty(k.shape, device=k.device, dtype=k.dtype)
    flashinfer.norm.rmsnorm(q, norm_weight, out=q_o)
    flashinfer.norm.rmsnorm(k, norm_weight, out=k_o)
    return q_o, k_o
```

API Usage Notes
---------------
- The evaluator looks for a `qknorm` function in the module namespace
- Function must handle tensor reshaping correctly (q and k may have arbitrary shapes)
- Must use flashinfer.norm.rmsnorm for normalization
- Function returns a tuple of (q_normalized, k_normalized) tensors
- **Important**: Inputs q and k may be **non-contiguous** due to weight-QKV fusion
- **Avoid**: Additional `.contiguous()` or `.transpose()` calls that trigger memory copies
- **Focus**: Vectorized memory access and operation fusion to minimize kernel launches

Scoring (0-100)
---------------
Performance is measured against baseline implementations:

```
geometric_mean_speedup = geometric_mean(baseline_times / answer_times)
score_unbounded = 100 * geometric_mean_speedup
score = clamp(score_unbounded, 0, 100)
```

- 0 points = Correctness fails, or no measurable baseline-relative throughput
- 50 points = 0.5x baseline-relative throughput
- 100 points = 1.0x or higher baseline-relative throughput

Evaluation Details
------------------
- Shapes focus on diverse batch-sizes, head-dim, num-kv-heads, num-qo-heads, e.g.:
  - (16, 8, 32, 128)
  - (128, 32, 32, 64)
- Correctness verified with tolerance: rtol=1e-2, atol=5e-3
- Performance measured using median execution time
- Requires CUDA backend and GPU support
