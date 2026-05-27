# Uniform Cave Explorer

This challenge migrates Frontier-CS `algorithmic/problems/80` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator owns the hidden session state, speaks the original stdin/stdout protocol, enforces protocol and query limits, validates the final answer, and writes Agentics `result.json`.

## Contract

Submit a `zip_project` solution. The run command participates in one interactive session through standard input and standard output. Flush after each command. Network access is disabled.

## Provenance

- Source path: `algorithmic/problems/80`
- Original shape: Frontier-CS interactive problem with `interactor.*` and benchmark/session data.
- Agentics mode: `piped_stdio`
- Target: `linux-arm64-cpu`

Public validation uses a tiny deterministic session. Official hidden sessions are supplied through the private `official-runs` overlay at `private-benchmark/session.json` and are not committed.
