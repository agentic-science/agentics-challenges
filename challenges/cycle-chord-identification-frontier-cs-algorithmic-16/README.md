# Cycle Chord Identification

This challenge migrates Frontier-CS `algorithmic/problems/16` (`Identify Chord`) as a faithful `piped_stdio` interactive task. The trusted evaluator compiles and runs the original Testlib `interactor.cpp`, so the hidden chord, shortest-path query responses, 500-query limit, final validation, and source query-count scoring stay judge-owned.

## Provenance

- Source path: `algorithmic/problems/16`
- Source type: interactive, `interactor.cpp`
- Agentics mode: `piped_stdio`
- Public validation: one small deterministic cycle with chord `(2, 5)`
- Official data: private Frontier-CS `testdata/*.in` sessions packaged outside Git under `private-benchmark/`

The source statement describes average per-test scoring, but the shipped interactor keeps the minimum per-case ratio within each source input file. This migration preserves the shipped interactor behavior.

## Private Assets

Upload `official-runs.zip` with `private-benchmark/session.json` and the source input and answer files referenced by that manifest. Official chords, source testdata, and evaluator-only files must remain out of Git.
