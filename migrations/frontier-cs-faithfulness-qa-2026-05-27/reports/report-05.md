# Frontier-CS Faithfulness QA Pass, Slice 05

Checklist read: `/home/maplespark/code/Agentics/migration-checklist.md`

Private asset note: I did not find local private ZIP overlays readily available for the slice handles. Private overlay structure, traversal, symlink, and overwrite checks are therefore marked as blocked subchecks only. Public bundle and Frontier-CS source comparisons were completed.

## Summary

- Reviewed: 25 challenges
- Verdict counts: faithful 12, minor drift 5, major drift 8, blocked 0
- Private ZIP subchecks blocked: 25
- Confirmed findings by severity: P0 0, P1 8, P2 5, P3 0

Confirmed P1 handles: `hidden-bipartite-graph-frontier-cs-algorithmic-106`, `hidden-circuit-gates-frontier-cs-algorithmic-101`, `hidden-cycle-length-frontier-cs-algorithmic-14`, `hidden-tree-median-frontier-cs-algorithmic-86`, `improv-rating-wagers-frontier-cs-algorithmic-77`, `ink-pen-selection-frontier-cs-algorithmic-68`, `inter-active-permutation-frontier-cs-algorithmic-53`, `inversion-recovery-frontier-cs-algorithmic-73`.

Confirmed P2 handles: `imagenet-1m-frontier-cs-imagenet-1m`, `imagenet-2-5m-frontier-cs-imagenet-2-5m`, `imagenet-200k-frontier-cs-imagenet-200k`, `imagenet-500k-frontier-cs-imagenet-500k`, `imagenet-5m-frontier-cs-imagenet-5m`.

## Challenge Reports

