from __future__ import annotations

import sys

MAX_SETS = 2_200_000


def main() -> int:
    data = [int(token) for token in sys.stdin.buffer.read().split()]
    if not data:
        return 0

    n, q = data[0], data[1]
    values = [0, *data[2 : 2 + n]]
    pos = 2 + n
    requirements = [(data[pos + 2 * i], data[pos + 2 * i + 1]) for i in range(q)]

    operations: list[tuple[int, int]] = []
    interval_id: dict[tuple[int, int], int] = {(i, i): i for i in range(1, n + 1)}
    next_id = n
    answers: list[int] = []

    for left, right in requirements:
        key = (left, right)
        if key in interval_id:
            answers.append(interval_id[key])
            continue

        ordered_indices = sorted(range(left, right + 1), key=lambda index: values[index])
        current_id = ordered_indices[0]
        for index in ordered_indices[1:]:
            if next_id >= MAX_SETS:
                break
            operations.append((current_id, index))
            next_id += 1
            current_id = next_id

        interval_id[key] = current_id
        answers.append(current_id)

    out = [str(n + len(operations))]
    out.extend(f"{left} {right}" for left, right in operations)
    out.append(" ".join(str(answer) for answer in answers))
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
