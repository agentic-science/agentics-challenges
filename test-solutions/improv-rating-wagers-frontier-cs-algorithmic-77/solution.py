from __future__ import annotations

import sys


def read_nonempty() -> str | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        stripped = line.strip()
        if stripped:
            return stripped


def solve_case(n: int, m: int) -> None:
    weights = [1.0 / n for _ in range(n)]
    beta = 0.7

    for _ in range(m):
        pred = read_nonempty()
        if pred is None:
            return
        ones = sum(weight for weight, bit in zip(weights, pred) if bit == "1")
        zeros = sum(weight for weight, bit in zip(weights, pred) if bit == "0")
        guess = "1" if ones > zeros else "0"
        print(guess, flush=True)

        actual = read_nonempty()
        if actual is None:
            return
        total = 0.0
        for index, bit in enumerate(pred):
            if bit != actual:
                weights[index] *= beta
            total += weights[index]
        if total <= 0.0:
            weights = [1.0 / n for _ in range(n)]
        else:
            weights = [weight / total for weight in weights]


def main() -> int:
    while True:
        header = read_nonempty()
        if header is None:
            return 0
        parts = header.split()
        if len(parts) == 1 and parts[0] == "0":
            return 0
        if len(parts) != 2:
            return 0
        solve_case(int(parts[0]), int(parts[1]))


if __name__ == "__main__":
    raise SystemExit(main())
