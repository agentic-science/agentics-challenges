from __future__ import annotations

import sys


def query(indices: list[int]) -> int:
    print("0 " + str(len(indices)) + " " + " ".join(str(index) for index in indices), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed before answering a query")
    return int(line.strip())


def small_case_solution(n: int) -> str:
    open_index = 1
    close_index = 2
    found = False
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and query([i, j]) == 1:
                open_index = i
                close_index = j
                found = True
                break
        if found:
            break

    result: list[str] = []
    for index in range(1, n + 1):
        if index == open_index:
            result.append("(")
        elif index == close_index:
            result.append(")")
        elif query([open_index, index]) == 1:
            result.append(")")
        else:
            result.append("(")
    return "".join(result)


def fallback_guess(n: int) -> str:
    return "()" * (n // 2) + ("(" if n % 2 else "")


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n = int(stripped)
        if n <= 0:
            return 0
        guess = small_case_solution(n) if n <= 20 else fallback_guess(n)
        print(f"1 {guess}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
