from __future__ import annotations

import sys


def read_nonempty() -> str | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        if line.strip():
            return line.strip()


def walk(steps: int) -> int:
    print(f"walk {steps}", flush=True)
    response = read_nonempty()
    if response is None:
        raise EOFError("interactor closed during walk")
    return int(response)


def solve_case() -> bool:
    start_label = walk(0)
    for length in range(1, 200000):
        if walk(1) == start_label:
            print(f"guess {length}", flush=True)
            break
    else:
        print("guess 1", flush=True)

    marker = read_nonempty()
    if marker is None or marker == "0 0":
        return False
    return marker == "NEXT"


def main() -> int:
    while solve_case():
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
