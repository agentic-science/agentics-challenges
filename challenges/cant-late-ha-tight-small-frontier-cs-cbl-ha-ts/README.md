# Cant Be Late: High Availability, Tight Deadline, Small Overhead

This challenge migrates Frontier-CS source path `research/problems/cant_be_late/high_availability_tight_deadline_small_overhead`.

Optimize a cloud spot-instance scheduling strategy for the Frontier-CS cant_be_late high/tight/small variant.

## Interface

Submit `solution.py` defining the Frontier-CS `Solution` strategy class.

## Evaluation

The evaluator imports the strategy and runs copied Frontier-CS simulator code. Public traces are synthetic; official traces are private.

Score is the source simulator normalized cost score on a 0-100 scale.

Public validation is intentionally tiny. Official scoring uses `official-runs.zip` mounted under `private-benchmark/` and not committed to Git.

## Trust Boundary

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports or executes participant Python from `/workspace`. Official private benchmark data is visible in that container and contains no secrets.
