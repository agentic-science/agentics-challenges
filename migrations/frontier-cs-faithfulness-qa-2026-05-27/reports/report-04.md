# Frontier-CS Faithfulness QA Report - Slice 04

Workspace: `/home/maplespark/code/Agentics`
Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`
Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`
Assignment file: `/tmp/frontier-faithfulness-qa/slice-04.txt`

## Summary

Reviewed 25 assigned challenges.

Verdict counts:

- Faithful: 22
- Minor drift: 0
- Major drift: 3
- Blocked: 0

Confirmed finding counts:

- P0: 0
- P1: 3
- P2: 0
- P3: 0

Confirmed P1 findings:

- `graph-connectivity-oracle-frontier-cs-algorithmic-25`
- `greedy-tree-blackbox-frontier-cs-algorithmic-93`
- `grid-robot-trap-frontier-cs-algorithmic-13`

Private asset ZIP inspection notes:

- Local official ZIP or unpacked official benchmark evidence was available for `fungus-jelly-transformation-frontier-cs-algorithmic-138`, `graph-color-transformation-frontier-cs-algorithmic-87`, and `graph-coloring-frontier-cs-algorithmic-186`.
- For the other challenges, the public bundle and source comparison was completed, but the private ZIP subcheck is blocked because the local private ZIP was not readily available. This did not block the public faithfulness verdicts.

## Challenge Reviews

### `flash-attn-kernel-frontier-cs-flash-attn`

- Frontier-CS source path: `research/problems/flash_attn`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/flash-attn-kernel-frontier-cs-flash-attn/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, `benchmark.py`, and `resources/submission_spec.json` define a FlashAttention kernel task scored by the provided Python evaluator over configured `(B, H, N, D, DV, causal)` cases.
  - Migrated `coexecuted-evaluator/source/evaluator.py` matches the source evaluator. The public `benchmark.py` and `public/submission_spec.json` use reduced public-smoke dimensions, while `v1/spec.json` wires the same evaluator contract through the Agentics coexecuted CUDA target.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally, so the private production dimensions could not be directly inspected.
- Suggested fix: none for the public bundle. If needed, inspect the private ZIP when available to confirm it restores the full Frontier-CS benchmark dimensions.

### `functional-cycle-reach-frontier-cs-algorithmic-252`

- Frontier-CS source path: `algorithmic/problems/252`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/functional-cycle-reach-frontier-cs-algorithmic-252/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` declares an interactive problem using `interactor.cc`; the statement describes the original query/answer protocol.
  - Migrated `spec.json` uses `piped_stdio`; `interactive-evaluator/interactor.cpp` matches the Frontier-CS interactor, and `public/session.json` records `source_problem_id: 252` with the Frontier-CS testlib wrapper adapter.
- Private asset subcheck: blocked. The local private ZIP was not readily available.
- Suggested fix: none.

### `fungus-jelly-transformation-frontier-cs-algorithmic-138`

- Frontier-CS source path: `algorithmic/problems/138`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/fungus-jelly-transformation-frontier-cs-algorithmic-138/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` points to checker `chk.cpp`; the source checker validates the contestant output against the official transformation constraints and scoring semantics.
  - Migrated `separated-evaluator/checker.cpp` is identical to the source checker. The unpacked official benchmark under `/tmp/agentics_smoke_y83hl1ub/bundles-official/fungus-jelly-transformation-frontier-cs-algorithmic-138/private-benchmark/runs.json` contains the expected three official cases and source metadata.
- Suggested fix: none.

### `fused-linear-ce-kernel-frontier-cs-fused-linear-ce`

- Frontier-CS source path: `research/problems/fused_linear_ce`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/fused-linear-ce-kernel-frontier-cs-fused-linear-ce/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, `benchmark.py`, and `resources/submission_spec.json` define a fused linear cross-entropy kernel task with numeric correctness and performance scoring in the Python evaluator.
  - Migrated `coexecuted-evaluator/source/evaluator.py` matches the source evaluator. The public spec uses reduced smoke dimensions, and `spec.json` runs the same coexecuted CUDA evaluation contract through Agentics.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private benchmark dimensions when the private ZIP is available.

### `fused-linear-jsd-kernel-frontier-cs-fused-linear-jsd`

