# Frontier-CS Faithfulness QA Report - Slice 06

Workspace: `/home/maplespark/code/Agentics`

Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`

Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`

Assignment file: `/tmp/frontier-faithfulness-qa/slice-06.txt`

I reviewed the migration checklist first, then inspected each assigned migrated bundle against the original Frontier-CS statement/config and the corresponding evaluator, interactor, checker, benchmark, or scoring code. I did not edit repository files, run GitHub/project/admin/publish operations, or mutate platform state. Test-solution quality and official score strength were kept out of scope.

## Summary

| Verdict | Count |
| --- | ---: |
| faithful | 19 |
| minor drift | 0 |
| major drift | 6 |
| blocked | 0 |

| Confirmed finding severity | Count |
| --- | ---: |
| P0 | 0 |
| P1 | 6 |
| P2 | 0 |
| P3 | 0 |

Private asset inspection note: canonical local private ZIPs were readily available and inspected for `knight-tour-path-frontier-cs-algorithmic-109`, `maximum-clique-frontier-cs-algorithmic-185`, and `maximum-independent-set-frontier-cs-algorithmic-184`. For the other assigned handles, the public/source comparison continued and only the private asset subcheck is marked blocked.

## Findings

### `knight-tour-path-frontier-cs-algorithmic-109`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/109`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/knight-tour-path-frontier-cs-algorithmic-109`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: the Frontier-CS problem is an output/scored optimization task; the source checker validates the submitted knight path and awards a ratio score through Testlib scoring output.
  - Migrated: `v1/spec.json` uses `separated_evaluator`; `v1/separated-evaluator/run.py` validates `AGENTICS_OUTPUT_DIR/answer.txt` and implements the same path-validity and ratio scoring shape.
  - Private assets: inspected `/tmp/agentics-private-assets/knight-tour-path-frontier-cs-algorithmic-109/knight-tour-path-frontier-cs-algorithmic-109-official-runs.zip`; entries are under `private-benchmark/`, contain `runs.json`, official `.in`, and official `.ans` files, and showed no traversal or symlink entries.
- Suggested fix: none.

### `lamp-ring-permutation-frontier-cs-algorithmic-3`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/3`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/lamp-ring-permutation-frontier-cs-algorithmic-3`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `config.yaml` declares `type: interactive` and `interactor: interactor.cc`. `statement.txt` defines an interactive lamp query and final permutation protocol. `interactor.cc` computes `lambda(cnt_round, cnt_query)` and calls `quitp(score_ratio, ...)`, so the score depends on rounds and queries, not exact answer file matching.
  - Migrated: `v1/statement.md` says the original interactive task was converted to an offline stdin/stdout contract. `v1/separated-evaluator/run.py` is an exact token comparator with score `100.0` for an exact reference match and `0.0` otherwise. `v1/public/runs.json` contains a synthetic `public smoke for ...` input with answer `0`.
  - Private assets: private ZIP not readily available locally; subcheck blocked. The public bundle already confirms the scoring/protocol drift.
- Suggested fix: rebuild as a `piped_stdio` interactive challenge using the original `interactor.cc` or a faithful Python equivalent that preserves the query protocol and efficiency scoring. If this offline version is intentional, publish it as a derived non-faithful challenge rather than a Frontier-CS migration.

