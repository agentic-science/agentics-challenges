# Modulo Collision Size

This challenge migrates Frontier-CS `algorithmic/problems/36` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden bucket count `n`, enforces the source query-cost limit, validates the final guess, and reports the source interactor ratio as the leaderboard score.

## Contract

- There is no initial participant-visible input for a source case.
- To query collision count, output `0 m x_1 ... x_m`, flush stdout, and read one integer response.
- Query values must be in `[1, 10^18]`; the total query cost is the sum of all `m`.
- To guess, output `1 n`.
- Agentics public validation contains one no-prompt source case. Official sessions may chain source cases back to back; after a final guess, the next case begins immediately with no banner. EOF means the session is complete.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/36`
- Original title: Hack!
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cpp`, and hidden bucket counts.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: source-equivalent `interactor.cpp` compiled with Testlib inside `interactive-evaluator/run.py`; it uses sparse per-query residue counts so official bucket counts up to the source limit do not require allocating `n` buckets.

Public validation is intentionally tiny. Official Frontier-CS hidden bucket-count data must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and is not committed.
