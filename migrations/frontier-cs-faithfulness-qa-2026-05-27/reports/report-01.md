# Frontier-CS Faithfulness QA Report: Slice 01

Checklist: `/home/maplespark/code/Agentics/migration-checklist.md`
Assignment: `/tmp/frontier-faithfulness-qa/slice-01.txt`
Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`
Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`

Common private asset note: I did not find local `official-runs.zip` or per-handle private ZIP overlays for this slice under the provided workspace. I marked private ZIP overlay inspection as a blocked subcheck for each challenge, and continued with the public bundle plus source comparison as requested.

- [x] `adaptive-impostor-search-frontier-cs-algorithmic-245`
  - Frontier-CS source: `algorithmic/problems/245`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/adaptive-impostor-search-frontier-cs-algorithmic-245`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`, and the migrated `v1/spec.json` uses `execution.mode: piped_stdio`. `diff -q` confirmed the source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. The Agentics README/statement cite `algorithmic/problems/245` and state that the wrapper preserves hidden state, protocol validation, query limits, and source scoring.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `adventure-rank-segmentation-frontier-cs-algorithmic-61`
  - Frontier-CS source: `algorithmic/problems/61`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/adventure-rank-segmentation-frontier-cs-algorithmic-61`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: check.cpp`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `check.cpp` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker computes participant score against `ref_score` and emits `Ratio`/`RatioUnbounded`; migrated `run.py` compiles the checker, runs it against stdin/stdout/answer data, parses those ratios, and reports `score`, `average_ratio`, and `unbounded_score`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `advertisement-rectangle-placement-frontier-cs-algorithmic-147`
  - Frontier-CS source: `algorithmic/problems/147`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/advertisement-rectangle-placement-frontier-cs-algorithmic-147`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker reports normalized `Ratio` and `RatioUnbounded`; migrated `run.py` compiles the checker and scales the parsed ratio to the public `score` metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `almost-monochromatic-cycle-frontier-cs-algorithmic-24`
  - Frontier-CS source: `algorithmic/problems/24`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/almost-monochromatic-cycle-frontier-cs-algorithmic-24`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker computes per-case score and emits `Ratio`/`RatioUnbounded`; migrated evaluator preserves checker execution and exposes both bounded and unbounded aggregate metrics.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `average-permutation-frontier-cs-algorithmic-124`
  - Frontier-CS source: `algorithmic/problems/124`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/average-permutation-frontier-cs-algorithmic-124`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`; migrated `v1/spec.json` uses `execution.mode: piped_stdio`. `diff -q` confirmed source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. The migrated README/statement explicitly preserve the interactive protocol and source scoring for `algorithmic/problems/124`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `balanced-graph-partition-frontier-cs-algorithmic-45`
  - Frontier-CS source: `algorithmic/problems/45`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/balanced-graph-partition-frontier-cs-algorithmic-45`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker scores `EC` and `CV` as `Ratio`; Agentics statement includes the original scoring text and `run.py` parses the checker ratio into the 0..100 metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `ball-pillar-sorting-frontier-cs-algorithmic-62`
  - Frontier-CS source: `algorithmic/problems/62`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/ball-pillar-sorting-frontier-cs-algorithmic-62`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` and points to `chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker validates the ball moves and scores `(1e7 - k) / 1e7`; Agentics statement carries the original operation limit and scoring, and `run.py` preserves checker execution.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `beacon-string-arrangement-frontier-cs-algorithmic-302`
  - Frontier-CS source: `algorithmic/problems/302`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/beacon-string-arrangement-frontier-cs-algorithmic-302`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default`, `checker: chk.cc`, `time: 2s`, `memory: 256m`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are identical. Source checker validates exact character counts and computes clamped penalty ratio; migrated statement includes that formula and the evaluator parses the source `Ratio`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `big-integer-subset-sum-frontier-cs-algorithmic-179`
  - Frontier-CS source: `algorithmic/problems/179`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/big-integer-subset-sum-frontier-cs-algorithmic-179`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cc` are identical. Source checker emits `Ratio: ...`; migrated statement preserves the subset-sum scoring formula and `run.py` parses the same checker ratio.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `big-prize-index-frontier-cs-algorithmic-127`
  - Frontier-CS source: `algorithmic/problems/127`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/big-prize-index-frontier-cs-algorithmic-127`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`; migrated `v1/spec.json` uses `execution.mode: piped_stdio`. `diff -q` confirmed source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. The migrated README/statement cite `algorithmic/problems/127` and preserve the source interactive evaluator assumptions.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `bigger-sokoban-layout-frontier-cs-algorithmic-43`
  - Frontier-CS source: `algorithmic/problems/43`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/bigger-sokoban-layout-frontier-cs-algorithmic-43`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cpp`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cpp` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker reports `Ratio` and `RatioUnbounded` from best moves; Agentics evaluator parses both bounded and unbounded scoring metrics.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `binary-quadratic-assignment-frontier-cs-algorithmic-181`
  - Frontier-CS source: `algorithmic/problems/181`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/binary-quadratic-assignment-frontier-cs-algorithmic-181`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cc` are identical. Source checker computes `Ratio: ...`; migrated evaluator compiles the same checker and scales the parsed ratio into the public `score` metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [ ] `binary-slate-machine-frontier-cs-algorithmic-81`
  - Frontier-CS source: `algorithmic/problems/81`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/binary-slate-machine-frontier-cs-algorithmic-81`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` is `type: interactive`; source `interactor.cc` calls `registerInteraction`, prints `N`, reads query operations, enforces `Q_MAX = 1000`, validates `m`, `a`, and `b`, replies with the machine result, then checks the final guessed binary string and scores based on `query_m_max`. Migrated `v1/spec.json` uses `execution.mode: separated_evaluator`; migrated `statement.md` says "all interaction is replaced by a single run input and a single submitted answer"; migrated `run.py` only token-compares `stdout.txt` with `answer_text` or `answer_path` and assigns `100` or `0`. This removes the interactive machine protocol and the original query-size scoring objective.
  - Suggested fix: Re-migrate as `piped_stdio` using the original `interactor.cc` and a `private-benchmark/session.json` overlay, preserving query validation, final answer validation, and the source score formula. If an offline exact-output benchmark is desired, publish it under a distinct non-faithfulness handle and document it as a derivative.

- [x] `binary-square-substrings-frontier-cs-algorithmic-228`
  - Frontier-CS source: `algorithmic/problems/228`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/binary-square-substrings-frontier-cs-algorithmic-228`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are identical. Source checker scores `max(0, 1 - log2(abs(cnt - ans) + 1) / 10)`; migrated statement includes that formula and `run.py` parses the checker `Ratio`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [ ] `bitwise-or-permutation-frontier-cs-algorithmic-82`
  - Frontier-CS source: `algorithmic/problems/82`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/bitwise-or-permutation-frontier-cs-algorithmic-82`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` is `type: interactive`; source `interactor.cc` exposes the `? i j` query protocol, enforces distinct in-range indices and `QUERY_LIMIT = 4269`, validates final `! p1 ... pn`, and scores by `(4269 - queries) / 10` normalized against optimal queries. Migrated `v1/spec.json` uses `separated_evaluator`; migrated `statement.md` says the original interaction is replaced by one stdin record and exact target answer; migrated `run.py` performs whitespace-token exact match only. This changes both the participant interface and the query-efficiency ranking objective.
  - Suggested fix: Re-migrate as `piped_stdio` with the copied `interactor.cc`, hidden permutation inputs, and `.ans` optimal-query metadata in `private-benchmark/session.json`. Keep the query count metrics as ranking/tie-breaker data.

