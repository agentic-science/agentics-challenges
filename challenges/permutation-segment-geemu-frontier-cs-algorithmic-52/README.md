# Permutation Segment Geemu

This challenge migrates Frontier-CS `algorithmic/problems/52` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden permutation, applies participant swaps to its private state, enforces operation limits, validates the final permutation up to the source reverse-value equivalence, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read `n l1 l2`, the permutation length and operation limits.
- To query value-contiguous segment count in an interval, output `1 l r`, flush stdout, and read one integer response.
- To swap current positions, output `2 i j`, flush stdout, and read confirmation `1`.
- To answer, output `3 p_1 ... p_n`.
- Agentics may run multiple source cases in one session. After each report, keep reading; a positive `n l1 l2` starts the next case and terminal `0 0 0` ends the session.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/52`
- Original title: Geemu
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cc`, hidden permutations, and reference operation counts.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden permutations and reference costs must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and are not committed.
