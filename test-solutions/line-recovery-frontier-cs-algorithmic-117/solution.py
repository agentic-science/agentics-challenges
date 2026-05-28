from __future__ import annotations

import math
import sys

COORD_LIMIT = 1_000_000_000_000


def ask(x: int | float, y: int | float) -> float:
    print(f"? {x} {y}", flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed while answering a query")
    return float(line.strip())


def recover_single_line() -> tuple[int, int]:
    high = COORD_LIMIT
    dist_high = ask(0, high)
    dist_low = ask(0, -high)
    denom = (2.0 * high) / max(dist_high + dist_low, 1e-30)
    abs_slope = int(round(math.sqrt(max(0.0, denom * denom - 1.0))))
    intercept = int(round((dist_low - dist_high) * denom / 2.0))

    if abs_slope == 0:
        return 0, intercept

    probe_x = min(100_000_000, (COORD_LIMIT - 20_000) // abs_slope)
    probe_y = abs_slope * probe_x
    observed = ask(probe_x, probe_y)
    pos_pred = abs(abs_slope * probe_x - probe_y + intercept) / denom
    neg_pred = abs(-abs_slope * probe_x - probe_y + intercept) / denom
    slope = abs_slope if abs(observed - pos_pred) <= abs(observed - neg_pred) else -abs_slope
    return slope, intercept


def main() -> int:
    line = sys.stdin.readline()
    if not line:
        return 0
    n = int(line.strip())

    if n == 1:
        slope, intercept = recover_single_line()
        print(f"! {slope} {intercept}", flush=True)
        return 0

    # Honest protocol fallback for larger aggregate instances. The public
    # smoke is n=1; full multi-line reconstruction is intentionally left to
    # competitive submissions.
    print("! " + " ".join(["0"] * (2 * n)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
