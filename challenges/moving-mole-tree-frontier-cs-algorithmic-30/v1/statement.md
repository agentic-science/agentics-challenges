# Moving Mole Tree

You interact with a rooted tree whose root is node `1`. A hidden mole starts at one node. You must identify the mole's current node.

For a query vertex `x`, the evaluator answers `1` if the mole is currently in the subtree of `x`. Otherwise it answers `0`; if the mole is not already at root, it moves one edge to its parent.

## Session

Each source-shaped session starts with:

```text
1
n
u1 v1
...
u(n-1) v(n-1)
```

The shipped source interactor requires `n = 5000`, and this migration preserves that official shape. Public validation uses a deterministic generated `n = 5000` smoke tree. Official evaluation may run several private source sessions back to back. After the last session the evaluator writes terminal `0` and then closes stdout. Treat EOF as successful session termination too.

## Queries

To query a subtree, write:

```text
? x
```

where `1 <= x <= n`, then flush stdout. The evaluator replies with `0` or `1` and updates the hidden mole state exactly as described above.

To answer the current source session, write:

```text
! x
```

where `x` is the mole's current node after all of your previous queries.

## Limits And Scoring

The shipped interactor loops for at most `500` query or answer operations. It scores a correct answer using the sum of queried depths:

```text
score = clamp((3 * best - depth_cost) / (2 * best), 0, 1)
```

Here `best` is the source answer-file value for that official tree, and `depth_cost` is the sum of the depths of every queried node. Agentics scales the bounded source ratio to the public `score` metric from `0` to `100`.

Malformed commands, out-of-range vertices, too many queries, EOF before a final answer, or a wrong current node are protocol failures. The trusted evaluator owns hidden mole state and writes `result.json`.
