# Hamiltonian Path

You are given a directed graph. Find a path that visits as many vertices as possible without repeating a vertex.

## Input

Your run command receives stdin:

```text
n m
a_1 a_2 a_3 a_4 a_5 a_6 a_7 a_8 a_9 a_10
u_1 v_1
...
u_m v_m
```

`n` is the number of vertices, `m` is the number of directed edges, and each `a_i` is a scoring threshold. Vertices are numbered from `1` to `n`.

## Output

Write two lines to stdout:

```text
k
p_1 p_2 ... p_k
```

`k` must be positive. Every path vertex must be in `1..n`, no vertex may appear twice, and every consecutive pair must be a directed edge in the input.

## Scoring

Invalid outputs receive `0`.

For a valid path of length `k`, each case score is:

```text
10 * count(threshold in a_1..a_10 where k >= threshold)
```

The leaderboard ranking metric is the average `score` across official cases on a 0-100 scale. Ties use `valid_cases`, then `total_path_length`.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run script is executed once per graph. It should read stdin and write stdout. No network access is available during setup, build, or run for this challenge.
