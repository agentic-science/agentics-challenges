from __future__ import annotations

import sys


def first_integer() -> int:
    token: list[str] = []
    while True:
        chunk = sys.stdin.buffer.read(8192)
        if not chunk:
            break
        for byte in chunk:
            char = chr(byte)
            if char.isspace():
                if token:
                    return int("".join(token))
            else:
                token.append(char)
    return int("".join(token)) if token else 1


def main() -> int:
    n = max(1, first_integer())
    sys.stdout.write(" ".join(str(index) for index in range(1, n + 1)))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
