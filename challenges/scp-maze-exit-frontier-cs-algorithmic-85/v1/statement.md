# SCP Maze Exit

This is an interactive challenge. You are lost in an infinite colored binary
tree. At each non-exit node, three incident edges have colors `0`, `1`, and `2`,
but you do not know which color moves closer to the exit. A ranging device can
report the current distance to the exit.

The original Frontier-CS problem was interactive. This Agentics migration keeps
the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

For each case, the evaluator writes:

```text
initialDeep
```

where `initialDeep <= 10000`.

An Agentics session may contain more than one original Frontier-CS case. After
you reach the exit for one case, keep reading stdin. If another positive
`initialDeep` arrives, solve that case. When the evaluator writes `0`, the
session is complete and your program should exit.

## Output

To measure your current distance, output:

```text
query
```

Flush stdout and read the current distance.

To move along one colored edge, output:

```text
move c
```

where `c` is `0`, `1`, or `2`. Flush stdout and read `1` if this move reaches
the exit, otherwise read `0`. Once a case returns `1`, do not issue more
commands for that case.

## Scoring

The source interactor allows at most `100000` moves and at most `100000`
distance queries. If you reach the exit, the source ratio is:

```text
5000 / queries
```

clamped to `[0, 1]` and reported as a 0-100 Agentics score. Fewer distance
queries are better. Invalid commands, invalid colors, EOF, too many moves, or
too many queries receive zero.

## Result Ownership

Your solution only communicates over stdin/stdout. The trusted interactive
evaluator owns the hidden maze path, answers all moves and distance queries,
enforces protocol validity, and writes `result.json`.
