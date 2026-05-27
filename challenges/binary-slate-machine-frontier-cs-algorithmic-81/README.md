# Binary Slate Machine

This challenge migrates Frontier-CS `algorithmic/problems/81` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden binary slate string, enforces the source query protocol and limits, validates the final answer, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read the initial integer `N` from stdin.
- To query the machine, output `1`, then `m`, then `m` integers for sequence `a`, then `m` integers for sequence `b`; flush stdout and read the machine response.
- To guess the current string, output `0` followed by the binary string `S`.
- Agentics may run multiple source cases in one session. After each guess, keep reading; a positive `N` starts the next case and terminal `N = 0` ends the session.
- At most `1000` queries are allowed, and each query must satisfy `1 <= m <= 1002` with all sequence values in `[0, m)`.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/81`
- Original title: Binary Slate Machine
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cc`, and hidden slate strings.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden slate data must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and is not committed.
