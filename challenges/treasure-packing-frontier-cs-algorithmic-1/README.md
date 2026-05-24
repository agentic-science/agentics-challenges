# Treasure Packing

Choose how many items of each treasure category to place in a 20 kg, 25 liter bag. Each submitted solution receives one JSON instance on stdin and writes one JSON object on stdout with integer counts for the same keys.

The evaluator validates the output keys, count bounds, total mass, and total volume. Valid outputs are scored by total value against the Frontier-CS baseline and best-known reference values for each case.

## Contract

Each run receives JSON on stdin:

```json
{
  "ruby": [3, 10, 1000, 2000]
}
```

Each item array is `[quantity_limit, value, mass_mg, volume_ul]`. The solution must write a JSON object whose keys exactly match the input keys:

```json
{
  "ruby": 2
}
```

Counts must be nonnegative integers, cannot exceed the category limit, and must keep total mass at or below `20000000` mg and total volume at or below `25000000` ul.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/1`
- Original title: Treasure Packing
- Original shape: default algorithmic problem with a custom checker, three official cases, and normalized value scoring against baseline and best-known references.

The Agentics version uses `separated_evaluator`: submitted solutions only emit candidate counts, while the trusted evaluator owns validation and scoring.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains a tiny deterministic public validation run.
- `v1/separated-evaluator/run.py` validates outputs and writes Agentics result JSON.

Official cases and reference scoring metadata are uploaded as a private asset overlay and are not committed.
