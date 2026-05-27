from __future__ import annotations

import itertools
import sys


def evaluate(gates: str, wiring: list[tuple[int, int]], bits: str) -> int:
    values = [int(ch) for ch in bits]
    for i in range(len(gates) - 1, -1, -1):
        u, v = wiring[i]
        gate_value = (values[u] & values[v]) if gates[i] == "&" else (values[u] | values[v])
        values[i] ^= gate_value
    return values[0]


def ask(bits: str) -> int:
    print(f"? {bits}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError
    value = int(line.strip())
    if value == -1:
        raise SystemExit(0)
    return value


def solve_case(n: int, r: int, wiring: list[tuple[int, int]]) -> None:
    if n > 12:
        print("! " + "&" * n, flush=True)
        return

    candidates = ["".join(chars) for chars in itertools.product("&|", repeat=n) if chars.count("|") <= r]
    m = 2 * n + 1
    patterns = [format(x, f"0{m}b") for x in range(1 << m)]
    used = 0
    while len(candidates) > 1 and used < 5000:
        chosen = None
        for bits in patterns:
            outputs = {evaluate(g, wiring, bits) for g in candidates}
            if len(outputs) > 1:
                chosen = bits
                break
        if chosen is None:
            break
        response = ask(chosen)
        used += 1
        candidates = [g for g in candidates if evaluate(g, wiring, chosen) == response]
    print("! " + candidates[0], flush=True)


def main() -> int:
    while True:
        header = sys.stdin.readline()
        if not header:
            return 0
        header = header.strip()
        if not header:
            continue
        n, r = map(int, header.split())
        wiring = []
        for _ in range(n):
            line = sys.stdin.readline()
            if not line:
                return 0
            wiring.append(tuple(map(int, line.split())))
        solve_case(n, r, wiring)


if __name__ == "__main__":
    raise SystemExit(main())
