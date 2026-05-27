# Inversion Recovery

This is an interactive `zip_project` challenge. For each case, the trusted evaluator prints:

```text
n
```

It has a hidden permutation `p1, p2, ..., pn` of `1..n`. To query a subarray, print:

```text
0 l r
```

where `1 <= l <= r <= n`. The evaluator replies with the parity of the number of inversions in `p_l, ..., p_r`.

You may ask at most 1,999,000 queries in a case. To finish the case, print:

```text
1 p1 p2 ... pn
```

The final answer does not count as a query. In Agentics, a session may contain multiple source cases; after a final answer, the next case begins immediately with another `n` line. Exit when stdin reaches EOF. Malformed output, invalid intervals, too many queries, EOF before a final answer, and wrong final permutations are handled by the source interactor.

Official scoring uses the source formula `(exp(-q / 249875) - exp(-8)) / (1 - exp(-8))`, averaged across private cases and scaled to `score` from 0 to 100. The trusted evaluator writes `result.json`.
