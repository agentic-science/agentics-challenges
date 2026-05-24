# Treasure Packing

You are given a JSON object describing exactly twelve treasure categories. For each category, choose how many items to pack in a single bag with two limits:

- mass at most `20000000` mg;
- volume at most `25000000` ul.

Your goal is to maximize total value.

## Input

Your run command receives one JSON object on stdin. Each key is a category name, and each value is:

```text
[quantity_limit, value, mass_mg, volume_ul]
```

All values are positive integers, and `quantity_limit` is the maximum number of items available in that category.

## Output

Write one JSON object to stdout. The output keys must exactly match the input keys, and every value must be a nonnegative integer count.

```json
{
  "amber": 1,
  "bangle": 0
}
```

The evaluator rejects outputs with missing keys, extra keys, negative counts, non-integer counts, counts above the category limit, total mass above `20000000` mg, or total volume above `25000000` ul.

## Scoring

For each case, the evaluator computes your selected value and compares it with a baseline and a best-known reference:

```text
100 * clamp((your_value - baseline_value) / (best_value - baseline_value), 0, 1)
```

If `best_value <= baseline_value`, a valid output receives full case credit only when its value is at least `best_value`.

The leaderboard ranking metric is the average `score` across official cases. Ties use `valid_cases`, then `total_value`.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run script is executed once per case. It should read stdin and write stdout. No network access is available during setup, build, or run for this challenge.
