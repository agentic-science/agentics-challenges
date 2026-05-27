# Frontier-CS Faithfulness QA Report - Slice 03

Checklist: `/home/maplespark/code/Agentics/migration-checklist.md`
Assignment: `/tmp/frontier-faithfulness-qa/slice-03.txt`
Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`
Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`

Private asset note: I did not find readily available local private ZIP overlays for these handles in the challenge repo or workspace. For every challenge below, the private ZIP content/overlay inspection subcheck is therefore blocked, while the public bundle/source comparison was completed.

## Summary

- Verdict counts: faithful 18, minor drift 2, major drift 5, blocked 0.
- Confirmed findings: P0 0, P1 5, P2 2, P3 0.
- Blocked subchecks: private asset ZIP inspection for all 25 challenges.

## Per-Challenge Review

- [x] `completely-multiplicative-function-frontier-cs-algorithmic-83`
  - Frontier-CS source: `algorithmic/problems/83`
  - Agentics path: `challenges/completely-multiplicative-function-frontier-cs-algorithmic-83`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: check.cpp`; migrated `v1/spec.json` uses `separated_evaluator` with `official_runs: private-benchmark/runs.json`. Source `check.cpp` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`, and the migrated runner compiles the checker and parses `Ratio`/`RatioUnbounded` into a 0-100 `score`.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `concentric-ring-lock-frontier-cs-algorithmic-108`
  - Frontier-CS source: `algorithmic/problems/108`
  - Agentics path: `challenges/concentric-ring-lock-frontier-cs-algorithmic-108`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`; migrated `v1/spec.json` uses `piped_stdio` with session files. Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`, and the migrated statement says the trusted evaluator enforces the original Frontier-CS protocol, query validation, and scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [ ] `cross-entropy-kernel-frontier-cs-cross-entropy`
  - Frontier-CS source: `research/problems/cross_entropy`
  - Agentics path: `challenges/cross-entropy-kernel-frontier-cs-cross-entropy`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `config.yaml` specifies `Triton 3.2.0 with CUDA 12.2` and Docker image `andylizf/triton-tlx:tlx-nv-cu122`; migrated `v1/spec.json` targets `agentics-cuda-cu130-gb10`, CUDA `13.0`, NVIDIA GB10, and `v1/coexecuted-evaluator/setup.py` installs `torch>=2.11.0,<2.12.0` plus `triton>=3.5.0,<4`. Source `resources/submission_spec.json` defaults to `M_list: [256, 512, 1024]` and `N: 8192`; migrated public `submission_spec.json` uses smoke shape `[8, 128]`, and migrated `benchmark.py` changes fallback defaults and warmup from `512,8192` to `8,128`. The source and migrated evaluator/baseline files are otherwise identical, and the migrated README says official scoring uses private source metadata, but the local private ZIP was not available to verify that override.
  - Suggested fix: either align the evaluator setup/runtime and benchmark defaults with the source CUDA 12.2/Triton 3.2 contract, or document the Agentics hardware/runtime remapping as an intentional scoring-environment change. Provide or inspect the private `private-benchmark/submission_spec.json` to confirm official metadata restores the original source shapes.

- [x] `cube-sphere-packing-frontier-cs-algorithmic-48`
  - Frontier-CS source: `algorithmic/problems/48`
  - Agentics path: `challenges/cube-sphere-packing-frontier-cs-algorithmic-48`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`; the migrated runner compiles the checker and preserves the checker-provided `Ratio` scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [ ] `cycle-chord-identification-frontier-cs-algorithmic-16`
  - Frontier-CS source: `algorithmic/problems/16`
  - Agentics path: `challenges/cycle-chord-identification-frontier-cs-algorithmic-16`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` lines 1-5 declare an interactive problem using `interactor.cpp`, and source `statement.txt` lines 3 and 21-34 define the query protocol `? x y` and final answer `! u v` with a 500-query limit. The source interactor computes shortest-path responses and scores by query count. Migrated `v1/spec.json` uses `separated_evaluator`, and migrated `statement.md` lines 3-5 explicitly replace all interaction with a single offline input and submitted answer. Migrated `run.py` compares normalized output tokens to a reference answer and assigns `100` for exact match or `0` otherwise.
  - Suggested fix: remigrate as `piped_stdio` using the original `interactor.cpp`, preserving hidden chord state, query responses, the 500-query limit, and the original query-count scoring formula.

