# Modpow Timing Key

This is an interactive challenge. A hidden device stores a modulus `n` and an
exponent `d`. It computes `a^d mod n` with the original Frontier-CS
square-and-multiply pseudocode, but it only reports the time taken by the
modular multiplications. Recover `d`.

The original Frontier-CS problem was interactive. This Agentics migration keeps
the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

For each case, the evaluator writes one integer:

```text
n
```

Official cases use the original generation model: `n = p*q` for two random
30-bit primes and `d` is coprime with `(p-1)*(q-1)`. Public validation may use a
smaller illustrative modulus for a deterministic smoke test.

An Agentics session may contain more than one original Frontier-CS case. After
you submit a final answer for one case, keep reading stdin. If another positive
`n` arrives, solve that case. When the evaluator writes `0`, the session is
complete and your program should exit.

## Output

To query the device, output:

```text
? a
```

where `0 <= a < n`. Flush stdout and read the reported time.

To finish the current case, output:

```text
! d
```

This final answer must be issued exactly once and must be the last request for
that case.

## Scoring

The source interactor allows at most `30000` timing queries. If `d` is correct,
the source ratio is based on query count:

```text
(30000 - queries) / (30000 - 4000)
```

clamped to `[0, 1]` and reported as a 0-100 Agentics score. Invalid commands,
invalid query values, too many queries, EOF, or an incorrect final key receive
zero.

## Result Ownership

Your solution only communicates over stdin/stdout. The trusted interactive
evaluator owns all hidden keys, computes all timing replies, enforces protocol
validity, and writes `result.json`.
