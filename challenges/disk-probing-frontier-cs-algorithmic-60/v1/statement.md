# Disk Probing

This is an interactive `zip_project` challenge. The trusted evaluator owns a hidden circular disk in a `100000 x 100000` square and runs the original Frontier-CS Testlib interactor for `algorithmic/problems/60`.

There is no startup input for a case. Your program should immediately begin sending probe commands:

```text
query x1 y1 x2 y2
```

The two endpoints must be distinct integer points with every coordinate in `[0, 100000]`. The evaluator replies with one decimal number: the length of the part of that segment lying inside the hidden disk, printed with seven digits after the decimal point.

You may ask at most 1024 probes. When you know the disk, print exactly one final answer:

```text
answer x y r
```

Here `(x, y)` is the integer center and `r` is the integer radius. After the final answer, exit without extra output. EOF before a final answer, malformed commands, invalid coordinates, repeated endpoints, too many probes, incorrect answers, and extra output are handled by the source interactor and receive the source verdict behavior.

The public session contains one small deterministic disk. Official scoring uses one private Frontier-CS-derived hidden disk and reports the source ratio `1 - queries / 1024`, scaled to `score` from 0 to 100. The trusted evaluator writes `result.json`; participant code must not write evaluator results.
