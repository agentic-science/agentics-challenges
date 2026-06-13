# Baseline solution for heap-tree-sum-frontier-cs-algorithmic-209

Uses depth-grouped aggregate distance sums. For source-sized cases it queries distances `1`, `2`, `h`, and sometimes `h + 1` for each hidden permutation index, then applies a closed-form layer-sum identity for the total tree weight.
