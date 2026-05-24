# Vector Addition Throughput

Write a CUDA implementation of element-wise vector addition:

```cpp
extern "C" __global__ void vector_add_kernel(
    const float* x,
    const float* y,
    float* out,
    int n
);
```

Place this kernel in `solution.cu` at the root of your submitted ZIP project. The coexecuted-evaluator compiles your source with `nvcc`, launches the kernel on contiguous `float32` vectors, checks `out[i] == x[i] + y[i]` within tolerance, and measures effective memory bandwidth.

## Scoring

The primary metric is `score`, a 0 to 100 throughput score derived from speedup over a reference CUDA kernel:

```text
score = clamp(50 * custom_bandwidth_gbps / reference_bandwidth_gbps, 0, 100)
```

Correctness is required. Incorrect output receives score 0.

## Constraints

- The validation vector length is `1048576`.
- Inputs are contiguous device arrays.
- The expected output is a contiguous device array supplied by the benchmark.
- The benchmark launches your kernel with a one-dimensional grid and 256 threads per block.
- Do not rely on network access or external services.

## Coexecuted-Evaluator Boundary

This challenge uses `coexecuted_benchmark`, so the trusted coexecuted-evaluator imports and compiles participant code from `/workspace` inside the evaluator container. Official private benchmark configuration shares that container with participant code. The private asset contains no secrets.
