# Permutation Reconstruction

This is an interactive challenge. There is a hidden permutation of length `n`. The interactor first prints:

```text
n
```

To ask a query, print one line:

```text
0 a1 a2 ... an
```

Each `ai` must be an integer in `[1, n]`. The query sequence does not need to be a permutation. The interactor replies with one integer: the number of positions where your sequence exactly matches the hidden permutation.

To make a final guess, print one line:

```text
1 p1 p2 ... pn
```

The final guess must be a valid permutation. The final guess does not count as a query. Flush stdout after every line you print.

The score is based on correctness and query efficiency relative to the session's baseline and `best_queries`. Wrong guesses, invalid messages, invalid permutations, or query-limit overflow receive score 0.

## Provenance

This challenge is based on Frontier-CS `algorithmic/problems/2`. The original statement called the problem `Permutation` and used a C++ `testlib` interactor. The Agentics migration keeps the same query semantics and implements them with `piped_stdio`.
