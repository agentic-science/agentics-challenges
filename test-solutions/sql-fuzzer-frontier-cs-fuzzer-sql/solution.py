from __future__ import annotations
class Solution:
    def solve(self, resources_path: str):
        return {"code":"""def fuzz(parse_sql):
    parse_sql([
        "CREATE TABLE users (id INT PRIMARY KEY, score INT);",
        "INSERT INTO users (id, score) VALUES (1, 7);",
        "SELECT id FROM users WHERE score BETWEEN 1 AND 10 ORDER BY id LIMIT 1;",
    ])
    return False
"""}
