from __future__ import annotations

import sys


def main() -> int:
    line = sys.stdin.readline()
    if line == "":
        return 0
    m = int(line.strip())
    advance = 1 if m > 1 else 0

    while True:
        state = sys.stdin.readline()
        if state == "":
            return 0
        marker = state.strip()
        if marker == "treasure":
            return 0

        # Take the passage currently marked for this chamber, then advance the
        # marker by one. This implements a per-chamber rotor walk.
        print(f"{advance} left 0", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
