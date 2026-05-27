# Steiner Tree Reconstruction

This is an interactive challenge. The evaluator first prints one integer `n`, the number of vertices in a hidden unweighted tree.

To query whether a vertex is in a Steiner subgraph, print one line:

```text
? k v s1 s2 ... sk
```

`1 <= k <= n`, `v` is in `[1, n]`, and `s1..sk` are distinct vertices in `[1, n]`. Flush stdout after the line. The evaluator replies `1` if `v` belongs to the minimal connected subgraph containing the set `S`, otherwise `0`. The total sum of all submitted `k` values must not exceed `3000000`; if the evaluator replies `-1`, exit immediately.

To submit the tree, print:

```text
!
u1 v1
u2 v2
...
u(n-1) v(n-1)
```

The edges may be in any order. Flush and then continue reading for another source case or exit on EOF.

The trusted evaluator owns the hidden tree, validates all query and final-answer syntax, enforces the total set-size limit, and writes `result.json`. Correct trees are scored by the original Frontier-CS query-count rule: full score through `3000` queries, zero beyond `1200000`, and linear interpolation between them.
