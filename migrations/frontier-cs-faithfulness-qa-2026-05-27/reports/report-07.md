# Frontier-CS Faithfulness QA Report - Slice 07

Checklist: `/home/maplespark/code/Agentics/migration-checklist.md`

Assignment: `/tmp/frontier-faithfulness-qa/slice-07.txt`

Private asset note: no local private ZIP overlay was readily available in the challenge repo for this slice. Private overlay contents, traversal/symlink checks, and exact private official manifest contents are therefore marked as a blocked subcheck only; public bundle/source comparisons continued.

## Summary

- Verdict counts: faithful 20, minor drift 1, major drift 4, blocked 0.
- Confirmed findings: P0 0, P1 4, P2 1, P3 0.
- Out of scope: test-solution quality and official score strength were not reviewed.

## Confirmed Findings

- P1: `modpow-timing-key-frontier-cs-algorithmic-79` changes an interactive timing-query problem into exact-reference offline output.
- P1: `modulo-collision-size-frontier-cs-algorithmic-36` changes an interactive collision-query problem into exact-reference offline output.
- P1: `moving-mole-tree-frontier-cs-algorithmic-30` changes an adaptive interactive tree-search problem into exact-reference offline output.
- P1: `permutation-segment-geemu-frontier-cs-algorithmic-52` changes an interactive query/swap/reconstruct problem into exact-reference offline output.
- P2: `polyomino-packing-frontier-cs-algorithmic-0` uses a score scale of `100000 * cells / area`; the Frontier-CS checker emits `cells / area` and the Frontier-CS judge multiplies ratios by 100.

## Per-Challenge Review

- [x] `mixed-gemm-frontier-cs-mixed-gemm`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/mixed_gemm`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/mixed-gemm-frontier-cs-mixed-gemm`
  - Verdict: faithful
  - Notes: Source `evaluator.py` and `resources/benchmark.py` are identical to migrated `v1/source-evaluator.py` and `v1/resources/benchmark.py`. Agentics uses `coexecuted_benchmark` with `acknowledge_danger: true`, matching the source shared-process GPU benchmark shape. Private ZIP subcheck blocked.

- [ ] `modpow-timing-key-frontier-cs-algorithmic-79`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/79`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/modpow-timing-key-frontier-cs-algorithmic-79`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source statement lines 30-41 define interactive `? a` timing queries and final `! d`; source interactor lines 41-59 returns `modPow(a,d,n)` timings and scores by query count. Migrated `statement.md` lines 3-17 explicitly replaces interaction with one stdin record and exact reference answer, and `separated-evaluator/run.py` lines 84-96 scores only token equality as 100 or 0.
  - Suggested fix: Re-migrate as `piped_stdio` using the source Testlib interactor, with private sessions containing hidden `(n,d)` data and query-count scoring.

- [ ] `modulo-collision-size-frontier-cs-algorithmic-36`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/36`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/modulo-collision-size-frontier-cs-algorithmic-36`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source statement lines 1-37 define an I/O interactive task with collision-count queries and a final guessed bucket count. Source interactor lines 15-44 reads action type `0` queries, returns collision counts, tracks total cost, and scores the final guess by cost. Migrated `statement.md` lines 3-17 changes this to exact-reference offline output with no query protocol.
  - Suggested fix: Re-migrate as `piped_stdio` using the original interactor and hidden `n` sessions, preserving total-query-cost scoring.

- [ ] `moving-mole-tree-frontier-cs-algorithmic-30`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/30`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/moving-mole-tree-frontier-cs-algorithmic-30`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source statement lines 1-17 and 41-65 define an interactive moving-target subtree query game. Source interactor lines 49-81 reads `? x`, mutates the mole position after negative replies, and scores by query depth against `best`. Migrated `statement.md` lines 3-17 turns this into exact-reference stdin/stdout with a fixed answer.
  - Suggested fix: Re-migrate as `piped_stdio` using the source interactor, preserving mole movement, query budget, and depth-based scoring.