- [x] `dango-stick-grouping-frontier-cs-algorithmic-217`
  - Frontier-CS source: `algorithmic/problems/217`
  - Agentics path: `challenges/dango-stick-grouping-frontier-cs-algorithmic-217`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`; migrated `v1/spec.json` uses `piped_stdio`. Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`; the public `session.json` uses the expected input/answer case wrapper, and the migrated statement preserves the interactive stdin/stdout contract.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [ ] `decoding-attn-kernel-frontier-cs-decoding-attn`
  - Frontier-CS source: `research/problems/decoding_attn`
  - Agentics path: `challenges/decoding-attn-kernel-frontier-cs-decoding-attn`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `config.yaml` specifies `Triton 3.2.0 with CUDA 12.2` and Docker image `andylizf/triton-tlx:tlx-nv-cu122`; migrated `v1/spec.json` targets `agentics-cuda-cu130-gb10`, CUDA `13.0`, NVIDIA GB10, and `v1/coexecuted-evaluator/setup.py` installs `torch>=2.11.0,<2.12.0` plus `triton>=3.5.0,<4`. Source `resources/submission_spec.json` defaults to `Z=1, H=8, M=1, Dq=64, Dv=64, N_list=[1024,2048,4096,8192]`; migrated public `submission_spec.json` uses smoke shape `[1,2,1,64,16,16]`, and migrated `benchmark.py` changes fallback defaults and warmup to those smaller smoke dimensions. The source and migrated evaluator/baseline files are otherwise identical, and the migrated README says official scoring uses private source metadata, but the local private ZIP was not available to verify that override.
  - Suggested fix: either align the evaluator setup/runtime and benchmark defaults with the source CUDA 12.2/Triton 3.2 contract, or document the Agentics hardware/runtime remapping as an intentional scoring-environment change. Provide or inspect the private `private-benchmark/submission_spec.json` to confirm official metadata restores the original source shapes.

- [x] `defensive-lineup-permutation-frontier-cs-algorithmic-313`
  - Frontier-CS source: `algorithmic/problems/313`
  - Agentics path: `challenges/defensive-lineup-permutation-frontier-cs-algorithmic-313`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/chk.cc`. The checker itself computes `score=1000*min(2,(B+1)/(Y+1))` and reports a ratio; the migrated runner compiles the same checker and captures Testlib partial points.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `delivery-route-selection-frontier-cs-algorithmic-152`
  - Frontier-CS source: `algorithmic/problems/152`
  - Agentics path: `challenges/delivery-route-selection-frontier-cs-algorithmic-152`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`. The migrated statement keeps the original stdin/stdout output shape and the runner preserves the checker ratio scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `demagnetized-magnets-frontier-cs-algorithmic-255`
  - Frontier-CS source: `algorithmic/problems/255`
  - Agentics path: `challenges/demagnetized-magnets-frontier-cs-algorithmic-255`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`; migrated `v1/spec.json` uses `piped_stdio`. Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`, and the public session wrapper points to the expected input and answer files.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `digit-grid-prefix-frontier-cs-algorithmic-110`
  - Frontier-CS source: `algorithmic/problems/110`
  - Agentics path: `challenges/digit-grid-prefix-frontier-cs-algorithmic-110`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; source checker reads exactly an 8 by 14 digit grid, ignores extra tokens, computes the longest readable integer prefix with 8-neighbor moves, and scores `Your/Best`. Migrated `run.py` implements the same `DIGIT_H=8`, `DIGIT_W=14`, neighbor construction, prefix-readability check, and `yours / best` ratio. The Agentics interface uses `AGENTICS_OUTPUT_DIR/answer.txt`, which is documented in `statement.md` and `runs.json`.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [ ] `dishonest-attendance-frontier-cs-algorithmic-104`
  - Frontier-CS source: `algorithmic/problems/104`
  - Agentics path: `challenges/dishonest-attendance-frontier-cs-algorithmic-104`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` line 1 declares `type: interactive`, and source `statement.txt` lines 3 and 15-24 define an adaptive query protocol over `? l r`, `! a`, and `#`, with dishonest/honest answer constraints and query-count scoring. Migrated `v1/spec.json` uses `separated_evaluator`, and migrated `statement.md` lines 3-5 explicitly replace interaction with one offline benchmark record and one canonical answer. Migrated `run.py` performs exact token matching against reference text and assigns 100/0.
  - Suggested fix: remigrate as an interactive `piped_stdio` challenge using the source interactor/checker behavior, preserving the query protocol, adversarial consistency constraints, answer attempts, and original query-efficiency scoring.

