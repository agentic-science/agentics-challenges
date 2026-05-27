# SQL Parser Test Case Generation

This challenge ports Frontier-CS `research/problems/grammar_fuzzing/seed/sql` into Agentics as a `coexecuted_benchmark` challenge. The trusted evaluator imports the participant's `solution.py`, calls `Solution.solve(resources_path)`, parses the returned SQL statements with the source SQL engine, and measures line and branch coverage.

## Provenance

- Source path: `research/problems/grammar_fuzzing/seed/sql`
- Source title: `SQL Parser Test Case Generation`
- Source files inspected: `readme`, `config.yaml`, `evaluator.py`, `run_evaluator.sh`, `evaluate.sh`, `resources/sql_grammar.txt`, and `resources/sql_engine/`
- Agentics mode: `coexecuted_benchmark`
- Official private asset: `official-runs.zip`

The grammar and parser resources are participant-visible, matching the source contract. The public config uses a tiny deterministic smoke setting. Official evaluation uses the source coverage scoring settings selected through a private `private-benchmark/config.json` overlay.

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports participant Python from `/workspace`. Official benchmark config is visible in that container and contains no secrets.
