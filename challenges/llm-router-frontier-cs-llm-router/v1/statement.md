# LLM Router

Submit a ZIP project containing `solution.py` with:

```python
class Solution:
    def solve(self, query: str, eval_name: str, candidate_models: list[str]) -> str:
        ...
```

For each offline prompt, return exactly one string from `candidate_models`, normally `["cheap", "mid", "expensive"]`. Invalid returns are treated by the source evaluator as `"cheap"` for that query.

The challenge is fully offline. External API calls and internet access are disabled. The public bundle includes the source reference dataset at `resources/reference_data.csv`; you may inspect it during solution development and at runtime. Official evaluation uses a separate private RouterBench test split.

Scoring follows the source evaluator. For each row, the chosen tier maps to one concrete LLM. The evaluator looks up that model's correctness and cost, then computes:

```text
raw_score = accuracy - 150.0 * avg_cost
score = raw_score / oracle_raw_score * 100
```

where the oracle chooses the lowest-cost correct tier for every row. The primary metric is `score`.

This challenge uses `coexecuted_benchmark` with `acknowledge_danger: true` because the trusted evaluator imports and executes participant Python from `/workspace`. Public validation is a tiny deterministic CSV. Official benchmark rows are private benchmark data, visible to participant code only during official coexecution, and contain no secrets.