### `large-graph-three-coloring-frontier-cs-algorithmic-177`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/177`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/large-graph-three-coloring-frontier-cs-algorithmic-177`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses a Testlib checker in `chk.cc` for validation and partial scoring.
  - Migrated: `v1/separated-evaluator/checker.cc` is byte-for-byte the same as the source checker; `v1/separated-evaluator/run.py` compiles and runs it with input, participant output, and answer paths, then parses the Testlib ratio/points result into the Agentics score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `large-max-three-sat-frontier-cs-algorithmic-175`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/175`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/large-max-three-sat-frontier-cs-algorithmic-175`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/checker.cc` matches source `chk.cc`; the separated evaluator compiles and invokes the checker and preserves ratio/points scoring.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `limited-shuffle-restore-frontier-cs-algorithmic-59`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/59`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/limited-shuffle-restore-frontier-cs-algorithmic-59`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: `config.yaml` declares an interactive task; `interactor.cpp` exposes `? i j` queries and final `!` permutation output, enforces `limit = n * 5 / 3 + 5`, and scores with the same bounded query-count ratio.
  - Migrated: `v1/spec.json` uses `piped_stdio`; `v1/interactive-evaluator/run.py` implements the same `?`/`!` protocol, query limit, permutation validation, and bounded score formula over session metadata containing the hidden array.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. Official faithfulness depends on the private sessions containing Frontier-CS-derived hidden arrays.
- Suggested fix: none for the public wrapper. Locate the official private ZIP and verify the hidden arrays were generated from the original source process.

### `line-recovery-frontier-cs-algorithmic-117`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/117`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/line-recovery-frontier-cs-algorithmic-117`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `interactor.cpp` for the interactive protocol and scoring.
  - Migrated: `v1/interactive-evaluator/interactor.cpp` is byte-for-byte the same as source `interactor.cpp`; the wrapper compiles and runs the Testlib interactor in `piped_stdio` mode and converts the report ratio to the Agentics score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private session verification.

### `llm-router-frontier-cs-llm-router`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/llm_router`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/llm-router-frontier-cs-llm-router`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `readme` documents `resources/reference_data.csv` as participant-visible reference data and gives example access paths using `os.path.join(problem_dir, "resources", "reference_data.csv")` and `resources/reference_data.csv`. The file exists in the Frontier-CS source resources. `evaluator.py` is the original LLM router evaluator.
  - Migrated: `v1/source-evaluator.py` matches the source evaluator, and the coexecuted wrapper correctly sets `trace_files` from config. However, the migrated bundle does not include `v1/resources/reference_data.csv`; it only includes the public validation dataset under `v1/public/datasets`. `v1/statement.md` changes the contract to say the evaluator owns benchmark rows and that the full benchmark is not exposed as a solution resource.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. The confirmed issue is with a source-public resource omitted from the public migrated bundle.
- Suggested fix: include the original `resources/reference_data.csv` as a participant-visible resource if it is public in Frontier-CS, while keeping official evaluation traces private. Restore the source README's reference-data access contract in the migrated statement.

### `llm-sql-large-frontier-cs-llm-sql-large`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/llm_sql/large`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/llm-sql-large-frontier-cs-llm-sql-large`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `evaluator.py` for the LLM SQL task, with trace files and column-merge configuration controlling the benchmark.
  - Migrated: `v1/source-evaluator.py` is byte-for-byte the same as source `evaluator.py`; `v1/spec.json` uses `coexecuted_benchmark` with `acknowledge_danger: true`; `v1/coexecuted-evaluator/run.py` sets `trace_files`, `col_merges`, and evaluator cache paths from the selected config before calling the source evaluator.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. Public validation uses a tiny deterministic config, which is acceptable as validation-only smoke data.
- Suggested fix: none for the public bundle. Locate the official private ZIP and verify it supplies the full large-task traces and config.

### `llm-sql-small-frontier-cs-llm-sql-small`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/llm_sql/small`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/llm-sql-small-frontier-cs-llm-sql-small`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `evaluator.py` for the small LLM SQL task, with trace files and column-merge configuration.
  - Migrated: `v1/source-evaluator.py` is byte-for-byte the same as source `evaluator.py`; `v1/spec.json` uses `coexecuted_benchmark` with `acknowledge_danger: true`; the coexecuted wrapper wires `trace_files`, `col_merges`, and cache paths into the copied evaluator.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. Public validation uses a small deterministic smoke config.
- Suggested fix: none for the public bundle. Locate the official private ZIP and verify it supplies the full small-task traces and config.

### `longest-common-subsequence-frontier-cs-algorithmic-188`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/188`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/longest-common-subsequence-frontier-cs-algorithmic-188`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `checker.cc`.
  - Migrated: `v1/separated-evaluator/checker.cc` is byte-for-byte the same as source `checker.cc`; the separated evaluator compiles and invokes it and maps Testlib ratio/points output to score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `lucky-string-keyboard-frontier-cs-algorithmic-165`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/165`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/lucky-string-keyboard-frontier-cs-algorithmic-165`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/checker.cpp` is byte-for-byte the same as source `chk.cc`; the separated evaluator compiles and invokes it and preserves checker scoring.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `magic-word-spells-frontier-cs-algorithmic-69`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/69`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/magic-word-spells-frontier-cs-algorithmic-69`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `config.yaml` declares `type: interactive` and `interactor: interactor.cc`. `statement.txt` requires the solution to output `n` distinct magic words, then answer spell-power queries. `interactor.cc` validates those answers and scores by compression ratio, calling `quitp(ratio, ...)`.
  - Migrated: `v1/statement.md` says the original interactive task was converted to offline stdin/stdout. `v1/separated-evaluator/run.py` only performs exact token comparison against a reference answer and assigns `100.0` or `0.0`. `v1/public/runs.json` uses a synthetic `public smoke for ...` input.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. The public bundle already confirms the scoring/protocol drift.
