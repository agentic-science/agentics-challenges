from __future__ import annotations

import json
import os
from pathlib import Path


STATEMENTS = [
    "CREATE TABLE users (id INT PRIMARY KEY, name TEXT NOT NULL, score REAL DEFAULT 0);",
    "INSERT INTO users (id, name, score) VALUES (1, 'ada', 9.5), (2, 'linus', 7.0);",
    "SELECT name, score FROM users WHERE score BETWEEN 7 AND 10 ORDER BY score DESC LIMIT 5;",
    "UPDATE users SET score = score + 1 WHERE name LIKE 'a%';",
    "DELETE FROM users WHERE id IN (SELECT id FROM users WHERE score < 1);",
    "SELECT u.name, COUNT(*) FROM users AS u LEFT JOIN users AS v ON u.id = v.id GROUP BY u.name HAVING COUNT(*) >= 1;",
]


def main() -> None:
    output_dir = Path(os.environ["AGENTICS_OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "statements.json").write_text(
        json.dumps({"statements": STATEMENTS}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
