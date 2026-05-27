# SQL Parser Test Case Generation

Submit a ZIP project containing `solution.py` with:

```python
class Solution:
    def solve(self, resources_path: str) -> list[str]:
        ...
```

The `resources_path` directory contains the participant-visible source resources:

```text
resources/
  sql_grammar.txt
  sql_engine/
    __init__.py
    parser.py
    tokenizer.py
    ast_nodes.py
    ast_to_sql.py
```

Return a list of SQL statement strings. The trusted evaluator parses each string with `sql_engine.parse_sql` while Python `coverage` measures `parser.py`, `tokenizer.py`, and `ast_nodes.py`. Statements that raise parser exceptions do not improve coverage.

The source score is:

```text
weighted_cov = 0.6 * line_coverage + 0.4 * branch_coverage
coverage_score = 0.7 * (weighted_cov / 100)^3 * 100
efficiency_bonus = 30 * 2^(-N / 50)
score = coverage_score + efficiency_bonus
```

where `N` is the number of returned string statements.

This challenge uses `coexecuted_benchmark` with `acknowledge_danger: true` because the trusted evaluator imports and executes participant Python from `/workspace`. External network access is disabled during evaluation. Public validation uses the same parser resources with a tiny smoke config; official scoring uses the source benchmark settings packaged outside Git as private config.
