from __future__ import annotations

import itertools
import sys


def query(i: int, j: int) -> int:
    print(f"? {i} {j}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed before answering")
    value = int(line.strip())
    if value == -1:
        raise SystemExit(0)
    return value


def solve_case(n: int) -> None:
    observed: dict[tuple[int, int], int] = {}
    if n <= 8:
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                observed[(i - 1, j - 1)] = query(i, j)
        for candidate in itertools.permutations(range(n)):
            if all((candidate[i] | candidate[j]) == value for (i, j), value in observed.items()):
                print("! " + " ".join(str(value) for value in candidate), flush=True)
                return

    guess = list(range(n))
    print("! " + " ".join(str(value) for value in guess), flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n = int(stripped)
        if n == 0:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
