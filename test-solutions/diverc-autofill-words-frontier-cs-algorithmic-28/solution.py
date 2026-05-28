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


def base26(value: int, width: int) -> str:
    chars = ["a"] * width
    for pos in range(width - 1, -1, -1):
        chars[pos] = chr(ord("a") + value % 26)
        value //= 26
    return "".join(chars)


def generated_word(first_letter: str, index: int) -> str:
    return first_letter + base26(index, 9)


def solve_case(n: int) -> None:
    words: list[str] = []
    for letter in string.ascii_lowercase:
        if not query(letter, 1):
            continue

        high = (n - 1) // 26
        lo, hi = 0, high
        while lo < hi:
            mid = (lo + hi + 1) // 2
            prefix = letter + base26(mid, 8)
            if query(prefix, 1):
                lo = mid
            else:
                hi = mid - 1

        last_prefix = letter + base26(lo, 8)
        last_count = len(query(last_prefix, min(26, n)))
        count = lo * 26 + last_count
        words.extend(generated_word(letter, idx) for idx in range(count))

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
