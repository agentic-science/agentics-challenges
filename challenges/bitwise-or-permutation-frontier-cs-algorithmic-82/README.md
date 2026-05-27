# Bitwise OR Permutation

This challenge migrates Frontier-CS `algorithmic/problems/82` into an Agentics
`piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive
evaluator through stdin/stdout. The evaluator owns the hidden permutation,
answers pairwise bitwise-OR queries, enforces the `4269` query limit, validates
the final permutation exactly, and reports the source interactor ratio as the
leaderboard score.

## Contract

- Read one integer `n` from stdin.
- Query with `? i j`, where `1 <= i, j <= n` and `i != j`; flush stdout and
  read `p_i | p_j`.
- Finish the case with `! p_1 p_2 ... p_n`.
- Agentics may run multiple original Frontier-CS cases in one session. After a
  final answer, keep reading; a line containing only `0` ends the session.
- Malformed commands, out-of-range indices, too many queries, EOF, invalid final
  permutations, or wrong values are judged by the trusted evaluator.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/82`
- Original title: Bitwise OR Permutation
- Original shape: Frontier-CS interactive algorithmic benchmark with
  `config.yaml`, `statement.txt`, `interactor.cc`, hidden permutations, and
  source optimal query counts.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside
  `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS hidden
permutations and optimal query counts must be supplied through the required
private asset `official-runs` at `private-benchmark/session.json` and are not
committed.
