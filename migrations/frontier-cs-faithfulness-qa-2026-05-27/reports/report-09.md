# Frontier-CS Faithfulness QA Report - Slice 09

Checklist read: `/home/maplespark/code/Agentics/migration-checklist.md`.

Scope note: I compared each assigned public Agentics bundle against the Frontier-CS source README/statement and evaluator, interactor, checker, or scoring code. I did not edit repository files and did not run platform, GitHub, admin, publish, or production-state operations.

Private asset note: I did not find local private ZIP overlays such as `official-runs.zip` or `private-benchmark*.zip` in the workspace or obvious `/tmp` locations. For every challenge below, the private ZIP overlay structure/content subcheck is therefore blocked only for that subcheck; public bundle and source comparison still proceeded.

## Summary

- Verdict counts:
  - Faithful: 15
  - Minor drift: 6
  - Major drift: 3
  - Blocked: 0
- Confirmed findings:
  - P0: 0
  - P1: 3
  - P2: 6
  - P3: 0
- Blocked subchecks: private ZIP overlay inspection for 24/24 challenges.

## Per-Challenge Results

- [x] `sequence-transform-operations-frontier-cs-algorithmic-247`
  - Frontier-CS source: `algorithmic/problems/247`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sequence-transform-operations-frontier-cs-algorithmic-247`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`, `time=2s`, `memory=512m`; the migrated spec uses `separated_evaluator`, public/private `runs.json`, and score/valid case metrics. The migrated `v1/separated-evaluator/chk.cc` is byte-identical to source `chk.cc`, and README/statement preserve the source path and original checker assumption.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `shuttle-pad-selection-frontier-cs-algorithmic-308`
  - Frontier-CS source: `algorithmic/problems/308`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/shuttle-pad-selection-frontier-cs-algorithmic-308`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`, `time=4s`, `memory=1024m`; the migrated spec uses `separated_evaluator` and the same score/valid-case metric pattern. The migrated `v1/separated-evaluator/chk.cc` is byte-identical to source `chk.cc`, and public validation is a small interface smoke as documented.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `signed-rooted-tree-frontier-cs-algorithmic-57`
  - Frontier-CS source: `algorithmic/problems/57`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/signed-rooted-tree-frontier-cs-algorithmic-57`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is interactive and source `interactor.cpp` prints `T`, each `n`, edges, supports `? 1 k ...`, `? 2 u`, final `!`, and scores by `min` case score with full score at `q <= n`. The migrated spec uses `piped_stdio`; `interactive-evaluator/run.py` implements the same query types, final sign-vector validation, and `score_for(q, n)` rule, and reports correctness/query/protocol metrics.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `skating-rink-route-frontier-cs-algorithmic-171`
  - Frontier-CS source: `algorithmic/problems/171`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/skating-rink-route-frontier-cs-algorithmic-171`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cc` is byte-identical to source `chk.cc`, and README/statement state that the original checker scores the original stdout format.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `sliding-tree-puzzle-frontier-cs-algorithmic-157`
  - Frontier-CS source: `algorithmic/problems/157`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sliding-tree-puzzle-frontier-cs-algorithmic-157`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cpp` is byte-identical to source `chk.cc`; docs preserve the original problem path, original output format, and private official-run expectation.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `small-max-three-sat-frontier-cs-algorithmic-178`
  - Frontier-CS source: `algorithmic/problems/178`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/small-max-three-sat-frontier-cs-algorithmic-178`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`, `time=1s`, `memory=1024m`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cc` is byte-identical to source `chk.cc`, preserving the Max-3-SAT assignment scoring.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `smudged-multiplication-poster-frontier-cs-algorithmic-263`
  - Frontier-CS source: `algorithmic/problems/263`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/smudged-multiplication-poster-frontier-cs-algorithmic-263`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`, public smoke data, and private official runs. The migrated `v1/separated-evaluator/chk.cc` is byte-identical to source `chk.cc`.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `snake-path-minima-frontier-cs-algorithmic-233`
  - Frontier-CS source: `algorithmic/problems/233`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/snake-path-minima-frontier-cs-algorithmic-233`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is interactive with `interactor.cc`; source interactor exposes the grid and answers `? l T`, validates final `! S1 ... Sm`, applies the `120n + m` query limit, and scores by total query cost. Migrated spec uses `piped_stdio`; `v1/interactive-evaluator/interactor.cpp` is byte-identical to source `interactor.cc`, and `run.py` compiles and runs that original interactor against session input/answer files.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `sorted-mode-array-frontier-cs-algorithmic-257`
  - Frontier-CS source: `algorithmic/problems/257`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sorted-mode-array-frontier-cs-algorithmic-257`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is interactive with `interactor.cc`; source interactor prints `n`, answers `? l r` with mode/frequency, validates final array, and scores by query count. Migrated spec uses `piped_stdio`; `v1/interactive-evaluator/interactor.cpp` is byte-identical to source `interactor.cc`, and `run.py` compiles and runs the original interactor.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `space-thief-stars-frontier-cs-algorithmic-63`
  - Frontier-CS source: `algorithmic/problems/63`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/space-thief-stars-frontier-cs-algorithmic-63`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `interactor.cpp` reads hidden `s,t`, prints only `n,m` and edges, supports up to 600 direction-orientation queries, answers reachability, then scores the final guess as `(600 - q) / 600`. The migrated statement says "all interaction is replaced by a single run input and a single submitted answer"; `v1/separated-evaluator/run.py` only token-compares stdout with a reference answer and assigns `100` or `0`.
  - Suggested fix: Restore a `piped_stdio` interactive evaluator that wraps or ports source `interactor.cpp`, keeps `s,t` hidden, enforces the 600-query protocol, and reports the source ratio scaled to 0-100. Do not replace the task with exact reference-answer matching.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `sphere-point-spread-frontier-cs-algorithmic-112`
  - Frontier-CS source: `algorithmic/problems/112`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sphere-point-spread-frontier-cs-algorithmic-112`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `chk.cc` reads `claimed_min_dist` and exactly `n` triples, then rejects any extra output with `quitf(_wa, "Extra output found after %d points", n)`. Migrated `validate_sphere_spread` parses all floats, checks only `len(values) < 1 + 3*n`, then slices the first `n` triples and ignores any trailing numeric tokens while awarding the same score.
  - Suggested fix: Make the Python validator reject any output with more than `1 + 3*n` numeric tokens, and ideally reject nonnumeric trailing text as strictly as Testlib would.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `sql-fuzzer-frontier-cs-fuzzer-sql`
  - Frontier-CS source: `research/problems/grammar_fuzzing/fuzzer/sql`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sql-fuzzer-frontier-cs-fuzzer-sql`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source evaluator loads `Solution.solve(resources_path)`, materializes a fuzzer artifact, calls `fuzz(parse_sql)` repeatedly, measures coverage with Python `coverage`, and uses the documented 60/40 coverage, cubic adjustment, and parse-call efficiency scoring. Migrated `v1/source-evaluator.py` is byte-identical to the source evaluator, and the coexecuted wrapper dispatches `runner: sql_fuzzer` to the same `load_solution_module`, `materialize_artifact`, `load_fuzzer_from_artifact`, and `evaluate_fuzzer` functions.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `sql-parser-coverage-frontier-cs-grammar-fuzzing-seed-sql`
  - Frontier-CS source: `research/problems/grammar_fuzzing/seed/sql`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/sql-parser-coverage-frontier-cs-grammar-fuzzing-seed-sql`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source evaluator imports participant `Solution`, calls `solve(resources_path) -> list[str]`, measures line and branch coverage with Python `coverage`, computes `weighted_cov = 0.6*line + 0.4*branch`, applies a cubic coverage score, and adds an efficiency bonus with `N_REF = 50`. Migrated `separated-evaluator/run.py` requires a file-system `statements.json`, traces Python lines manually with `sys.settrace`, adds regex-defined `feature_coverage`, uses a linear `0.7*line_coverage + 0.3*feature_coverage` score, and has no branch-coverage or source efficiency formula.
  - Suggested fix: Port the source evaluator faithfully. Either use `coexecuted_benchmark` and call `Solution.solve(resources_path)` directly, or keep a separated file contract but compute source-equivalent line/branch coverage and the exact source scoring formula, including the `N_REF = 50` efficiency bonus.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `steiner-tree-reconstruction-frontier-cs-algorithmic-89`
  - Frontier-CS source: `algorithmic/problems/89`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/steiner-tree-reconstruction-frontier-cs-algorithmic-89`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `interactor.cc` is interactive: it prints only `n`, keeps the hidden tree in the answer file, answers `? k v S...` Steiner-membership queries, enforces a total set-size limit of 3,000,000, validates final tree edges, and scores by query count with full score at `Q <= 3000`. The migrated statement says interaction is replaced by a single input and exact canonical output; `v1/separated-evaluator/run.py` only token-compares stdout to the reference answer and returns `100` or `0`.
  - Suggested fix: Restore a `piped_stdio` evaluator that wraps or ports source `interactor.cc`, keeps the hidden tree judge-owned, enforces query/set-size limits, validates final tree reconstruction, and preserves the source query-count scoring.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `strawberry-cake-cuts-frontier-cs-algorithmic-158`
  - Frontier-CS source: `algorithmic/problems/158`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/strawberry-cake-cuts-frontier-cs-algorithmic-158`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cpp` is byte-identical to source `chk.cc`, preserving the original geometric cutting validator and score.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `substring-ab-program-frontier-cs-algorithmic-23`
  - Frontier-CS source: `algorithmic/problems/23`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/substring-ab-program-frontier-cs-algorithmic-23`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=check.cpp`; the migrated spec uses `separated_evaluator`. The migrated checker differs only by widening the `mes` buffer from `char mes[30]` to `char mes[256]` before the same `sprintf("Ratio: %lf", ratio)` and `quitp(ratio, ...)`, preserving source validation/scoring while avoiding premature checker failure.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `symreg-mccormick-frontier-cs-symreg-mccormick`
  - Frontier-CS source: `research/problems/symbolic_regression/mccormick`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/symreg-mccormick-frontier-cs-symreg-mccormick`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `resources/pyproject.toml` includes `pysr>=0.16`, `numpy`, `pandas`, and `sympy`, and the migrated statement copies the source dependency block recommending `pysr==0.19.0`. Migrated `v1/coexecuted-evaluator/setup.py` writes an evaluator environment with only `numpy>=1.26`, `pandas>=2.2`, and `sympy>=1.13`; `pysr` is absent even though participant `solution.py` is imported by the coexecuted evaluator. The source evaluator and scoring code themselves are byte-identical.
  - Suggested fix: Add `pysr` and its required runtime support to the coexecuted evaluator setup, or revise the statement and examples if PySR is intentionally unsupported. Faithful migration should match the source dependency contract.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `symreg-mixed-polyexp-frontier-cs-symreg-mixed-polyexp`
  - Frontier-CS source: `research/problems/symbolic_regression/mixed_polyexp_4d`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/symreg-mixed-polyexp-frontier-cs-symreg-mixed-polyexp`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `resources/pyproject.toml` includes `pysr>=0.16`, and the migrated statement includes the source PySR dependency/example text. Migrated `v1/coexecuted-evaluator/setup.py` installs only `numpy`, `pandas`, and `sympy`; `pysr` is absent. The source evaluator and scoring code are byte-identical.
  - Suggested fix: Add `pysr` and required runtime support to the evaluator setup, or remove/update the PySR dependency contract if intentionally unsupported.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `symreg-peaks-frontier-cs-symreg-peaks`
  - Frontier-CS source: `research/problems/symbolic_regression/peaks`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/symreg-peaks-frontier-cs-symreg-peaks`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `resources/pyproject.toml` includes `pysr>=0.16`, and the migrated statement lists `pysr==0.19.0` plus a PySR example. Migrated `v1/coexecuted-evaluator/setup.py` installs only `numpy`, `pandas`, and `sympy`; `pysr` is absent. The source evaluator and scoring code are byte-identical.
  - Suggested fix: Add `pysr` and required runtime support to the evaluator setup, or remove/update the PySR dependency contract if intentionally unsupported.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `symreg-ripple-frontier-cs-symreg-ripple`
  - Frontier-CS source: `research/problems/symbolic_regression/ripple`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/symreg-ripple-frontier-cs-symreg-ripple`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `resources/pyproject.toml` includes `pysr>=0.16`, and the migrated statement includes the source PySR dependency/example text. Migrated `v1/coexecuted-evaluator/setup.py` installs only `numpy`, `pandas`, and `sympy`; `pysr` is absent. The source evaluator and scoring code are byte-identical.
  - Suggested fix: Add `pysr` and required runtime support to the evaluator setup, or remove/update the PySR dependency contract if intentionally unsupported.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [ ] `symreg-sincos-frontier-cs-symreg-sincos`
  - Frontier-CS source: `research/problems/symbolic_regression/sincos`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/symreg-sincos-frontier-cs-symreg-sincos`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `resources/pyproject.toml` includes `pysr>=0.16`, and the migrated statement includes the source PySR dependency/example text. Migrated `v1/coexecuted-evaluator/setup.py` installs only `numpy`, `pandas`, and `sympy`; `pysr` is absent. The source evaluator and scoring code are byte-identical.
  - Suggested fix: Add `pysr` and required runtime support to the evaluator setup, or remove/update the PySR dependency contract if intentionally unsupported.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `table-card-passing-frontier-cs-algorithmic-220`
  - Frontier-CS source: `algorithmic/problems/220`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/table-card-passing-frontier-cs-algorithmic-220`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cc` is byte-identical to source `chk.cc`, preserving the original card-passing operation validation.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `temperature-lis-boost-frontier-cs-algorithmic-229`
  - Frontier-CS source: `algorithmic/problems/229`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/temperature-lis-boost-frontier-cs-algorithmic-229`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`, `checker_type=testlib`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/chk.cc` is byte-identical to source `chk.cc`, preserving validation of 10 interval operations and LIS-ratio scoring.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.

- [x] `terrain-leveling-truck-frontier-cs-algorithmic-166`
  - Frontier-CS source: `algorithmic/problems/166`
  - Agentics path: `challenge-repos/agentics-challenges/challenges/terrain-leveling-truck-frontier-cs-algorithmic-166`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source config is `type=default`, `checker=chk.cc`; the migrated spec uses `separated_evaluator`. The migrated `v1/separated-evaluator/checker.cpp` is byte-identical to source `chk.cc`, preserving operation validation and cost-based score.
  - Suggested fix: None.
  - Private ZIP overlay subcheck: blocked, local overlay not found.
