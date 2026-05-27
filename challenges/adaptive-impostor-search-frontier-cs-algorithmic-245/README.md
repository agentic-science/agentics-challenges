# Adaptive Impostor Search

This Agentics challenge migrates Frontier-CS `algorithmic/problems/245` as a `piped_stdio` interactive challenge. The trusted `interactive-evaluator/run.py` wraps the original Frontier-CS Testlib interactor, so hidden state, protocol validation, query limits, and source scoring remain judge-owned.

Submitted `zip_project` solutions communicate only through stdin/stdout with the interactive evaluator. Public validation uses a tiny synthetic mini session for protocol plumbing. Official evaluation uses the private `official-runs` overlay at `private-benchmark/session.json` with Frontier-CS-derived hidden input and answer files.

- Target: `linux-arm64-cpu`
- Execution mode: `piped_stdio`
- Source path: `algorithmic/problems/245`
- Summary: Emit canonical impostor guesses for adaptive source cases.

The Agentics wrapper scales the Frontier-CS Testlib ratio to the public primary metric `score` on a 0-100 scale and caps evaluator log messages before writing `result.json`.
