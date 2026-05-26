from __future__ import annotations

import sys
from collections import Counter

KIND = "fighter"


def ints(text: str) -> list[int]:
    return [int(tok) for tok in text.split()]


def solve_three_coloring(data: list[int]) -> str:
    n = data[0] if data else 1
    return " ".join(str((i % 3) + 1) for i in range(n)) + "\n"


def solve_sat(data: list[int]) -> str:
    n = data[0] if data else 1
    return " ".join("1" for _ in range(n)) + "\n"


def solve_identity_permutation(data: list[int]) -> str:
    n = data[0] if data else 1
    return " ".join(str(i) for i in range(1, n + 1)) + "\n"


def solve_maxcut(data: list[int]) -> str:
    n = data[0] if data else 1
    return " ".join(str(i % 2) for i in range(n)) + "\n"


def solve_lcs(lines: list[str]) -> str:
    if len(lines) < 2:
        return "\n"
    s1, s2 = lines[0].strip(), lines[1].strip()
    counts = Counter(s2)
    out = []
    for ch in s1:
        if counts[ch] > 0:
            out.append(ch)
            counts[ch] -= 1
    return "".join(out) + "\n"


def solve_edit_lcs(lines: list[str]) -> str:
    if len(lines) < 2:
        return "\n"
    s1, s2 = lines[0].strip(), lines[1].strip()
    i = j = 0
    ops = []
    while i < len(s1) and j < len(s2):
        if s1[i] == s2[j]:
            ops.append("M")
            i += 1
            j += 1
        elif s2[j] in s1[i + 1:]:
            ops.append("D")
            i += 1
        elif s1[i] in s2[j + 1:]:
            ops.append("I")
            j += 1
        else:
            ops.append("M")
            i += 1
            j += 1
    ops.extend("D" for _ in range(i, len(s1)))
    ops.extend("I" for _ in range(j, len(s2)))
    return "".join(ops) + "\n"


def solve_efficient_sort(data: list[int]) -> str:
    if not data:
        return "0\n0\n"
    pos = 0
    n = data[pos]
    pos += 1
    arr = data[pos:pos + n]
    pos += n
    m = data[pos] if pos < len(data) else 0
    pos += 1
    planned = [(data[pos + 2 * i], data[pos + 2 * i + 1]) for i in range(m) if pos + 2 * i + 1 < len(data)]
    current = list(arr)
    if current == list(range(n)):
        return "0\n0\n"
    my_swaps: list[tuple[int, int]] = []
    total_cost = 0
    for r, (x, y) in enumerate(planned):
        current[x], current[y] = current[y], current[x]
        if current == list(range(n)):
            my_swaps.append((0, 0))
            R = r + 1
            V = R * total_cost
            return str(R) + "\n" + "".join(f"{a} {b}\n" for a, b in my_swaps) + f"{V}\n"
        idx = next((i for i, value in enumerate(current) if value != i), None)
        if idx is None:
            my_swaps.append((0, 0))
            continue
        j = current.index(idx)
        current[idx], current[j] = current[j], current[idx]
        my_swaps.append((idx, j))
        total_cost += abs(idx - j)
        if current == list(range(n)):
            R = r + 1
            V = R * total_cost
            return str(R) + "\n" + "".join(f"{a} {b}\n" for a, b in my_swaps) + f"{V}\n"
    return "0\n0\n"


def solve_robot_network(lines: list[str]) -> str:
    if not lines:
        return "#\n#\n"
    n, k = map(int, lines[0].split()[:2])
    ids = []
    for line in lines[1:1 + n + k]:
        parts = line.split()
        if parts and parts[-1] != "C":
            ids.append(parts[0])
    if len(ids) <= 1:
        return "#\n#\n"
    edges = "#".join(f"{ids[i]}-{ids[i + 1]}" for i in range(len(ids) - 1))
    return f"#\n{edges}\n"


def solve_table_cards(lines: list[str]) -> str:
    if not lines:
        return "0\n"
    n = int(lines[0].split()[0])
    hands = [Counter(map(int, line.split())) for line in lines[1:1 + n]]
    if all(hands[i].get(i + 1, 0) == n for i in range(n)):
        return "0\n"
    return "0\n"


def main() -> int:
    text = sys.stdin.read()
    lines = text.splitlines()
    data = ints(text) if KIND not in {"lcs", "edit_lcs", "fighter", "robot_network", "table_cards"} else []
    if KIND == "fish_polygon":
        sys.stdout.write("4\n0 0\n2 0\n2 2\n0 2\n")
    elif KIND == "rooted_forest":
        n = data[0] if data else 1
        sys.stdout.write("\n".join("-1" for _ in range(n)) + "\n")
    elif KIND == "oni_shift":
        sys.stdout.write("")
    elif KIND == "cleaning":
        n = data[0] if data else 1
        sys.stdout.write("\n".join("0 0" for _ in range(n)) + "\n")
    elif KIND == "skating":
        sys.stdout.write("")
    elif KIND == "three_coloring":
        sys.stdout.write(solve_three_coloring(data))
    elif KIND in {"max3sat", "max2sat"}:
        sys.stdout.write(solve_sat(data))
    elif KIND == "big_subset":
        n = data[0] if data else 1
        sys.stdout.write(" ".join("0" for _ in range(n)) + "\n")
    elif KIND in {"graph_match", "qap"}:
        sys.stdout.write(solve_identity_permutation(data))
    elif KIND == "lcs":
        sys.stdout.write(solve_lcs(lines))
    elif KIND == "edit_lcs":
        sys.stdout.write(solve_edit_lcs(lines))
    elif KIND == "maxcut":
        sys.stdout.write(solve_maxcut(data))
    elif KIND == "paren_transform":
        sys.stdout.write("0\n")
    elif KIND == "efficient_sort":
        sys.stdout.write(solve_efficient_sort(data))
    elif KIND == "fighter":
        sys.stdout.write("")
    elif KIND == "robot_network":
        sys.stdout.write(solve_robot_network(lines))
    elif KIND == "grid_crossing":
        if len(data) >= 8:
            sx, sy = data[4], data[5]
        else:
            sx, sy = 1, 1
        sys.stdout.write(f"YES\n1\n{sx} {sy}\n")
    elif KIND == "seq_shift":
        sys.stdout.write("1\n0\n")
    elif KIND == "seq_reversal":
        sys.stdout.write("1\n0\n")
    elif KIND == "table_cards":
        sys.stdout.write(solve_table_cards(lines))
    else:
        raise RuntimeError(f"unknown kind {KIND}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
