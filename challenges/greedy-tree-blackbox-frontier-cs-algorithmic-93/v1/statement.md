# Greedy Tree Blackbox

This is an interactive challenge. The evaluator first prints:

```text
n ty
```

The hidden object is a rooted tree on vertices `1..n`. Every internal node has at least two children. `ty` is a source test identifier and has no algorithmic effect.

For a query, print one line:

```text
? sz v1 v2 ... vsz
```

The `vi` values must be distinct vertices in `[1, n]`. The evaluator scans the sequence from left to right, greedily keeps a node only when it is neither an ancestor nor a descendant of any already kept node, and replies with the number of kept nodes. Flush after every query.

To answer, print one line:

```text
! p1 p2 ... pn
```

`pi` is the parent of vertex `i`; the root must have parent `0`. Flush and then continue reading for another source case or exit on EOF.

The trusted evaluator owns the hidden parent array, rejects duplicate or out-of-range query elements, validates the exact parent array, and writes `result.json`. Source scoring gives full credit through `45000` queries, zero at or above `200000`, and the original clamped linear ratio between those counts.
