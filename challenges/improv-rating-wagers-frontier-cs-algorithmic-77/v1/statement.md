# Improv Rating Wagers

This is an interactive challenge. You play as Izzy in a sequence of improv
wagers. For every wager, the evaluator first reveals the other participants'
binary predictions. You must output Izzy's prediction before the evaluator
reveals the actual outcome.

The original Frontier-CS problem was interactive. This Agentics migration keeps
the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

For each case, the evaluator writes:

```text
n m
```

Then, for each of the `m` wagers, it writes one binary string of length `n`.
The `i`-th character is the prediction made by participant `i`.

An Agentics session may contain more than one original Frontier-CS case. After a
case ends, keep reading stdin. If another `n m` header arrives, solve that case.
When the evaluator writes a line containing only `0`, the session is complete
and your program should exit.

## Output

For each wager, output exactly one integer:

```text
0
```

or:

```text
1
```

Flush stdout after every prediction. The evaluator then writes the true outcome,
also `0` or `1`, before proceeding to the next wager.

## Scoring

Let `c` be Izzy's number of wrong predictions. Let `b` be the smallest number of
wrong predictions made by any other participant. The trusted evaluator uses the
same source score as Frontier-CS:

```text
min((2*b - c) / b, 1)
```

clamped at zero and reported as a 0-100 Agentics score. Output outside `0` and
`1`, EOF before the session ends, or malformed protocol data receives zero.

## Result Ownership

Your solution only communicates over stdin/stdout. The trusted interactive
evaluator owns all hidden wager outcomes, enforces protocol validity, and writes
`result.json`.
