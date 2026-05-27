# Frontier-CS Faithfulness QA Issues And Decisions

Date: 2026-05-27

Raw QA artifacts:

- Checklist: `frontier-cs-faithfulness-qa-2026-05-27/checklist.md`
- Assignments: `frontier-cs-faithfulness-qa-2026-05-27/assignments/`
- Subagent reports: `frontier-cs-faithfulness-qa-2026-05-27/reports/`

## Scope

This log records the first faithfulness QA pass over migrated Frontier-CS
challenges. Test-solution quality and official score strength were explicitly
out of scope for this pass.

Reviewed challenge bundles: 247

- Faithful: 191
- Minor drift: 21
- Major drift: 35
- P0: 0
- P1: 35
- P2: 21

## Decisions

- CUDA/Triton performance challenges may be retargeted from the source
  CUDA 12.2/L4-style Frontier-CS runtime to the Agentics CUDA 13.0/GB10 target.
  This runtime retarget is accepted and is not by itself a migration blocker.
- Private ZIP overlay inspection was blocked for most subagents because they did
  not have reliable local access to the private bundles. Run a later dedicated
  private-bundle QA pass with subagents given explicit access to the private
  bundle store.
- Source-interactive Frontier-CS challenges migrated as offline exact-output
  `separated_evaluator` challenges are P1 faithfulness breaks. Re-migrate these
  as `piped_stdio` with the original interactor or a faithful equivalent,
  preserving hidden state, protocol validation, query limits, final-answer
  validation, and source scoring.
- If an offline exact-output version is intentionally useful, keep it only as a
  separate derivative challenge and do not label it as a faithful Frontier-CS
  migration.

## P1 Issues

