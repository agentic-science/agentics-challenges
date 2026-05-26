from __future__ import annotations

import sys


def send(values: list[int]) -> int:
    print("0 " + " ".join(str(value) for value in values), flush=True)
    reply = sys.stdin.readline()
    if reply == "":
        raise RuntimeError("interactive evaluator closed stdin")
    return int(reply.strip())


def main() -> None:
    first = sys.stdin.readline()
    if first == "":
        return
    n = int(first.strip())
    permutation: list[int | None] = [None] * n

    for index in range(n):
        for value in range(2, n + 1):
            probe = [1] * n
            probe[index] = value
            matches = send(probe)
            if matches == 0:
                permutation[index] = 1
                break
            if matches == 2:
                permutation[index] = value
                break
        if permutation[index] is None:
            permutation[index] = 1

    print("1 " + " ".join(str(value) for value in permutation), flush=True)


if __name__ == "__main__":
    main()
