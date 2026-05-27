from __future__ import annotations

import sys

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
LIMIT = 10**18


def prime_power_query(p: int) -> int:
    value = 1
    while value * p <= LIMIT:
        value *= p
    return value


def ask(q: int) -> int:
    print(f"0 {q}", flush=True)
    response = sys.stdin.readline()
    if not response:
        raise EOFError("interactor closed before answering")
    return int(response.strip())


def exponent_of(value: int, p: int) -> int:
    exponent = 0
    while value % p == 0 and value > 0:
        exponent += 1
        value //= p
    return exponent


def solve_game() -> None:
    divisor_count = 1
    saw_factor = False
    for p in PRIMES:
        g = ask(prime_power_query(p))
        exp = exponent_of(g, p)
        if exp:
            saw_factor = True
            divisor_count *= exp + 1
    answer = divisor_count if saw_factor else 2
    print(f"1 {answer}", flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        games = int(stripped)
        if games <= 0:
            return 0
        for _ in range(games):
            solve_game()


if __name__ == "__main__":
    raise SystemExit(main())
