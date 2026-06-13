# Inversion Recovery Baseline Solution

This solution uses interval inversion parity as an on-demand comparator. For positions `i < j`, four cached interval queries isolate whether `p_i > p_j`; sorting positions by that comparator recovers the hidden permutation exactly.
