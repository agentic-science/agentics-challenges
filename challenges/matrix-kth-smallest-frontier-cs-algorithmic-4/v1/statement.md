# Matrix K-th Smallest

The judge owns a hidden `n x n` matrix whose rows and columns are nondecreasing. Your task is to identify the `k`-th smallest matrix value.

At session start the evaluator writes:

```text
n k
```

To inspect one cell, write `QUERY x y`, flush, and read the integer value at row `x`, column `y`. Coordinates are one-based and must be in `[1, n]`.

To finish the current case, write `DONE ans`, flush, and continue reading. A positive `n k` starts another source case, while `0 0` means the Agentics session is complete and your program should exit. EOF before `DONE`, malformed commands, out-of-bounds queries, exceeding the source query limit, or a wrong final answer receive zero from the trusted evaluator. The trusted evaluator writes `result.json`; participant code must only speak the stdin/stdout protocol.

The official score is the original Frontier-CS query-efficiency score for a correct answer, scaled to `score` from 0 to 100.