- Frontier-CS source path: `research/problems/fused_linear_jsd`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/fused-linear-jsd-kernel-frontier-cs-fused-linear-jsd/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, `benchmark.py`, and `resources/submission_spec.json` define the fused linear Jensen-Shannon divergence kernel contract and scoring.
  - Migrated `coexecuted-evaluator/source/evaluator.py` matches the source evaluator; the public resources are reduced for smoke execution while the Agentics spec keeps the same evaluator interface.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private benchmark dimensions when the private ZIP is available.

### `gdpa-attention-kernel-frontier-cs-gdpa-attn`

- Frontier-CS source path: `research/problems/gdpa_attention`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gdpa-attention-kernel-frontier-cs-gdpa-attn/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, `benchmark.py`, and `resources/submission_spec.json` define the GDPA attention kernel and evaluator scoring.
  - Migrated `coexecuted-evaluator/source/evaluator.py` matches the source evaluator; the public benchmark dimensions are reduced for smoke testing, and `spec.json` preserves the coexecuted CUDA evaluation flow.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private benchmark dimensions when the private ZIP is available.

### `gemm-annoying-frontier-cs-gemm-annoying`

- Frontier-CS source path: `research/problems/gemm_optimization/annoying`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-annoying-frontier-cs-gemm-annoying/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and benchmark resources define GEMM optimization for the annoying shape set.
  - Migrated evaluator preserves the Frontier-CS GEMM evaluator behavior while reading Agentics metadata shapes from `spec_path` via `AGENTICS_GEMM_SHAPES`. Public shapes are reduced to smoke-sized cases, which is consistent with the migration checklist pattern for public bundles.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally, so full private shape restoration could not be verified.
- Suggested fix: none for the public bundle. Inspect the private ZIP when available to confirm the original annoying shape set is restored.

### `gemm-k-skewed-frontier-cs-gemm-k-skewed`

- Frontier-CS source path: `research/problems/gemm_optimization/k_skewed`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-k-skewed-frontier-cs-gemm-k-skewed/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and benchmark resources define the k-skewed GEMM optimization benchmark.
  - Migrated evaluator keeps the Frontier-CS GEMM scoring behavior and obtains Agentics-provided shapes through `AGENTICS_GEMM_SHAPES`; public shapes are intentionally reduced for smoke execution.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Inspect the private ZIP when available to confirm full source shapes.

### `gemm-near-tile-frontier-cs-gemm-near-tile`

- Frontier-CS source path: `research/problems/gemm_optimization/near_tile`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-near-tile-frontier-cs-gemm-near-tile/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and benchmark resources define the near-tile GEMM benchmark.
  - Migrated evaluator preserves the Frontier-CS GEMM evaluator and maps Agentics metadata shapes into the evaluator through `AGENTICS_GEMM_SHAPES`; public shapes are smoke-sized.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Inspect private benchmark metadata when available.

### `gemm-rectangles-frontier-cs-gemm-rectangles`

- Frontier-CS source path: `research/problems/gemm_optimization/rectangles`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-rectangles-frontier-cs-gemm-rectangles/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and benchmark resources define the rectangular GEMM benchmark and scoring.
  - Migrated evaluator retains the Frontier-CS GEMM behavior and reads Agentics metadata shapes through `AGENTICS_GEMM_SHAPES`; public shapes are reduced for smoke testing.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Inspect private benchmark metadata when available.

### `gemm-squares-frontier-cs-gemm-squares`

- Frontier-CS source path: `research/problems/gemm_optimization/squares`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-squares-frontier-cs-gemm-squares/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and `resources/submission_spec.json` define the square GEMM optimization problem.
  - Migrated `source-evaluator.py` matches the source evaluator. Public metadata is reduced for smoke runs, but the evaluator contract and scoring are preserved.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private shapes when available.

### `gemm-transformer-frontier-cs-gemm-transformer`

- Frontier-CS source path: `research/problems/gemm_optimization/transformerish`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/gemm-transformer-frontier-cs-gemm-transformer/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and benchmark resources define the transformer-like GEMM shape suite.
  - Migrated `source-evaluator.py` matches the source evaluator; public shapes are smoke-sized while the evaluator contract is preserved.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private shapes when available.

### `graph-color-transformation-frontier-cs-algorithmic-87`

