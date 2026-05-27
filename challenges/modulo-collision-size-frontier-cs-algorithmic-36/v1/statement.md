# Modulo Collision Size

This is an interactive challenge. The trusted evaluator hides an integer `n`, the number of buckets in an `unordered_set`, and you must recover it by asking collision-count queries.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cpp` protocol in a `piped_stdio` session.

## Input

There is no initial input for a source case. Public validation contains one tiny smoke case. Official evaluation may chain multiple source cases; after you submit a final answer for one case, the next case begins immediately with no banner. If the evaluator reaches the end of the session, stdin closes and your program should exit.

## Output

To ask a query, output:

```text
0 m x_1 x_2 ... x_m
```

Then flush stdout and read one integer response from stdin. The response is the number of hash collisions caused by inserting the values in order into a fresh table with `n` buckets. Each query value must be in `[1, 10^18]`, and the total cost over a source case is the sum of all `m`.

To guess the hidden bucket count for the current source case, output:

```text
1 n
```

The guess itself does not count as a query. For chained no-prompt Agentics sessions, start the next source case after the guess; EOF means the evaluator is done.

## Scoring

The source interactor enforces total query cost at most `1,000,000`. A wrong guess, malformed command, out-of-range query value, or exceeded cost limit receives zero for that case. Otherwise, the source ratio is `min(1, 1000001 / (Q + 1))`, where `Q` is the total query cost. Agentics reports the average source ratio as `score` from 0 to 100.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
