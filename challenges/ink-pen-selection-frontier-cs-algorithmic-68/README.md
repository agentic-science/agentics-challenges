# Ink Pen Selection

This challenge migrates Frontier-CS `algorithmic/problems/68` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator compiles and runs the original Frontier-CS Testlib `interactor.cpp`, preserving hidden ink permutations, the write-test protocol, final two-pen validation, and source scoring by fraction of successful cases.

Submitted `zip_project` solutions communicate only through stdin/stdout. The evaluator first prints `t`, then each case prints `n`. The participant may try pens with `0 i`, which consumes one unit if the pen still has ink, and must end the case with `1 i j`. The next case starts immediately after a valid selection, until all `t` cases are complete.

- Source path: `algorithmic/problems/68`
- Original title: `Pen`
- Execution mode: `piped_stdio`
- Public validation: one tiny deterministic permutation
- Official evaluation: private Frontier-CS-derived source cases in `private-benchmark/session.json`

Malformed commands, out-of-range pen indices, choosing the same pen twice, EOF before all cases finish, and invalid action types are handled by the source interactor. The trusted evaluator writes `result.json`; participant code must not create it.
