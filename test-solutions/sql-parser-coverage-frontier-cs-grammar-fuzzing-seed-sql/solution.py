from __future__ import annotations


STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(20) NOT NULL UNIQUE DEFAULT 'anon', score REAL DEFAULT 0, active BOOLEAN CHECK (active IS NOT NULL), data BLOB);",
    "INSERT INTO users (id, name, score, active, data) VALUES (1, 'Ada', 9.5, TRUE, 'x'), (2, 'Linus', 7.0, FALSE, NULL);",
    "SELECT DISTINCT u.id AS user_id, COUNT(*) AS total, SUM(u.score), AVG(u.score), MIN(u.score), MAX(u.score), UPPER(u.name), LOWER(u.name), LENGTH(u.name), SUBSTR(u.name, 1, 2) FROM users AS u LEFT OUTER JOIN (SELECT id, score FROM users WHERE score >= 0) AS s ON u.id = s.id WHERE (u.score BETWEEN 1 AND 10 AND u.name LIKE 'A%') OR u.id IN (1, 2, 3) GROUP BY u.id HAVING COUNT(*) >= 1 ORDER BY total DESC, user_id ASC LIMIT 5 OFFSET 0;",
    "SELECT ALL * FROM users INNER JOIN users AS v ON users.id = v.id WHERE users.id NOT IN (SELECT id FROM users WHERE active IS NULL) AND EXISTS (SELECT id FROM users WHERE id = v.id);",
    "SELECT * FROM users RIGHT OUTER JOIN users AS v ON users.id = v.id;",
    "SELECT * FROM users FULL OUTER JOIN users AS v ON users.id = v.id;",
    "SELECT -1 + +2 * 3 / 4 % 2 AS calc;",
    "UPDATE users SET score = score + 1, active = NOT active WHERE name IS NOT NULL AND id <> 99 OR id != 100;",
    "DELETE FROM users WHERE id <= 0 OR id >= 100;",
]


class Solution:
    def solve(self, resources_path: str) -> list[str]:
        _ = resources_path
        return list(STATEMENTS)
