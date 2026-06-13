from __future__ import annotations

import os
from pathlib import Path


IRREDUCIBLE_POLYS = [
    0,
    0b11,
    0b111,
    0b1011,
    0b10011,
    0b100101,
    0b1000011,
    0b10000011,
    0b100011011,
    0b1000000011,
    0b10000001001,
    0b100000000101,
    0b1000000001001,
    0b10000000011011,
    0b100000000101011,
    0b1000000000000011,
]


def read_n() -> int:
    text = (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")
    tokens = text.split()
    return int(tokens[0]) if tokens else 1


def write_values(values: list[int]) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    body = " ".join(map(str, values))
    out.write_text(f"{len(values)}\n{body}\n", encoding="utf-8")


def gf_mul(a: int, b: int, degree: int, poly: int) -> int:
    result = 0
    mask = (1 << degree) - 1
    low_poly = poly & mask
    for _ in range(degree):
        if b & 1:
            result ^= a
        b >>= 1
        carry = (a >> (degree - 1)) & 1
        a = (a << 1) & mask
        if carry:
            a ^= low_poly
    return result


def gf_pow3(value: int, degree: int, poly: int) -> int:
    return gf_mul(gf_mul(value, value, degree, poly), value, degree, poly)


def algebraic_sidon_set(n: int) -> list[int]:
    if n <= 1:
        return [1] if n == 1 else []

    bit_width = n.bit_length()
    left_bits = bit_width // 2
    right_bits = bit_width - left_bits
    poly = IRREDUCIBLE_POLYS[left_bits]
    values: list[int] = []

    if bit_width % 2 == 1:
        for x in range(1 << left_bits):
            value = ((gf_pow3(x, left_bits, poly) ^ 1) << left_bits) | x
            if 1 <= value <= n:
                values.append(value)
    else:
        limit = min(1 << left_bits, n >> right_bits)
        for x in range(limit):
            value = (x << right_bits) | (gf_pow3(x, left_bits, poly) ^ 1)
            if 1 <= value <= n:
                values.append(value)

    return values or [1]


def greedy_small_set(n: int) -> list[int]:
    chosen: list[int] = []
    used_xors: set[int] = set()
    for candidate in range(1, n + 1):
        new_xors = [candidate ^ value for value in chosen]
        if any(value in used_xors for value in new_xors):
            continue
        chosen.append(candidate)
        used_xors.update(new_xors)
    return chosen


def main() -> int:
    n = read_n()
    values = algebraic_sidon_set(n)
    if n <= 5000:
        greedy = greedy_small_set(n)
        if len(greedy) > len(values):
            values = greedy
    write_values(values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
