from __future__ import annotations

import sys


def main() -> int:
    tokens = sys.stdin.read().split()
    if not tokens:
        return 0
    n = int(tokens[0]); t = int(tokens[1])
    rows = tokens[2:2 + n]
    bi = bj = 0
    for i, row in enumerate(rows):
        j = row.find('0')
        if j != -1:
            bi, bj = i, j
            break
    pairs = []
    if bj + 1 < n:
        pairs.append('RL')
    if bj > 0:
        pairs.append('LR')
    if bi + 1 < n:
        pairs.append('DU')
    if bi > 0:
        pairs.append('UD')
    if t <= 0 or not pairs:
        sys.stdout.write('\n')
    elif t == 1:
        sys.stdout.write(pairs[0][0] + '\n')
    else:
        sys.stdout.write(pairs[0][:min(2, t)] + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
