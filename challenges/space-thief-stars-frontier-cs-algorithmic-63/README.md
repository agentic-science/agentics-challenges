# Space Thief Stars

This challenge migrates Frontier-CS `algorithmic/problems/63` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator compiles and runs the original Frontier-CS Testlib `interactor.cpp`, preserving the hidden key and treasure stars, directed-edge query protocol, 600-query limit, final guess validation, and source scoring.

Submitted `zip_project` solutions communicate only through stdin/stdout. A case starts when the evaluator prints `N M` followed by the undirected edges. The participant may ask orientation queries and then prints one final guess. Agentics sessions may contain multiple source cases: after a final guess, the next case starts immediately with another `N M` line, and EOF means there are no more cases.

- Source path: `algorithmic/problems/63`
- Original title: `Space Thief`
- Execution mode: `piped_stdio`
- Public validation: one tiny deterministic path graph
- Official evaluation: private Frontier-CS-derived source cases in `private-benchmark/session.json`

Malformed commands, invalid orientation bits, invalid final guesses, excess queries, and EOF before a final guess are handled by the source interactor. The trusted evaluator writes `result.json`; participant code must not create it.
