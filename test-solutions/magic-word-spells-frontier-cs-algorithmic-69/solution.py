from __future__ import annotations

import sys


def binary_words(n: int) -> list[str]:
    words: list[str] = []
    length = 1
    while len(words) < n:
        for mask in range(1 << length):
            chars = ["O" if (mask >> bit) & 1 else "X" for bit in range(length - 1, -1, -1)]
            words.append("".join(chars))
            if len(words) == n:
                break
        length += 1
    return words


def solve_case(n: int, q: int) -> None:
    for word in binary_words(n):
        print(word)
    sys.stdout.flush()

    for query_index in range(q):
        line = sys.stdin.readline()
        if line == "":
            return
        u = (query_index % n) + 1
        v = ((query_index * 37 + 13) % n) + 1
        print(f"{u} {v}", flush=True)


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
