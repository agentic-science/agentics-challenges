# Frontier-CS Faithfulness QA Report: Slice 02

Checklist: `/home/maplespark/code/Agentics/migration-checklist.md`
Assignment: `/tmp/frontier-faithfulness-qa/slice-02.txt`
Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`
Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`

Common private asset note: I did not find local `official-runs.zip` or per-handle private ZIP overlays for this slice under the provided workspace. I marked private ZIP overlay inspection as a blocked subcheck for each challenge, and continued with the public bundle plus source comparison as requested.

- [x] `cant-late-la-loose-large-frontier-cs-cbl-la-ll`
  - Frontier-CS source: `research/problems/cant_be_late/low_availability_loose_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-la-loose-large-frontier-cs-cbl-la-ll`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant `evaluator.py` imports `LOW_AVAILABILITY_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` sets `family: cant_be_late`, the same low-availability region set, `deadline: 70`, and `changeover_delays: [0.2]`. `diff -qr` confirmed the migrated `coexecuted-evaluator/source/common` matches Frontier-CS `common` evaluator/simulator files, except for intentionally omitted `real_traces.tar.gz`. Migrated `v1/spec.json` uses `coexecuted_benchmark`, declares `acknowledge_danger: true`, and uses `private-benchmark/real_traces.tar.gz` for official data.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-la-loose-small-frontier-cs-cbl-la-ls`
  - Frontier-CS source: `research/problems/cant_be_late/low_availability_loose_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-la-loose-small-frontier-cs-cbl-la-ls`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same low region set, `deadline: 70`, and `changeover_delays: [0.05]`. The copied common evaluator/simulator source matches Frontier-CS common files except for the private trace archive, and the Agentics spec keeps the coexecuted benchmark shape with private score-only benchmark data.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-la-tight-large-frontier-cs-cbl-la-tl`
  - Frontier-CS source: `research/problems/cant_be_late/low_availability_tight_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-la-tight-large-frontier-cs-cbl-la-tl`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` uses the same low region set, `deadline: 52`, and `changeover_delays: [0.2]`. The migrated common evaluator/simulator source matches Frontier-CS common files except for the private trace archive, and the spec uses `coexecuted_benchmark` with the documented shared-container trust boundary.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-la-tight-small-frontier-cs-cbl-la-ts`
  - Frontier-CS source: `research/problems/cant_be_late/low_availability_tight_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-la-tight-small-frontier-cs-cbl-la-ts`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same low region set, `deadline: 52`, and `changeover_delays: [0.05]`. The copied source common tree is byte-identical to Frontier-CS common files except for `real_traces.tar.gz`, and `v1/spec.json` keeps the normalized simulator score as the ranking metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ma-loose-large-frontier-cs-cbl-ma-ll`
  - Frontier-CS source: `research/problems/cant_be_late/mixed_availability_loose_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ma-loose-large-frontier-cs-cbl-ma-ll`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `ALL_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` lists the same eight mixed high and low regions, `deadline: 70`, and `changeover_delays: [0.2]`. Migrated common evaluator/simulator files match Frontier-CS common files, and official traces are kept out of Git behind the declared private asset path.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ma-loose-small-frontier-cs-cbl-ma-ls`
  - Frontier-CS source: `research/problems/cant_be_late/mixed_availability_loose_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ma-loose-small-frontier-cs-cbl-ma-ls`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `ALL_REGIONS`, `LOOSE_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` lists the same mixed region set, `deadline: 70`, and `changeover_delays: [0.05]`. The copied common evaluator/simulator source matches Frontier-CS, and the spec declares the correct coexecuted benchmark mode and private benchmark directory.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ma-tight-large-frontier-cs-cbl-ma-tl`
  - Frontier-CS source: `research/problems/cant_be_late/mixed_availability_tight_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ma-tight-large-frontier-cs-cbl-ma-tl`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `ALL_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `LARGE_OVERHEAD`; migrated `variant-config.json` lists the same mixed region set, `deadline: 52`, and `changeover_delays: [0.2]`. Migrated evaluator source matches Frontier-CS common code except for private trace material, and the Agentics README/statement preserve source provenance and the normalized cost scoring.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-ma-tight-small-frontier-cs-cbl-ma-ts`
  - Frontier-CS source: `research/problems/cant_be_late/mixed_availability_tight_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-ma-tight-small-frontier-cs-cbl-ma-ts`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `ALL_REGIONS`, `TIGHT_DEADLINE_CONFIG`, and `SMALL_OVERHEAD`; migrated `variant-config.json` lists the same mixed region set, `deadline: 52`, and `changeover_delays: [0.05]`. The copied common evaluator/simulator source is faithful, and `v1/spec.json` exposes the same score, cost, and anchor metrics without committing official traces.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-ha-loose-large-frontier-cs-cblm-ha-ll`
  - Frontier-CS source: `research/problems/cant_be_late_multi/high_availability_loose_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-ha-loose-large-frontier-cs-cblm-ha-ll`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `HIGH_AVAILABILITY_SCENARIOS`, `LOOSE_DEADLINE`, and `LARGE_OVERHEAD`; migrated `variant-config.json` uses the same high-availability scenario families, `deadline_hours: 48`, and `restart_overhead_hours: 0.2`. `diff -qr` confirmed migrated multi-region common evaluator/simulator files match Frontier-CS common files except for the private trace archive. The Agentics spec uses `coexecuted_benchmark` with `acknowledge_danger: true`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-ha-loose-small-frontier-cs-cblm-ha-ls`
  - Frontier-CS source: `research/problems/cant_be_late_multi/high_availability_loose_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-ha-loose-small-frontier-cs-cblm-ha-ls`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `HIGH_AVAILABILITY_SCENARIOS`, `LOOSE_DEADLINE`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same high-availability scenarios, `deadline_hours: 48`, and `restart_overhead_hours: 0.05`. The copied common source matches Frontier-CS, and official data is declared as the private benchmark trace archive.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-ha-tight-large-frontier-cs-cblm-ha-tl`
  - Frontier-CS source: `research/problems/cant_be_late_multi/high_availability_tight_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-ha-tight-large-frontier-cs-cblm-ha-tl`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `HIGH_AVAILABILITY_SCENARIOS`, `TIGHT_DEADLINE`, and `LARGE_OVERHEAD`; migrated `variant-config.json` uses the same high-availability scenarios, `deadline_hours: 36`, and `restart_overhead_hours: 0.2`. The common evaluator/simulator source matches Frontier-CS, and score/cost metrics are produced by the copied source evaluator path.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-ha-tight-small-frontier-cs-cblm-ha-ts`
  - Frontier-CS source: `research/problems/cant_be_late_multi/high_availability_tight_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-ha-tight-small-frontier-cs-cblm-ha-ts`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `HIGH_AVAILABILITY_SCENARIOS`, `TIGHT_DEADLINE`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same high-availability scenarios, `deadline_hours: 36`, and `restart_overhead_hours: 0.05`. The migrated common source matches Frontier-CS common files except for private traces, and the challenge documents the coexecuted trust boundary.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-la-loose-large-frontier-cs-cblm-la-ll`
  - Frontier-CS source: `research/problems/cant_be_late_multi/low_availability_loose_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-la-loose-large-frontier-cs-cblm-la-ll`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_SCENARIOS`, `LOOSE_DEADLINE`, and `LARGE_OVERHEAD`; migrated `variant-config.json` uses the same low-availability scenario families, `deadline_hours: 48`, and `restart_overhead_hours: 0.2`. The copied common evaluator/simulator source is faithful except for omitted private trace data, and official scenarios are referenced only through private benchmark data.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-la-loose-small-frontier-cs-cblm-la-ls`
  - Frontier-CS source: `research/problems/cant_be_late_multi/low_availability_loose_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-la-loose-small-frontier-cs-cblm-la-ls`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_SCENARIOS`, `LOOSE_DEADLINE`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same low-availability scenarios, `deadline_hours: 48`, and `restart_overhead_hours: 0.05`. The common evaluator/simulator source matches Frontier-CS and the spec preserves coexecuted execution with private official traces.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-la-tight-large-frontier-cs-cblm-la-tl`
  - Frontier-CS source: `research/problems/cant_be_late_multi/low_availability_tight_deadline_large_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-la-tight-large-frontier-cs-cblm-la-tl`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_SCENARIOS`, `TIGHT_DEADLINE`, and `LARGE_OVERHEAD`; migrated `variant-config.json` uses the same low-availability scenarios, `deadline_hours: 36`, and `restart_overhead_hours: 0.2`. Migrated evaluator source matches Frontier-CS common code except for the private trace archive, and scoring remains the source normalized cost score.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `cant-late-multi-la-tight-small-frontier-cs-cblm-la-ts`
  - Frontier-CS source: `research/problems/cant_be_late_multi/low_availability_tight_deadline_small_overhead`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cant-late-multi-la-tight-small-frontier-cs-cblm-la-ts`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source variant imports `LOW_AVAILABILITY_SCENARIOS`, `TIGHT_DEADLINE`, and `SMALL_OVERHEAD`; migrated `variant-config.json` uses the same low-availability scenarios, `deadline_hours: 36`, and `restart_overhead_hours: 0.05`. The copied common evaluator/simulator source matches Frontier-CS, and the Agentics manifest/spec/README agree on handle, mode, source path, and private benchmark trace asset.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/real_traces.tar.gz` overlay ZIP is available locally.

- [x] `carrot-santa-route-frontier-cs-algorithmic-44`
  - Frontier-CS source: `algorithmic/problems/44`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/carrot-santa-route-frontier-cs-algorithmic-44`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is a default checker task with `checker: chk.cc` and three source cases; migrated `v1/spec.json` uses `separated_evaluator`. `diff -u` produced no differences between source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp`. Source checker validates the Hamiltonian route and reports `Ratio`/`RatioUnbounded`; migrated `run.py` compiles that checker, parses the same ratio text, and scales the average to the public `score` metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `center-basket-transfer-frontier-cs-algorithmic-113`
  - Frontier-CS source: `algorithmic/problems/113`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/center-basket-transfer-frontier-cs-algorithmic-113`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is a default checker task with `checker: chk.cc`, `checker_type: testlib`, and three source cases; migrated `v1/spec.json` uses `separated_evaluator`. `diff -u` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker enforces center-ball transfer moves and emits `Ratio`; migrated `run.py` compiles the checker and maps the parsed ratio to `score`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `chameleon-color-pairs-frontier-cs-algorithmic-203`
  - Frontier-CS source: `algorithmic/problems/203`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/chameleon-color-pairs-frontier-cs-algorithmic-203`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`; migrated `v1/spec.json` uses `execution.mode: piped_stdio` with `public/session.json` and `private-benchmark/session.json`. `diff -u` confirmed source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. The wrapper compiles the source interactor, lets it own hidden color/love data and query limits, and parses Testlib's report-file score ratio into the 0-100 `score` metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `circular-door-order-frontier-cs-algorithmic-135`
  - Frontier-CS source: `algorithmic/problems/135`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/circular-door-order-frontier-cs-algorithmic-135`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is `type: interactive` with `interactor.cc`; migrated `v1/spec.json` uses `execution.mode: piped_stdio`. `diff -u` confirmed source `interactor.cc` and migrated `v1/interactive-evaluator/interactor.cpp` are identical. Source interactor sends `k n`, enforces distinct triple queries and the query cap, validates the final circular order, and reports a Testlib partial score; migrated `run.py` wraps that interactor and scales its ratio to `score`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/session.json` overlay ZIP is available locally.

