# World Map

Draw a square grid map whose cell colors represent countries. The adjacencies between different colors in the grid must exactly match the input country-adjacency graph. Smaller maps score better through the ratio `K / N`.

Each submitted solution receives one graph on stdin and writes one candidate map to stdout. The evaluator validates the map shape, country colors, required graph edges, and forbidden non-edges before assigning a score.

## Contract

Each run receives stdin in this format:

```text
N M
A_1 B_1
...
A_M B_M
```

Countries are numbered from `1` to `N`, and every edge is an undirected adjacency.

The solution must write:

```text
K
K K ... K
C_1,1 ... C_1,K
...
C_K,1 ... C_K,K
```

The second line contains `K` row lengths, matching the Frontier-CS sample-grader output format. In this Agentics version every row length must equal `K`, and `K` must be at most `240`.

For every input edge, at least one pair of side-adjacent cells must use those two colors. For every side-adjacent pair of cells with different colors, that color pair must be an input edge. To preserve the source checker behavior, isolated country colors are not required to appear unless they are needed for an input edge.

## Scoring

For each valid case, let `R = K / N`. The per-case score is:

```text
100 * clamp((6 - R) / (6 - 1.5), 0, 1)
```

The leaderboard ranking metric is the average `score` across official cases. Ties use `valid_cases`, then `average_ratio`.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/6`
- Original title: World Map
- Original shape: default algorithmic problem with a Testlib special judge, three official cases, and ratio scoring by `K / N`.

The source problem exposes a `create_map` function interface through its CMS grader. The Agentics version uses `zip_project` with stdin/stdout and one graph per run. The private official run manifest strips the source sample-grader `T=1` wrapper while preserving the official graph cases. The private overlay also keeps the raw source `.in` and `.ans` files out of public Git.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains a tiny deterministic public validation graph.
- `v1/separated-evaluator/run.py` validates maps and writes Agentics result JSON.

Official Frontier-CS cases and raw source testdata are packaged as a private asset overlay and are not committed.