- [ ] `disk-probing-frontier-cs-algorithmic-60`
  - Frontier-CS source: `algorithmic/problems/60`
  - Agentics path: `challenges/disk-probing-frontier-cs-algorithmic-60`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` lines 1-7 declare `type: interactive` with `interactor.cpp`, and source `statement.txt` lines 6 and 16-34 define a probe/response protocol with `query x1 y1 x2 y2` and final `answer x y r`, plus a 1024-probe limit. Migrated `v1/spec.json` uses `separated_evaluator`, and migrated `statement.md` lines 3-5 replace probes with an offline benchmark record and exact canonical answer. Migrated `run.py` only token-compares stdout to the reference answer and assigns 100/0.
  - Suggested fix: remigrate as `piped_stdio` with the original `interactor.cpp`, preserving geometric probe responses, tolerance handling, probe limit, and source scoring.

- [x] `distinct-bakery-types-frontier-cs-algorithmic-141`
  - Frontier-CS source: `algorithmic/problems/141`
  - Agentics path: `challenges/distinct-bakery-types-frontier-cs-algorithmic-141`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`; migrated `v1/spec.json` uses `piped_stdio`. Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`, preserving `?`, `R`, and `!` protocol handling and cost-based ratio scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `distinct-xor-set-frontier-cs-algorithmic-111`
  - Frontier-CS source: `algorithmic/problems/111`
  - Agentics path: `challenges/distinct-xor-set-frontier-cs-algorithmic-111`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; source checker reads `n`, validates a length-prefixed set with unique elements in `1..n`, rejects duplicate pairwise XOR values, and scores `Your/Best`. Migrated `run.py` implements the same validation in `validate_xor_set`, including range checks, duplicate value checks, duplicate pairwise XOR checks, and `m / best` scoring. The Agentics file-output interface is documented in `statement.md` and `runs.json`.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [ ] `diverc-autofill-words-frontier-cs-algorithmic-28`
  - Frontier-CS source: `algorithmic/problems/28`
  - Agentics path: `challenges/diverc-autofill-words-frontier-cs-algorithmic-28`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` lines 1-8 declare an interactive Testlib interactor, and source `statement.txt` lines 6 and 21-34 define an autocomplete query protocol where `query S K` returns lexicographically minimal matching words and `answer S1 ... SN` ends the case, with scoring based on total requested `K`. Migrated `v1/spec.json` uses `separated_evaluator`, and migrated `statement.md` lines 3-5 state that all interaction is replaced by one offline input and one canonical target answer. Migrated `run.py` exact-matches stdout tokens to reference answer text and assigns 100/0.
  - Suggested fix: remigrate as `piped_stdio` with the original `interactor.cc`, preserving autocomplete query responses, total-K scoring, and multi-case interactive flow.

