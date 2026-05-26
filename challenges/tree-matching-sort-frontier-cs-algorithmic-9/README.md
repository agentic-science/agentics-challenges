# Tree Matching Sort

Sort a permutation on a tree using parallel matching swaps with as few rounds as possible.

This challenge migrates Frontier-CS `algorithmic/problems/9` into the Agentics `zip_project` and `separated_evaluator` contract. Each solution run receives one batch/checker-style case on stdin and writes the original problem output to stdout.

## Provenance

- Source path: `algorithmic/problems/9`
- Source title: Tree Matching Sort
- Source checker: `chk.cc` using Testlib-style `registerTestlibCmd`
- Source config: default algorithmic CPU problem
- Official source test cases: packaged outside Git in `official-runs.zip`

## Public And Private Data

`v1/public/runs.json` contains a tiny deterministic smoke case. The official inputs, answer/reference files, auxiliary testdata files, and scoring metadata are packaged as a private overlay at `private-benchmark/runs.json` plus `private-benchmark/source-testdata/`.

## Evaluation

The public evaluator compiles the migrated checker inside the evaluator container, runs it for each solution output, parses the checker ratio, and reports aggregate Agentics metrics. The checker copy preserves the original validation logic; fixed-size ratio-message buffers were widened where necessary to avoid aborting before emitting the original score text.
