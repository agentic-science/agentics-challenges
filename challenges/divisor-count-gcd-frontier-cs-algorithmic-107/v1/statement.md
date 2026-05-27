# Guess Divisors Count

You are playing one or more independent games against a trusted evaluator. In each game the evaluator has fixed a hidden integer `1 <= X <= 10^9`. You do not need to recover `X`; you need to output an estimate of the number of positive divisors of `X`.

This is a `piped_stdio` interactive challenge. At the start of each source testcase the evaluator prints one integer `T`, the number of games in that testcase. After you answer the `T` games, the next source testcase, if any, begins immediately with another `T`. After all Agentics cases are complete, the evaluator prints a single `0` sentinel and closes the session. Your solution may also terminate on EOF.

To ask a query in the current game, print and flush:

```text
0 Q
```

where `1 <= Q <= 10^18`. The evaluator replies with `gcd(X, Q)`. The original source interactor allows at most 100 queries per game.

To finish the current game, print and flush:

```text
1 ans
```

The answer is accepted if either `|ans - d| <= 7` or `1/2 <= ans / d <= 2`, where `d` is the true divisor count of the hidden integer.

Malformed output, an invalid query, exceeding the per-game query limit, EOF before all games are answered, or an answer outside the accepted approximation window receives the original source failure handling. The trusted evaluator alone writes `result.json`; participant output is never trusted as a result file.

The leaderboard score is the original Testlib ratio scaled to `0..100`: `(100 - q) / 100`, where `q` is the maximum query count used by any accepted game in the source testcase. Public validation is a tiny deterministic smoke session. Official scoring uses private Frontier-CS hidden integers and judge-owned divisor counts packaged outside Git.
