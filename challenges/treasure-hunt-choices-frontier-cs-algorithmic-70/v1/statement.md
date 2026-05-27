# Treasure Hunt Choices

This is an interactive challenge migrated from Frontier-CS `algorithmic/problems/70`.

The evaluator prints graph cases. During traversal it prints the shuffled neighbor descriptors for the current vertex; reply with a 1-based choice index. Visit all vertices before the move limit.

## Scoring

Invalid protocol messages, out-of-range values, query-limit overflow, wrong final answers, or premature exit receive score `0`. Correct sessions are scored using the source-derived query or move efficiency rule and reported through the primary `score` metric on a 0-100 scale.

## Solution Interface

Submit a `zip_project` solution with `agentics.solution.json`. The run command communicates with the evaluator over stdin/stdout. Flush stdout after every command.