- [ ] `hidden-bipartite-graph-frontier-cs-algorithmic-106`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/106`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-bipartite-graph-frontier-cs-algorithmic-106`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `config.yaml` declares `type: interactive` with `interactor.cpp`; the interactor accepts `?` set queries, enforces `MAXQ = 5000`, validates final `Y` or `N` certificates, and scores by remaining query budget. Agentics `v1/spec.json` declares `separated_evaluator`; `v1/statement.md` says the original interaction was replaced by an offline stdin/stdout contract; `v1/separated-evaluator/run.py` only compares stdout tokens to `answer_text` or `answer_path` and assigns 100 or 0.
  - Suggested fix: Restore the original interactive protocol as `piped_stdio` using the Frontier-CS interactor and private `session.json`, or rename/document the task as a non-faithful offline derivative outside the Frontier-CS faithfulness set.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `hidden-circuit-gates-frontier-cs-algorithmic-101`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/101`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-circuit-gates-frontier-cs-algorithmic-101`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cpp` runs an interactive circuit protocol with `?` binary-string queries, `!` gate-string final answers, `QUERY_LIMIT = 5000`, and score from `QUERY_COUNT`. Agentics uses `separated_evaluator`, and its statement/run.py replace the protocol with exact reference-output matching on one stdin record.
  - Suggested fix: Migrate as `piped_stdio` with the source interactor and session data so query validation, final answer validation, and query-count scoring are preserved.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `hidden-cycle-length-frontier-cs-algorithmic-14`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/14`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-cycle-length-frontier-cs-algorithmic-14`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cpp` exposes a live `walk x` and `guess g` protocol, dynamically assigns hidden labels, enforces `MAX_Q = 200000`, and scores the correct guess by a log-space query-count curve. Agentics `statement.md` explicitly replaces all interaction with a single offline answer, and `run.py` uses exact token equality.
  - Suggested fix: Restore the `walk` and `guess` protocol through `piped_stdio` and preserve the query-count scoring curve from the interactor.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `hidden-pair-product-frontier-cs-algorithmic-134`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/134`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-pair-product-frontier-cs-algorithmic-134`
  - Verdict: faithful
  - Notes: Source `config.yaml` is interactive and uses `interactor.cc`; Agentics `spec.json` uses `piped_stdio` with `official_session = private-benchmark/session.json`. The migrated `v1/interactive-evaluator/interactor.cpp` is byte-identical to the Frontier-CS interactor, and `run.py` compiles it and reports the source ratio as score.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `hidden-position-pair-frontier-cs-algorithmic-132`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/132`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-position-pair-frontier-cs-algorithmic-132`
  - Verdict: faithful
  - Notes: Source uses an interactive Testlib interactor. Agentics uses `piped_stdio`; the migrated `interactive-evaluator/interactor.cpp` is byte-identical to source `interactor.cc`, and the wrapper preserves per-case source-ratio scoring and protocol error reporting.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `hidden-tree-median-frontier-cs-algorithmic-86`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/86`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/hidden-tree-median-frontier-cs-algorithmic-86`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cc` sends `n`, accepts LCA-style triple queries with action `0`, validates a final tree with action `1`, and scores with `min((ref_queries + 1) / (your_queries + 1), 1)`. Agentics declares `separated_evaluator`; its statement replaces interaction with one stdin record and exact reference answer matching.
  - Suggested fix: Use `piped_stdio` with the original interactor so hidden tree queries, final tree validation, and query-count scoring remain intact.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `imagenet-1m-frontier-cs-imagenet-1m`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/imagenet_pareto/1m`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/imagenet-1m-frontier-cs-imagenet-1m`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Frontier-CS `evaluator.py` and `score_config.json` are byte-identical to Agentics `v1/source-evaluator.py` and `v1/score_config.json`, preserving dataset generation, parameter limit, and accuracy scoring. Runtime dependencies drift: source `resources/pyproject.toml` allows Python `>=3.10,<3.13`, Torch `>=2.2,<2.4`, NumPy `>=1.24`; Agentics `coexecuted-evaluator/setup.py` writes a separate uv project requiring Python `>=3.12,<3.13`, Torch `>=2.3,<2.6`, NumPy `>=1.26`. The migrated statement still states PyTorch `2.2-2.4`.
  - Suggested fix: Align `setup.py` dependency bounds with the source runtime, or explicitly document and justify the migrated runtime range in the statement and README.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `imagenet-2-5m-frontier-cs-imagenet-2-5m`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/imagenet_pareto/2_5m`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/imagenet-2-5m-frontier-cs-imagenet-2-5m`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Agentics preserves source `evaluator.py` and `score_config.json` byte-for-byte, including the 2.5M parameter limit and linear accuracy score. The runtime setup drifts from source `resources/pyproject.toml` and statement text: source Torch is `>=2.2,<2.4`, while Agentics inline uv setup installs `torch>=2.3,<2.6`; source NumPy is `>=1.24`, while Agentics requires `>=1.26`.
  - Suggested fix: Use the source dependency range in the uv setup, or update public docs to declare the new official runtime.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `imagenet-200k-frontier-cs-imagenet-200k`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/imagenet_pareto/200k`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/imagenet-200k-frontier-cs-imagenet-200k`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source and migrated evaluator/scoring files are byte-identical. Source readme and `resources/pyproject.toml` define CPU PyTorch `2.2-2.4` and NumPy `>=1.24`; Agentics `setup.py` uses an inline uv project with Python `3.12`, `torch>=2.3,<2.6`, and `numpy>=1.26`, while `statement.md` still preserves the original PyTorch `2.2-2.4` environment details.
  - Suggested fix: Make the setup runtime match the source contract or update the statement/README to make the new runtime an explicit migration choice.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `imagenet-500k-frontier-cs-imagenet-500k`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/imagenet_pareto/500k`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/imagenet-500k-frontier-cs-imagenet-500k`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `evaluator.py` and `score_config.json` match the migrated copies, preserving the 500K budget and scoring. The migrated setup does not use the copied source `resources/pyproject.toml`; it installs broader/newer Python package ranges than the source and contradicts the statement environment text.
  - Suggested fix: Align the uv setup with the source dependency policy, or update docs to state the migrated official dependency versions.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `imagenet-5m-frontier-cs-imagenet-5m`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/imagenet_pareto/5m`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/imagenet-5m-frontier-cs-imagenet-5m`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Evaluator and score config are byte-identical to Frontier-CS, preserving the 5M parameter limit. The runtime setup drifts in the same way as the other ImageNet variants: source says Torch `>=2.2,<2.4`, NumPy `>=1.24`; Agentics setup installs Torch `>=2.3,<2.6`, NumPy `>=1.26`, and requires Python `3.12`.
  - Suggested fix: Pin the uv setup to source-compatible dependency bounds or document the changed runtime as intentional.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `impartial-game-graph-frontier-cs-algorithmic-231`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/231`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/impartial-game-graph-frontier-cs-algorithmic-231`
  - Verdict: faithful
  - Notes: Source is interactive and uses `interactor.cc`; Agentics uses `piped_stdio` with `interactive-evaluator/interactor.cpp` byte-identical to source. The wrapper compiles and runs the Testlib interactor and carries over source-ratio scoring.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `improv-rating-wagers-frontier-cs-algorithmic-77`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/77`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/improv-rating-wagers-frontier-cs-algorithmic-77`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `config.yaml` is interactive and `interactor.cc` streams each prediction to the contestant, reads one binary wager/answer per row, reveals the true answer, and scores against the best predictor error count. Agentics turns this into a separated exact-reference stdout task, losing the online prediction protocol and ratio formula.
  - Suggested fix: Migrate with `piped_stdio` and the original interactor, including per-row answer reveal and final ratio calculation.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `increasing-subsequence-permutation-frontier-cs-algorithmic-33`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/33`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/increasing-subsequence-permutation-frontier-cs-algorithmic-33`
  - Verdict: faithful
  - Notes: Source `checker.cpp` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`. Agentics `run.py` compiles the checker and parses `Ratio` and `RatioUnbounded`, preserving partial scoring and invalid-output behavior.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `independent-set-complement-score-frontier-cs-algorithmic-183`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/183`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/independent-set-complement-score-frontier-cs-algorithmic-183`
  - Verdict: faithful
  - Notes: Source `checker.cc` reads a binary independent-set vector, rejects selected adjacent endpoints, and reports `Ratio = (N - K_optimal) / (N - K_user)`. Agentics `run.py` implements the same independent-set validation and complement score through `validate_independent_set(..., complement_score=True)`.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `induced-triple-graph-frontier-cs-algorithmic-120`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/120`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/induced-triple-graph-frontier-cs-algorithmic-120`
  - Verdict: faithful
  - Notes: Source interactive `interactor.cpp` is byte-identical to migrated `interactive-evaluator/interactor.cpp`. Agentics `spec.json` uses `piped_stdio`, and the wrapper preserves the source protocol and score extraction.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `ink-pen-selection-frontier-cs-algorithmic-68`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/68`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/ink-pen-selection-frontier-cs-algorithmic-68`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cpp` sends each test case, accepts decrement queries `op = 0` with immediate 1/0 responses, accepts final pair reports `op = 1`, and scores `cnt / t`. Agentics `statement.md` replaces all interaction with a single benchmark record and `run.py` does exact reference matching.
  - Suggested fix: Restore the decrement-query protocol under `piped_stdio` and keep the original `cnt / t` scoring.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `inter-active-permutation-frontier-cs-algorithmic-53`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/53`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/inter-active-permutation-frontier-cs-algorithmic-53`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cc` sends `n`, reads `k`, accepts `?` permutation queries, validates `!` final permutation answers, enforces a safety query limit, and scores quadratically by query count. Agentics declares `separated_evaluator` and exact stdout-token matching, so the interactive query strategy and score curve are absent.
  - Suggested fix: Use `piped_stdio` with the source interactor and session data.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `interval-dag-computer-frontier-cs-algorithmic-7`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/7`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/interval-dag-computer-frontier-cs-algorithmic-7`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/checker.cpp`. Agentics uses separated evaluation, compiles the copied checker, and preserves Testlib ratio parsing.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `interval-set-merge-frontier-cs-algorithmic-225`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/225`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/interval-set-merge-frontier-cs-algorithmic-225`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/chk.cc`. Agentics `run.py` compiles `chk.cc`, uses Testlib `points` output, and averages the same per-case partial score.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `inverse-counting-path-frontier-cs-algorithmic-58`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/58`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/inverse-counting-path-frontier-cs-algorithmic-58`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/checker.cpp`. Agentics wrapper preserves checker-based validation and `Ratio`/`RatioUnbounded` score extraction.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [ ] `inversion-recovery-frontier-cs-algorithmic-73`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/73`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/inversion-recovery-frontier-cs-algorithmic-73`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS `interactor.cpp` sends `n`, answers interval parity queries `op = 0`, validates final permutation output `op = 1`, and scores a correct guess with an exponential query-count formula. Agentics uses offline exact output matching, removing the query protocol and partial-credit behavior.
  - Suggested fix: Restore the original interactor through `piped_stdio` and keep the query-count score curve.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `island-shuttle-routing-frontier-cs-algorithmic-309`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/309`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/island-shuttle-routing-frontier-cs-algorithmic-309`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/chk.cc`. The migrated wrapper compiles the checker and uses Testlib `points` output for the same partial-score contract.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `job-shop-scheduling-frontier-cs-algorithmic-46`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/46`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/job-shop-scheduling-frontier-cs-algorithmic-46`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/checker.cpp`. Agentics `run.py` compiles the checker and parses `Ratio` and `RatioUnbounded`, preserving the makespan scoring formula.
  - Private ZIP subcheck: blocked, no local private overlay found.

- [x] `kangaroo-tree-map-frontier-cs-algorithmic-137`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/137`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/kangaroo-tree-map-frontier-cs-algorithmic-137`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `separated-evaluator/checker.cpp`. The wrapper uses the copied checker and preserves the source partial-scoring path.
  - Private ZIP subcheck: blocked, no local private overlay found.