- [x] `mycelium-delay-tour-frontier-cs-algorithmic-304`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/304`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/mycelium-delay-tour-frontier-cs-algorithmic-304`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/chk.cc`; Agentics `run.py` compiles the source-derived checker and parses Testlib partial points. Private ZIP subcheck blocked.

- [x] `nbody-random-100k-frontier-cs-nbody-100k`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/nbody_simulation/random_100k`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/nbody-random-100k-frontier-cs-nbody-100k`
  - Verdict: faithful
  - Notes: Source common files `baseline.cpp`, `benchmark.cpp`, `evaluator_common.py`, `timing.h`, and `world.h` are byte-identical to migrated `v1/nbody-common`. Source variant config uses 100000 particles, 3 iterations, 3 runs, min speedup 1.0, max speedup 7.5; migrated wrapper dispatches `run_nbody` from config and official config is private. Private ZIP subcheck blocked.

- [x] `nbody-random-10k-frontier-cs-nbody-10k`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/research/problems/nbody_simulation/random_10k`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/nbody-random-10k-frontier-cs-nbody-10k`
  - Verdict: faithful
  - Notes: Source common files are byte-identical to migrated `v1/nbody-common`. Source variant config uses 10000 particles, 5 iterations, 3 runs, min speedup 1.0, max speedup 5.5; migrated wrapper dispatches `run_nbody` from public/private config with `coexecuted_benchmark` and `acknowledge_danger: true`. Private ZIP subcheck blocked.

- [x] `noisy-membership-search-frontier-cs-algorithmic-123`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/123`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/noisy-membership-search-frontier-cs-algorithmic-123`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; Agentics `run.py` compiles the Testlib interactor and reports the source ratio scaled to 0-100. Private ZIP subcheck blocked.

- [x] `number-loop-uniqueness-frontier-cs-algorithmic-145`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/145`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/number-loop-uniqueness-frontier-cs-algorithmic-145`
  - Verdict: faithful
  - Notes: Source `checker.cpp` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`; migrated `run.py` parses source `Ratio:`/Testlib points and averages case scores on the same 0-100 scale. Private ZIP subcheck blocked.

- [x] `oni-board-shift-frontier-cs-algorithmic-169`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/169`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/oni-board-shift-frontier-cs-algorithmic-169`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`; migrated wrapper compiles the checker and parses `Ratio:`/`RatioUnbounded:`. Private ZIP subcheck blocked.

- [x] `online-mst-decisions-frontier-cs-algorithmic-153`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/153`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/online-mst-decisions-frontier-cs-algorithmic-153`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; Agentics uses `piped_stdio` and the generic Testlib interactor wrapper. Private ZIP subcheck blocked.

- [x] `operator-sequence-recovery-frontier-cs-algorithmic-119`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/119`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/operator-sequence-recovery-frontier-cs-algorithmic-119`
  - Verdict: faithful
  - Notes: Source `interactor.cpp` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; session metadata points back to `algorithmic/problems/119`, and the wrapper preserves source Testlib scoring. Private ZIP subcheck blocked.

- [x] `orthogonal-fishing-polygon-frontier-cs-algorithmic-167`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/167`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/orthogonal-fishing-polygon-frontier-cs-algorithmic-167`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`; migrated statement and metrics describe the same checker-ratio scoring. Private ZIP subcheck blocked.

- [x] `palindrome-maze-path-frontier-cs-algorithmic-11`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/11`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/palindrome-maze-path-frontier-cs-algorithmic-11`
  - Verdict: faithful
  - Notes: Migrated checker differs only by increasing the local message buffer from 30 to 256 bytes; scoring and validation logic are otherwise source-equivalent. `run.py` compiles the checker and parses the same `Ratio:`/`RatioUnbounded:` message. Private ZIP subcheck blocked.

- [x] `palindromic-grid-paths-frontier-cs-algorithmic-256`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/256`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/palindromic-grid-paths-frontier-cs-algorithmic-256`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; migrated `piped_stdio` execution preserves source protocol and ratio scoring. Private ZIP subcheck blocked.

