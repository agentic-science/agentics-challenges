from __future__ import annotations

import string
import sys


def read_int_line() -> int | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        line = line.strip()
        if line:
            return int(line)


def query(prefix: str, k: int) -> list[str]:
    print(f"query {prefix} {k}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed during query")
    parts = line.split()
    count = int(parts[0])
    return parts[1 : 1 + count]


def solve_case(n: int) -> None:
    seen: set[str] = set()
    words: list[str] = []
    for letter in string.ascii_lowercase:
        for word in query(letter, n):
            if word not in seen:
                seen.add(word)
                words.append(word)
        if len(words) >= n:
            break
    print("answer " + " ".join(words[:n]), flush=True)


def main() -> int:
    while True:
        t = read_int_line()
        if t is None or t <= 0:
            return 0
        for _ in range(t):
            n = read_int_line()
            if n is None:
                return 0
            solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