- [ ] `divisor-count-gcd-frontier-cs-algorithmic-107`
  - Frontier-CS source: `algorithmic/problems/107`
  - Agentics path: `challenges/divisor-count-gcd-frontier-cs-algorithmic-107`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Source `config.yaml` lines 1-5 declare `type: interactive` with `interactor.cpp`, and source `statement.txt` lines 8 and 24-34 define an I/O interactive protocol where `0 Q` queries return `gcd(X,Q)` and `1 ans` submits an approximate divisor count, scored by maximum query count. Migrated `v1/spec.json` uses `separated_evaluator`, and migrated `statement.md` lines 3-5 replace interaction with an offline record and exact reference answer. Migrated `run.py` exact-matches stdout tokens and assigns 100/0.
  - Suggested fix: remigrate as `piped_stdio` using the original `interactor.cpp`, preserving hidden `X`, GCD responses, approximate-answer acceptance, 100-query limit, and the source query-count score.

- [x] `dna-matching-probability-frontier-cs-algorithmic-121`
  - Frontier-CS source: `algorithmic/problems/121`
  - Agentics path: `challenges/dna-matching-probability-frontier-cs-algorithmic-121`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` and references `chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cpp`, preserving the source ratio output.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `drone-delivery-tour-frontier-cs-algorithmic-248`
  - Frontier-CS source: `algorithmic/problems/248`
  - Agentics path: `challenges/drone-delivery-tour-frontier-cs-algorithmic-248`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/chk.cc`. The checker preserves the required `(city,point)@...` format, city/point validation, cost computation, and ratio scoring; migrated runner captures Testlib partial points.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `duplicate-position-search-frontier-cs-algorithmic-35`
  - Frontier-CS source: `algorithmic/problems/35`
  - Agentics path: `challenges/duplicate-position-search-frontier-cs-algorithmic-35`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `statement.txt` declares an interactive protocol with `? x |S| ...` membership queries, final `! y`, and 5000-query scoring. Source `interactor.cpp` generates hidden arrays and scores 100 for up to 500 queries, linearly to 0 at 5000. Migrated `v1/spec.json` uses `piped_stdio`; migrated `interactive-evaluator/run.py` prints `T`, implements the same query and final-answer protocol over session metadata, enforces the 5000-query limit, and uses the same `case_score` formula.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `edit-transcript-lcs-frontier-cs-algorithmic-189`
  - Frontier-CS source: `algorithmic/problems/189`
  - Agentics path: `challenges/edit-transcript-lcs-frontier-cs-algorithmic-189`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: checker.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `checker.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`, preserving transcript validation and LCS-ratio scoring. Migrated `run.py` compiles the same checker and parses `Ratio` from Testlib output.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `editor-width-discovery-frontier-cs-algorithmic-122`
  - Frontier-CS source: `algorithmic/problems/122`
  - Agentics path: `challenges/editor-width-discovery-frontier-cs-algorithmic-122`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: interactive` with `interactor: interactor.cc`; migrated `v1/spec.json` uses `piped_stdio`. Source `interactor.cc` is byte-identical to migrated `v1/interactive-evaluator/interactor.cpp`, preserving the source protocol and ratio scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `efficient-permutation-sorting-frontier-cs-algorithmic-207`
  - Frontier-CS source: `algorithmic/problems/207`
  - Agentics path: `challenges/efficient-permutation-sorting-frontier-cs-algorithmic-207`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`, preserving swap-round validation, computed `V`, and ratio scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `fighter-base-strike-planning-frontier-cs-algorithmic-210`
  - Frontier-CS source: `algorithmic/problems/210`
  - Agentics path: `challenges/fighter-base-strike-planning-frontier-cs-algorithmic-210`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`, preserving strike-plan parsing, score accumulation, best-possible normalization, and `Ratio` output.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.

- [x] `fixed-length-sequence-shift-frontier-cs-algorithmic-213`
  - Frontier-CS source: `algorithmic/problems/213`
  - Agentics path: `challenges/fixed-length-sequence-shift-frontier-cs-algorithmic-213`
  - Verdict: faithful
  - Severity: none
  - Evidence: Source `config.yaml` declares `type: default` with `checker: chk.cc`; migrated `v1/spec.json` uses `separated_evaluator`. Source `chk.cc` is byte-identical to migrated `v1/separated-evaluator/checker.cc`, preserving move legality checks, final permutation validation, operation-limit behavior, and ratio scoring.
  - Suggested fix: none for the public bundle/source comparison. Private ZIP inspection remains blocked.