- [x] `parenthesis-sequence-transformation-frontier-cs-algorithmic-205`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/205`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/parenthesis-sequence-transformation-frontier-cs-algorithmic-205`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`; wrapper preserves source `Ratio:`/`RatioUnbounded:` scoring. Private ZIP subcheck blocked.

- [x] `patrol-route-visibility-frontier-cs-algorithmic-151`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/151`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/patrol-route-visibility-frontier-cs-algorithmic-151`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`; migrated run wrapper parses source checker ratio and averages official cases. Private ZIP subcheck blocked.

- [x] `pepe-racing-order-frontier-cs-algorithmic-254`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/254`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/pepe-racing-order-frontier-cs-algorithmic-254`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; Agentics session wrapper compiles and runs that interactor. Private ZIP subcheck blocked.

- [x] `permutation-four-subsequences-frontier-cs-algorithmic-227`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/227`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/permutation-four-subsequences-frontier-cs-algorithmic-227`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/chk.cc`; migrated wrapper uses the same Testlib partial score. Private ZIP subcheck blocked.

- [x] `permutation-move-sort-frontier-cs-algorithmic-26`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/26`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/permutation-move-sort-frontier-cs-algorithmic-26`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`; migrated wrapper preserves ratio and unbounded-ratio parsing. Private ZIP subcheck blocked.

- [x] `permutation-reconstruction-frontier-cs-algorithmic-2`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/2`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/permutation-reconstruction-frontier-cs-algorithmic-2`
  - Verdict: faithful
  - Notes: Source interactor prints `n`, accepts action `0` match-count queries, action `1` final permutation, and scores `100 * clamp((10000 - queries)/(10000 - best_queries), 0, 1)`. Migrated `interactive-evaluator/run.py` implements the same protocol and formula with session metadata for `permutation`, `best_queries`, and `max_queries`. Private ZIP subcheck blocked.

- [ ] `permutation-segment-geemu-frontier-cs-algorithmic-52`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/52`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/permutation-segment-geemu-frontier-cs-algorithmic-52`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source statement lines 3-43 define interactive operations `1 l r`, `2 i j`, and `3 p_1 ... p_n`, scored by `(r1+r2+1)/(s1+s2+1)`. Source interactor lines 60-126 enforces ask/swap/report operations, updates current permutation, and scores by operation counts. Migrated `statement.md` lines 3-17 changes the task to a one-shot exact-reference stdin/stdout answer.
  - Suggested fix: Re-migrate as `piped_stdio` with the source interactor, preserving ask/swap state, reverse-equivalence acceptance, limits, and operation-count scoring.

- [x] `pet-shelter-simulation-frontier-cs-algorithmic-154`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/154`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/pet-shelter-simulation-frontier-cs-algorithmic-154`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; migrated execution is `piped_stdio` with source Testlib ratio scoring. Private ZIP subcheck blocked.

- [x] `poker-action-seeds-frontier-cs-algorithmic-143`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/143`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/poker-action-seeds-frontier-cs-algorithmic-143`
  - Verdict: faithful
  - Notes: Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; wrapper compiles the copied interactor and preserves source report parsing. Private ZIP subcheck blocked.

- [ ] `polyomino-packing-frontier-cs-algorithmic-0`
  - Frontier-CS source: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS/algorithmic/problems/0`
  - Agentics path: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges/challenges/polyomino-packing-frontier-cs-algorithmic-0`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source checker lines 148-151 computes `score = totalCells / area` and emits it as `Ratio:`; Frontier-CS judge lines 343-367 parses `Ratio:` and multiplies the average by 100 for the final score. Migrated `separated-evaluator/run.py` line 166 computes `100000.0 * total_cells / total_area`, and `statement.md` lines 40-48 plus `spec.json` line 107 document that scale.
  - Suggested fix: Preserve source evaluator scale by scoring `100 * total_cells / (W * H)` in Agentics, or use the source checker wrapper directly and update `statement.md`/`spec.json` to match.
