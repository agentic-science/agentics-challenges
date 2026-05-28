from __future__ import annotations

import random
import sys


POSITIONS = 1000
BITS = 30
SEED = 1006
WEIGHT = 6


def build_codes() -> list[int]:
    rng = random.Random(SEED)
    codes: list[int] = []
    used_signatures: set[int] = set()
    bit_indices = list(range(BITS))

    while len(codes) < POSITIONS:
        mask = 0
        for bit in rng.sample(bit_indices, WEIGHT):
            mask |= 1 << bit
        if mask in used_signatures:
            continue

        new_signatures = [mask]
        seen = {mask}
        for existing in codes:
            signature = mask | existing
            if signature in used_signatures or signature in seen:
                break
            seen.add(signature)
            new_signatures.append(signature)
        else:
            codes.append(mask)
            used_signatures.update(new_signatures)
    return codes


def build_lookup(codes: list[int]) -> dict[int, tuple[int, int]]:
    lookup: dict[int, tuple[int, int]] = {}
    for a in range(POSITIONS):
        for b in range(a, POSITIONS):
            signature = codes[a] | codes[b]
            if signature in lookup:
                raise RuntimeError("pair signatures must be unique")
            lookup[signature] = (a + 1, b + 1)
    return lookup


def read_answer_bits() -> list[int]:
    parts: list[str] = []
    while not parts:
        line = sys.stdin.readline()
        if not line:
            return []
        parts = line.split()
    count = int(parts[0])
    while len(parts) < count + 1:
        line = sys.stdin.readline()
        if not line:
            break
        parts.extend(line.split())
    return [int(value) for value in parts[1 : count + 1]]


def main() -> int:
    codes = build_codes()
    lookup = build_lookup(codes)

    while True:
        header = sys.stdin.readline()
        if not header:
            return 0
        _robots, _hours = map(int, header.split())

        for bit in range(BITS):
            positions = [str(index + 1) for index, mask in enumerate(codes) if (mask >> bit) & 1]
            print(f"? {len(positions)} {' '.join(positions)}", flush=True)

        print("@", flush=True)
        bits = read_answer_bits()
        observed = 0
        for bit, value in enumerate(bits):
            if value:
                observed |= 1 << bit

        a, b = lookup[observed]
        print(f"! {a} {b}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
