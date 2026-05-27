from __future__ import annotations

import sys

try:
    n = int(sys.stdin.readline())
    print("! " + " ".join(map(str, range(1, max(1, n) + 1))), flush=True)
except Exception:
    pass
