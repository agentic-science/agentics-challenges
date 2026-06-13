from __future__ import annotations

import select
import sys


N = 100


def emit_empty_graph() -> None:
    print("!", flush=True)
    row = "0" * N
    for _ in range(N):
        print(row, flush=True)


def wait_for_next_case() -> bool:
    ready, _, _ = select.select([sys.stdin], [], [], 1.0)
    if not ready:
        return False
    line = sys.stdin.readline()
    if line == "":
        return False
    return line.strip() == "NEXT"


def main() -> int:
    while True:
        emit_empty_graph()
        if not wait_for_next_case():
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
