from __future__ import annotations

import struct
import sys

INPUT_HEADER = struct.Struct("<8sIIII")
OUTPUT_HEADER = struct.Struct("<8sIII")
INPUT_MAGIC = b"AGMMIN1\0"
OUTPUT_MAGIC = b"AGMMOUT1"


def main() -> None:
    data = sys.stdin.buffer.read()
    if len(data) < INPUT_HEADER.size:
        raise SystemExit("truncated matrix input")
    magic, cases, m, k, n = INPUT_HEADER.unpack_from(data, 0)
    if magic != INPUT_MAGIC:
        raise SystemExit("invalid matrix input magic")
    values = struct.unpack_from(f"<{cases * (m * k + k * n)}f", data, INPUT_HEADER.size)
    cursor = 0
    out: list[float] = []
    for _ in range(cases):
        a = values[cursor:cursor + m * k]
        cursor += m * k
        b = values[cursor:cursor + k * n]
        cursor += k * n
        for row in range(m):
            for col in range(n):
                total = 0.0
                for inner in range(k):
                    total += a[row * k + inner] * b[inner * n + col]
                out.append(total)
    sys.stdout.buffer.write(OUTPUT_HEADER.pack(OUTPUT_MAGIC, cases, m, n))
    sys.stdout.buffer.write(struct.pack(f"<{len(out)}f", *out))


if __name__ == "__main__":
    main()
