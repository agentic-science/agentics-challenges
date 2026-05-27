# Lamp Ring Permutation

The judge owns a hidden cyclic permutation `p_1, ..., p_n` of lamp labels. It also owns a hidden set `S` of currently lit lamp positions, initially empty.

At session start the evaluator writes two integers:

```text
subtask n
```

To query, write one line with `L` followed by `L` labels in `[1, n]`, then flush. The evaluator toggles those labels in order. After each toggle it returns `1` if the current lit set contains an adjacent pair on the hidden cycle, otherwise `0`; all `L` response bits are returned in order on one line. The lit set is not reset between queries.

To answer the current case, write `-1` followed by a permutation of all `n` labels, then flush. Any cyclic shift or reversal of the hidden cycle is accepted. The answer line does not count as a query.

Agentics may chain multiple source test files in one stdin/stdout session. After a correct final answer, keep reading: another positive `subtask n` starts the next case, while `0 0` means the session is complete and your program should exit. EOF before a final answer, malformed integers, out-of-range labels, excessive query rounds, excessive total operations, or an incorrect final permutation receive zero from the trusted evaluator. The trusted evaluator writes `result.json`; participant code must only speak the protocol above.

The score is the original Frontier-CS ratio based on query rounds and total toggles, scaled to `score` from 0 to 100.
