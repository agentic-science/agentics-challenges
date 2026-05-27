# Uniform Cave Explorer

This is an interactive challenge migrated from Frontier-CS `algorithmic/problems/80`.

The evaluator prints `m`, then repeatedly prints the current chamber marker. Reply `c left|right t` to place the marker and take a passage. The session ends when `treasure` is printed.

## Scoring

Invalid protocol messages, out-of-range values, query-limit overflow, wrong final answers, or premature exit receive score `0`. Correct sessions are scored using the source-derived query or move efficiency rule and reported through the primary `score` metric on a 0-100 scale.

## Solution Interface

Submit a `zip_project` solution with `agentics.solution.json`. The run command communicates with the evaluator over stdin/stdout. Flush stdout after every command.
