# Frontier-CS Faithfulness QA Report - Slice 08

## Scope And Method

Reviewed every handle in `/tmp/frontier-faithfulness-qa/slice-08.txt` against:

- Frontier-CS source root: `/home/maplespark/code/Agentics/challenge-repos/Frontier-CS`
- Agentics challenge repo: `/home/maplespark/code/Agentics/challenge-repos/agentics-challenges`
- Checklist: `/home/maplespark/code/Agentics/migration-checklist.md`

No repository files were edited. No GitHub, project admin, publish, or production-state operations were run.

Private asset note: I searched the workspace and `/tmp/frontier-faithfulness-qa` for assignment-local `official-runs.zip` or expanded `private-benchmark` overlays. They were not readily available for these handles. Per instruction, I marked only the private ZIP content inspection subcheck as blocked and continued with the public bundle/source comparison.

## Summary

- Total challenges reviewed: 24
- Verdict counts: faithful 19, minor drift 4, major drift 1, blocked 0
- Confirmed findings: P0 0, P1 1, P2 4, P3 0
- Private ZIP content subcheck blocked: 24 of 24

## Challenge Reports

- [x] `prefix-suffix-permutation-sort-frontier-cs-algorithmic-15`
  - Frontier-CS source: `algorithmic/problems/15`
  - Agentics path: `challenges/prefix-suffix-permutation-sort-frontier-cs-algorithmic-15`
  - Verdict: faithful
  - Notes: Source config is a default Testlib checker problem using `chk.cc`; migrated `v1/separated-evaluator/checker.cpp` is byte-for-byte identical to the source checker. Agentics `spec.json` uses `separated_evaluator`, reads `public/runs.json` for validation and `private-benchmark/runs.json` for official runs, and the evaluator wrapper compiles the checker and averages the checker ratio on a 0-100 scale. README and statement preserve `algorithmic/problems/15` and source title. Private ZIP content inspection blocked because no local official overlay was found.

- [x] `prime-resonance-retuning-frontier-cs-algorithmic-314`
  - Frontier-CS source: `algorithmic/problems/314`
  - Agentics path: `challenges/prime-resonance-retuning-frontier-cs-algorithmic-314`
  - Verdict: faithful
  - Notes: Source config declares `type=default`, `checker=chk.cc`, `time=5s`, `memory=512m`; migrated `v1/separated-evaluator/chk.cc` is byte-for-byte identical. Agentics `spec.json` uses `separated_evaluator`, with official runs at `private-benchmark/runs.json`, and the wrapper parses Testlib partial points into the public `score` metric. Private ZIP content inspection blocked.

- [x] `push-pop-empress-program-frontier-cs-algorithmic-8`
  - Frontier-CS source: `algorithmic/problems/8`
  - Agentics path: `challenges/push-pop-empress-program-frontier-cs-algorithmic-8`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. The source is a default checker task; Agentics uses the matching `separated_evaluator` stdio contract and scales the checker ratio to 0-100 across runs. README/statement preserve `algorithmic/problems/8` and original title `The Empress`. Private ZIP content inspection blocked.

- [x] `pyramid-ball-swaps-frontier-cs-algorithmic-162`
  - Frontier-CS source: `algorithmic/problems/162`
  - Agentics path: `challenges/pyramid-ball-swaps-frontier-cs-algorithmic-162`
  - Verdict: faithful
  - Notes: Source config is default `checker=chk.cc`, 3 cases; migrated `v1/separated-evaluator/checker.cpp` is byte-for-byte identical. Agentics keeps the batch stdio solution interface and separated checker scoring. Required private path is `private-benchmark/runs.json`, matching `spec.json`. Private ZIP content inspection blocked.

