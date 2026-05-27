from __future__ import annotations

import sys

try:
    m = int(sys.stdin.readline())
    print(f"0 left {0 if m <= 0 else 0 % m}", flush=True)
except Exception:
    pass
