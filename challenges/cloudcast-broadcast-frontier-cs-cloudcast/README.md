# Cloudcast Broadcast Optimization

This challenge migrates Frontier-CS source path `research/problems/cloudcast`.

Design low-cost multi-cloud broadcast routes under throughput and bandwidth constraints.

## Interface

Submit `solution.py` whose `Solution.solve(spec_path)` returns code or a program path defining `search_algorithm(src, dsts, G, num_partitions)`.

## Evaluation

The evaluator imports the submitted search algorithm. Public validation uses a synthetic three-node network; official scoring uses private profiles/configs.

The score is `100 / (1 + total_cost)` from the source simulator.

Public validation is intentionally tiny. Official scoring uses `official-runs.zip` mounted under `private-benchmark/` and not committed to Git.

## Trust Boundary

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports or executes participant Python from `/workspace`. Official private benchmark data is visible in that container and contains no secrets.