- [x] `black-white-components-frontier-cs-algorithmic-75`
  - Frontier-CS source: `algorithmic/problems/75`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/black-white-components-frontier-cs-algorithmic-75`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is default-shaped with `chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker validates the requested black/white connected components and computes a ratio from operations/area; Agentics statement includes the original problem statement and uses the source checker for scoring.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `boolean-expression-synthesis-frontier-cs-algorithmic-241`
  - Frontier-CS source: `algorithmic/problems/241`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/boolean-expression-synthesis-frontier-cs-algorithmic-241`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default`, `checker: chk.cc`, `n_cases: 5`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are identical. Source checker validates synthesized boolean expressions and scores based on operation count relative to `m0`; migrated statement includes the source formula and evaluator parses source `Ratio`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [ ] `bracket-sequence-recovery-frontier-cs-algorithmic-40`
  - Frontier-CS source: `algorithmic/problems/40`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/bracket-sequence-recovery-frontier-cs-algorithmic-40`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cpp`; source interactor prints `n`, accepts `0 k i1 ... ik` queries, computes the number of regular bracket substrings for the queried subsequence, enforces at most 200 queries, and scores the final guess as `(200 - q) / 200`. Migrated `v1/spec.json` uses `separated_evaluator`; migrated `statement.md` says all interaction is replaced by one stdin record and exact answer; migrated `run.py` only compares output tokens with the reference and scores `100` or `0`. This removes the query protocol and query-efficiency scoring.
  - Suggested fix: Re-migrate as `piped_stdio` using source `interactor.cpp`, preserving query responses, the 200-query limit, and the `(200 - q) / 200` scoring. If kept offline, treat it as a derivative challenge rather than a faithful Frontier-CS migration.

