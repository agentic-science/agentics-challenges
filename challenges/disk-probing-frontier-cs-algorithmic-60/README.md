# Disk Probing

This challenge migrates Frontier-CS `algorithmic/problems/60` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator compiles and runs the original Frontier-CS Testlib `interactor.cpp`, so the hidden disk, segment-query protocol, 1024-query limit, exact final-answer validation, and source query-efficiency scoring remain evaluator-owned.

Submitted `zip_project` solutions communicate only through stdin/stdout. This source problem has no startup prompt: a participant begins by writing `query x1 y1 x2 y2` commands and eventually writes one `answer x y r` command. To preserve that no-prompt source framing, each Agentics session contains one original source-style case.

- Source path: `algorithmic/problems/60`
- Original title: `Problem K: Probing the Disk`
- Execution mode: `piped_stdio`
- Public validation: one tiny deterministic sample-style hidden disk
- Official evaluation: private Frontier-CS-derived hidden disk in `private-benchmark/session.json`

Malformed commands, out-of-range coordinates, repeated endpoints, excess queries, incorrect final answers, EOF before the final answer, and extra output handled by the Testlib interactor receive the original source verdict behavior. The trusted evaluator writes `result.json`; participant code must not create it.
