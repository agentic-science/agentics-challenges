from __future__ import annotations

import random
import sys

try:
    m = int(sys.stdin.readline())
    rng = random.Random(80)
    while True:
        state = sys.stdin.readline().strip()
        if state in {"treasure", ""}:
            break
        print(f"{rng.randrange(max(1, m))} left {rng.randrange(max(1, m))}", flush=True)
except Exception:
    pass
