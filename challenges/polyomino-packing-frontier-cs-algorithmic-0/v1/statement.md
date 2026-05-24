# Polyomino Packing

You are given several polyominoes on a unit square grid. Each polyomino is described by local integer cell coordinates. Place every polyomino into one axis-aligned rectangle using optional reflection, rotation, and translation. Your goal is to keep the rectangle area small.

## Input

Each run receives one instance on stdin:

```text
n
k_1
x_11 y_11
...
k_n
x_n1 y_n1
...
```

`n` is the number of polyominoes. For each piece `i`, `k_i` is the number of cells, followed by `k_i` local coordinates.

## Output

Write:

```text
W H
X_1 Y_1 R_1 F_1
...
X_n Y_n R_n F_n
```

`W` and `H` are positive rectangle dimensions. For each piece:

- `F_i = 1` reflects the local cell coordinates across the y-axis before rotation; `F_i = 0` leaves them unreflected.
- `R_i` must be one of `0`, `1`, `2`, or `3`, meaning that the reflected coordinates are rotated clockwise by `90 * R_i` degrees.
- `(X_i, Y_i)` is then added as the translation.

All transformed cells must lie inside `[0, W) x [0, H)`, and no two transformed cells may overlap. Extra output tokens are rejected.

## Scoring

Each valid case scores:

```text
100000 * total_cells / (W * H)
```

Higher is better. If any case is invalid, the official submission receives score `0`.

## Public Validation

The public validation instance is intentionally tiny and deterministic. Official scoring uses hidden Frontier-CS instances uploaded as private benchmark data.
