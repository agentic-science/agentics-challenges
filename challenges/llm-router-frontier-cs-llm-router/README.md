# LLM Router

This challenge ports Frontier-CS `research/problems/llm_router` into Agentics as a `coexecuted_benchmark` challenge. The trusted evaluator imports the participant's `solution.py`, calls `Solution.solve(query, eval_name, candidate_models)` once per prompt, and scores the selected tier with the original accuracy-minus-cost formula.

## Provenance

- Source path: `research/problems/llm_router`
- Source title: `LLM Router`
- Source files inspected: `readme`, `config.yaml`, `evaluator.py`, `download_datasets.sh`, `resources/prepare_data.py`, and `resources/reference_data.csv`
- Agentics mode: `coexecuted_benchmark`
- Official private asset: `official-runs.zip`

The committed public validation CSV is tiny and deterministic. The participant-visible reference dataset from the source bundle remains public under `v1/resources/reference_data.csv`. The source-scale official RouterBench test split is packaged outside Git under `private-benchmark/`.

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports participant Python from `/workspace`. Official private benchmark rows are visible in that container and contain no secrets.
