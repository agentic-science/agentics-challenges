from __future__ import annotations

import sys


def query(indices: list[int]) -> int:
    print("0 " + str(len(indices)) + " " + " ".join(map(str, indices)), flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise SystemExit(0)
    return int(line.strip())


def has_opposite(reference: int, group: list[int]) -> bool:
    if not group:
        return False
    left_probe = [reference] * len(group) + group
    if query(left_probe) > 0:
        return True
    right_probe = group + [reference] * len(group)
    return query(right_probe) > 0


def find_opposite(reference: int, n: int) -> int:
    rest = [index for index in range(1, n + 1) if index != reference]
    group: list[int] | None = None
    for start in range(0, len(rest), 500):
        chunk = rest[start : start + 500]
        if has_opposite(reference, chunk):
            group = chunk
            break
    if group is None:
        return rest[0]

    while len(group) > 1:
        mid = len(group) // 2
        left = group[:mid]
        right = group[mid:]
        if has_opposite(reference, left):
            group = left
        else:
            group = right
    return group[0]


def classify(open_index: int, close_index: int, n: int) -> str:
    result = ["?"] * (n + 1)
    result[open_index] = "("
    result[close_index] = ")"

    unknown = [index for index in range(1, n + 1) if result[index] == "?"]
    for start in range(0, len(unknown), 7):
        chunk = unknown[start : start + 7]
        probe: list[int] = []
        base = 0
        for bit, index in enumerate(chunk):
            weight = 1 << bit
            base += weight
            for _ in range(weight):
                probe.extend([open_index, index, close_index, close_index, close_index])
        value = query(probe) - base
        for bit, index in enumerate(chunk):
            result[index] = "(" if value & (1 << bit) else ")"

    return "".join(result[1:])


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n = int(stripped)
        if n <= 0:
            return 0

        reference = 1
        opposite = find_opposite(reference, n)
        if query([reference, opposite]) == 1:
            open_index, close_index = reference, opposite
        else:
            open_index, close_index = opposite, reference

        print("1 " + classify(open_index, close_index, n), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
