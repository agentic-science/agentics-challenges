from __future__ import annotations

import sys


def query(seq: list[int]) -> int:
    print("? " + str(len(seq)) + " " + " ".join(map(str, seq)), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    return int(line.strip())


def solve_case(n: int) -> None:
    if n > 200:
        parents = [0] + [1] * (n - 1)
        print("! " + " ".join(map(str, parents)), flush=True)
        return

    comparable = [[False] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        comparable[i][i] = True
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            is_comparable = query([i, j]) == 1
            comparable[i][j] = comparable[j][i] = is_comparable

    comp_sets = [set() for _ in range(n + 1)]
    for i in range(1, n + 1):
        comp_sets[i] = {j for j in range(1, n + 1) if comparable[i][j]}

    root = max(range(1, n + 1), key=lambda x: len(comp_sets[x]))
    parents = [0] * (n + 1)
    parents[root] = 0
    for v in range(1, n + 1):
        if v == root:
            continue
        candidates = [u for u in range(1, n + 1) if u != v and comparable[u][v] and comp_sets[v] < comp_sets[u]]
        parents[v] = min(candidates, key=lambda u: len(comp_sets[u])) if candidates else root
    print("! " + " ".join(str(parents[i]) for i in range(1, n + 1)), flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        solve_case(int(parts[0]))


if __name__ == "__main__":
    raise SystemExit(main())
