# Bitwise OR Permutation

This is an interactive challenge. A hidden permutation `p` contains every value
from `0` to `n - 1` exactly once. You may ask for the bitwise OR of two hidden
positions, then must recover the whole permutation.

The original Frontier-CS problem was interactive. This Agentics migration keeps
the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

For each case, the evaluator writes:

```text
n
```

Official cases have `3 <= n <= 2048`. Public validation uses a tiny deterministic
case.

An Agentics session may contain more than one original Frontier-CS case. After
you submit a final permutation for one case, keep reading stdin. If another
positive `n` arrives, solve that case. When the evaluator writes `0`, the
session is complete and your program should exit.

## Output

To ask a query, output:

```text
? i j
```

where `1 <= i, j <= n` and `i != j`. Flush stdout and read the integer
`p_i | p_j`.

To finish the current case, output:

```text
! p_1 p_2 ... p_n
```

The final answer does not count as a query.

## Scoring

The source interactor enforces a hard limit of `4269` answered queries. It
validates that the final sequence is exactly the hidden permutation. For
accepted runs, it computes the original raw score `(4269 - queries) / 10` and
reports a source ratio against the optimal query count recorded with that hidden
case. Agentics scales that ratio to 0-100.

Invalid commands, invalid indices, too many queries, EOF, a non-permutation
answer, or a wrong permutation receives zero.

## Result Ownership

Your solution only communicates over stdin/stdout. The trusted interactive
evaluator owns the hidden permutation, answers all OR queries, enforces protocol
validity, and writes `result.json`.
