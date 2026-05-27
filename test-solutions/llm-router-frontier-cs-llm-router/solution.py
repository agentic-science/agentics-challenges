from __future__ import annotations


class Solution:
    def solve(self, query: str, eval_name: str, candidate_models: list[str]) -> str:
        _ = (query, eval_name)
        if "cheap" in candidate_models:
            return "cheap"
        return candidate_models[0]
