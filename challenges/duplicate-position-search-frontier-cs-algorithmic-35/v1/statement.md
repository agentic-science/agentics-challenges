# Duplicate Position Search

This is an interactive challenge migrated from Frontier-CS `algorithmic/problems/35`.

The evaluator prints `T`, then for each case prints `n`. Query `? x m i1 ... im` asks whether value `x` appears at any selected hidden index. Final answer `! x` must be the singleton value.

## Scoring

Invalid protocol messages, out-of-range values, query-limit overflow, wrong final answers, or premature exit receive score `0`. Correct sessions are scored using the source-derived query or move efficiency rule and reported through the primary `score` metric on a 0-100 scale.

## Solution Interface

Submit a `zip_project` solution with `agentics.solution.json`. The run command communicates with the evaluator over stdin/stdout. Flush stdout after every command.
