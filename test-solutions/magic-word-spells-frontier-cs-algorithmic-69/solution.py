from __future__ import annotations

import sys


def power(text: str) -> int:
    seen: set[str] = set()
    for start in range(len(text)):
        for end in range(start + 1, len(text) + 1):
            seen.add(text[start:end])
    return len(seen)


def words_for(n: int) -> list[str]:
    base = ["X", "XXO", "XOXO"]
    if n <= len(base):
        return base[:n]
    words = base[:]
    for index in range(len(base) + 1, n + 1):
        words.append("X" * index + "O")
    return words


def solve_case(n: int, q: int) -> None:
    words = words_for(n)
    for word in words:
        print(word)
    sys.stdout.flush()

    lookup: dict[int, tuple[int, int]] = {}
    if n <= 20:
        for i, first in enumerate(words, start=1):
            for j, second in enumerate(words, start=1):
                p = power(first + second)
                lookup.setdefault(p, (i, j))

    for _ in range(q):
        line = sys.stdin.readline()
        if line == "":
            return
        pair = lookup.get(int(line.strip()), (1, 1))
        print(f"{pair[0]} {pair[1]}", flush=True)


def main() -> None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return
        if not line.strip():
            continue
        n, q = map(int, line.split())
        solve_case(n, q)


if __name__ == "__main__":
    main()
