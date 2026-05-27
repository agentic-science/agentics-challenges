# DiverC Autofill Words

This challenge migrates Frontier-CS `algorithmic/problems/28` (`Hacking the Project`) as a faithful `piped_stdio` interactive task. The trusted evaluator compiles and runs the original Testlib `interactor.cc`, preserving the generated word lists, prefix query responses, answer validation, and source scoring.

## Provenance

- Source path: `algorithmic/problems/28`
- Source type: interactive, `interactor.cc`
- Agentics mode: `piped_stdio`
- Public validation: one tiny deterministic dictionary-count case
- Official data: private Frontier-CS `testdata/*.in` sessions packaged outside Git under `private-benchmark/`

The original statement says the service can be adaptive. The shipped interactor deterministically generates up to 1000 lexicographic 10-character words for each starting letter and uses hidden per-letter counts from the input file. This migration preserves that shipped evaluator behavior.

## Private Assets

Upload `official-runs.zip` with `private-benchmark/session.json` and the source input and answer files referenced by that manifest. Official per-letter counts and source testdata must remain out of Git.
