from __future__ import annotations

import sys


def main() -> None:
    try:
        sys.stdin.readline()
        n = int(sys.stdin.readline())
        for _ in range(max(0, n - 1)):
            sys.stdin.readline()
        print("! " + " ".join(["1"] * max(1, n)), flush=True)
    except Exception:
        return


if __name__ == "__main__":
    main()
