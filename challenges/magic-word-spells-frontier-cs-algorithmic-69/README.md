# Magic Word Spells

This challenge migrates Frontier-CS `algorithmic/problems/69` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator compiles and runs the original Frontier-CS Testlib `interactor.cc`, preserving the word validation rules, generated power questions, exact ordered-pair checks, and source length-ratio scoring.

Submitted `zip_project` solutions communicate only through stdin/stdout. The source interactor prints `n q`, then reads `n` participant-created words over `{X, O}`. It sends `q` spell powers, each derived from the participant's own words and evaluator-owned ordered pairs, and expects the exact ordered pair of word indices after each power.

- Source path: `algorithmic/problems/69`
- Original title: `Magic Words`
- Execution mode: `piped_stdio`
- Public validation: one tiny deterministic `n = 3` session
- Official evaluation: private Frontier-CS-derived source cases and optimal totals in `private-benchmark/session.json`

Malformed words, duplicate words, length violations, invalid answers, wrong ordered pairs, and EOF are handled by the source interactor. The trusted evaluator writes `result.json`; participant code must not create it.
