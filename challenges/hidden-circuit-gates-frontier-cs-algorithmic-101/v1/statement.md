# Hidden Circuit Gates

This is an interactive challenge. The evaluator first prints `N R`, then `N` wiring lines `Ui Vi`. Slot `i` uses switch outputs `Ui` and `Vi`, where the hidden gate at slot `i` is either AND (`&`) or OR (`|`). The hidden gate string is evaluator-only.

For a query, print one line:

```text
? s
```

`s` must be a binary string of length `2N + 1`, setting switches `0..2N`. The evaluator computes the circuit from high indices down to slot `0` and replies with the output of switch `0`, either `0` or `1`. At most `5000` queries are allowed. Flush after each query.

To answer, print one line:

```text
! t
```

`t` must have length `N` and contain only `&` and `|`. It must exactly match all hidden slot types. Flush and then continue reading for another source case or exit on EOF.

Malformed strings, wrong lengths, invalid characters, query-limit failures, and wrong gate strings are rejected by the trusted evaluator. The evaluator writes `result.json`. The source score is full through `900` queries, zero from `5000` queries, and linear between those limits.