| Challenge | Source | Decision |
| --- | --- | --- |
| `binary-slate-machine-frontier-cs-algorithmic-81` | `algorithmic/problems/81` | Re-migrate as `piped_stdio`; preserve machine query protocol, `Q_MAX`, final string validation, and query-size scoring. |
| `bitwise-or-permutation-frontier-cs-algorithmic-82` | `algorithmic/problems/82` | Re-migrate as `piped_stdio`; preserve OR-query protocol, query limit, final permutation validation, and query-efficiency scoring. |
| `bracket-sequence-recovery-frontier-cs-algorithmic-40` | `algorithmic/problems/40` | Re-migrate as `piped_stdio`; preserve bracket-subsequence queries, 200-query limit, and `(200 - q) / 200` scoring. |
| `cycle-chord-identification-frontier-cs-algorithmic-16` | `algorithmic/problems/16` | Re-migrate as `piped_stdio`; preserve `? x y` queries, hidden chord state, 500-query limit, and query-count scoring. |
| `dishonest-attendance-frontier-cs-algorithmic-104` | `algorithmic/problems/104` | Re-migrate as `piped_stdio`; preserve adaptive dishonest/honest query protocol and source query-efficiency scoring. |
| `disk-probing-frontier-cs-algorithmic-60` | `algorithmic/problems/60` | Re-migrate as `piped_stdio`; preserve geometric probe responses, tolerance handling, probe limit, and source scoring. |
| `diverc-autofill-words-frontier-cs-algorithmic-28` | `algorithmic/problems/28` | Re-migrate as `piped_stdio`; preserve autocomplete query responses, total requested `K` accounting, and multi-case flow. |
| `divisor-count-gcd-frontier-cs-algorithmic-107` | `algorithmic/problems/107` | Re-migrate as `piped_stdio`; preserve hidden `X`, GCD replies, approximate-answer acceptance, 100-query limit, and score. |
| `graph-connectivity-oracle-frontier-cs-algorithmic-25` | `algorithmic/problems/25` | Re-migrate as `piped_stdio`; preserve binary-string connectivity queries, final answer validation, and query-count ratio. |
| `greedy-tree-blackbox-frontier-cs-algorithmic-93` | `algorithmic/problems/93` | Re-migrate as `piped_stdio`; preserve black-box tree queries, final parent-array validation, and query-count scoring. |
| `grid-robot-trap-frontier-cs-algorithmic-13` | `algorithmic/problems/13` | Re-migrate as `piped_stdio`; preserve robot movement feedback, 3000-turn limit, trap success behavior, and turn scoring. |
| `hidden-bipartite-graph-frontier-cs-algorithmic-106` | `algorithmic/problems/106` | Re-migrate as `piped_stdio`; preserve set-query protocol, `MAXQ`, certificate validation, and remaining-budget score. |
| `hidden-circuit-gates-frontier-cs-algorithmic-101` | `algorithmic/problems/101` | Re-migrate as `piped_stdio`; preserve circuit queries, gate-string final answer, `QUERY_LIMIT`, and query-count score. |
| `hidden-cycle-length-frontier-cs-algorithmic-14` | `algorithmic/problems/14` | Re-migrate as `piped_stdio`; preserve `walk`/`guess` protocol, dynamic labels, `MAX_Q`, and log-space query score. |
| `hidden-tree-median-frontier-cs-algorithmic-86` | `algorithmic/problems/86` | Re-migrate as `piped_stdio`; preserve triple queries, final tree validation, and `(ref_queries + 1) / (your_queries + 1)` score. |
| `improv-rating-wagers-frontier-cs-algorithmic-77` | `algorithmic/problems/77` | Re-migrate as `piped_stdio`; preserve online prediction/wager reveal flow and predictor-error ratio scoring. |
| `ink-pen-selection-frontier-cs-algorithmic-68` | `algorithmic/problems/68` | Re-migrate as `piped_stdio`; preserve decrement-query protocol, final pair reports, and `cnt / t` scoring. |
| `inter-active-permutation-frontier-cs-algorithmic-53` | `algorithmic/problems/53` | Re-migrate as `piped_stdio`; preserve permutation queries, final permutation answers, query limits, and quadratic query score. |
| `inversion-recovery-frontier-cs-algorithmic-73` | `algorithmic/problems/73` | Re-migrate as `piped_stdio`; preserve original interactive inversion-recovery protocol and query-count scoring. |
| `lamp-ring-permutation-frontier-cs-algorithmic-3` | `algorithmic/problems/3` | Re-migrate as `piped_stdio`; preserve lamp query/final permutation protocol and round/query efficiency scoring. |
| `llm-router-frontier-cs-llm-router` | `research/problems/llm_router` | Fix public resources: include source-public `resources/reference_data.csv` and restore the participant-visible reference-data contract while keeping official traces private. |
| `magic-word-spells-frontier-cs-algorithmic-69` | `algorithmic/problems/69` | Re-migrate as `piped_stdio`; preserve magic-word generation, spell query phase, validation, and compression-ratio score. |
| `mamba2-scan-frontier-cs-mamba2-scan` | `research/problems/mamba2_scan` | Restore source-scale `resources/submission_spec.json` or ensure and document an official private override with full source dimensions; tiny shapes belong only in public validation. |
| `matrix-kth-smallest-frontier-cs-algorithmic-4` | `algorithmic/problems/4` | Re-migrate as `piped_stdio`; preserve `QUERY`/`DONE` protocol, query limits, and query-budget interpolation score. |
| `maximum-position-permutation-frontier-cs-algorithmic-17` | `algorithmic/problems/17` | Re-migrate as `piped_stdio`; preserve `? l r`/`! x` protocol and log-based query-count scoring. |
| `modpow-timing-key-frontier-cs-algorithmic-79` | `algorithmic/problems/79` | Re-migrate as `piped_stdio`; preserve timing queries, final key guess, and query-count scoring. |
| `modulo-collision-size-frontier-cs-algorithmic-36` | `algorithmic/problems/36` | Re-migrate as `piped_stdio`; preserve collision-count queries, total query cost, final bucket guess, and cost score. |
| `moving-mole-tree-frontier-cs-algorithmic-30` | `algorithmic/problems/30` | Re-migrate as `piped_stdio`; preserve moving-target subtree queries, mole movement, query budget, and depth score. |
| `permutation-segment-geemu-frontier-cs-algorithmic-52` | `algorithmic/problems/52` | Re-migrate as `piped_stdio`; preserve ask/swap/report operations, state updates, reverse-equivalence acceptance, and operation-count score. |
| `scp-maze-exit-frontier-cs-algorithmic-85` | `algorithmic/problems/85` | Re-migrate as `piped_stdio`; preserve `move`/`query` protocol, hard limits, hidden maze seed, and `5000 / querycnt` score. |
| `space-thief-stars-frontier-cs-algorithmic-63` | `algorithmic/problems/63` | Re-migrate as `piped_stdio`; preserve hidden `s,t`, orientation queries, 600-query limit, and `(600 - q) / 600` score. |
| `sql-parser-coverage-frontier-cs-grammar-fuzzing-seed-sql` | `research/problems/grammar_fuzzing/seed/sql` | Port source scoring faithfully: call the source `Solution.solve(resources_path)` contract or compute source-equivalent line/branch coverage, cubic coverage score, and `N_REF = 50` efficiency bonus. |
| `steiner-tree-reconstruction-frontier-cs-algorithmic-89` | `algorithmic/problems/89` | Re-migrate as `piped_stdio`; preserve Steiner-membership queries, total set-size limit, final tree validation, and query-count scoring. |
| `tree-centroid-guess-frontier-cs-algorithmic-54` | `algorithmic/problems/54` | Re-migrate as `piped_stdio`; preserve hidden tree, distance queries, centroid validation, query limits, and query-count scoring. |
| `weighted-tree-distances-frontier-cs-algorithmic-10` | `algorithmic/problems/10` | Re-migrate as `piped_stdio`; preserve hidden weighted tree, distance queries, final edge-list validation, and query-count scoring. |

