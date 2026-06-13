# Sequence Transform Operations Baseline

Implements a constructive equal-sum baseline.
For `N >= 3`, it first applies direct operations that greedily reduce distance to the target, then uses a four-operation identity translation to move one remaining unit at a time from positions with surplus to positions with deficit.
For `N = 2`, it handles the only nontrivial operation directly.
The sequence is valid for reachable cases but is not intended to be operation-optimal.
