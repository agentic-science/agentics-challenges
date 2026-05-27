from __future__ import annotations

import sys


def try_pen(index: int) -> int:
    print(f"0 {index}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactive evaluator closed before replying")
    return int(line.strip())


def solve_case(n: int) -> None:
    threshold = min(3, max(1, n // 4))
    scores = [0] * n
    for index in range(n):
        for _ in range(threshold):
            if try_pen(index) == 1:
                scores[index] += 1
            else:
                break
    chosen = sorted(range(n), key=lambda i: (scores[i], i), reverse=True)[:2]
    if len(chosen) < 2:
        chosen = [0, 1]
    print(f"1 {chosen[0]} {chosen[1]}", flush=True)


def main() -> None:
    first = sys.stdin.readline()
    if first == "":
        return
    t = int(first.strip())
    for _ in range(t):
        line = sys.stdin.readline()
        if line == "":
            return
        solve_case(int(line.strip()))


if __name__ == "__main__":
    main()