- [ ] `qknorm-frontier-cs-qknorm`
  - Frontier-CS source: `research/problems/qknorm`
  - Agentics path: `challenges/qknorm-frontier-cs-qknorm`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source `research/problems/qknorm/evaluator.py` and `resources/benchmark.py` are copied byte-for-byte into `v1/source-evaluator.py` and `v1/resources/benchmark.py`, so the interface/scoring code shape is preserved. However the source runtime config requires `L4:1`, `andylizf/triton-tlx:tlx-nv-cu122-nvcc`, and documents `CUDA 12.2, Python 3.11, PyTorch 2.0+, flashinfer 0.5.0, Triton 3.0+` (`config.yaml` lines 7-14). The Agentics spec targets `agentics-cuda-cu130-gb10`, CUDA 13.0, NVIDIA GB10 (`v1/spec.json` lines 25-73), and setup installs Python 3.12 with `torch>=2.11.0,<2.12.0`, `triton>=3.5.0,<4`, and `flashinfer-python>=0.5.0` (`v1/coexecuted-evaluator/setup.py` lines 5-7). This retargets a performance benchmark to a materially different GPU/software stack, so official rankings are not directly faithful to Frontier-CS even though evaluator code is copied. Private official config/submission spec inspection blocked.
  - Suggested fix: Reproduce the source CUDA 12.2/L4 stack if the challenge is meant to be a faithful Frontier-CS score, or explicitly document/publish it as an Agentics-retargeted benchmark. Pin flashinfer/Triton/PyTorch as close to source as possible, and verify the private overlay supplies the official source-shaped `config.json` and `submission_spec.json`.

- [x] `quadratic-witness-packing-frontier-cs-algorithmic-315`
  - Frontier-CS source: `algorithmic/problems/315`
  - Agentics path: `challenges/quadratic-witness-packing-frontier-cs-algorithmic-315`
  - Verdict: faithful
  - Severity: None
  - Evidence: Source config declares default `checker=chk.cc`, 10 cases; migrated `v1/separated-evaluator/chk.cc` is byte-for-byte identical. Agentics `spec.json` uses `separated_evaluator` and the wrapper converts Testlib partial score to a 0-100 average. README/statement preserve source path and original statement. Private ZIP content inspection blocked.
  - Suggested fix: None for public/source comparison.

- [ ] `quant-dot-int4-frontier-cs-quant-dot-int4`
  - Frontier-CS source: `research/problems/quant_dot_int4`
  - Agentics path: `challenges/quant-dot-int4-frontier-cs-quant-dot-int4`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source evaluator and benchmark files are byte-for-byte copied into the Agentics bundle. The source runtime config uses CUDA 12.2 image `andylizf/triton-tlx:tlx-nv-cu122` with GPU enabled (`config.yaml` lines 5-8). The Agentics target is `agentics-cuda-cu130-gb10`, CUDA 13.0, NVIDIA GB10 (`v1/spec.json` lines 25-73), and setup installs Python 3.12 with `torch>=2.11.0,<2.12.0` and `triton>=3.5.0,<4` (`setup.py` line 7). The scoring is performance-sensitive, so this runtime/hardware retarget can change official ordering relative to Frontier-CS. Private official overlay inspection blocked.
  - Suggested fix: Use a source-equivalent CUDA 12.2/L4 environment if faithful ranking is required, or document the challenge as a retargeted Agentics CUDA benchmark. Confirm the private overlay carries source-equivalent official shapes.

- [ ] `ragged-attention-frontier-cs-ragged-attn`
  - Frontier-CS source: `research/problems/ragged_attention`
  - Agentics path: `challenges/ragged-attention-frontier-cs-ragged-attn`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: Source evaluator and benchmark files are byte-for-byte copied. Source runtime config documents `Triton 3.2.0 with CUDA 12.2`, image `andylizf/triton-tlx:tlx-nv-cu122`, and `L4:1` (`config.yaml` lines 4-10). The Agentics bundle targets CUDA 13.0/GB10 (`v1/spec.json` lines 25-73) and setup installs Python 3.12 with `triton>=3.5.0,<4` (`setup.py` line 7). The benchmark is explicitly performance-based, so this is a runtime faithfulness drift. Private official config/submission spec inspection blocked.
  - Suggested fix: Either match the source CUDA 12.2/Triton 3.2/L4 runtime or document the retargeted hardware/software contract and avoid presenting scores as Frontier-CS-equivalent. Confirm private official metadata uses the original `M_list`, `N`, `Dq`, `Dv`, and `len_min_ratio`.

