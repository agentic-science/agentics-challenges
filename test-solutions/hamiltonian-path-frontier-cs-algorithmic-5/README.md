# Hamiltonian Path Baseline

Deterministic public-data-only baseline for `hamiltonian-path-frontier-cs-algorithmic-5`.

The runner parses the graph, emits an exact longest path for DAG inputs, and otherwise tries several bounded greedy forward/backward path extensions plus simple insertion repair. It always falls back to a one-vertex valid path when no edge extension is found.
