from __future__ import annotations

import sys


def constructive_sort(p: list[int]) -> list[tuple[int, int]] | None:
    n = len(p)
    target = list(range(1, n + 1))
    if p == target:
        return []
    if n <= 3:
        return None

    current = list(p)
    ops: list[tuple[int, int]] = []

    def do_op(x: int, y: int) -> bool:
        if x <= 0 or y <= 0 or x + y >= n or len(ops) >= 4 * n:
            return False
        current[:] = current[-y:] + current[x : n - y] + current[:x]
        ops.append((x, y))
        return True

    def move_helper_to_end() -> bool:
        pos = current.index(n)
        if pos == n - 1:
            return True
        if pos == n - 2:
            return do_op(1, 2) and do_op(1, 1)
        return do_op(pos + 1, 1)

    def put_one_first() -> bool:
        pos = current.index(1)
        if pos == 0:
            return True
        y_between = n - pos - 2
        if y_between > 0:
            return do_op(pos + 1, 1) and do_op(1, 1)
        return do_op(1, 1) and do_op(1, 2)

    def place_value(value: int) -> bool:
        prefix = value - 1
        pos = current.index(value)
        if pos == prefix:
            return True
        x_len = pos - prefix
        y_len = n - pos - 2
        if y_len > 0:
            return (
                do_op(prefix, 1)
                and do_op(1 + x_len, prefix)
                and do_op(prefix + 1, 1 + x_len)
                and do_op(1, prefix + 1)
            )
        if x_len == 1:
            if prefix == 1:
                return do_op(1, 2) and do_op(1, 1) and do_op(2, 1) and do_op(1, 1) and do_op(1, 2)
            return do_op(1, 1) and do_op(1, 2) and do_op(2, 2) and do_op(2, 1)
        return do_op(prefix, 3) and do_op(1, prefix + x_len) and do_op(1, prefix + 2)

    if not move_helper_to_end() or not put_one_first():
        return None
    for value in range(2, n):
        if not place_value(value):
            return None
    return ops if current == target and len(ops) < 4 * n else None


def main() -> int:
    data = [int(token) for token in sys.stdin.read().split()]
    if not data:
        return 0
    n = data[0]
    p = data[1 : 1 + n]
    ops = constructive_sort(p) or []

    sys.stdout.write(f"{len(ops)}\n")
    for x, y in ops:
        sys.stdout.write(f"{x} {y}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
