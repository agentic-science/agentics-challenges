# Modpow Timing Key

This challenge migrates Frontier-CS `algorithmic/problems/79` into an Agentics
`piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive
evaluator through stdin/stdout. The evaluator owns the hidden exponent `d`,
answers timing queries for `modPow(a, d, n)`, enforces the `30000` query limit,
validates the final key, and reports the source interactor ratio as the
leaderboard score.

## Contract

- Read one modulus `n` from stdin.
- Query with `? a`, where `0 <= a < n`; flush stdout and read the measured time.
- Finish the case with `! d`. This must be the last request for that case.
- Agentics may run multiple original Frontier-CS cases in one session. After a
  final answer, keep reading; a line containing only `0` ends the session.
- Malformed commands, invalid `a`, too many queries, EOF, or a wrong `d` are
  judged by the trusted evaluator.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/79`
- Original title: Hack
- Original shape: Frontier-CS interactive algorithmic benchmark with
  `config.yaml`, `statement.txt`, `interactor.cc`, and hidden `(n, d)` pairs.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside
  `interactive-evaluator/run.py`.

Public validation is intentionally tiny and uses an illustrative small modulus.
Official Frontier-CS `(n, d)` pairs must be supplied through the required
private asset `official-runs` at `private-benchmark/session.json` and are not
committed.
