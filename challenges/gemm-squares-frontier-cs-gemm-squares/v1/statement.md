# GEMM Squares Optimization

Ported from Frontier-CS `research/problems/gemm_optimization/squares`.

## Agentics Interface

Submit a ZIP project containing the source interface described below. The trusted evaluator imports or compiles participant code from `/workspace`, so this challenge uses `coexecuted_benchmark` with `acknowledge_danger: true`.

## Public And Official Data

Public validation uses a small deterministic configuration committed under `v1/public`. Official scoring uses the private `official-runs` overlay under `private-benchmark/`.

## Original Statement

GEMM Optimization Problem
=========================

Problem Setting
---------------
Design and optimize high-performance Triton kernels for General Matrix-Matrix Multiplication (GEMM) on GPU. This problem focuses on implementing efficient matrix multiplication kernels using Triton's JIT compilation system.

The challenge involves optimizing:
- **Memory access patterns**: Efficient loading and storing of matrix data
- **Block tiling**: Optimal block sizes for GPU execution
- **Autotuning**: Leveraging Triton's autotuning capabilities
- **Activation functions**: Implementing GELU activation within the kernel
- **Performance benchmarking**: Achieving speedup over baseline implementations

Target
------
- **Primary**: Maximize geometric mean speedup over baseline (higher is better)
- **Secondary**: Ensure correctness across diverse matrix shapes
- **Tertiary**: Minimize kernel launch overhead and memory usage

API Specification
-----------------
Implement a `Solution` class that returns a Triton kernel implementation:

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
import triton
import triton.language as tl

def matmul(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Matrix multiplication with GELU activation.
    
    Args:
        a: Input tensor of shape (M, K)
        b: Input tensor of shape (K, N)
    
    Returns:
        Output tensor of shape (M, N) with GELU activation applied
    """
    pass
```

Required GELU Implementation:
```python
@triton.jit
def gelu(x):
    return x * 0.5 * (1.0 + tl.extra.cuda.libdevice.erf(x * 0.7071067811865476))
```

API Usage Notes
---------------
- The evaluator looks for a `matmul` function in the module namespace
- Function must handle tensor strides and memory layouts correctly
- Must use Triton JIT compilation for kernel definition
- Should leverage Triton's autotuning features for optimization
- Kernel must apply GELU activation to the result before returning

Scoring (0-100)
---------------
Performance is measured against baseline implementations:

```
geometric_mean_speedup = geometric_mean(baseline_times / answer_times)
raw_score = min(geometric_mean_speedup, 3.0)  # Cap at 3x speedup
score = (raw_score - 1.0) / 2.0 * 100  # Map 1x-3x to 0-100
```

- 0 points = No speedup (1x baseline performance)
- 50 points = 2x speedup over baseline
- 100 points = 3x+ speedup over baseline

Evaluation Details (squares variant)
-----------------------------------
- Only square shapes with equal M=N=K from 512 to 8192, step 1024:
  - Shapes: (s, s, s) for s ∈ {512, 1536, 2560, 3584, 4608, 5632, 6656, 7680, 8192}
- Correctness verified with tolerance: rtol=1e-2, atol=5e-3
- Performance measured using median execution time
- Requires CUDA backend and GPU support