## P2 Issues

| Challenge | Source | Decision |
| --- | --- | --- |
| `clique-cover-frontier-cs-algorithmic-187` | `algorithmic/problems/187` | Fixed: evaluator rejects extra tokens after the required `N` clique IDs to match Testlib trailing-output behavior. |
| `cross-entropy-kernel-frontier-cs-cross-entropy` | `research/problems/cross_entropy` | Verified: runtime retarget accepted; backup private `submission_spec.json` is source-equivalent. |
| `decoding-attn-kernel-frontier-cs-decoding-attn` | `research/problems/decoding_attn` | Verified: runtime retarget accepted; backup private `submission_spec.json` is source-equivalent. |
| `imagenet-1m-frontier-cs-imagenet-1m` | `research/problems/imagenet_pareto/1m` | Fixed: evaluator setup dependency bounds now align with the source runtime contract. |
| `imagenet-2-5m-frontier-cs-imagenet-2-5m` | `research/problems/imagenet_pareto/2_5m` | Fixed: evaluator setup dependency bounds now align with the source runtime contract. |
| `imagenet-200k-frontier-cs-imagenet-200k` | `research/problems/imagenet_pareto/200k` | Fixed: evaluator setup dependency bounds now align with the source runtime contract. |
| `imagenet-500k-frontier-cs-imagenet-500k` | `research/problems/imagenet_pareto/500k` | Fixed: evaluator setup dependency bounds now align with the source runtime contract. |
| `imagenet-5m-frontier-cs-imagenet-5m` | `research/problems/imagenet_pareto/5m` | Fixed: evaluator setup dependency bounds now align with the source runtime contract. |
| `polyomino-packing-frontier-cs-algorithmic-0` | `algorithmic/problems/0` | Fixed: score now uses the source ratio scaled once by Agentics. |
| `qknorm-frontier-cs-qknorm` | `research/problems/qknorm` | Fixed and verified: runtime retarget accepted; public/resource specs and backup private spec now match the source `flashinfer ==0.5.0` contract. |
| `quant-dot-int4-frontier-cs-quant-dot-int4` | `research/problems/quant_dot_int4` | Verified: runtime retarget accepted; backup private `submission_spec.json` is source-equivalent. |
| `ragged-attention-frontier-cs-ragged-attn` | `research/problems/ragged_attention` | Verified: runtime retarget accepted; backup private `submission_spec.json` is source-equivalent. |
| `rectangle-free-points-frontier-cs-algorithmic-27` | `algorithmic/problems/27` | Fixed: invalid cases contribute zero per case, not zero the whole aggregate. |
| `sphere-point-spread-frontier-cs-algorithmic-112` | `algorithmic/problems/112` | Fixed: evaluator rejects extra numeric or nonnumeric trailing output after the required `1 + 3n` values. |
| `symreg-mccormick-frontier-cs-symreg-mccormick` | `research/problems/symbolic_regression/mccormick` | Fixed: participant-facing PySR guidance removed and resource dependency metadata aligned with the Agentics runtime. |
| `symreg-mixed-polyexp-frontier-cs-symreg-mixed-polyexp` | `research/problems/symbolic_regression/mixed_polyexp_4d` | Fixed: participant-facing PySR guidance removed and resource dependency metadata aligned with the Agentics runtime. |
| `symreg-peaks-frontier-cs-symreg-peaks` | `research/problems/symbolic_regression/peaks` | Fixed: participant-facing PySR guidance removed and resource dependency metadata aligned with the Agentics runtime. |
| `symreg-ripple-frontier-cs-symreg-ripple` | `research/problems/symbolic_regression/ripple` | Fixed: participant-facing PySR guidance removed and resource dependency metadata aligned with the Agentics runtime. |
| `symreg-sincos-frontier-cs-symreg-sincos` | `research/problems/symbolic_regression/sincos` | Fixed: participant-facing PySR guidance removed and resource dependency metadata aligned with the Agentics runtime. |
| `vector-addition-frontier-cs-vector-addition-2-20` | `research/problems/vector_addition/2_20` | Fixed: aligned with the later faithful vector-add migrations using source evaluator/spec path and `Solution.solve(spec_path)`. |
| `world-map-frontier-cs-algorithmic-6` | `algorithmic/problems/6` | Fixed: removed the extra missing-color rejection to preserve the official checker behavior. |