- Frontier-CS source path: `algorithmic/problems/87`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/graph-color-transformation-frontier-cs-algorithmic-87/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` points to checker `chk.cc`; the source statement and checker define the accepted graph color transformation output and validation.
  - Migrated `separated-evaluator/checker.cpp` is identical to the source checker. The unpacked official benchmark under `/tmp/agentics_smoke_y83hl1ub/bundles-official/graph-color-transformation-frontier-cs-algorithmic-87/private-benchmark/runs.json` contains three official cases and source metadata.
- Suggested fix: none.

### `graph-coloring-frontier-cs-algorithmic-186`

- Frontier-CS source path: `algorithmic/problems/186`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/graph-coloring-frontier-cs-algorithmic-186/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source statement defines score as `C*/C * 100`, where `C` is the contestant color count and `C*` is the official answer. Source `checker.cc` reads the graph and contestant colors, rejects adjacent equal colors, reads the optimal answer, and reports the corresponding ratio.
  - Migrated `separated-evaluator/run.py` implements the same validation: it reads the input graph, parses `output/answer.txt`, rejects same-color adjacent endpoints, computes `ref / used`, and maps the ratio to a 0-100 score. Local private ZIP `/tmp/agentics-private-assets/graph-coloring-frontier-cs-algorithmic-186/graph-coloring-frontier-cs-algorithmic-186-official-runs.zip` contains the expected private benchmark cases, answers, and `runs.json` entries.
- Suggested fix: none.

### `graph-connectivity-oracle-frontier-cs-algorithmic-25`

- Frontier-CS source path: `algorithmic/problems/25`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/graph-connectivity-oracle-frontier-cs-algorithmic-25/v1`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source `config.yaml` declares `type: interactive` with `checker: interactor.cc`. Source `statement.txt` describes an interactive protocol: the judge prints graph size, the contestant asks `? s` binary-string connectivity queries, then submits final answer `! x`; score depends on query count. Source `interactor.cc` prints `n`, reads `?` queries, replies with query results, reads final `!`, validates the answer, and reports a query-count ratio across test cases.
  - Migrated `spec.json` uses `separated_evaluator`, not an interactive execution mode. Migrated `statement.md` says the interaction is replaced by a single run input and a single submitted answer. Migrated `separated-evaluator/run.py` compares stdout tokens against `expected.txt` and assigns only exact-match 100 or 0.
- Suggested fix: restore the interactive `piped_stdio` migration using the original Frontier-CS interactor and query-count scoring. Do not flatten this problem to a static exact-output task.

### `graph-isomorphism-edge-match-frontier-cs-algorithmic-180`

- Frontier-CS source path: `algorithmic/problems/180`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/graph-isomorphism-edge-match-frontier-cs-algorithmic-180/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` uses checker `chk.cc`; the source checker validates the graph isomorphism edge-match output according to the problem statement.
  - Migrated `separated-evaluator/checker.cc` is identical to the source checker and the bundle preserves the separated checker execution flow.
- Private asset subcheck: blocked. The local private ZIP was not readily available; only smoke result artifacts were readily visible.
- Suggested fix: none.

### `graph-three-coloring-frontier-cs-algorithmic-174`

- Frontier-CS source path: `algorithmic/problems/174`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/graph-three-coloring-frontier-cs-algorithmic-174/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` uses checker `chk.cc`; the source checker enforces the three-coloring output constraints.
  - Migrated `separated-evaluator/checker.cc` is identical to the source checker and preserves the checker-based scoring contract.
- Private asset subcheck: blocked. The local private ZIP was not readily available; only smoke result artifacts were readily visible.
- Suggested fix: none.

### `greedy-tree-blackbox-frontier-cs-algorithmic-93`

- Frontier-CS source path: `algorithmic/problems/93`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/greedy-tree-blackbox-frontier-cs-algorithmic-93/v1`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`. Source `statement.txt` describes a stdio black-box tree protocol: queries of the form `? sz v...`, a final `! parent array`, and query-count scoring with full score up to 45,000 queries and zero score above 200,000. Source `interactor.cc` reads the hidden parent array, serves greedy black-box queries, validates the final parent array, and reports the query-count ratio.
  - Migrated `spec.json` uses `separated_evaluator`. Migrated `statement.md` says the interaction has been replaced by a single run input and submitted answer. Migrated `separated-evaluator/run.py` compares tokens to `expected.txt` and scores exact match as 100 or 0.
- Suggested fix: restore `piped_stdio` with the original Frontier-CS interactor and query-count scoring. Keep the black-box query protocol visible to solutions.

### `grid-required-area-crossing-frontier-cs-algorithmic-212`

