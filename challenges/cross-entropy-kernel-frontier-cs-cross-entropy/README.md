# Cross Entropy Kernel Optimization

This challenge migrates Frontier-CS source path `research/problems/cross_entropy`.

Optimize a Triton cross-entropy loss kernel against PyTorch GPU baselines.

## Interface

Submit `solution.py` whose `Solution.solve(spec_path)` returns code or a program path defining the required kernel function.

## Evaluation

The evaluator imports participant code in a PyTorch/Triton CUDA environment. Public validation uses tiny tensor shapes; official scoring uses private source metadata.

Correctness is mandatory; source benchmark score is reported on a 0-100 scale.

Public validation is intentionally tiny. Official scoring uses `official-runs.zip` mounted under `private-benchmark/` and not committed to Git.

## Trust Boundary

This challenge uses `coexecuted_benchmark`: trusted evaluator code imports or executes participant Python from `/workspace`. Official private benchmark data is visible in that container and contains no secrets.
