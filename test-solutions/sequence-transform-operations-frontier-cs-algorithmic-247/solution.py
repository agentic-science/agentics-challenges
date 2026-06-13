from __future__ import annotations

import itertools
import sys


def apply_operation(values: list[int], i: int, j: int) -> None:
    old_i = values[i - 1]
    old_j = values[j - 1]
    values[i - 1] = old_j - 1
    values[j - 1] = old_i + 1


def operation_effect(n: int, operations: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    source_at = list(range(n))
    offset = [0] * n
    for i, j in operations:
        a = i - 1
        b = j - 1
        source_at[a], source_at[b] = source_at[b], source_at[a]
        offset[a], offset[b] = offset[b] - 1, offset[a] + 1
    return tuple(source_at), tuple(offset)


def translation_table() -> dict[tuple[int, int, int], tuple[tuple[int, int], ...]]:
    table: dict[tuple[int, int, int], tuple[tuple[int, int], ...]] = {}
    pairs = ((1, 2), (1, 3), (2, 3))
    for length in range(1, 5):
        for operations in itertools.product(pairs, repeat=length):
            source_at, offset = operation_effect(3, operations)
            if source_at == (0, 1, 2) and sum(abs(value) for value in offset) == 2:
                table.setdefault(offset, operations)
        if len(table) == 6:
            return table
    raise RuntimeError("failed to build translation table")


TRANSLATIONS = translation_table()


def unit_transfer(positive: int, negative: int, helper: int) -> tuple[tuple[int, int], ...]:
    positions = sorted((positive, negative, helper))
    rank = {position: index for index, position in enumerate(positions)}
    desired = [0, 0, 0]
    desired[rank[positive]] = 1
    desired[rank[negative]] = -1
    pattern = TRANSLATIONS[tuple(desired)]
    return tuple((positions[a - 1], positions[b - 1]) for a, b in pattern)


def construct_operations(a: list[int], b: list[int]) -> list[tuple[int, int]] | None:
    n = len(a)
    if sum(a) != sum(b):
        return None
    if a == b:
        return []
    if n == 2:
        transformed = [a[1] - 1, a[0] + 1]
        return [(1, 2)] if transformed == b else None

    current = a[:]
    operations: list[tuple[int, int]] = []
    while True:
        best_pair: tuple[int, int] | None = None
        best_delta = 0
        for i in range(n):
            for j in range(i + 1, n):
                before = abs(current[i] - b[i]) + abs(current[j] - b[j])
                after_i = current[j] - 1
                after_j = current[i] + 1
                after = abs(after_i - b[i]) + abs(after_j - b[j])
                delta = before - after
                if delta > best_delta:
                    best_delta = delta
                    best_pair = (i + 1, j + 1)
        if best_pair is None:
            break
        operations.append(best_pair)
        apply_operation(current, *best_pair)

    delta = [target - value for value, target in zip(current, b)]
    positives = [index for index, value in enumerate(delta) if value > 0]
    negatives = [index for index, value in enumerate(delta) if value < 0]
    pos_cursor = 0
    neg_cursor = 0

    while pos_cursor < len(positives):
        positive = positives[pos_cursor]
        negative = negatives[neg_cursor]
        helper = 0
        while helper in (positive, negative):
            helper += 1

        transfer = min(delta[positive], -delta[negative])
        for _ in range(transfer):
            for operation in unit_transfer(positive + 1, negative + 1, helper + 1):
                operations.append(operation)
                apply_operation(current, *operation)
        delta[positive] -= transfer
        delta[negative] += transfer
        if delta[positive] == 0:
            pos_cursor += 1
        if delta[negative] == 0:
            neg_cursor += 1

    if current != b:
        raise RuntimeError("constructed operations failed to reach target")
    return operations


def main() -> int:
    data = [int(token) for token in sys.stdin.buffer.read().split()]
    if not data:
        return 0
    n = data[0]
    a = data[1 : 1 + n]
    b = data[1 + n : 1 + 2 * n]
    operations = construct_operations(a, b)
    if operations is None:
        sys.stdout.write("No\n")
        return 0
    lines = ["Yes", str(len(operations))]
    lines.extend(f"{i} {j}" for i, j in operations)
    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