- Suggested fix: restore the interactive protocol with the source `interactor.cc` or a faithful equivalent, preserving the word-generation phase, query phase, and compression-ratio scoring. Otherwise classify this as a derived offline challenge.

### `mamba2-scan-frontier-cs-mamba2-scan`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/mamba2_scan`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/mamba2-scan-frontier-cs-mamba2-scan`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `readme` specifies Mamba2 scan test cases with `L = 2048, 4096`, `D = 512`, `chunk = 128`, and `BD = 128`. `resources/submission_spec.json` contains `L_list: [2048, 4096]`, `D: 512`, `chunk: 128`, and `BD: 128`.
  - Migrated: `v1/source-evaluator.py` matches the source evaluator and `v1/statement.md` still describes the full source dimensions. However, both `v1/resources/submission_spec.json` and `v1/public/submission_spec.json` shrink the benchmark metadata to `L_list: [16]`, `D: 16`, `chunk: 8`, and `BD: 16`. `v1/coexecuted-evaluator/run.py` defaults to `resources/submission_spec.json` when a config does not override `submission_spec_path`.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. If the official private overlay overrides the spec with full dimensions, that would fix official scoring, but the public source resource remains inconsistent with the source and migrated statement.
- Suggested fix: restore `v1/resources/submission_spec.json` to the Frontier-CS full benchmark spec and keep tiny dimensions only in public validation fixtures, or ensure and document an official private override that points to a full private spec.

### `manhattan-compass-prospecting-frontier-cs-algorithmic-303`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/303`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/manhattan-compass-prospecting-frontier-cs-algorithmic-303`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/chk.cc` is byte-for-byte the same as source `chk.cc`; the separated evaluator compiles/runs the checker and converts the Testlib ratio/points result to Agentics score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `manhattan-deposit-locations-frontier-cs-algorithmic-140`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/140`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/manhattan-deposit-locations-frontier-cs-algorithmic-140`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `interactor.cc` for the interactive protocol and scoring.
  - Migrated: `v1/interactive-evaluator/interactor.cpp` is byte-for-byte the same as source `interactor.cc`; the wrapper compiles/runs it in `piped_stdio` mode and parses the Testlib report ratio into score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private session verification.

### `matrix-kth-smallest-frontier-cs-algorithmic-4`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/4`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/matrix-kth-smallest-frontier-cs-algorithmic-4`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `config.yaml` declares `type: interactive` and `interactor: interactor.cc`. `statement.txt` defines `QUERY x y` and `DONE ans`; `interactor.cc` counts queries, enforces `QUERY_LIMIT`, and scores correct answers by the query budget interpolation before calling `quitp(score, ...)`.
  - Migrated: `v1/statement.md` explicitly converts the original interactive task to offline stdin/stdout. `v1/separated-evaluator/run.py` performs exact token comparison and awards only `100.0` or `0.0`. `v1/public/runs.json` uses synthetic `public smoke for ...` input.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. The public bundle already confirms the scoring/protocol drift.
- Suggested fix: restore the interactive `QUERY`/`DONE` contract using the original interactor or a faithful equivalent, including query-limit scoring.

### `max-cut-frontier-cs-algorithmic-192`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/192`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/max-cut-frontier-cs-algorithmic-192`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/checker.cc` is byte-for-byte the same as source `chk.cc`; the separated evaluator compiles/runs the checker and preserves partial scoring.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `max-three-sat-frontier-cs-algorithmic-176`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/176`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/max-three-sat-frontier-cs-algorithmic-176`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/checker.cc` is byte-for-byte the same as source `chk.cc`; the separated evaluator compiles/runs it and preserves Testlib ratio/points scoring.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `max-two-sat-frontier-cs-algorithmic-193`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/193`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/max-two-sat-frontier-cs-algorithmic-193`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS scoring is implemented by `chk.cc`.
  - Migrated: `v1/separated-evaluator/checker.cc` is byte-for-byte the same as source `chk.cc`; the separated evaluator compiles/runs it and preserves Testlib ratio/points scoring.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private asset verification.

