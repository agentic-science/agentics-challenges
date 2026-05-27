# Ink Pen Selection

This is an interactive `zip_project` challenge. The evaluator first prints the number of cases:

```text
t
```

For each case, it prints:

```text
n
```

The hidden ink amounts form a permutation of `0, 1, ..., n - 1`. To try pen `i`, print:

```text
0 i
```

The evaluator replies with `1` if the pen had ink before this write and consumes one unit from that pen. It replies with `0` if the pen was already empty.

To finish the case, print two distinct pen indices:

```text
1 i j
```

The case succeeds if the remaining ink in those two pens sums to at least `n`. After the selection, the next case starts immediately with its `n`, or the session ends after all `t` cases. EOF before completing the announced cases, malformed output, invalid pen indices, equal selected indices, and invalid action types are handled by the source interactor.

Official scoring is the source ratio `successful_cases / t`, scaled to `score` from 0 to 100. The trusted evaluator owns all hidden ink states and writes `result.json`.