- [x] `bridge-blasting-harvest-frontier-cs-algorithmic-306`
  - Frontier-CS source: `algorithmic/problems/306`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/bridge-blasting-harvest-frontier-cs-algorithmic-306`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default`, `checker: chk.cc`, `n_cases: 10`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are identical. Source checker validates daily bridge blasting plans and computes `Score=... Ratio: ...`; migrated statement includes that scoring text and evaluator parses the checker ratio into the public normalized score.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `brush-stroke-area-frontier-cs-algorithmic-133`
  - Frontier-CS source: `algorithmic/problems/133`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/brush-stroke-area-frontier-cs-algorithmic-133`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. `diff -q` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker computes area/difference score and emits `Ratio`/`RatioUnbounded`; migrated evaluator compiles the same checker and scales the parsed ratio to `score`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `candy-tilt-moves-frontier-cs-algorithmic-160`
  - Frontier-CS source: `algorithmic/problems/160`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/candy-tilt-moves-frontier-cs-algorithmic-160`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`; migrated `v1/spec.json` uses `execution.mode: piped_stdio`. `diff -q` confirmed source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. Migrated README/statement preserve the interactive evaluator wrapper and source scoring assumptions for `algorithmic/problems/160`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `cant-late-ha-loose-large-frontier-cs-cbl-ha-ll`
  - Frontier-CS source: `research/problems/cant_be_late/high_availability_loose_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ha-loose-large-frontier-cs-cbl-ha-ll`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant `evaluator.py` imports `HIGH_AVAILABILITY_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` lists the same four high-availability env paths, `duration: 48`, `deadline: 70`, and `changeover_delays: [0.2]`. `diff -q` confirmed the migrated `coexecuted-evaluator/source/common` files match Frontier-CS `common` evaluator/simulator files. Migrated `v1/spec.json` uses `coexecuted_benchmark`, sets `acknowledge_danger: true`, omits a solution run profile, and documents the shared-container trust boundary.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ha-loose-small-frontier-cs-cbl-ha-ls`
  - Frontier-CS source: `research/problems/cant_be_late/high_availability_loose_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ha-loose-small-frontier-cs-cbl-ha-ls`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant `evaluator.py` imports `HIGH_AVAILABILITY_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` lists the same env paths, `duration: 48`, `deadline: 70`, and `changeover_delays: [0.05]`. The migrated common evaluator/simulator source is byte-identical to Frontier-CS common files, and `v1/spec.json` correctly uses `coexecuted_benchmark` with `acknowledge_danger: true` and no solution run profile.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ha-tight-large-frontier-cs-cbl-ha-tl`
  - Frontier-CS source: `research/problems/cant_be_late/high_availability_tight_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ha-tight-large-frontier-cs-cbl-ha-tl`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant `evaluator.py` imports `HIGH_AVAILABILITY_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` lists the same env paths, `duration: 48`, `deadline: 52`, and `changeover_delays: [0.2]`. The migrated common evaluator/simulator source matches Frontier-CS common files, and the challenge README/statement preserve the source path, API contract, normalized cost scoring, and coexecuted trust-boundary warning.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ha-tight-small-frontier-cs-cbl-ha-ts`
  - Frontier-CS source: `research/problems/cant_be_late/high_availability_tight_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ha-tight-small-frontier-cs-cbl-ha-ts`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant `evaluator.py` imports `HIGH_AVAILABILITY_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` lists the same env paths, `duration: 48`, `deadline: 52`, and `changeover_delays: [0.05]`. The migrated common evaluator/simulator source matches Frontier-CS common files, and `v1/spec.json` uses `coexecuted_benchmark`, `acknowledge_danger: true`, private score-only benchmark policy, and no solution run profile.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

## Summary

Verdict counts:

- faithful: 22
- minor drift: 0
- major drift: 3
- blocked: 0

Confirmed findings by severity:

- P0: 0
- P1: 3
- P2: 0
- P3: 0

Confirmed P1 findings:

- `binary-slate-machine-frontier-cs-algorithmic-81`: source interactive query machine migrated as offline exact-output benchmark.
- `bitwise-or-permutation-frontier-cs-algorithmic-82`: source interactive OR-query protocol and query-efficiency scoring migrated as offline exact-output benchmark.
- `bracket-sequence-recovery-frontier-cs-algorithmic-40`: source interactive bracket-query protocol and `(200 - q) / 200` scoring migrated as offline exact-output benchmark.

Blocked subchecks:

- Private ZIP overlay inspection blocked for all 25 challenges because the local private overlay ZIPs were not readily available in the provided workspace.
