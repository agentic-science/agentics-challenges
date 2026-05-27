# Improv Rating Wagers

This challenge migrates Frontier-CS `algorithmic/problems/77` into an Agentics
`piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive
evaluator through stdin/stdout. The evaluator owns the hidden wager outcomes,
streams each participant prediction string, enforces that every Izzy prediction
is `0` or `1`, and reports the source interactor ratio as the leaderboard score.

## Contract

- Read one case header `n m` from stdin.
- For each of the `m` wagers, read the other participants' prediction string,
  output one prediction bit, flush stdout, and then read the actual outcome bit.
- Agentics may run multiple original Frontier-CS cases in one session. After a
  case ends, keep reading; a line containing only `0` ends the session.
- Malformed output, EOF before the case is complete, or any prediction outside
  `0` and `1` is judged by the trusted evaluator.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/77`
- Original title: Improv Rating Wagers
- Original shape: Frontier-CS interactive algorithmic benchmark with
  `config.yaml`, `statement.txt`, `interactor.cc`, and hidden wager streams.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside
  `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS wager streams must
be supplied through the required private asset `official-runs` at
`private-benchmark/session.json` and are not committed.
