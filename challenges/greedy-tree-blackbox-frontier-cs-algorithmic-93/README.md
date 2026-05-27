# Greedy Tree Blackbox

This challenge migrates Frontier-CS `algorithmic/problems/93` as a faithful `piped_stdio` interactive task. The trusted interactive evaluator owns the hidden source state, speaks the original stdin/stdout protocol, enforces protocol and query limits, validates the final answer, and writes Agentics `result.json`.

Submitted `zip_project` solutions communicate only through stdin/stdout. Private official source cases are visible only to the trusted evaluator.

## Contract

- Source path: `algorithmic/problems/93`.
- Original title: Greedy.
- Agentics mode: `piped_stdio`.
- Evaluator adapter: the original Frontier-CS Testlib interactor is copied to `v1/interactive-evaluator/interactor.cpp` and compiled by `interactive-evaluator/run.py`.
- Public validation is a tiny deterministic smoke case. Official scoring uses the private `official-runs` ZIP overlay at `private-benchmark/session.json`.
- A session may contain one or more original source cases. After finishing a case, keep reading stdin; EOF means the Agentics session is complete.

Protocol errors, malformed output, query-limit failures, and wrong final answers receive the source interactor's zero score for the affected case. The leaderboard `score` is the average source ratio scaled to 0..100.
