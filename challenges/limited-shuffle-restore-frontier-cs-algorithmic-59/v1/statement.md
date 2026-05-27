# Limited Shuffle Restore

This is an interactive challenge migrated from Frontier-CS `algorithmic/problems/59`.

The evaluator prints `n`. Query `? i j` compares hidden permutation positions and returns `<` or `>`. Final answer `! a1 ... an` must match the hidden permutation.

## Scoring

Invalid protocol messages, out-of-range values, query-limit overflow, wrong final answers, or premature exit receive score `0`. Correct sessions are scored using the source-derived query or move efficiency rule and reported through the primary `score` metric on a 0-100 scale.

## Solution Interface

Submit a `zip_project` solution with `agentics.solution.json`. The run command communicates with the evaluator over stdin/stdout. Flush stdout after every command.
