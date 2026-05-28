from __future__ import annotations

import sys


def ask(indices: tuple[int, ...]) -> tuple[int, int]:
    print("0 " + str(len(indices)) + " " + " ".join(map(str, indices)), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed while answering a query")
    left, right = map(int, line.split())
    return left, right


def scan_with_pivot(n: int, pivot: int) -> dict[tuple[int, int], list[int]]:
    buckets: dict[tuple[int, int], list[int]] = {}
    all_indices = tuple(range(1, n + 1))
    for index in all_indices:
        if index == pivot:
            continue
        query = tuple(value for value in all_indices if value not in (pivot, index))
        response = ask(query)
        buckets.setdefault(response, []).append(index)
    return buckets


def solve_by_pair_exclusion(n: int) -> tuple[int, int]:
    low_median = n // 2
    high_median = low_median + 1

    pivot = 1
    buckets = scan_with_pivot(n, pivot)

    both_medians_removed = buckets.get((low_median - 1, high_median + 1))
    if both_medians_removed:
        return pivot, both_medians_removed[0]

    high_median_bucket = buckets.get((low_median, high_median + 1))
    low_median_bucket = buckets.get((low_median - 1, high_median))

    if high_median_bucket:
        high_median_index = high_median_bucket[0]
        high_candidates = buckets.get((low_median, high_median), [])
        if high_candidates:
            second = scan_with_pivot(n, high_candidates[0])
            low_candidates = second.get((low_median - 1, high_median + 1), [])
            if low_candidates:
                return low_candidates[0], high_median_index
            low_candidates = second.get((low_median - 1, high_median), [])
            if low_candidates:
                return low_candidates[0], high_median_index
        return pivot, high_median_index

    if low_median_bucket:
        low_median_index = low_median_bucket[0]
        low_candidates = buckets.get((low_median, high_median), [])
        if low_candidates:
            second = scan_with_pivot(n, low_candidates[0])
            high_candidates = second.get((low_median, high_median + 1), [])
            if high_candidates:
                return low_median_index, high_candidates[0]
            high_candidates = second.get((low_median - 1, high_median + 1), [])
            if high_candidates:
                return low_median_index, high_candidates[0]
        return low_median_index, pivot

    return 1, 2


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
            continue
        n = int(line)
        if n >= 6 and n % 2 == 0:
            answer = solve_by_pair_exclusion(n)
        else:
            answer = (1, 2)
        print(f"1 {answer[0]} {answer[1]}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
