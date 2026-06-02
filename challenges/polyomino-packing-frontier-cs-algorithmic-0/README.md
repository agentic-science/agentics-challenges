# Polyomino Packing

Place every input polyomino in one axis-aligned rectangle. Each submitted solution receives one instance on stdin and writes the rectangle dimensions followed by one transform per piece on stdout.

The evaluator validates reflection, rotation, translation, bounds, and overlap. Valid placements score by density: `100 * total_cells / (W * H)`.

## Contract

Each run receives stdin in this format:

```text
n
k_1
x_11 y_11
...
```

Each polyomino has `k_i` local grid cells. The solution must write:

```text
W H
X_1 Y_1 R_1 F_1
...
X_n Y_n R_n F_n
```

`W` and `H` must be positive. For each piece, `F_i` is `1` to reflect across the y-axis before rotation, `R_i` is the number of clockwise 90-degree rotations, and `(X_i, Y_i)` is the final translation. All transformed cells must land in `[0, W) x [0, H)` with no overlap.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/0`
- Original title: Pack the Polyominoes (Reflections Allowed)
- Original shape: default algorithmic problem with a special judge, 70 official cases, and density scoring.

The Agentics version uses `separated_evaluator`: submitted solutions only emit candidate placements, while the trusted evaluator owns validation and scoring. Frontier-CS accepts any positive rectangle dimensions; this migration follows that contract.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains a tiny deterministic public validation instance.
- `v1/separated-evaluator/run.py` validates placements and writes Agentics result JSON.

Official Frontier-CS instances are uploaded as a private asset overlay and are not committed.
