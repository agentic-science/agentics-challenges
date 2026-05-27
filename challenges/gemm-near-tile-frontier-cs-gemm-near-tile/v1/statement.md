# GEMM Optimization: Near-Tile Shapes

Source provenance: `research/problems/gemm_optimization/near_tile` from Frontier-CS.

Optimize a Triton GEMM with GELU around tile-boundary dimensions.

## What To Submit

Submit `solution.py` whose `Solution.solve(spec_path)` returns code or a program path defining the required kernel function.

## Scoring

Correctness is mandatory; source benchmark score is reported on a 0-100 scale.

## Public And Official Data

Committed public data is a small smoke benchmark. Official evaluation uses private benchmark data from `official-runs.zip`.

## Risks

Requires actual CUDA hardware for smoke; private metadata is visible to participant code but contains no secrets.
