# Graph Connectivity Oracle

You interact with a hidden undirected simple graph on `n` vertices. You must decide whether the graph is connected.

For a chosen subset `S`, the judge returns `|N(S) \\ S|`, the number of vertices outside `S` that have at least one edge to a vertex in `S`.

## Session

The evaluator starts each Frontier-CS source session by writing an integer `T`. For each test case it then writes `n`. Public validation uses one small graph; official evaluation may run several private source sessions back to back. After the last session the evaluator writes terminal `0` and then closes stdout. Treat EOF as successful session termination too.

## Source Wire Format

The original interactor has a token-level parsing quirk. It reads a whole operation as one token, then consumes the subset bits starting at character index `2`. To preserve source behavior, write query tokens in this form:

```text
?#0101
```

The first character is `?`, the second character is ignored by the source interactor, and the next `n` characters are the binary subset indicator. Any separator character can be used in position `1`; `#` is recommended.

The evaluator replies with one integer, the value of `|N(S) \\ S|`.

To answer the current case, write one token:

```text
!#1
```

Use `1` if the graph is connected and `0` otherwise. The first character is `!`, the second character is ignored, and character index `2` is parsed as the answer.

## Limits And Scoring

The source interactor allows at most `3500` operations per test case. It increments the counter before both query and final-answer parsing, exactly as the shipped source does.

For each source case, `best_score = n * max(1, floor(log2(n)))`, and the raw score is:

```text
(3500 - operations) / (3500 - best_score)
```

The source clamps the public ratio at `1.0` when aggregating cases and reports the average over the source session. Agentics scales that ratio to the public `score` metric from `0` to `100`.

Malformed tokens, invalid subset characters, too many operations, EOF before a final answer, or a wrong connectivity judgement are protocol failures. The trusted evaluator owns hidden graphs and writes `result.json`.
