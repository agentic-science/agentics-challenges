# Cascading Flip Schedule on a Power Grid Tree

Choose a vertex service order on a tree whose removals flip unserviced neighbors.

Submitted `zip_project` solutions are run once per case. Each run reads the case from standard input and writes its answer to standard output. Network access is disabled for setup, build, run, and evaluator stages.

## Provenance

- Source: Frontier-CS `algorithmic/problems/305`.
- Source config: `type=default`, `checker=chk.cc`, `time=2s`, `memory=1024m`.
- Migration target: `linux-arm64-cpu`.
- Execution mode: `separated_evaluator`.

## Scoring

The trusted evaluator compiles and runs the original Frontier-CS Testlib checker for each case. The checker result is converted to a public `score` metric on a 0-100 scale and averaged across runs. Malformed outputs rejected by the checker receive zero for that case.

## Data Split

The public bundle contains a tiny deterministic smoke fixture in `v1/public/runs.json`. Official Frontier-CS test inputs, reference outputs, and checker scoring metadata are packaged outside Git as `official-runs.zip`, which provides `private-benchmark/runs.json`.
