# SQL Parser Coverage Fuzzing

Write a ZIP project that generates SQL statements for a Python SQL parser. Your goal is to maximize the evaluator's parser coverage score while keeping the output valid and bounded.

Each run receives a JSON file:

```text
AGENTICS_INPUT_DIR/case.json
```

Your `run.sh` must write:

```text
AGENTICS_OUTPUT_DIR/statements.json
```

`statements.json` must be either a JSON array of SQL strings or an object with a `statements` array. Example:

```json
{
  "statements": [
    "CREATE TABLE users (id INT PRIMARY KEY, name TEXT);",
    "INSERT INTO users (id, name) VALUES (1, 'ada');",
    "SELECT name FROM users WHERE id = 1;"
  ]
}
```

The evaluator parses your statements with the bundled parser target and reports:

- `score`: combined line and feature coverage on a 0-100 scale.
- `line_coverage`: executable parser lines reached.
- `feature_coverage`: evaluator-defined SQL feature categories exercised.
- `valid_statements`: statements that parsed successfully.

Malformed JSON, non-string statements, empty output, excessive statement counts, or oversized statements receive no score for that run.

## Limits

The evaluator may provide per-run limits in `case.json`:

- `statement_limit`: maximum number of statements to score.
- `max_statement_bytes`: maximum UTF-8 size per statement.

Do not rely on internet access during setup, build, or run.

## Provenance

This challenge is based on Frontier-CS `research/problems/grammar_fuzzing/seed/sql`. The original benchmark called `Solution.solve(resources_path)` and expected `list[str]`. The Agentics version uses the normal `zip_project` protocol and a separated trusted evaluator.
