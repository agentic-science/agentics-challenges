# Grid Robot Trap

The judge owns a robot on the positive integer grid. All cells start white. Each turn you blacken one cell and the robot moves to a white adjacent cell according to the trusted source interactor.

At the start of a source case the evaluator writes:

```text
sx sy
```

For each turn, write one line `x y`, flush, and read the robot response. Your coordinates must satisfy `1 <= x, y <= 3000`. If the robot is trapped, the evaluator writes `0 0`; that completes the current source case. Otherwise the evaluator writes the robot's new positive coordinates, which become the current position for the next turn.

Agentics may chain multiple source cases. After a case returns `0 0`, keep reading: another positive `sx sy` starts the next case, while a second `0 0` at case boundary means the session is complete and your program should exit. EOF before trapping the robot, malformed coordinates, out-of-range marks, or failing to trap within 3000 turns receive zero from the trusted evaluator. The trusted evaluator writes `result.json`; participant code must only speak the stdin/stdout protocol.

The official score is the original Frontier-CS turn-efficiency score, scaled to `score` from 0 to 100.
