# Inter Active Permutation

This challenge migrates Frontier-CS `algorithmic/problems/53` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden derangement, enforces the source query protocol and safety limit, validates the final permutation, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read `t`, then read one `n` for each source test case.
- For each case, output a fixed position `k`.
- To query, output `? q_1 ... q_n`, flush stdout, and read one integer response.
- To answer, output `! p_1 ... p_n`.
- The source input file owns all test-case framing; no extra Agentics terminal marker is added.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/53`
- Original title: G2. Inter Active (Hard Version)
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cc`, and hidden derangements.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden derangements must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and are not committed.
