# SQL Parser Coverage Fuzzing

Generate SQL statements that exercise a bundled Python SQL parser. The submitted ZIP project runs once per Agentics invocation and writes `statements.json` to `AGENTICS_OUTPUT_DIR`.

The evaluator parses the generated statements, measures which parser lines and SQL feature categories were exercised, and reports a coverage-oriented score.

## Contract

Each run receives `case.json` in `AGENTICS_INPUT_DIR`. The solution must write:

```text
AGENTICS_OUTPUT_DIR/statements.json
```

The file must contain either a JSON array of strings or an object with a `statements` array:

```json
[
  "CREATE TABLE users (id INT PRIMARY KEY, name TEXT);",
  "SELECT name FROM users WHERE id = 1;"
]
```

The evaluator rejects excessive statement counts and oversized statements before parsing.

## Provenance

This challenge is migrated from Frontier-CS:

- `research/problems/grammar_fuzzing/seed/sql`
- Original title: SQL Parser Test Case Generation
- Original shape: `Solution.solve(resources_path) -> list[str]`, scored by parser coverage and efficiency.

The Agentics version uses `separated_evaluator`: submitted solutions only produce statement files, while the trusted evaluator owns scoring.

## Files

- `v1/spec.json` declares the Agentics bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/runs.json` contains a small deterministic public validation run.
- `v1/resources/sql_engine` and `v1/resources/sql_grammar.txt` contain the public parser target.
- `v1/evaluator/run.py` validates outputs and writes Agentics result JSON.

Official run metadata is uploaded as a private asset overlay and is not committed.
