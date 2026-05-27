from __future__ import annotations

import sys


def main() -> None:
    t = int(sys.stdin.readline())
    for _ in range(t):
        _n, m, _start, _base = map(int, sys.stdin.readline().split())
        for _ in range(m):
            sys.stdin.readline()
        while True:
            line = sys.stdin.readline().strip()
            if line in {"AC", "F", ""}:
                break
            values = list(map(int, line.split()))
            degree = values[0]
            choice = 1
            for index in range(degree):
                if values[1 + 2 * index + 1] == 0:
                    choice = index + 1
                    break
            print(choice, flush=True)


if __name__ == "__main__":
    main()
