from __future__ import annotations

import json
import sys


MAX_MASS_MG = 20_000_000
MAX_VOLUME_UL = 25_000_000


def item_score(entry: tuple[str, list[int]]) -> tuple[float, int, str]:
    name, values = entry
    quantity_limit, value, mass_mg, volume_ul = values
    resource_cost = (mass_mg / MAX_MASS_MG) + (volume_ul / MAX_VOLUME_UL)
    return (value / resource_cost, value * quantity_limit, name)


def main() -> int:
    items = json.load(sys.stdin)
    counts = {name: 0 for name in items}
    remaining_mass = MAX_MASS_MG
    remaining_volume = MAX_VOLUME_UL

    for name, values in sorted(items.items(), key=item_score, reverse=True):
        quantity_limit, _value, mass_mg, volume_ul = values
        by_mass = remaining_mass // mass_mg
        by_volume = remaining_volume // volume_ul
        count = int(min(quantity_limit, by_mass, by_volume))
        if count <= 0:
            continue
        counts[name] = count
        remaining_mass -= count * mass_mg
        remaining_volume -= count * volume_ul

    json.dump(counts, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
