from __future__ import annotations

import math
import sys


def bits(value: int) -> int:
    return value.bit_length()


def modpow_time(a: int, d: int, n: int) -> int:
    result = 1
    x = a
    total = 0
    for bit in range(60):
        bx = bits(x) + 1
        if (d >> bit) & 1:
            total += (bits(result) + 1) * bx
            result = (result * x) % n
        total += bx * bx
        x = (x * x) % n
    return total


def query(a: int) -> int:
    print(f"? {a}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed before answering")
    return int(line.strip())


def factor_small(n: int) -> tuple[int, int] | None:
    limit = math.isqrt(n)
    if limit > 100000:
        return None
    for candidate in range(2, limit + 1):
        if n % candidate == 0:
            return candidate, n // candidate
    return None


def solve_case(n: int) -> None:
    factors = factor_small(n)
    observations: dict[int, int] = {}
    for a in range(min(n, 64)):
        observations[a] = query(a)

    answer = 1
    if factors is not None:
        p, q = factors
        phi = (p - 1) * (q - 1)
        if phi <= 200000:
            for candidate in range(1, phi):
                if math.gcd(candidate, phi) != 1:
                    continue
                if all(modpow_time(a, candidate, n) == observed for a, observed in observations.items()):
                    answer = candidate
                    break

    print(f"! {answer}", flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n = int(stripped)
        if n == 0:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
