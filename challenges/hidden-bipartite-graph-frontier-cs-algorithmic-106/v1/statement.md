# Hidden Bipartite Graph

You are communicating with a trusted evaluator that owns a hidden simple undirected connected graph. Your program must decide whether the graph is bipartite while seeing only answers to subset edge-count queries.

This is a `piped_stdio` interactive challenge. At the start of each case the evaluator prints one integer `n`, the number of vertices. After all Agentics cases are complete, the evaluator prints a single `0` sentinel and closes the session. Your solution may also terminate on EOF.

To ask a query, print two lines and flush:

```text
? k
s1 s2 ... sk
```

The set size must satisfy `1 <= k <= n`; the listed vertices must be distinct and in `1..n`. The evaluator replies with the number of hidden graph edges with both endpoints inside the set. The original source interactor enforces a limit of 5000 queries per case.

When ready, print the final proof in one of these forms:

```text
Y s
a1 a2 ... as
```

for a valid bipartition side, or:

```text
N l
c1 c2 ... cl
```

for an odd cycle whose consecutive vertices, including the final-to-first pair, are hidden graph edges.

Malformed output, invalid vertices, duplicate query vertices, exceeding the query limit, EOF before a final answer, or a wrong proof receives the original source failure handling. The trusted evaluator alone writes `result.json`; participant output is never trusted as a result file.

The leaderboard score is the original Testlib ratio scaled to `0..100`: `(5000 - q) / 5000`, where `q` is the source interactor loop count when the final answer is accepted. Public validation uses a tiny deterministic smoke graph. Official scoring uses private Frontier-CS testdata packaged outside Git.
