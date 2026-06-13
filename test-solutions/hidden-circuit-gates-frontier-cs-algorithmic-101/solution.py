from __future__ import annotations

from collections import deque
import sys


def ask(bits: list[str]) -> int:
    try:
        print("? " + "".join(bits), flush=True)
    except BrokenPipeError:
        raise SystemExit(0) from None
    line = sys.stdin.readline()
    if not line:
        raise SystemExit(0)
    token = line.strip()
    if token in {"-1", "NEXT", "0 0"}:
        raise SystemExit(0)
    try:
        value = int(token)
    except ValueError:
        raise SystemExit(0) from None
    if value == -1:
        raise SystemExit(0)
    if value not in (0, 1):
        raise SystemExit(0)
    return value


def solve_case(n: int, _r: int, wiring: list[tuple[int, int]]) -> None:
    total_switches = 2 * n + 1
    parent = [-1] * total_switches
    for i, (u, v) in enumerate(wiring):
        parent[u] = i
        parent[v] = i

    subtree_size = [0] * n
    heavy = [-1] * n

    for i in range(n - 1, -1, -1):
        u, v = wiring[i]
        size = 1
        best_child = -1
        best_size = -1
        for child in (u, v):
            if child < n:
                child_size = subtree_size[child]
                size += child_size
                if child_size > best_size:
                    best_size = child_size
                    best_child = child
        subtree_size[i] = size
        heavy[i] = best_child

    gate_type = ["?"] * n

    def side_child(node: int) -> int:
        u, v = wiring[node]
        if heavy[node] == -1:
            return v
        return v if u == heavy[node] else u

    def apply_known_ancestors(head: int, bits: list[str]) -> None:
        current = head
        while parent[current] != -1:
            p = parent[current]
            u, v = wiring[p]
            sibling = v if u == current else u
            if gate_type[p] == "&":
                bits[sibling] = "1"
            current = p

    def path_from(head: int) -> list[int]:
        path: list[int] = []
        current = head
        while current != -1 and current < n:
            path.append(current)
            current = heavy[current]
        return path

    def segment_has_or(path: list[int], left: int, right: int) -> bool:
        bits = ["0"] * total_switches
        apply_known_ancestors(path[0], bits)

        for index in range(left):
            node = path[index]
            if gate_type[node] == "&":
                bits[side_child(node)] = "1"

        for index in range(left, right + 1):
            bits[side_child(path[index])] = "1"

        return ask(bits) == 1

    queue: deque[int] = deque([0])
    seen_heads: set[int] = set()

    while queue:
        head = queue.popleft()
        if head in seen_heads or head >= n:
            continue
        seen_heads.add(head)

        path = path_from(head)
        pos = 0
        while pos < len(path):
            if not segment_has_or(path, pos, len(path) - 1):
                for index in range(pos, len(path)):
                    gate_type[path[index]] = "&"
                break

            lo, hi = pos, len(path) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if segment_has_or(path, pos, mid):
                    hi = mid
                else:
                    lo = mid + 1

            for index in range(pos, lo):
                gate_type[path[index]] = "&"
            gate_type[path[lo]] = "|"
            pos = lo + 1

        for node in path:
            u, v = wiring[node]
            for child in (u, v):
                if child < n and child != heavy[node]:
                    queue.append(child)

    for i, value in enumerate(gate_type):
        if value == "?":
            gate_type[i] = "&"
    try:
        print("! " + "".join(gate_type), flush=True)
    except BrokenPipeError:
        raise SystemExit(0) from None


def main() -> int:
    while True:
        header = sys.stdin.readline()
        if not header:
            return 0
        header = header.strip()
        if not header:
            continue
        if header in {"-1", "0 0"}:
            return 0
        if header == "NEXT":
            continue
        parts = header.split()
        if len(parts) != 2:
            return 0
        try:
            n, r = map(int, parts)
        except ValueError:
            return 0
        wiring = []
        for _ in range(n):
            line = sys.stdin.readline()
            if not line:
                return 0
            try:
                u, v = map(int, line.split())
            except ValueError:
                return 0
            wiring.append((u, v))
        solve_case(n, r, wiring)


if __name__ == "__main__":
    raise SystemExit(main())
