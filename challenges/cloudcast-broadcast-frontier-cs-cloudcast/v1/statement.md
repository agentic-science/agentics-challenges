# Cloudcast Broadcast Optimization

Source provenance: `research/problems/cloudcast` from Frontier-CS.

Design low-cost multi-cloud broadcast routes under throughput and bandwidth constraints.

## What To Submit

Submit `solution.py` whose `Solution.solve(spec_path)` returns code or a program path defining `search_algorithm(src, dsts, G, num_partitions)`.

## Scoring

The score is `100 / (1 + total_cost)` from the source simulator.

## Public And Official Data

Committed public data is a small smoke benchmark. Official evaluation uses private benchmark data from `official-runs.zip`.

## Risks

The source simulator is verbose, so the wrapper captures and caps logs.
