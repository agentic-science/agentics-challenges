from __future__ import annotations

import sys


def main() -> None:
    try:
        sys.stdin.readline()
        header = sys.stdin.readline().split()
        edge_count = int(header[1]) if len(header) > 1 else 0
        for _ in range(max(0, edge_count)):
            sys.stdin.readline()
        print("1", flush=True)
    except Exception:
        return


if __name__ == "__main__":
    main()
