# Hidden Cycle Length

This challenge migrates Frontier-CS `algorithmic/problems/14` as a faithful `piped_stdio` interactive task. The trusted evaluator compiles and runs the source Testlib interactor, preserving the hidden cycle length, token position, lazy random label assignment, `walk`/`guess` protocol, 200000-walk limit, and source log-space scoring curve.

- Source title: hidden cycle length interactive problem
- Source files inspected: `statement.txt`, `config.yaml`, `interactor.cpp`, and `testdata/`
- Agentics mode: `piped_stdio`
- Private asset: `official-runs.zip` provides `private-benchmark/session.json` plus official `.in` and `.ans` files outside Git

Public validation is a tiny deterministic smoke case. Official evaluation uses the private Frontier-CS cases and reports the source interactor ratio as `score` on a 0-100 scale.
