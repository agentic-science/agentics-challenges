from __future__ import annotations

from array import array
import sys


def ask(i: int, j: int) -> int:
    print(f"? {i} {j}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed while answering query")
    value = int(line.strip())
    if value == -1:
        raise SystemExit(0)
    return value


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    n = int(line.strip())
    pair_or = [array("H", [0]) * (n + 1) for _ in range(n + 1)]
    totals = [0] * (n + 1)

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            value = ask(i, j)
            pair_or[i][j] = value
            pair_or[j][i] = value
            totals[i] += value
            totals[j] += value

    zero_index = min(range(1, n + 1), key=lambda idx: totals[idx])
    permutation = [0] * n
    for idx in range(1, n + 1):
        if idx != zero_index:
            permutation[idx - 1] = pair_or[zero_index][idx]

    print("! " + " ".join(map(str, permutation)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
