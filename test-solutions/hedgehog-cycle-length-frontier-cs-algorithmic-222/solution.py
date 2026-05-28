from __future__ import annotations

import math
import sys


MAX_VERTICES = 1_000_000


def ask(vertex: int, steps: int) -> int:
    print(f"? {vertex} {steps}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    value = int(line.strip())
    if value == -1:
        raise SystemExit(0)
    return value


def answer(length: int) -> bool:
    print(f"! {length}", flush=True)
    line = sys.stdin.readline()
    if not line:
        return False
    return line.strip() == "1"


def solve_graph() -> bool:
    start = ask(1, 1)
    block = int(math.isqrt(MAX_VERTICES)) + 1
    baby: dict[int, int] = {start: 0}
    for steps in range(1, block + 1):
        node = ask(start, steps)
        if node == start:
            return answer(steps)
        baby.setdefault(node, steps)

    limit = MAX_VERTICES // block + 3
    for jump in range(1, limit + 1):
        steps = jump * block
        node = ask(start, steps)
        if node in baby:
            length = steps - baby[node]
            if length > 0:
                return answer(length)
    return answer(1)


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    graphs = int(line.strip())
    for _ in range(graphs):
        if not solve_graph():
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
