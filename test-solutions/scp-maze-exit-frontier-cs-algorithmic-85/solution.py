from __future__ import annotations

import sys


def do_query() -> int:
    print("query", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed before answering query")
    return int(line.strip())


def do_move(color: int) -> int:
    print(f"move {color}", flush=True)
    line = sys.stdin.readline()
    if line == "":
        raise EOFError("interactor closed before answering move")
    return int(line.strip())


def solve_case(initial_deep: int) -> None:
    distance = do_query()
    if distance <= 0:
        return
    previous_exit_color: int | None = None

    while distance > 0:
        colors = range(3) if previous_exit_color is None else (color for color in range(3) if color != previous_exit_color)
        for color in colors:
            reached = do_move(color)
            if reached == 1:
                return
            new_distance = do_query()
            if new_distance < distance:
                distance = new_distance
                previous_exit_color = color
                break
            back = do_move(color)
            if back == 1:
                return
        else:
            return
    _ = initial_deep


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        initial_deep = int(stripped)
        if initial_deep == 0:
            return 0
        solve_case(initial_deep)


if __name__ == "__main__":
    raise SystemExit(main())
