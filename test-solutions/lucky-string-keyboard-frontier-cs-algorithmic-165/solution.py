from __future__ import annotations

import sys


def main() -> int:
    data = sys.stdin.read().split()
    if not data:
        return 0
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    _si = int(data[idx]); idx += 1
    _sj = int(data[idx]); idx += 1
    grid = data[idx:idx + n]; idx += n
    words = data[idx:idx + m]
    first: dict[str, tuple[int, int]] = {}
    fallback = (0, 0)
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            first.setdefault(ch, (r, c))
    out: list[str] = []
    for word in words:
        for ch in word:
            r, c = first.get(ch, fallback)
            out.append(f'{r} {c}')
    sys.stdout.write('\n'.join(out) + ('\n' if out else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
