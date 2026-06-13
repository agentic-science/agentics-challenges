from __future__ import annotations

import math
import sys

RATE_SAMPLES_PER_DECISION = 24
RATE_SAMPLE_BUDGET = 120_000

used_rate_samples = 0


def read_line() -> str | None:
    line = sys.stdin.readline()
    if line == "":
        return None
    line = line.strip()
    if line == "-1":
        raise SystemExit(0)
    return line


def rate(samples: int) -> tuple[float, float]:
    global used_rate_samples

    print(f"RATE {samples}", flush=True)
    line = read_line()
    if line is None:
        raise EOFError("interactor closed during RATE")
    parts = line.split()
    if not parts or parts[0] != "RATES":
        return 0.0, 0.0
    used_rate_samples += samples
    return float(parts[1]), float(parts[2])


def bounded_rate() -> tuple[float, float]:
    remaining = RATE_SAMPLE_BUDGET - used_rate_samples
    if remaining <= 0:
        return 0.0, 0.0
    return rate(min(RATE_SAMPLES_PER_DECISION, remaining))


def choose_action(stack: int, pot: int, win: float, draw: float) -> str:
    if stack <= 0:
        return "ACTION CHECK"
    equity = win + 0.5 * draw
    if equity < 0.54:
        return "ACTION CHECK"
    pressure = pot if equity < 0.67 else 2 * pot
    amount = max(1, min(stack, int(math.ceil(pressure))))
    return f"ACTION RAISE {amount}"


def play_session(first_line: str) -> str | None:
    hands = int(first_line)
    for _hand in range(hands):
        while True:
            line = read_line()
            if line is None or line.startswith("SCORE"):
                return line
            if line.startswith("RESULT"):
                break
            if line.startswith("OPP"):
                continue
            if not line.startswith("STATE "):
                continue

            parts = line.split()
            stack = int(parts[3])
            pot = int(parts[5])
            _alice = read_line()
            _board = read_line()
            if _alice is None or _board is None:
                return None
            win, draw = bounded_rate()
            print(choose_action(stack, pot, win, draw), flush=True)

    return read_line()


def main() -> int:
    line = read_line()
    while line is not None:
        if line.startswith("SCORE"):
            line = read_line()
            continue
        line = play_session(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
