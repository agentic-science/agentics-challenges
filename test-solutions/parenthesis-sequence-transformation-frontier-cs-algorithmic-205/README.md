# Parenthesis Sequence Transformation Smoke Solution

Reads stdin and emits a general structural transformation. The construction
uses one temporary trailing `()` catalyst, decomposes the source into flat
atoms, rebuilds the target with op 4 rotations, and removes the catalyst. It is
intended as a meaningful non-cheating smoke solution rather than an optimal
solver.
