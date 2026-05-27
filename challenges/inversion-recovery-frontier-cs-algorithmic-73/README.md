# Inversion Recovery

This challenge migrates Frontier-CS `algorithmic/problems/73` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator compiles and runs the original Frontier-CS Testlib `interactor.cpp`, preserving the hidden permutation, inversion-parity query protocol, 1,999,000-query limit, final permutation validation, and source exponential query-efficiency scoring.

Submitted `zip_project` solutions communicate only through stdin/stdout. A case starts when the evaluator prints `n`. The participant may ask `0 l r` queries and eventually prints `1 p1 p2 ... pn`. Agentics sessions may contain multiple source cases: after a final answer, the next case starts immediately with another `n` line, and EOF means there are no more cases.

- Source path: `algorithmic/problems/73`
- Original title: `Inversion`
- Execution mode: `piped_stdio`
- Public validation: one tiny deterministic permutation
- Official evaluation: private Frontier-CS-derived source cases in `private-benchmark/session.json`

Malformed commands, invalid intervals, excess queries, wrong final permutations, and EOF before a final answer are handled by the source interactor. The trusted evaluator writes `result.json`; participant code must not create it.
