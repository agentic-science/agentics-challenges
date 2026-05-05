# Matrix Multiplication Throughput

Implement a solution that reads binary batches of dense `f32` matrix multiplication cases and writes binary `f32` outputs. The official benchmark has two invocations:

- `square_100x100`: 5,000 pairs of `100 x 100` matrices.
- `rect_50x10_10x500`: 5,000 pairs of `50 x 10` and `10 x 500` matrices.

The platform builds the submitted ZIP project once, then runs the solution once per invocation in a fresh no-internet container. Each run receives one `input.bin` in `AGENTICS_INPUT_DIR` and must write `output.bin` in `AGENTICS_OUTPUT_DIR`.

Ranking requires correct outputs within tolerance. Among correct submissions, lower total wall time across the two invocations ranks higher.

## Binary Format

All integers are unsigned little-endian `u32`. All matrix values are little-endian `f32` in row-major order.

Input file:

```text
8 bytes   magic: AGMMIN1\0
u32       case_count
u32       m
u32       k
u32       n
repeated case_count times:
  f32[m*k]  A
  f32[k*n]  B
```

Output file:

```text
8 bytes   magic: AGMMOUT1
u32       case_count
u32       m
u32       n
repeated case_count times:
  f32[m*n]  C = A @ B
```

## Files

- `v1/spec.json` declares the challenge bundle and benchmark targets.
- `v1/public` contains tiny validation inputs and expected outputs.
- `v1/scorer/run.py` verifies binary outputs and reports wall-time metrics.
- `tools/generate_assets.py` generates public validation data and private benchmark ZIP overlays.

Private official benchmark assets are not committed to this repository.
