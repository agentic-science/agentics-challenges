from __future__ import annotations

import sys


def force(left: list[int], right: list[int]) -> int:
    print(f"? {len(left)} {len(right)}", flush=True)
    print(" ".join(map(str, left)), flush=True)
    print(" ".join(map(str, right)), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during magnet query")
    return int(line.strip())


def solve_case(n: int) -> None:
    anchor = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if force([i], [j]) != 0:
                anchor = i
                break
        if anchor:
            break

    if not anchor:
        print("! 0", flush=True)
        return

    demagnetized: list[int] = []
    for idx in range(1, n + 1):
        if idx == anchor:
            continue
        if force([anchor], [idx]) == 0:
            demagnetized.append(idx)

    suffix = " " + " ".join(map(str, demagnetized)) if demagnetized else ""
    print("! " + str(len(demagnetized)) + suffix, flush=True)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    test_count = int(first.strip())
    if test_count <= 0:
        return 0
    for _ in range(test_count):
        line = sys.stdin.readline()
        if not line:
            return 0
        solve_case(int(line.strip()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
