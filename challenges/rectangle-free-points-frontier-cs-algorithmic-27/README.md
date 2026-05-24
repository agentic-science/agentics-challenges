# Rectangle-Free Points

Choose grid cells so that no four selected cells form the corners of an axis-aligned rectangle. Each submitted solution receives one grid size on stdin and writes the selected cells on stdout.

The evaluator validates coordinate bounds, duplicate points, and rectangle-freeness. Valid outputs score by the Frontier-CS checker formula `100 * min(k / (1.5 * U(n, m)), 1)`, where `k` is the number of selected points and `U(n, m)` is the benchmark upper bound.

## Contract

Each run receives stdin in this format:

```text
n m
```

The solution must write:

```text
k
r_1 c_1
...
r_k c_k
```

Rows are in `[1, n]`, columns are in `[1, m]`, and all listed cells must be distinct. The chosen set must not contain two distinct rows and two distinct columns with all four corner cells selected.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/27`
- Original title: rectangle-free grid point placement
- Original shape: default algorithmic problem with a special judge, 3 official cases, and point-count scoring.

The Agentics version uses `separated_evaluator`: submitted solutions only emit candidate point sets, while the trusted evaluator owns validation and scoring.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains tiny deterministic public validation instances.
- `v1/separated-evaluator/run.py` validates point sets and writes Agentics result JSON.

Official Frontier-CS grid sizes are uploaded as a private asset overlay and are not committed.
