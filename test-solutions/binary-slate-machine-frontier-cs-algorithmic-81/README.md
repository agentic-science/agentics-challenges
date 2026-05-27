# Binary Slate Machine Prefix/Suffix Baseline

Uses direct one-bit probes for the first half of the string, then recovers the
second half by testing candidate suffixes with a small automaton. It is a simple
non-optimal baseline that keeps the maximum query size around half of `N`.