- [x] `cleaning-duty-automaton-frontier-cs-algorithmic-170`
  - Frontier-CS source: `algorithmic/problems/170`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cleaning-duty-automaton-frontier-cs-algorithmic-170`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is a default checker task with `checker: chk.cc`, `time: 10s`, and three source cases; migrated `v1/spec.json` uses `separated_evaluator` with matching CPU limits. `diff -u` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cc` are identical. Source checker simulates `N` transition pairs for `L` weeks and reports `Ratio`/`RatioUnbounded`; migrated `run.py` compiles the checker and parses the source score ratio.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [ ] `clique-cover-frontier-cs-algorithmic-187`
  - Frontier-CS source: `algorithmic/problems/187`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/clique-cover-frontier-cs-algorithmic-187`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `checker.cc` reads exactly `n` clique IDs with `ouf.readInt()` and then calls `quitf(_ok, ...)`; Testlib checks for trailing output on `_ok` and rejects extra data as dirt. Migrated `v1/separated-evaluator/run.py` reimplements clique-cover validation in Python, but `validate_clique_cover` parses all integers and then truncates with `group_ids = group_ids[:n]`. A solution that prints a valid first `n` IDs followed by extra integer tokens would be accepted by the migrated evaluator, while the original Frontier-CS checker would reject it as malformed output. The clique validity and `K_optimal / used_cliques` scoring otherwise match the source checker.
  - Suggested fix: In `validate_clique_cover`, reject extra tokens after the first `n` clique IDs, matching Testlib's trailing-output check. Applying the same exact-length check to the shared graph validators would avoid this drift in related reimplemented checkers.

- [x] `cloudcast-broadcast-frontier-cs-cloudcast`
  - Frontier-CS source: `research/problems/cloudcast`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/cloudcast-broadcast-frontier-cs-cloudcast`
  - Verdict: faithful
  - Severity: none
  - Evidence: `diff -u` confirmed migrated `coexecuted-evaluator/source/evaluator.py` matches Frontier-CS `research/problems/cloudcast/evaluator.py`; `diff -qr` shows the copied evaluator resources match source code resources, while examples/profiles/submission spec are supplied through public or private `cloudcast/` data at runtime. Source `submission_spec.json` evaluates five configs with `num_vms: 2`; migrated `run.py` copies either `public/cloudcast` or `private-benchmark/cloudcast` into `resources` before invoking the source evaluator. Migrated `v1/spec.json` uses `coexecuted_benchmark`, `acknowledge_danger: true`, and the same `100 / (1 + total_cost)` score.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until the `private-benchmark/cloudcast/...` overlay ZIP is available locally.

