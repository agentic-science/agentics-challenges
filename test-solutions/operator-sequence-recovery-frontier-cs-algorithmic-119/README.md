# Smoke solution for operator-sequence-recovery-frontier-cs-algorithmic-119

Recovers operators from right to left with one query per operator. The query
zeros the prefix, probes the current operator with `1`, and uses known suffix
additions to distinguish `+` from multiplication.
