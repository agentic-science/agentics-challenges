# Maximum Position Permutation

You are given an unknown permutation of length `n`. Your task is to determine the position of value `n`.

## Session

The evaluator starts each Frontier-CS source session by writing an integer `T`. For each test case it then writes `n`. Public validation uses two small cases; official evaluation may run several private source sessions back to back. After the last session the evaluator writes terminal `0` and then closes stdout. Treat EOF as successful session termination too.

## Queries

To ask for interval information, write:

```text
? l r
```

where `1 <= l < r <= n`, then flush stdout. The evaluator replies with the position of the second-largest value in the hidden subarray `p[l..r]`.

To answer the current case, write:

```text
! x
```

where `x` is the position of value `n`.

## Limits And Scoring

For each test case, the source interactor enforces:

- `2 <= n <= 100000`
- the total `n` over the source session is at most `100000`
- the sum of `(r - l + 1)` over all queries in a test case is at most `30n`

Let `q` be the query count and `L = log2(n)`. The source score for a test case is `100` when `q <= L`, `0` when `q >= 15L`, and linearly interpolated between those values. The final source score is the minimum bounded percentage over all cases in the source session. Agentics scales that ratio to the public `score` metric from `0` to `100`.

Malformed commands, invalid intervals, exceeding the segment-sum limit, EOF before a final answer, or a wrong position are protocol failures. The trusted evaluator owns hidden data and writes `result.json`.