- Frontier-CS source path: `algorithmic/problems/212`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/grid-required-area-crossing-frontier-cs-algorithmic-212/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` uses checker `chk.cc`; the source checker validates the grid required-area crossing output.
  - Migrated `separated-evaluator/checker.cc` is identical to the source checker and preserves checker-based validation.
- Private asset subcheck: blocked. The local private ZIP was not readily available; only smoke result artifacts were readily visible.
- Suggested fix: none.

### `grid-robot-trap-frontier-cs-algorithmic-13`

- Frontier-CS source path: `algorithmic/problems/13`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/grid-robot-trap-frontier-cs-algorithmic-13/v1`
- Verdict: major drift
- Severity: P1
- Evidence:
  - Source `config.yaml` declares `type: interactive` with `checker: interactor.cc`. Source `statement.txt` describes an interactive robot game where the judge returns robot positions after moves and the contestant must trap the robot, with scoring tied to the number of turns and a limit of 3000. Source `interactor.cc` prints the start position, reads move commands, replies with robot positions, emits `0 0` on success, and fails on too many queries.
  - Migrated `spec.json` uses `separated_evaluator`. Migrated `statement.md` says the interaction is replaced by single input and output. Migrated `separated-evaluator/run.py` performs exact token matching against `expected.txt` and scores only 100 or 0.
- Suggested fix: restore the interactive `piped_stdio` migration with the original robot interactor and turn-count scoring.

### `grid-route-feedback-frontier-cs-algorithmic-149`

- Frontier-CS source path: `algorithmic/problems/149`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/grid-route-feedback-frontier-cs-algorithmic-149/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` declares an interactive problem using the Frontier-CS interactor; the statement describes grid route feedback through stdio.
  - Migrated `spec.json` uses `piped_stdio`, and `interactive-evaluator/interactor.cpp` is identical to the source interactor, preserving the protocol and scoring semantics.
- Private asset subcheck: blocked. The local private ZIP was not readily available.
- Suggested fix: none.

### `group-gemm-frontier-cs-group-gemm`

- Frontier-CS source path: `research/problems/group_gemm`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/group-gemm-frontier-cs-group-gemm/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `README.md`, `evaluator.py`, and `resources/submission_spec.json` define grouped GEMM evaluation and scoring.
  - Migrated `source-evaluator.py` matches the source evaluator; public metadata is reduced for smoke execution while the same evaluator and submission contract are preserved.
- Private asset subcheck: blocked. The official private ZIP was not readily available locally.
- Suggested fix: none for the public bundle. Confirm private shapes when available.

### `hamiltonian-path-frontier-cs-algorithmic-5`

- Frontier-CS source path: `algorithmic/problems/5`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/hamiltonian-path-frontier-cs-algorithmic-5/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source statement and checker validate a directed simple path, reject invalid or repeated vertices, and score according to how many length thresholds are reached, with score derived from the checkpoint ratio.
  - Migrated `separated-evaluator/run.py` implements the same behavior: parse the graph and submitted vertex sequence, reject missing edges or duplicate vertices, then compute `10 * count(threshold where path length >= threshold)`. This matches the source checker's sorted-threshold ratio semantics.
- Private asset subcheck: blocked. The local private ZIP was not readily available.
- Suggested fix: none.

### `heap-tree-sum-frontier-cs-algorithmic-209`

- Frontier-CS source path: `algorithmic/problems/209`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/heap-tree-sum-frontier-cs-algorithmic-209/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` declares an interactive problem using the Frontier-CS interactor; the statement describes heap-tree query semantics.
  - Migrated `spec.json` uses `piped_stdio`, and `interactive-evaluator/interactor.cpp` is identical to the source interactor, preserving the protocol and scoring.
- Private asset subcheck: blocked. The local private ZIP was not readily available.
- Suggested fix: none.

### `hedgehog-cycle-length-frontier-cs-algorithmic-222`

- Frontier-CS source path: `algorithmic/problems/222`
- Agentics bundle path: `challenge-repos/agentics-challenges/challenges/hedgehog-cycle-length-frontier-cs-algorithmic-222/v1`
- Verdict: faithful
- Severity: none
- Evidence:
  - Source `config.yaml` declares an interactive problem using the Frontier-CS interactor; the statement describes the hedgehog cycle-length query protocol.
  - Migrated `spec.json` uses `piped_stdio`, and `interactive-evaluator/interactor.cpp` is identical to the source interactor, preserving the original protocol and scoring semantics.
- Private asset subcheck: blocked. The local private ZIP was not readily available.
- Suggested fix: none.
