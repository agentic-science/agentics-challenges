from __future__ import annotations

import functools
import sys


def race(pepes: list[int]) -> int:
    print("? " + " ".join(str(pepe) for pepe in pepes), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during race")
    return int(line)


def solve_n2_case() -> None:
    labels = [1, 2, 3, 4]

    def compare(left: int, right: int) -> int:
        winner = race([left, right])
        return -1 if winner == left else 1

    ordered = sorted(labels, key=functools.cmp_to_key(compare))
    print("! " + " ".join(str(label) for label in ordered[:3]), flush=True)


def solve_fallback(n: int) -> None:
    labels = list(range(1, n * n + 1))
    wins = {label: 0 for label in labels}
    for start in range(0, len(labels), n):
        group = labels[start:start + n]
        if len(group) < n:
            group.extend(labels[:n - len(group)])
        wins[race(group)] += 1
    ordered = sorted(labels, key=lambda label: (-wins[label], label))
    need = n * n - n + 1
    print("! " + " ".join(str(label) for label in ordered[:need]), flush=True)


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    t = int(line)
    for _ in range(t):
        n_line = sys.stdin.readline()
        if not n_line:
            return 0
        n = int(n_line)
        if n == 2:
            solve_n2_case()
        else:
            solve_fallback(n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
