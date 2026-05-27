# DiverC Autofill Words

You interact with an autofill service backed by a hidden dictionary of distinct lowercase words. For a prefix `S` and integer `K`, the service returns the first `K` hidden words with that prefix in lexicographic order, or fewer if fewer exist.

## Session

The evaluator starts each Frontier-CS source session by writing `T`, then `N`, the number of hidden words. The shipped source test files each contain one case. Official evaluation may run several private source sessions back to back. After the last session the evaluator writes terminal `0` and then closes stdout. Treat EOF as successful session termination too.

## Queries

To query the service, write:

```text
query S K
```

where `1 <= |S| < 10` in the shipped interactor and `1 <= K <= N`, then flush stdout. The evaluator replies on one line:

```text
k W1 W2 ... Wk
```

where `0 <= k <= K` and the words are in lexicographic order.

To submit the dictionary, write:

```text
answer W1 W2 ... WN
```

There is no per-case acknowledgement after `answer`; the source interactor finishes that source session immediately.

## Limits And Scoring

The source interactor accepts at most `4000` operations. Let `sumK` be the sum of every queried `K`. The shipped source score is:

```text
score = clamp((4000 - sumK) / (4000 - 2400), 0, 1)
```

The source also reports an unbounded ratio for diagnostics. Agentics scales the bounded source ratio to the public `score` metric from `0` to `100`.

Malformed commands, invalid prefixes, invalid `K`, repeated answer words, EOF before an answer, or an answer rejected by the source interactor are protocol failures. The trusted evaluator owns hidden word counts and writes `result.json`.
