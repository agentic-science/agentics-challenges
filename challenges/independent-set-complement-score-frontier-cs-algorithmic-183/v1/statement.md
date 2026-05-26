# Independent Set Complement Score

Ported from Frontier-CS `algorithmic/problems/183`.

## Task

Select an independent set under the original complement-style Frontier-CS scoring formula.

Each run provides the original problem input as:

```text
AGENTICS_INPUT_DIR/input.txt
```

Your solution must write its answer as:

```text
AGENTICS_OUTPUT_DIR/answer.txt
```

The expected output format and constraints follow the original Frontier-CS statement for `algorithmic/problems/183`. The separated evaluator validates output shape and task constraints, then computes a normalized score against evaluator-owned reference data.

## Scoring

The primary metric is `score`, an average normalized Frontier-CS score on a 0-100 scale. Invalid outputs receive zero for that case. The public validation case is intentionally small and deterministic; official cases and reference answers are private.
