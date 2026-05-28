from __future__ import annotations

import sys


def ask(index: int) -> bool:
    print(f"? {index}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed during bakery query")
    return line.strip().upper().startswith("Y")


def reset() -> None:
    print("R", flush=True)


def solve_case(n: int, k: int) -> None:
    if n == 1:
        print("! 1", flush=True)
        return

    if k >= n:
        distinct = 0
        for idx in range(1, n + 1):
            if not ask(idx):
                distinct += 1
        print(f"! {distinct}", flush=True)
        return

    block_size = max(1, k // 2)
    groups: list[list[int]] = []

    for start in range(1, n + 1, block_size):
        reset()
        reps: list[int] = []
        for idx in range(start, min(n, start + block_size - 1) + 1):
            if not ask(idx):
                reps.append(idx)
        groups.append(reps)

    while len(groups) > 1:
        merged_round: list[list[int]] = []
        for pos in range(0, len(groups), 2):
            if pos + 1 >= len(groups):
                merged_round.append(groups[pos])
                continue

            left = groups[pos]
            right = groups[pos + 1]
            merged = list(left)
            matched = [False] * len(right)

            if k == 1:
                for ridx, candidate in enumerate(right):
                    for rep in left:
                        reset()
                        ask(rep)
                        if ask(candidate):
                            matched[ridx] = True
                            break
            else:
                chunk = max(1, min(len(left), k // 2))
                remaining = list(range(len(right)))
                for offset in range(0, len(left), chunk):
                    current_left = left[offset : offset + chunk]
                    capacity = max(1, k - len(current_left))
                    for scan in range(0, len(remaining), capacity):
                        reset()
                        for rep in current_left:
                            ask(rep)
                        for ridx in remaining[scan : scan + capacity]:
                            if not matched[ridx] and ask(right[ridx]):
                                matched[ridx] = True
                    remaining = [ridx for ridx in remaining if not matched[ridx]]
                    if not remaining:
                        break

            for ridx, candidate in enumerate(right):
                if not matched[ridx]:
                    merged.append(candidate)
            merged_round.append(merged)
        groups = merged_round

    distinct = len(groups[0]) if groups else 0
    print(f"! {distinct}", flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        parts = line.split()
        if not parts:
            continue
        if len(parts) == 1 and parts[0] == "0":
            return 0
        if len(parts) >= 2:
            n, k = map(int, parts[:2])
        else:
            more = sys.stdin.readline()
            if not more:
                return 0
            n, k = int(parts[0]), int(more.strip())
        solve_case(n, k)


if __name__ == "__main__":
    raise SystemExit(main())
