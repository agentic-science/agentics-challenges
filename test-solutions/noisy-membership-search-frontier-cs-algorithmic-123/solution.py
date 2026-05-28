from __future__ import annotations

import sys


def ask(values: range) -> bool:
    items = " ".join(str(value) for value in values)
    print(f"? {len(values)} {items}", flush=True)
    reply = sys.stdin.readline().strip()
    if reply not in {"YES", "NO"}:
        raise EOFError("interactor closed or sent an invalid reply")
    return reply == "YES"


def reliable_membership(values: range) -> bool:
    replies = [ask(values), ask(values), ask(values)]
    return sum(1 for reply in replies if reply) >= 2


def guess(value: int) -> bool:
    print(f"! {value}", flush=True)
    reply = sys.stdin.readline().strip()
    return reply == ":)"


def solve_case(n: int) -> None:
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if reliable_membership(range(lo, mid + 1)):
            hi = mid
        else:
            lo = mid + 1
    guess(lo)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        solve_case(int(line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
