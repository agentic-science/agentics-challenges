# Tree Centroid Guess

This is an interactive challenge. The evaluator hides a tree with exactly one centroid. You know only `n` and may query distances between vertices before reporting the centroid.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

The evaluator writes one integer `n`, the number of nodes in the hidden tree. Public validation uses a tiny smoke tree; official evaluation uses the private Frontier-CS tree. EOF after the final answer means the session is complete.

## Output

To ask the distance between two vertices, output:

```text
? u v
```

where `1 <= u, v <= n`. Then flush stdout and read one integer response from stdin.

To submit the unique centroid, output:

```text
! x
```

The answer is validated by the trusted source interactor against the private centroid answer.

## Scoring

Let `Q` be the number of distance queries. The source interactor has base limit `100,000`, zero-score limit `400,000`, and a safety cap slightly above the zero-score limit. If the centroid is correct, the bounded source ratio is `1` for `Q <= 100,000`, `0` for `Q >= 400,000`, and `((400000 - Q) / 300000)^2` between those limits. Malformed commands, invalid vertices, safety-limit failures, or a wrong centroid receive zero. Agentics reports the source ratio as `score` from 0 to 100.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
