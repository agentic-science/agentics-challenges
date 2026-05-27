# Frontier-CS Faithfulness QA Slice 10

Workspace: `/home/maplespark/code/Agentics`

Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`

Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`

Assignment file: `/tmp/frontier-faithfulness-qa/slice-10.txt`

## Summary

- Reviewed challenges: 24
- Verdict counts: faithful 20, minor drift 2, major drift 2, blocked 0
- Confirmed findings: P0 0, P1 2, P2 2, P3 0
- Private asset inspection: only `vertex-cover-frontier-cs-algorithmic-182` had a handle-specific local private ZIP readily available under `/tmp/agentics-private-assets`. All other private ZIP subchecks are marked blocked at the subcheck level only.

## Findings

- [x] `three-hop-shortcut-dag-frontier-cs-algorithmic-239`
  - Frontier-CS source: `algorithmic/problems/239`
  - Agentics path: `challenges/three-hop-shortcut-dag-frontier-cs-algorithmic-239`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 4 cases, 2s/512m. The migrated spec uses `separated_evaluator` with official runs at `private-benchmark/runs.json`; README preserves source path/config and scoring notes. The migrated `v1/separated-evaluator/chk.cc` is byte-for-byte identical to the source checker, and the wrapper scales Testlib points to `score` on 0..100. Public data is tiny. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `tile-path-score-frontier-cs-algorithmic-148`
  - Frontier-CS source: `algorithmic/problems/148`
  - Agentics path: `challenges/tile-path-score-frontier-cs-algorithmic-148`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. The migrated spec uses `separated_evaluator`, and README/statement identify `algorithmic/problems/148`. Migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`; the wrapper compiles the checker and parses `Ratio` or Testlib points into the primary `score`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `torus-dna-reconstruction-frontier-cs-algorithmic-150`
  - Frontier-CS source: `algorithmic/problems/150`
  - Agentics path: `challenges/torus-dna-reconstruction-frontier-cs-algorithmic-150`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. The migrated spec uses `separated_evaluator`; statement and README preserve source provenance. Migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`, and official cases are declared under `private-benchmark/runs.json`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `toy-train-loop-rotation-frontier-cs-algorithmic-156`
  - Frontier-CS source: `algorithmic/problems/156`
  - Agentics path: `challenges/toy-train-loop-rotation-frontier-cs-algorithmic-156`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. Migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`; Agentics spec uses `separated_evaluator` with the expected public and private run manifests. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `treasure-hunt-choices-frontier-cs-algorithmic-70`
  - Frontier-CS source: `algorithmic/problems/70`
  - Agentics path: `challenges/treasure-hunt-choices-frontier-cs-algorithmic-70`
  - Verdict: faithful
  - Notes: Source is interactive: `interactor.cc` prints the map count and graph, shuffles neighbor order, accepts one neighbor choice per move, prints `AC` or `F`, and scores with full score up to `base_move_count` and quadratic decay through `2 * base_move_count`. Migrated spec uses `piped_stdio`; `interactive-evaluator/run.py` owns the graph/session, shuffles from a session seed, enforces one integer choice in range, prints `AC`/`F`, and uses the same bounded score rule. Public session is a small deterministic graph. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `treasure-packing-frontier-cs-algorithmic-1`
  - Frontier-CS source: `algorithmic/problems/1`
  - Agentics path: `challenges/treasure-packing-frontier-cs-algorithmic-1`
  - Verdict: faithful
  - Notes: Source statement defines JSON input/output with 12 treasure categories and score `clamp((value - baseline) / (best - baseline), 0, 1)`. Source `chk.cc` validates category counts, mass, volume, and baseline/best scoring. Migrated `separated-evaluator/run.py` implements the same JSON contract, validates exact key set and constraints, and reports average score. Public data is synthetic and small. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `tree-anomaly-pair-frontier-cs-algorithmic-258`
  - Frontier-CS source: `algorithmic/problems/258`
  - Agentics path: `challenges/tree-anomaly-pair-frontier-cs-algorithmic-258`
  - Verdict: faithful
  - Notes: Source is interactive with hidden anomaly nodes, `? c nodes...` probes, `! a b` guesses, and query-count scoring in `interactor.cc`. Migrated spec uses `piped_stdio`; migrated `interactive-evaluator/interactor.cpp` is byte-for-byte identical to source `interactor.cc`, and the Python wrapper compiles/runs the Testlib interactor against session input/answer files. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [ ] `tree-centroid-guess-frontier-cs-algorithmic-54`
  - Frontier-CS source: `algorithmic/problems/54`
  - Agentics path: `challenges/tree-centroid-guess-frontier-cs-algorithmic-54`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS statement says this is interactive: contestants only read `n`, ask distance queries with `? u v`, then answer `! x`; score depends on query count with `K_base=100000` and `K_zero=400000`. Source `interactor.cc` reads the hidden tree and expected centroid, answers distance queries, validates the final centroid, and emits the query-count ratio. The migrated statement explicitly says "all interaction is replaced by a single run input and a single submitted answer"; `separated-evaluator/run.py` only token-compares stdout against `answer_text` or `answer_path` and gives exact-match 100/0. The public run is a dummy string plus answer `0`, not a source-shaped interactive case.
  - Suggested fix: Re-migrate as `piped_stdio` using the original Testlib interactor or a faithful stdin/stdout interactive adapter that keeps hidden tree state, distance queries, query limits, and query-count scoring. If an offline exact-answer benchmark is intentionally desired, publish it as a new non-Frontier-faithful challenge rather than a faithful Frontier-CS migration.

- [x] `tree-flip-service-order-frontier-cs-algorithmic-305`
  - Frontier-CS source: `algorithmic/problems/305`
  - Agentics path: `challenges/tree-flip-service-order-frontier-cs-algorithmic-305`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 8 cases, 2s/1024m. Agentics spec uses `separated_evaluator`, README preserves source config, and migrated `chk.cc` is byte-for-byte identical to source `chk.cc`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `tree-matching-sort-frontier-cs-algorithmic-9`
  - Frontier-CS source: `algorithmic/problems/9`
  - Agentics path: `challenges/tree-matching-sort-frontier-cs-algorithmic-9`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 1s/1024m. Agentics spec uses `separated_evaluator`, and migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`. The wrapper preserves Testlib ratio/unbounded-ratio parsing for score metrics. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `tv-network-broadcast-frontier-cs-algorithmic-161`
  - Frontier-CS source: `algorithmic/problems/161`
  - Agentics path: `challenges/tv-network-broadcast-frontier-cs-algorithmic-161`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. Migrated spec uses `separated_evaluator`; migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`, and the wrapper parses checker ratio/points into the public `score`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `umbrella-gcd-sequence-frontier-cs-algorithmic-41`
  - Frontier-CS source: `algorithmic/problems/41`
  - Agentics path: `challenges/umbrella-gcd-sequence-frontier-cs-algorithmic-41`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 1s/512m. Agentics spec uses `separated_evaluator`; migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`, with ratio/unbounded-ratio parsing preserved by the wrapper. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `uniform-cave-explorer-frontier-cs-algorithmic-80`
  - Frontier-CS source: `algorithmic/problems/80`
  - Agentics path: `challenges/uniform-cave-explorer-frontier-cs-algorithmic-80`
  - Verdict: faithful
  - Notes: Source `interactor.cpp` reads hidden cave `(n, m, adj)`, prints `m`, maintains per-chamber marker side/position, accepts `c side t`, counts visited directed passages, prints `treasure`, and scores `(50000 - q) / 50000`. Migrated spec uses `piped_stdio`; `interactive-evaluator/run.py` implements the same cave state, command validation, 50000 move limit, treasure response, and 0..100 scaling. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `variable-length-sequence-reversal-frontier-cs-algorithmic-214`
  - Frontier-CS source: `algorithmic/problems/214`
  - Agentics path: `challenges/variable-length-sequence-reversal-frontier-cs-algorithmic-214`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 2s/512m. Agentics spec uses `separated_evaluator`; migrated `checker.cc` is byte-for-byte identical to source `chk.cc`. Public data is tiny and source official data is declared private. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `vector-add-2-24-frontier-cs-vector-add-2-24`
  - Frontier-CS source: `research/problems/vector_addition/2_24`
  - Agentics path: `challenges/vector-add-2-24-frontier-cs-vector-add-2-24`
  - Verdict: faithful
  - Notes: Source readme/config describe a Triton/PyTorch coexecuted benchmark for vector length `2^24`, with source evaluator and `resources/submission_spec.json`. Migrated spec uses `coexecuted_benchmark` with `acknowledge_danger: true`, CUDA target, no solution run profile, and uv setup. Migrated `source-evaluator.py` and `resources/vector-add.py` are byte-for-byte identical to the source evaluator/resource file. Public config overrides size to `1024` only for validation; official config is declared private at `private-benchmark/config.json` and `private-benchmark/submission_spec.json`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `vector-add-2-28-frontier-cs-vector-add-2-28`
  - Frontier-CS source: `research/problems/vector_addition/2_28`
  - Agentics path: `challenges/vector-add-2-28-frontier-cs-vector-add-2-28`
  - Verdict: faithful
  - Notes: Source readme/config describe a Triton/PyTorch coexecuted benchmark for vector length `2^28`, using the same evaluator shape as 2_24. Migrated spec uses `coexecuted_benchmark` with `acknowledge_danger: true`, CUDA target, no solution run profile, and uv setup. Migrated `source-evaluator.py` and `resources/vector-add.py` are byte-for-byte identical to source. Public config is a small validation override; official config/spec are declared private. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [ ] `vector-addition-frontier-cs-vector-addition-2-20`
  - Frontier-CS source: `research/problems/vector_addition/2_20`
  - Agentics path: `challenges/vector-addition-frontier-cs-vector-addition-2-20`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `evaluator.py` requires a `Solution` class and calls `solution_instance.solve(spec_path)`, then loads the returned artifact's `add` function. It uses source constants `NUM_VECTOR_SAMPLES=5`, `GPU_WARMUP_ITERS=10`, `INNER_ADD_WARMUP_ITERS=5`, and `triton.testing.do_bench` for PyTorch, CPU, and custom timings before applying the geometric-mean scoring formula. The migrated README and statement instead present the primary interface as root-level `add(x, y)`. Migrated `run.py` accepts direct `add`, and its fallback calls `Solution.solve(None)` rather than passing the submission spec path. It also uses a custom CUDA-event/perf-counter timing path with default warmups `5` and `gpu_warmups=5`, not the source `do_bench` path and warmup constants. This can change accepted source-style submissions and benchmark timing/ranking behavior, though the vector length and normalization formula remain similar.
  - Suggested fix: Align this bundle with the later 2_24/2_28 migrations by vendoring the original `source-evaluator.py` and `resources/submission_spec.json`, dispatching through the common `frontier_python_evaluate` wrapper, and passing the actual spec path into `Solution.solve`. If the direct `add(x, y)` interface is intentional, document it as an Agentics-specific interface change and keep the source-compatible path fully faithful.

