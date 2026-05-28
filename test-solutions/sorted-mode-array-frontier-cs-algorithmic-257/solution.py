from __future__ import annotations

import sys


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


def main() -> int:
    while True:
        line = read_line()
        if line is None:
            return 0
        if not line:
            continue
        n = int(line)
        values = [query(index) for index in range(1, n + 1)]
        print("! " + " ".join(map(str, values)), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
