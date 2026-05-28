from __future__ import annotations

import sys


def solve(data: list[int]) -> str:
    if not data:
        return "1\n0\n"

    n = data[0]
    values = data[1 : 1 + n]
    operations: list[tuple[int, int]] = []

    # x = 2 turns each allowed cyclic shift into an adjacent swap. This is not
    # optimized, but it is a transparent baseline and passes the public smoke.
    for _ in range(n):
        changed = False
        for index in range(n - 1):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                operations.append((index + 1, 0))
                changed = True
        if not changed:
            break

    return (
        f"2\n{len(operations)}\n"
        + "".join(f"{left} {direction}\n" for left, direction in operations)
    )


def main() -> int:
    data = [int(token) for token in sys.stdin.buffer.read().split()]
    sys.stdout.write(solve(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