- [x] `vertex-cover-frontier-cs-algorithmic-182`
  - Frontier-CS source: `algorithmic/problems/182`
  - Agentics path: `challenges/vertex-cover-frontier-cs-algorithmic-182`
  - Verdict: faithful
  - Notes: Source checker validates an `N`-line binary vector, rejects uncovered edges, and scores `K_optimal / K_user`. Migrated `separated-evaluator/run.py` uses the `vertex_cover` validator with the same edge coverage and ratio logic. The handle-specific private ZIP was available at `/tmp/agentics-private-assets/vertex-cover-frontier-cs-algorithmic-182/vertex-cover-frontier-cs-algorithmic-182-official-runs.zip`; `zipinfo` showed only regular files under `private-benchmark/...`, no traversal or symlink entries. Private cases and answers match source testdata checksums for `1..3.in` and `1..3.ans`, and `runs.json` points to the expected private paths.

- [x] `ward-map-compression-frontier-cs-algorithmic-163`
  - Frontier-CS source: `algorithmic/problems/163`
  - Agentics path: `challenges/ward-map-compression-frontier-cs-algorithmic-163`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. Migrated spec uses `separated_evaluator`; migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`, preserving validation and scoring behavior. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `warehouse-box-removal-frontier-cs-algorithmic-164`
  - Frontier-CS source: `algorithmic/problems/164`
  - Agentics path: `challenges/warehouse-box-removal-frontier-cs-algorithmic-164`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/256m. Migrated spec uses `separated_evaluator`; migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [x] `weighted-set-cover-frontier-cs-algorithmic-50`
  - Frontier-CS source: `algorithmic/problems/50`
  - Agentics path: `challenges/weighted-set-cover-frontier-cs-algorithmic-50`
  - Verdict: faithful
  - Notes: Source config is `type=default`, `checker=chk.cc`, 3 cases, 10s/1024m. Migrated spec uses `separated_evaluator`; migrated `checker.cpp` is byte-for-byte identical to source `chk.cc`, and README notes the retained checker with widened ratio-message buffers where needed. Private ZIP subcheck blocked: no handle-specific local ZIP found.

- [ ] `weighted-tree-distances-frontier-cs-algorithmic-10`
  - Frontier-CS source: `algorithmic/problems/10`
  - Agentics path: `challenges/weighted-tree-distances-frontier-cs-algorithmic-10`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS statement and `interactor.cc` define an interactive hidden weighted-tree reconstruction task. The interactor prints `T` and each `n`, answers `? u v` distance queries from hidden tree data, validates the final `! u v w ...` edge list, and scores by query count using full threshold `5n` and zero threshold `n^2/3`. The migrated statement explicitly says all interaction is replaced by a single stdin record and exact answer; migrated `separated-evaluator/run.py` only token-compares stdout with an expected answer and awards exact-match 100/0. The public run is a dummy string plus answer `0`, not a source-shaped tree-distance interaction.
  - Suggested fix: Re-migrate as `piped_stdio` using the source Testlib interactor or a faithful adapter that preserves hidden tree state, distance queries, final edge-list validation, and query-count scoring. Do not label the exact-reference offline version as a faithful Frontier-CS migration.

- [ ] `world-map-frontier-cs-algorithmic-6`
  - Frontier-CS source: `algorithmic/problems/6`
  - Agentics path: `challenges/world-map-frontier-cs-algorithmic-6`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `chk.cc` reads one graph, then validates output `P`, `P` row lengths all equal to `P`, grid colors in `1..n`, forbids adjacencies not in the graph, requires every listed graph edge to be represented, and scores `(6 - K/N) / (6 - 1.5)`. It does not check that every country color appears at least once, even though the source statement says every country should have at least one cell. Migrated `separated-evaluator/run.py` additionally rejects missing colors before checking adjacency representation. This makes the Agentics evaluator stricter than the Frontier-CS checker for cases with isolated countries or otherwise missing colors.
  - Suggested fix: Decide whether this migration is preserving the official Frontier-CS checker behavior or intentionally correcting the checker to match the statement. For strict evaluator faithfulness, remove the extra missing-color rejection or run the source checker. If keeping the stricter statement-faithful rule, document the intentional deviation in README/statement/provenance.

- [x] `xor-permutation-recovery-frontier-cs-algorithmic-249`
  - Frontier-CS source: `algorithmic/problems/249`
  - Agentics path: `challenges/xor-permutation-recovery-frontier-cs-algorithmic-249`
  - Verdict: faithful
  - Notes: Source is interactive: contestants read `n`, ask `? i j`, receive `p_i | p_j`, and answer the full permutation. Migrated spec uses `piped_stdio`; migrated `interactive-evaluator/interactor.cpp` is byte-for-byte identical to source `interactor.cc`, and the wrapper compiles/runs it against session files while scaling the Testlib ratio to `score`. Private ZIP subcheck blocked: no handle-specific local ZIP found.

## Final Counts

- Faithful: 20
- Minor drift: 2
- Major drift: 2
- Blocked verdicts: 0
- Confirmed severity counts: P0 0, P1 2, P2 2, P3 0

