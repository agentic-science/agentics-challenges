from __future__ import annotations

import sys

MAX_SINGLETON_QUERIES = 4096


def read_line() -> str | None:
    line = sys.stdin.readline()
    if line == "":
        return None
    stripped = line.strip()
    if stripped == "-1":
        raise SystemExit(0)
    return stripped


def query(index: int) -> int:
    print(f"? {index} {index}", flush=True)
    line = read_line()
    if line is None:
        raise EOFError("interactor closed during query")
    value, _freq = map(int, line.split())
    return value


def sample_indices(n: int) -> list[int]:
    if n <= MAX_SINGLETON_QUERIES:
        return list(range(1, n + 1))
    count = min(n, MAX_SINGLETON_QUERIES)
    return sorted({1 + (step * (n - 1)) // (count - 1) for step in range(count)})


def reconstruct_bounded(n: int) -> list[int]:
    anchors = [(index, query(index)) for index in sample_indices(n)]
    values: list[int] = []
    for position, (index, value) in enumerate(anchors):
        next_index = anchors[position + 1][0] if position + 1 < len(anchors) else n + 1
        values.extend([value] * (next_index - index))
    return values[:n]


def main() -> int:
    while True:
        line = read_line()
        if line is None:
            return 0
        if not line:
            continue
        n = int(line)
        values = reconstruct_bounded(n)
        print("! " + " ".join(map(str, values)), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
