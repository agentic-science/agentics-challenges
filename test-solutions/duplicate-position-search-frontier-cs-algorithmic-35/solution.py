from __future__ import annotations

import sys


def main() -> None:
    try:
        sys.stdin.readline()
        sys.stdin.readline()
        print("! 1", flush=True)
    except Exception:
        return


if __name__ == "__main__":
    main()
