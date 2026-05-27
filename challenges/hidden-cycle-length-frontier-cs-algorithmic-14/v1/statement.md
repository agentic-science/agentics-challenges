# Hidden Cycle Length

The judge owns a hidden cycle of length `n` and a token initially placed at a hidden starting vertex. Each vertex has a visible label. The starting vertex is labeled with its own position; newly visited positions receive unique labels lazily from the source interactor.

At the start of a source case the evaluator is ready for commands; it does not reveal `n`.

To move the token, write:

```text
walk x
```

where `0 <= x <= 10^9`, then flush. The evaluator moves `x` steps forward around the hidden cycle and returns the visible label at the reached vertex. A `walk 0` command returns the current label and counts as a walk.

To finish the current case, write `guess g`, flush, and continue reading. The guess must be in `[1, 10^9]`; it is correct only when `g = n`.

Agentics may chain multiple source cases. After a correct guess, read one wrapper-framing line. `NEXT` means another hidden source case begins and you should start issuing `walk` or `guess` commands for it. `0 0` means the session is complete and your program should exit. Malformed commands, too many walks, EOF before a guess, or a wrong guess receive zero from the trusted evaluator. The trusted evaluator writes `result.json`; participant code must only speak the stdin/stdout protocol.

The official score is the original Frontier-CS log-space query-count score, scaled to `score` from 0 to 100.