- [x] `colored-ball-pole-sorting-frontier-cs-algorithmic-142`
  - Frontier-CS source: `algorithmic/problems/142`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/colored-ball-pole-sorting-frontier-cs-algorithmic-142`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is a default checker task with `checker: chk.cc` and three source cases; migrated `v1/spec.json` uses `separated_evaluator`. `diff -u` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cpp` are identical. Source checker validates capacity-constrained top-ball moves, enforces the `2,000,000` operation limit, and emits `Ratio`/`RatioUnbounded`; migrated `run.py` compiles that checker and scales the parsed ratio to `score`.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

- [x] `communication-robot-network-frontier-cs-algorithmic-211`
  - Frontier-CS source: `algorithmic/problems/211`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/communication-robot-network-frontier-cs-algorithmic-211`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` is a default checker task with `checker: chk.cc`, `time: 10s`, and four source cases; migrated `v1/spec.json` uses `separated_evaluator` with matching run limits. `diff -u` confirmed source `chk.cc` and migrated `v1/separated-evaluator/checker.cc` are identical. Source checker validates relay choices, edge syntax, connectivity, relay restrictions, and normalized cost ratio; migrated `run.py` compiles the same checker and maps its `Ratio` to the 0-100 `score` metric.
  - Suggested fix: None for public/source bundle. Private ZIP overlay subcheck remains blocked until `private-benchmark/runs.json` overlay ZIP is available locally.

## Summary

Verdict counts:

- faithful: 24
- minor drift: 1
- major drift: 0
- blocked: 0

Confirmed findings by severity:

- P0: 0
- P1: 0
- P2: 1
- P3: 0

Confirmed P2 findings:

- `clique-cover-frontier-cs-algorithmic-187`: migrated Python validator accepts extra integer tokens after the required `N` clique IDs, while the original Testlib checker would reject trailing output.

Blocked subchecks:

- Private ZIP overlay inspection blocked for all 25 challenges because the local private overlay ZIPs were not readily available in the provided workspace.
