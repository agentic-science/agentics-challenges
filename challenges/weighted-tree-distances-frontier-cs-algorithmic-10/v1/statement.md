# Weighted Tree Distances

The judge owns one or more hidden weighted trees. Edge weights are positive integers. For each tree you may query distances and must output every edge with its weight.

At the start of each Frontier-CS source file the evaluator writes `T`. If `T` is positive, it then writes `n` for each dataset before that dataset's interaction begins. If the Agentics wrapper writes terminal `T = 0`, the session is complete and your program should exit.

For a dataset, write `? u v`, flush, and read the distance between vertices `u` and `v`. Vertices are one-based, must lie in `[1, n]`, and must be distinct.

To answer the dataset, write:

```text
! u_1 v_1 w_1 u_2 v_2 w_2 ... u_{n-1} v_{n-1} w_{n-1}
```

The edges may be in any order. After answering, continue reading: either the next `n` in the same source file, a new positive `T` for another source file, or terminal `0`.

Malformed commands, invalid vertices, duplicate or non-existing answer edges, wrong weights, EOF before an answer, or exceeding the source query limit receive zero from the trusted evaluator. The trusted evaluator writes `result.json`; participant code must only speak the stdin/stdout protocol.

The official score is the original Frontier-CS query-efficiency score averaged by source file, scaled to `score` from 0 to 100.
