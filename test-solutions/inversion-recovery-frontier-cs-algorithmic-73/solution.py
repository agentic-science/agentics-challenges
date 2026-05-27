from __future__ import annotations

import itertools
import sys


def ask(l: int, r: int) -> int:
    print(f"0 {l} {r}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before replying")
    return int(line.strip())


def inversion_parity(values: tuple[int, ...], left: int, right: int) -> int:
    parity = 0
    for i in range(left, right):
        for j in range(i + 1, right + 1):
            parity ^= int(values[i] > values[j])
    return parity


def solve_case(n: int) -> None:
    if n > 8:
        print("1 " + " ".join(str(value) for value in range(1, n + 1)), flush=True)
        return

    answers: dict[tuple[int, int], int] = {}
    for left in range(1, n + 1):
        for right in range(left + 1, n + 1):
            answers[(left - 1, right - 1)] = ask(left, right)

    for perm in itertools.permutations(range(1, n + 1)):
        if all(inversion_parity(perm, left, right) == parity for (left, right), parity in answers.items()):
            print("1 " + " ".join(str(value) for value in perm), flush=True)
            return
    print("1 " + " ".join(str(value) for value in range(1, n + 1)), flush=True)


def main() -> None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return
        if not line.strip():
            continue
        solve_case(int(line.strip()))


if __name__ == "__main__":
    main()