- [x] `random-subset-sum-frontier-cs-algorithmic-64`
  - Frontier-CS source: `algorithmic/problems/64`
  - Agentics path: `challenges/random-subset-sum-frontier-cs-algorithmic-64`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`; source config is a default checker problem with 3 cases and a manifest in testdata. Agentics keeps the stdio per-case interface, separated evaluator mode, and 0-100 average checker-ratio metric. Private ZIP content inspection blocked.

- [x] `ranger-shift-balancing-frontier-cs-algorithmic-312`
  - Frontier-CS source: `algorithmic/problems/312`
  - Agentics path: `challenges/ranger-shift-balancing-frontier-cs-algorithmic-312`
  - Verdict: faithful
  - Notes: Source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are byte-for-byte identical. Source config is default checker, 10 cases; Agentics uses `separated_evaluator` with official run manifest path `private-benchmark/runs.json` and Testlib partial-score scaling. Private ZIP content inspection blocked.

- [ ] `rectangle-free-points-frontier-cs-algorithmic-27`
  - Frontier-CS source: `algorithmic/problems/27`
  - Agentics path: `challenges/rectangle-free-points-frontier-cs-algorithmic-27`
  - Verdict: minor drift
  - Severity: P2
  - Evidence: The source statement says invalid outputs receive 0 "for that test" and the final score is the average over tests (`statement.txt` lines 29-30). Source checker rejects invalid outputs with `quitp(0.0, ...)` and otherwise returns a per-case ratio (`chk.cc` lines 151-182). The Agentics Python evaluator reimplements the checker and computes the same `1.5 * U` ratio per case (`run.py` lines 132-158), but its aggregate returns `score: average_score if all_valid else 0.0` (`run.py` lines 201-210), so one invalid case zeros the entire official score instead of only that case. Private ZIP content inspection blocked.
  - Suggested fix: Change aggregation to always average per-case scores, with invalid cases contributing 0, or switch back to compiling the original `chk.cc` through the common Testlib wrapper.

- [x] `rectangle-knapsack-packing-frontier-cs-algorithmic-47`
  - Frontier-CS source: `algorithmic/problems/47`
  - Agentics path: `challenges/rectangle-knapsack-packing-frontier-cs-algorithmic-47`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. The source checker parses the JSON packing, validates bounds/rotation/overlap/limits, and scores `(value - baseline)/(best - baseline)`; Agentics runs that checker in separated evaluator mode and scales average ratios to 0-100. Private ZIP content inspection blocked.

- [x] `rectjoin-grid-rectangles-frontier-cs-algorithmic-159`
  - Frontier-CS source: `algorithmic/problems/159`
  - Agentics path: `challenges/rectjoin-grid-rectangles-frontier-cs-algorithmic-159`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. Source config is default checker, 3 cases; Agentics keeps the separated checker contract and declares official runs at `private-benchmark/runs.json`. Private ZIP content inspection blocked.

- [x] `repaired-road-set-frontier-cs-algorithmic-253`
  - Frontier-CS source: `algorithmic/problems/253`
  - Agentics path: `challenges/repaired-road-set-frontier-cs-algorithmic-253`
  - Verdict: faithful
  - Notes: Source config is `type: interactive` with `interactor.cc`; migrated `v1/interactive-evaluator/interactor.cpp` is byte-for-byte identical. Agentics `spec.json` uses `piped_stdio`, compiles the source interactor, feeds session input/answer files, and reports the Testlib ratio as `score` on a 0-100 scale. Statement preserves the interactive protocol and cost model. Private ZIP content inspection blocked.

- [x] `resonant-bay-layout-frontier-cs-algorithmic-311`
  - Frontier-CS source: `algorithmic/problems/311`
  - Agentics path: `challenges/resonant-bay-layout-frontier-cs-algorithmic-311`
  - Verdict: faithful
  - Notes: Source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are byte-for-byte identical. Source config is default checker, 10 cases; Agentics uses the matching separated evaluator contract and private run manifest path. Private ZIP content inspection blocked.

- [x] `resonator-emitter-layout-frontier-cs-algorithmic-310`
  - Frontier-CS source: `algorithmic/problems/310`
  - Agentics path: `challenges/resonator-emitter-layout-frontier-cs-algorithmic-310`
  - Verdict: faithful
  - Notes: Source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are byte-for-byte identical. Agentics preserves the default checker task shape through `separated_evaluator` and the wrapper converts Testlib output to the declared `score` metric. Private ZIP content inspection blocked.

- [x] `revolutionary-tree-decomposition-frontier-cs-algorithmic-22`
  - Frontier-CS source: `algorithmic/problems/22`
  - Agentics path: `challenges/revolutionary-tree-decomposition-frontier-cs-algorithmic-22`
  - Verdict: faithful
  - Notes: Source config is default checker `checker.cpp`; migrated checker differs only by enlarging the local message buffer from `char mes[30]` to `char mes[256]`, while the ratio formula and `quitp` message are otherwise unchanged. Agentics uses `separated_evaluator`, compiles the checker, and averages source ratios. Private ZIP content inspection blocked.

- [x] `robust-forgotten-route-frontier-cs-algorithmic-155`
  - Frontier-CS source: `algorithmic/problems/155`
  - Agentics path: `challenges/robust-forgotten-route-frontier-cs-algorithmic-155`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. Source config is default checker, 3 cases; Agentics preserves stdio case execution and checker-based partial scoring. Private ZIP content inspection blocked.

- [x] `rooted-forest-attractiveness-frontier-cs-algorithmic-168`
  - Frontier-CS source: `algorithmic/problems/168`
  - Agentics path: `challenges/rooted-forest-attractiveness-frontier-cs-algorithmic-168`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cc`. The migrated bundle uses `separated_evaluator`, keeps the original output validation/scoring behavior through Testlib, and points official scoring at `private-benchmark/runs.json`. Private ZIP content inspection blocked.

