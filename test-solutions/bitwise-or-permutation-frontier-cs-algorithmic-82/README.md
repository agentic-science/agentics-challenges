# Bitwise OR Permutation Test Solution

This deterministic solver samples a bounded set of pivots, chooses one with a
small estimated bit mask, identifies the zero-valued index without using hidden
answers, and reconstructs every value with OR queries against that zero index.
It loops across Frontier source sessions in the same stdin/stdout run.
