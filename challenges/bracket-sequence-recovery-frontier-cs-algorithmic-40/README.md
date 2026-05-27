# Bracket Sequence Recovery

This challenge migrates Frontier-CS `algorithmic/problems/40` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden bracket sequence, enforces the 200-query limit, validates the final string, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read `n`, the length of the hidden sequence.
- To query, output `0 k i_1 ... i_k`, flush stdout, and read the number of non-empty regular bracket substrings in the selected string.
- Each query must satisfy `1 <= k <= 1000` and `1 <= i_j <= n`.
- To answer, output `1 s`, where `s` is the recovered bracket string.
- Agentics may run multiple source cases in one session. After each answer, keep reading; a positive `n` starts the next case and terminal `n = 0` ends the session.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/40`
- Original title: Interactive RBS
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cpp`, and hidden bracket strings.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cpp` compiled with Testlib inside `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden bracket data must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and is not committed.
