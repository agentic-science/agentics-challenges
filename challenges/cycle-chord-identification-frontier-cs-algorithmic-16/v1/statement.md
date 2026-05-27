# Cycle Chord Identification

You interact with a hidden undirected cycle on vertices `1..n`. The cycle has edges `(i, i+1)` and `(n, 1)`, and the judge has added one hidden non-adjacent chord. Your task is to identify the chord.

## Session

The evaluator starts each Frontier-CS source session by writing an integer `T`. For each test case it then writes `n`. Public validation uses one tiny case; official evaluation may run several private source sessions back to back. After the last session the evaluator writes terminal `0` and then closes stdout. Treat EOF as successful session termination too.

## Queries

To query a shortest-path distance, write:

```text
? x y
```

where `1 <= x, y <= n`, then flush stdout. The evaluator replies with one integer, the shortest-path distance between `x` and `y` in the cycle plus hidden chord graph.

To answer the current case, write:

```text
! u v
```

where `u` and `v` are your guessed chord endpoints. The evaluator replies with `1` for a correct guess and `-1` for an incorrect guess. A correct guess advances to the next test case or source session. An incorrect guess ends the run with score zero for that source session.

## Limits And Scoring

The original Frontier-CS interactor allows at most `500` distance queries per test case. The final answer does not count as a query. The trusted evaluator writes `result.json`; participant programs must not create or modify it.

The source scoring function is:

```text
f(Q) = 100 - Q^2 / 200                                 for 0 <= Q <= 40
f(Q) = 72 * exp(-0.0329013504337 * (Q - 40)) + 20      for 40 < Q <= 100
f(Q) = 30 * (1 - (Q - 100) / 400)^2                    for 100 < Q <= 500
f(Q) = 0                                               for Q > 500
```

The shipped source interactor reports the minimum ratio inside a source input file; this migration preserves that behavior and scales it to the public `score` metric from `0` to `100`.

Malformed commands, out-of-range vertices, too many queries, EOF before a final answer, or a wrong chord are protocol failures.
