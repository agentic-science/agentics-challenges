# SCP Maze Exit

This challenge migrates Frontier-CS `algorithmic/problems/85` into an Agentics
`piped_stdio` interactive bundle with the original Testlib interactor protocol.

Submitted `zip_project` solutions communicate with the trusted interactive
evaluator through stdin/stdout. The evaluator owns the hidden colored path to
the exit, answers distance queries, enforces the move and query limits, and
reports the source interactor ratio as the leaderboard score.

## Contract

- Read one integer `initialDeep` from stdin.
- Output `query` to read the current distance to the exit.
- Output `move c`, where `c` is `0`, `1`, or `2`, to traverse an edge color.
  The evaluator replies `1` only when the move reaches the exit, otherwise `0`.
- Agentics may run multiple original Frontier-CS cases in one session. After the
  evaluator reports `1`, keep reading; a line containing only `0` ends the
  session.
- Once a move reaches the exit for a case, do not send another command for that
  case.
- Malformed commands, invalid colors, EOF, too many moves, or too many queries
  are judged by the trusted evaluator.
- Network access is disabled during setup, build, and run.

## Provenance

- Source path: `algorithmic/problems/85`
- Original title: Maze
- Original shape: Frontier-CS interactive algorithmic benchmark with
  `config.yaml`, `statement.txt`, `interactor.cc`, and hidden maze seed data.
- Agentics mode: `piped_stdio`.
- Trusted evaluator: copied source `interactor.cc` compiled with Testlib inside
  `interactive-evaluator/run.py`.

Public validation is intentionally tiny. Official Frontier-CS maze data must be
supplied through the required private asset `official-runs` at
`private-benchmark/session.json` and is not committed.
