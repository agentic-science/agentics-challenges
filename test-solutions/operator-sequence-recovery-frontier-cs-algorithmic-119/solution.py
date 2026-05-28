from __future__ import annotations

import sys


def query(values: list[int]) -> int:
    print("? " + " ".join(str(value) for value in values), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during query")
    return int(line)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
            continue
        n = int(line)
        ops = [0] * n
        known_suffix_additions = 0

        for index in range(n - 1, -1, -1):
            values = [0] * (n + 1)
            values[index + 1] = 1
            for suffix in range(index + 2, n + 1):
                values[suffix] = 1

            result = query(values)
            if result == known_suffix_additions + 1:
                ops[index] = 0
                known_suffix_additions += 1
            else:
                ops[index] = 1

        print("! " + " ".join(str(op) for op in ops), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
