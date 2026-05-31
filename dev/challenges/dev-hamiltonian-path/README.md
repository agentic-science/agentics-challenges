# Hamiltonian Path (Dev)

This local development variant uses only public CPU fixtures and does not require private asset backups.


Find a long simple directed path in a graph. Each submitted solution receives one graph on stdin and writes the path length followed by the vertex sequence on stdout.

The evaluator validates that every vertex is in range, no vertex repeats, and every consecutive pair is a directed edge from the input. Valid paths score by the number of configured thresholds they reach.

## Contract

Each run receives stdin in this format:

```text
n m
a_1 a_2 a_3 a_4 a_5 a_6 a_7 a_8 a_9 a_10
u_1 v_1
...
u_m v_m
```

The solution must write:

```text
k
p_1 p_2 ... p_k
```

`k` must be a positive integer, every `p_i` must be in `1..n`, vertices must be unique, and every `(p_i, p_{i+1})` must be a directed edge.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/5`
- Original title: Hamiltonian Path Challenge
- Original shape: default algorithmic problem with a special judge, three official cases, and threshold scoring by path length.

The Agentics version uses `separated_evaluator`: submitted solutions only emit candidate paths, while the trusted evaluator owns validation and scoring.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains a tiny deterministic public validation graph.
- `v1/separated-evaluator/run.py` validates paths and writes Agentics result JSON.

Official graph cases are uploaded as a private asset overlay and are not committed.
