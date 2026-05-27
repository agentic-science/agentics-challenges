# Mamba2 Scan Optimization

This challenge ports Frontier-CS `research/problems/mamba2_scan` into Agentics as a `coexecuted_benchmark` challenge. The trusted evaluator imports the participant's `solution.py`, materializes the returned `chunk_scan` implementation, and runs the source GPU correctness and performance benchmark.

## Provenance

- Source path: `research/problems/mamba2_scan`
- Source title: `Mamba2 Scan Optimization Problem`
- Source files inspected: `readme`, `config.yaml`, `evaluator.py`, `resources/benchmark.py`, `resources/baseline.py`, and `resources/submission_spec.json`
- Agentics mode: `coexecuted_benchmark`
- Official private asset: `official-runs.zip`

The public validation spec uses a tiny CUDA smoke shape. Official evaluation uses the source-scale shapes from the original submission spec, selected through a private `private-benchmark/config.json` overlay. No hidden answer data or secrets are committed.

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports or executes participant Python from `/workspace`. Official benchmark config is visible in that container and contains no secrets.
