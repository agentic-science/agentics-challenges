# Hidden Tree Median

This is an interactive challenge. The evaluator first prints one integer `n`. There is a hidden non-adaptive tree on vertices `1..n`.

To ask a median query, print one line:

```text
0 a b c
```

The three vertices must be distinct and in `[1, n]`. Flush stdout after the line. The evaluator replies with the vertex minimizing the sum of distances to `a`, `b`, and `c`, which is the tree median of the three queried nodes. At most `20000` queries are allowed per source case.

When you have recovered the tree, print one line:

```text
1 u1 v1 u2 v2 ... u(n-1) v(n-1)
```

The submitted pairs must be exactly the hidden tree edges, in any order. Flush and then either continue reading for another source case or exit when stdin reaches EOF.

Malformed commands, out-of-range or repeated query vertices, too many queries, duplicate/self-loop final edges, wrong trees, or output after EOF are handled by the trusted evaluator and receive the source score. The evaluator writes `result.json`; participant code must not create it. Scoring is the original Frontier-CS ratio `min((ref_queries + 1) / (your_queries + 1), 1)` averaged over source cases and scaled to `score` from 0 to 100.