### `maximum-clique-frontier-cs-algorithmic-185`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/185`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/maximum-clique-frontier-cs-algorithmic-185`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS checker validates clique membership/edges and reports an optimization ratio through Testlib output.
  - Migrated: `v1/separated-evaluator/run.py` validates `AGENTICS_OUTPUT_DIR/answer.txt` for clique constraints and applies the same maximum-clique ratio scoring shape. The migrated statement and spec use separated evaluation appropriate for this output task.
  - Private assets: inspected `/tmp/agentics-private-assets/maximum-clique-frontier-cs-algorithmic-185/maximum-clique-frontier-cs-algorithmic-185-official-runs.zip`; entries are under `private-benchmark/`, contain `runs.json`, official `.in`, and official `.ans` files, and showed no traversal or symlink entries.
- Suggested fix: none.

### `maximum-independent-set-frontier-cs-algorithmic-184`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/184`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/maximum-independent-set-frontier-cs-algorithmic-184`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS checker validates independent-set membership/non-edges and reports an optimization ratio through Testlib output.
  - Migrated: `v1/separated-evaluator/run.py` validates `AGENTICS_OUTPUT_DIR/answer.txt` for independent-set constraints and applies the same maximum-independent-set ratio scoring shape. The migrated statement and spec use separated evaluation appropriate for this output task.
  - Private assets: inspected `/tmp/agentics-private-assets/maximum-independent-set-frontier-cs-algorithmic-184/maximum-independent-set-frontier-cs-algorithmic-184-official-runs.zip`; entries are under `private-benchmark/`, contain `runs.json`, official `.in`, and official `.ans` files, and showed no traversal or symlink entries.
- Suggested fix: none.

### `maximum-position-permutation-frontier-cs-algorithmic-17`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/17`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/maximum-position-permutation-frontier-cs-algorithmic-17`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source: `config.yaml` declares `type: interactive` and `interactor: interactor.cpp`. `statement.txt` defines query `? l r` and final answer `! x`, with final score based on query count between `log2(n)` and `15*log2(n)` and the final score as the minimum over test cases.
  - Migrated: `v1/statement.md` states that the original interactive problem was converted to offline stdin/stdout. `v1/separated-evaluator/run.py` performs exact token comparison and awards only `100.0` or `0.0`. `v1/public/runs.json` uses synthetic `public smoke for ...` input.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked. The public bundle already confirms the scoring/protocol drift.
- Suggested fix: restore the interactive `? l r`/`! x` protocol and query-count scoring using the original interactor or a faithful equivalent.

### `maze-wall-localization-frontier-cs-algorithmic-243`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/243`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/maze-wall-localization-frontier-cs-algorithmic-243`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `interactor.cc` for the interactive protocol and scoring.
  - Migrated: `v1/interactive-evaluator/interactor.cpp` is byte-for-byte the same as source `interactor.cc`; the wrapper compiles/runs it in `piped_stdio` mode and parses the Testlib report ratio into score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private session verification.

### `median-permutation-indices-frontier-cs-algorithmic-144`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/144`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/median-permutation-indices-frontier-cs-algorithmic-144`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `interactor.cc` for the interactive protocol and scoring.
  - Migrated: `v1/interactive-evaluator/interactor.cpp` is byte-for-byte the same as source `interactor.cc`; the wrapper compiles/runs it in `piped_stdio` mode and parses the Testlib report ratio into score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private session verification.

### `mineral-pairing-frontier-cs-algorithmic-125`

- Frontier-CS source path: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/125`
- Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/mineral-pairing-frontier-cs-algorithmic-125`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source: Frontier-CS uses `interactor.cc` for the interactive protocol and scoring.
  - Migrated: `v1/interactive-evaluator/interactor.cpp` is byte-for-byte the same as source `interactor.cc`; the wrapper compiles/runs it in `piped_stdio` mode and parses the Testlib report ratio into score.
  - Private assets: canonical private ZIP not readily available locally; subcheck blocked.
- Suggested fix: none for the public bundle. Locate the official private ZIP for private session verification.

