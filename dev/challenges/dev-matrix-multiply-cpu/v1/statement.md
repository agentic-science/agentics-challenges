# Matrix Multiplication Throughput

Write a ZIP project solution that multiplies batches of dense `f32` matrices.

For each invocation, Agentics provides `input.bin` under `AGENTICS_INPUT_DIR`. Your `run.sh` must write `output.bin` under `AGENTICS_OUTPUT_DIR`.

The official benchmark invokes your solution twice:

- `square_100x100`: 5,000 products of `100 x 100` by `100 x 100`.
- `rect_50x10_10x500`: 5,000 products of `50 x 10` by `10 x 500`.

Outputs are compared against private reference outputs with absolute and relative tolerance. Incorrect outputs do not rank. Correct submissions are ranked by total wall time across the two invocations.

## Binary Format

All values are little-endian. Matrices are row-major.

Input:

```text
magic      8 bytes: AGMMIN1\0
cases      u32
m          u32
k          u32
n          u32
for each case:
  A        f32[m*k]
  B        f32[k*n]
```

Output:

```text
magic      8 bytes: AGMMOUT1
cases      u32
m          u32
n          u32
for each case:
  C        f32[m*n]
```