- [x] `rope-network-segments-frontier-cs-algorithmic-301`
  - Frontier-CS source: `algorithmic/problems/301`
  - Agentics path: `challenges/rope-network-segments-frontier-cs-algorithmic-301`
  - Verdict: faithful
  - Notes: Source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are byte-for-byte identical. Source config is default checker, 10 cases; Agentics preserves checker execution and 0-100 average score. Private ZIP content inspection blocked.

- [x] `rotated-square-packing-frontier-cs-algorithmic-42`
  - Frontier-CS source: `algorithmic/problems/42`
  - Agentics path: `challenges/rotated-square-packing-frontier-cs-algorithmic-42`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. Source config is default checker, 3 cases; Agentics uses `separated_evaluator` and preserves the checker ratio scoring. Private ZIP content inspection blocked.

- [x] `rush-hour-puzzle-frontier-cs-algorithmic-72`
  - Frontier-CS source: `algorithmic/problems/72`
  - Agentics path: `challenges/rush-hour-puzzle-frontier-cs-algorithmic-72`
  - Verdict: faithful
  - Notes: Source `chk.cc` is byte-for-byte identical to migrated `v1/separated-evaluator/checker.cpp`. Source config is default checker, 3 cases; Agentics keeps the original output contract in statement and checker-based scoring in separated evaluator mode. Private ZIP content inspection blocked.

- [ ] `scp-maze-exit-frontier-cs-algorithmic-85`
  - Frontier-CS source: `algorithmic/problems/85`
  - Agentics path: `challenges/scp-maze-exit-frontier-cs-algorithmic-85`
  - Verdict: major drift
  - Severity: P1
  - Evidence: Frontier-CS config is interactive and names `interactor.cc` (`config.yaml` lines 1-8). The source interactor reads hidden `deep, seed`, sends `deep` to the contestant, accepts `move c` and `query`, enforces 100000 move/query limits, and scores `5000.0 / querycnt` through `quitp` (`interactor.cc` lines 21-78). The Agentics bundle instead uses `separated_evaluator` (`v1/spec.json` lines 90-100), the statement explicitly says all interaction is replaced by one stdin record and one exact submitted answer (`statement.md` lines 3-17), and `run.py` compares whitespace-normalized output tokens against `answer_text`/`answer_path` for 100/0 exact-reference scoring (`run.py` lines 43-106). This changes the participant interface and scoring objective from interactive pathfinding with query minimization to offline answer lookup. Private ZIP content inspection blocked, but the public bundle/source drift is confirmed.
  - Suggested fix: Migrate as `piped_stdio` with an interactive evaluator that compiles and runs the original `interactor.cc`, with private `session.json` carrying the hidden `deep seed` input and answer/report paths. Preserve `move`/`query` protocol, hard limits, and `5000/querycnt` Testlib ratio scaled to 0-100.

- [x] `sensor-hub-clustering-frontier-cs-algorithmic-307`
  - Frontier-CS source: `algorithmic/problems/307`
  - Agentics path: `challenges/sensor-hub-clustering-frontier-cs-algorithmic-307`
  - Verdict: faithful
  - Notes: Source `chk.cc` and migrated `v1/separated-evaluator/chk.cc` are byte-for-byte identical. Source config is default checker, 10 cases; Agentics uses the matching separated evaluator shape and required private path `private-benchmark/runs.json`. Private ZIP content inspection blocked.
