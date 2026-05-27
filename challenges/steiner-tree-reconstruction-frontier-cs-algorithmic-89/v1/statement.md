# Steiner Tree Reconstruction

You receive one Frontier-CS-derived benchmark record on stdin. Print the canonical target answer for that record.

The original Frontier-CS problem was interactive. This Agentics migration uses an offline stdin/stdout contract: all interaction is replaced by a single run input and a single submitted answer. The trusted separated evaluator owns the reference answer for each run.

## Input

The input is the benchmark record for one case. Its format follows the migrated source data for Frontier-CS `algorithmic/problems/89`.

## Output

Print the answer tokens for the case. Whitespace is flexible, but the token sequence must match the reference exactly.

## Scoring

Each exact match receives `100`; any mismatch, malformed output, timeout, or nonzero solution exit receives `0` for that case. The leaderboard `score` is the average across official cases. Ties use `valid_cases`.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is executed once per case, reads stdin, and writes stdout. Network access is disabled.
