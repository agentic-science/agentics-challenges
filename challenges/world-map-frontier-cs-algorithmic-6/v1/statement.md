# World Map

You are given an undirected graph whose vertices are countries. Draw a square grid map where each cell is colored with one country number. Your map must realize exactly the graph adjacencies.

## Input

Your run command receives one scenario on stdin:

```text
N M
A_1 B_1
...
A_M B_M
```

`N` is the number of countries, numbered from `1` to `N`. Each pair `A_i B_i` is an undirected adjacency between two different countries. Benchmark inputs list each pair with `A_i < B_i` and contain no duplicate pairs.

## Output

Write:

```text
K
Q_1 Q_2 ... Q_K
C_1,1 C_1,2 ... C_1,K
...
C_K,1 C_K,2 ... C_K,K
```

`K` is the side length of the map and must satisfy `1 <= K <= 240`. Each `Q_i` must equal `K`; this line is kept for compatibility with the original sample-grader format. Every `C_i,j` must be a country number in `1..N`.

Your grid must satisfy all of these rules:

- For every input edge `(A_i, B_i)`, there is at least one side-adjacent cell pair colored `A_i` and `B_i`.
- For every side-adjacent cell pair with different colors, that color pair is one of the input edges.

To match the original Frontier-CS checker, colors for isolated countries do not need to appear unless they are needed to represent an input edge.

Extra output tokens are rejected.

## Scoring

Invalid outputs receive `0`.

For a valid map, let:

```text
R = K / N
```

The case score is:

```text
100 * clamp((6 - R) / (6 - 1.5), 0, 1)
```

Higher is better. A valid map with `K/N <= 1.5` receives full score for that case. The leaderboard ranking metric is the average `score` across official cases. Ties use `valid_cases`, then `average_ratio`.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run script is executed once per graph. It should read stdin and write stdout. No network access is available during setup, build, or run for this challenge.

## Public Validation

The public validation instance is intentionally tiny and deterministic. Official scoring uses hidden Frontier-CS graph cases uploaded as private benchmark data.