## P2 Fix Pass

Date: 2026-05-28

All P2s above were addressed with challenge-bundle or private-bundle fixes:

- `clique-cover-frontier-cs-algorithmic-187`: evaluator now rejects extra tokens after the required output values.
- `sphere-point-spread-frontier-cs-algorithmic-112`: evaluator now requires exactly `1 + 3n` numeric values.
- `polyomino-packing-frontier-cs-algorithmic-0`: scoring now uses `100 * cells / rectangle_area`, matching the source checker ratio scaled once by Agentics, and invalid cases contribute zero per case.
- `rectangle-free-points-frontier-cs-algorithmic-27`: invalid cases now contribute zero per case instead of zeroing the whole aggregate.
- `world-map-frontier-cs-algorithmic-6`: removed the extra missing-color rejection to preserve the official checker behavior.
- `imagenet-{200k,500k,1m,2-5m,5m}`: evaluator setup dependency bounds now match the source runtime contract for Python, PyTorch, NumPy, and tqdm.
- `symreg-{mccormick,mixed-polyexp,peaks,ripple,sincos}`: participant-facing docs and resource pyprojects now match the Agentics runtime contract, which provides NumPy, pandas, and SymPy but not evaluator-provided PySR/Julia.
- `qknorm-frontier-cs-qknorm`: public/resource specs and the backup private bundle now use the source `flashinfer_version ==0.5.0` submission spec.
- `cross-entropy-kernel-frontier-cs-cross-entropy`, `decoding-attn-kernel-frontier-cs-decoding-attn`, `quant-dot-int4-frontier-cs-quant-dot-int4`, `qknorm-frontier-cs-qknorm`, and `ragged-attention-frontier-cs-ragged-attn`: backup private submission specs were JSON-canonicalized against the Frontier-CS source specs and verified source-equivalent.
- `vector-addition-frontier-cs-vector-addition-2-20`: re-aligned to the faithful vector-add pattern using the source evaluator, source resource/spec path, `Solution.solve(spec_path)`, a tiny public config, and a private official overlay with the source submission spec.

## Later QA Pass

Run a dedicated private-bundle QA pass with subagents that can access the
private bundle store. For each migrated challenge, inspect:

- Private ZIP path and object-store backup location.
- ZIP traversal and symlink safety.
- No public file overwrites.
- Expected `private-benchmark/...` structure.
- Official source inputs, answer files, configs, and submission specs match the
  Frontier-CS source or the documented Agentics retarget decision.
