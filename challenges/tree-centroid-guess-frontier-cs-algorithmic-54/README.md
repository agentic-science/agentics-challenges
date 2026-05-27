# Tree Centroid Guess

This challenge migrates Frontier-CS `algorithmic/problems/54` into an Agentics `piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive evaluator through stdin/stdout. The evaluator owns the hidden tree, answers distance queries, validates the final centroid, enforces the source safety limit, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read `n`, the number of nodes in the hidden tree.
- To query distance, output `? u v`, flush stdout, and read the distance.
- To answer, output `! x`, where `x` is the unique centroid.
- The official source case is a single hidden tree. EOF after the final answer means the session is complete.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/54`
- Original title: Centroid Guess
- Original shape: Frontier-CS interactive algorithmic benchmark with `config.yaml`, `statement.txt`, `interactor.cc`, a hidden tree, and a private centroid answer.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden tree data must be supplied through the required private asset `official-runs` at `private-benchmark/session.json` and is not committed.
