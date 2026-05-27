from __future__ import annotations


class Solution:
    def solve(self, resources_path: str) -> list[str]:
        _ = resources_path
        return [
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, score REAL DEFAULT 0, active BOOLEAN CHECK (active IS NOT NULL));",
            "INSERT INTO users (id, name, score, active) VALUES (1, 'Ada', 9.5, TRUE), (2, 'Linus', 7.0, FALSE);",
            "SELECT DISTINCT u.name AS username, COUNT(*) AS n FROM users AS u LEFT OUTER JOIN users AS v ON u.id = v.id WHERE u.score BETWEEN 1 AND 10 AND u.name LIKE 'A%' GROUP BY u.name HAVING COUNT(*) >= 1 ORDER BY n DESC, username ASC LIMIT 5 OFFSET 0;",
            "SELECT * FROM (SELECT id, LOWER(name) AS lower_name FROM users WHERE id IN (1, 2, 3)) AS sub WHERE EXISTS (SELECT id FROM users WHERE users.id = sub.id);",
            "UPDATE users SET score = score + 1, active = NOT active WHERE id NOT IN (SELECT id FROM users WHERE score < 0);",
            "DELETE FROM users WHERE name IS NULL OR score <= 0;",
        ]
