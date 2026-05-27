from __future__ import annotations

import itertools
import sys


def response_for(candidate: tuple[int, ...], query_perm: tuple[int, ...], k: int) -> int:
    total = 0
    n = len(candidate)
    for i in range(n):
        if i + 1 == k:
            continue
        for j in range(i + 1, n):
            if candidate[query_perm[i] - 1] == query_perm[j]:
                total += 1
    return total


def ask(query_perm: tuple[int, ...]) -> int:
    print("? " + " ".join(str(value) for value in query_perm), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed before answering a query")
    value = int(line.strip())
    if value == -1:
        raise EOFError("interactor rejected the protocol")
    return value


def derangement_guess(n: int) -> list[int]:
    return list(range(2, n + 1)) + [1]


def solve_case(n: int) -> list[int]:
    k = 1
    print(k, flush=True)
    if n > 7:
        return derangement_guess(n)

    candidates = [
        perm
        for perm in itertools.permutations(range(1, n + 1))
        if all(perm[index] != index + 1 for index in range(n))
    ]
    for query_perm in itertools.permutations(range(1, n + 1)):
        answer = ask(query_perm)
        candidates = [
            candidate
            for candidate in candidates
            if response_for(candidate, query_perm, k) == answer
        ]
        if len(candidates) == 1:
            return list(candidates[0])
    return list(candidates[0]) if candidates else derangement_guess(n)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    t = int(first.strip())
    for _ in range(t):
        line = sys.stdin.readline()
        if not line:
            return 0
        n = int(line.strip())
        guess = solve_case(n)
        print("! " + " ".join(str(value) for value in guess), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
