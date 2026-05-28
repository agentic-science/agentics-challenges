from __future__ import annotations

import sys


def adjacent_swap_sort(values: list[int], limit: int) -> list[tuple[int, int]] | None:
    arr = list(values)
    operations: list[tuple[int, int]] = []
    for target in range(1, len(arr) + 1):
        pos = arr.index(target)
        wanted = target - 1
        while pos > wanted:
            arr[pos - 1], arr[pos] = arr[pos], arr[pos - 1]
            operations.append((pos, pos + 1))
            if len(operations) > limit:
                return None
            pos -= 1
    return operations


def main() -> int:
    data = [int(token) for token in sys.stdin.read().split()]
    if not data:
        return 0
    n = data[0]
    values = data[1:1 + n]
    limit = 200 * n
    operations = adjacent_swap_sort(values, limit)
    if operations is None:
        print(1)
        print(0)
        return 0

    print(1)
    print(len(operations))
    for left, right in operations:
        print(left, right)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
