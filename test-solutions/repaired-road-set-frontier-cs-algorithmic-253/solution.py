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


def query(vertices: list[int]) -> int:
    print("? " + str(len(vertices)) + " " + " ".join(map(str, vertices)), flush=True)
    return int(read_line())


def main() -> int:
    while True:
        try:
            t = int(read_line())
        except EOFError:
            return 0
        for _ in range(t):
            n, m = map(int, read_line().split())
            edges = [tuple(map(int, read_line().split())) for _ in range(m)]

            for road in range(1, m + 1):
                print(f"- {road}", flush=True)

            repaired: list[int] = []
            for road, (_a, b) in enumerate(edges, start=1):
                print(f"+ {road}", flush=True)
                witnesses = [node for node in range(1, n + 1) if node != b]
                repaired.append(query(witnesses))
                print(f"- {road}", flush=True)

            print("! " + " ".join(map(str, repaired)), flush=True)
            verdict = read_line()
            if verdict != "1":
                return 0


if __name__ == "__main__":
    raise SystemExit(main())
