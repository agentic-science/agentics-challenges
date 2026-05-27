# Graph Connectivity Oracle

This challenge migrates Frontier-CS `algorithmic/problems/25` as a faithful `piped_stdio` interactive task. The trusted evaluator compiles and runs the original Testlib `interactor.cc`, preserving the hidden graph, cut-neighborhood oracle, 3500-operation limit, final connectivity validation, and source scoring.

## Provenance

- Source path: `algorithmic/problems/25`
- Source type: interactive, `interactor.cc`
- Agentics mode: `piped_stdio`
- Public validation: one tiny connected graph
- Official data: private Frontier-CS `testdata/*.in` and `testdata/*.ans` sessions packaged outside Git under `private-benchmark/`

The shipped source interactor reads each operation as a single token and ignores character index `1`. This means the accepted wire tokens are `?<separator><bits>` and `!<separator><answer>`, for example `?#0101` and `!#1`. The migration preserves that source quirk instead of normalizing it.

## Private Assets

Upload `official-runs.zip` with `private-benchmark/session.json` and the source input and answer files referenced by that manifest. Official graphs and answer-edge files must remain out of Git.
