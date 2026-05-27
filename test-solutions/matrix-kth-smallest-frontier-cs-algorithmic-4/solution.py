from __future__ import annotations

import sys


def read_nonempty() -> str | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        if line.strip():
            return line.strip()


def query(x: int, y: int) -> int:
    print(f"QUERY {x} {y}", flush=True)
    response = read_nonempty()
    if response is None:
        raise EOFError("interactor closed during query")
    return int(response)


def solve_case(n: int, k: int) -> None:
    values: list[int] = []
    if n * n <= 50000:
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                values.append(query(x, y))
        answer = sorted(values)[k - 1]
    else:
        values = [query(i, i) for i in range(1, min(n, 50000) + 1)]
        answer = sorted(values)[min(k - 1, len(values) - 1)]
    print(f"DONE {answer}", flush=True)


def main() -> int:
    while True:
        header = read_nonempty()
        if header is None:
            return 0
        parts = header.split()
        if len(parts) >= 2 and parts[0] == "0" and parts[1] == "0":
            return 0
        n, k = int(parts[0]), int(parts[1])
        solve_case(n, k)


if __name__ == "__main__":
    raise SystemExit(main())
