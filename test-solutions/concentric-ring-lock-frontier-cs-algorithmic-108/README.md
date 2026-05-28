# Test solution for concentric-ring-lock-frontier-cs-algorithmic-108

Builds a deterministic C++ interactive solver. It reconstructs the global uncovered-section map from two full ring scans, then uses short per-ring fingerprints against that map to recover the relative offsets while staying inside the source rotation limit.
