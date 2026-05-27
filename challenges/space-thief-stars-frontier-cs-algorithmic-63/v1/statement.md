# Space Thief Stars

This is an interactive `zip_project` challenge. For each case, the trusted evaluator prints:

```text
N M
U0 V0
...
U(M-1) V(M-1)
```

The graph is connected and undirected. A hidden key star `A` and treasure star `B` are fixed by the evaluator.

To ask a question, print one line beginning with `0`, followed by `M` integers. For edge `i`, output `0` to orient it from `Ui` to `Vi`, or `1` to orient it from `Vi` to `Ui`:

```text
0 d0 d1 ... d(M-1)
```

The evaluator replies with `1` if `B` is reachable from `A` in that directed graph, and `0` otherwise. You may ask at most 600 questions in a case.

To finish the case, print:

```text
1 A B
```

The final guess does not count as a query. In Agentics, a session may contain multiple source cases; after a final guess, the next case begins immediately with another `N M` line. Exit when stdin reaches EOF. Malformed output, invalid bits, too many queries, EOF before a final guess, and wrong guesses are handled by the source interactor. The trusted evaluator writes `result.json`.

Official scoring uses the source ratio `(600 - q) / 600` for each case, averaged across private cases and scaled to `score` from 0 to 100.
