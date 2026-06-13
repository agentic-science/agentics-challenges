# imagenet-500k-frontier-cs-imagenet-500k Baseline Solution

Deterministic nearest-centroid baseline for the synthetic ImageNet Pareto task.

The solution estimates class centers from the provided training and validation loaders, applies shrinkage toward the global feature mean, and returns a fixed linear classifier implementing nearest-center scoring.
It uses only the challenge-provided labeled examples and metadata, so it is suitable for public validation and official evaluation without hard-coded public paths.
