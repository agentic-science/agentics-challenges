# Improv Rating Wagers

This challenge migrates Frontier-CS `algorithmic/problems/77` into an Agentics `separated_evaluator` bundle with the `zip_project` stdin/stdout solution contract.

Submitted solutions are executed once per run. Each run provides a Frontier-CS-derived benchmark record on stdin, and the solution writes the canonical target answer to stdout. The trusted evaluator compares the submitted output with the run's reference answer after whitespace normalization and reports the average exact-reference score.

## Contract

- Read the complete stdin payload for the run.
- Write the canonical answer tokens to stdout.
- Whitespace between tokens is ignored, but token values and order must match the reference answer exactly.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/77`
- Original title: Improv Rating Wagers
- Original shape: Frontier-CS interactive-style algorithmic benchmark with source config, statement, interactor, and testdata.
- Agentics mode: `separated_evaluator`.

Public validation is intentionally tiny. Official Frontier-CS-derived runs and reference answers are supplied through the required private asset `official-runs` and are not committed.
