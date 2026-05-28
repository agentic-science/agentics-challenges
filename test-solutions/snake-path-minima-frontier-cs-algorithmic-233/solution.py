from __future__ import annotations

import sys


def read_line() -> str:
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed")
    stripped = line.strip()
    if stripped == "-1":
        raise SystemExit(0)
    return stripped


def ask(length: int, time_index: int) -> int:
    print(f"? {length} {time_index}", flush=True)
    return int(read_line())


def main() -> int:
    while True:
        try:
            t = int(read_line())
        except EOFError:
            return 0
        for _ in range(t):
            n, m = map(int, read_line().split())
            for _row in range(n):
                read_line()

            values: list[int] = []
            total_pairs = n * (2 * n - 1)
            query_limit = 120 * n + m
            if total_pairs <= query_limit:
                for length in range(1, n + 1):
                    for time_index in range(1, 2 * n):
                        values.append(ask(length, time_index))
            else:
                for length in range(1, n + 1):
                    for time_index in range(1, 2 * n):
                        if len(values) >= query_limit:
                            break
                        values.append(ask(length, time_index))
                    if len(values) >= query_limit:
                        break

            values.sort()
            answer = values[:m]
            if len(answer) < m:
                answer.extend([answer[-1] if answer else 1] * (m - len(answer)))
            print("! " + " ".join(map(str, answer)), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
