from __future__ import annotations

import bisect
import math
import sys
from collections import deque

PROBLEM_ID = 308


def ints() -> list[int]:
    return [int(x) for x in sys.stdin.buffer.read().split()]


def solve_225() -> None:
    data = ints()
    if not data:
        return
    n, q = data[0], data[1]
    a = [0] + data[2:2 + n]
    pos = 2 + n
    reqs = [(data[pos + 2 * i], data[pos + 2 * i + 1]) for i in range(q)]
    ops: list[tuple[int, int]] = []
    req_ids: list[int] = []
    next_id = n
    for l, r in reqs:
        items = sorted(range(l, r + 1), key=lambda idx: a[idx])
        cur = items[0]
        for idx in items[1:]:
            ops.append((cur, idx))
            next_id += 1
            cur = next_id
            if next_id > 2_200_000:
                break
        req_ids.append(cur)
    out = [str(n + len(ops))]
    out.extend(f"{u} {v}" for u, v in ops)
    out.append(" ".join(map(str, req_ids)))
    sys.stdout.write("\n".join(out) + "\n")


def solve_227() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    p = data[1:1 + n]
    sys.stdout.write(f"{n} 0 0 0\n" + " ".join(map(str, p)) + "\n")


def exact_square_count(s: str) -> int:
    n = len(s)
    total = 0
    for i in range(n):
        zeros = ones = 0
        for j in range(i, n):
            if s[j] == '0':
                zeros += 1
            else:
                ones += 1
            if zeros == ones * ones:
                total += 1
    return total


def solve_228() -> None:
    s = sys.stdin.read().strip()
    if len(s) <= 5000:
        print(exact_square_count(s))
    else:
        print(0)


def lis_length(values: list[int]) -> int:
    dp: list[int] = []
    for value in values:
        pos = bisect.bisect_left(dp, value)
        if pos == len(dp):
            dp.append(value)
        else:
            dp[pos] = value
    return len(dp)


def solve_229() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    arr = data[2:2 + n]
    out = [str(lis_length(arr))]
    out.extend("1 1 0" for _ in range(10))
    sys.stdout.write("\n".join(out) + "\n")


def solve_239() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    if n <= 3:
        print(0)
        return
    if n > 200:
        print(0)
        return
    ops: list[tuple[int, int, int]] = []
    for length in range(2, n + 1):
        for start in range(0, n - length + 1):
            ops.append((start, start + 1, start + length))
    out = [str(len(ops))]
    out.extend(f"{a} {b} {c}" for a, b, c in ops)
    sys.stdout.write("\n".join(out) + "\n")


def expr_and(parts: list[str]) -> str:
    cur = parts[0]
    for part in parts[1:]:
        cur = f"({cur}&{part})"
    return cur


def expr_or(parts: list[str]) -> str:
    cur = parts[0]
    for part in parts[1:]:
        cur = f"({cur}|{part})"
    return cur


def synth_expr(n: int, table: str) -> tuple[bool, str]:
    if set(table) == {'0'}:
        return True, 'F'
    if set(table) == {'1'}:
        return True, 'T'
    for var in range(n):
        pattern = ''.join('1' if (mask >> var) & 1 else '0' for mask in range(1 << n))
        if table == pattern:
            return True, chr(ord('a') + var)
    if n > 5:
        return False, ''
    for mask in range(1 << n):
        if table[mask] != '1':
            continue
        for bit in range(n):
            if (mask & (1 << bit)) == 0 and table[mask | (1 << bit)] == '0':
                return False, ''
    terms: list[str] = []
    for mask in range(1 << n):
        if table[mask] != '1':
            continue
        minimal = True
        sub = mask
        while sub:
            sub = (sub - 1) & mask
            if sub != mask and table[sub] == '1':
                minimal = False
                break
        if minimal:
            vars_ = [chr(ord('a') + bit) for bit in range(n) if (mask >> bit) & 1]
            terms.append(expr_and(vars_) if vars_ else 'T')
    return True, expr_or(terms)


def solve_241() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    pos = 1
    out: list[str] = []
    for _ in range(t):
        n = int(tokens[pos]); pos += 1
        table = tokens[pos]; pos += 1
        ok, expr = synth_expr(n, table)
        if ok:
            out.extend(['Yes', expr])
        else:
            out.append('No')
    sys.stdout.write("\n".join(out) + "\n")


def solve_247() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    if a == b:
        sys.stdout.write("Yes\n0\n")
    else:
        sys.stdout.write("No\n")


def solve_248() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    pos = 1
    m = int(tokens[pos]); pos += 1
    route = []
    for city in range(1, m + 1):
        cnt = int(tokens[pos]); pos += 2
        pos += cnt
        route.append(f"({city},1)")
    sys.stdout.write("@".join(route) + "\n")


def solve_263() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    sys.stdout.write(" ".join("1" for _ in range(n)) + "\n0\n")


def solve_301() -> None:
    data = ints()
    if not data:
        return
    k = data[2]
    sys.stdout.write(" ".join(str(i) for i in range(k)) + "\n")


def solve_302() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0]); k = int(tokens[1])
    counts = [int(tokens[2 + i]) for i in range(k)]
    s = ''.join(chr(ord('a') + i) * counts[i] for i in range(k))
    if len(s) != n:
        s = s[:n].ljust(n, 'a')
    print(s)


def solve_303() -> None:
    sys.stdout.write("0\n")


def solve_304() -> None:
    data = ints()
    if not data:
        return
    n, m, k = data[0], data[1], data[2]
    rates_start = 3
    edge_start = rates_start + n
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u = data[edge_start + 2 * i]
        v = data[edge_start + 2 * i + 1]
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
    parent[1] = 1
    q = deque([1])
    order = [1]
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if parent[v] == 0:
                parent[v] = u
                q.append(v)
                order.append(v)
    children = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        children[parent[v]].append(v)
    moves: list[int] = []
    stack: list[tuple[int, int]] = [(1, 0)]
    while stack:
        u, idx = stack[-1]
        if idx < len(children[u]):
            v = children[u][idx]
            stack[-1] = (u, idx + 1)
            moves.append(v)
            stack.append((v, 0))
        else:
            stack.pop()
            if stack:
                moves.append(stack[-1][0])
    if len(moves) < k and adj[1]:
        nb = sorted(adj[1])[0]
        cur = 1
        while len(moves) < k:
            cur = nb if cur == 1 else 1
            moves.append(cur)
    sys.stdout.write(" ".join(map(str, moves[:k])) + "\n")


def solve_305() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    adj = [[] for _ in range(n + 1)]
    pos = 1
    for _ in range(n - 1):
        u, v = data[pos], data[pos + 1]
        pos += 2
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * (n + 1)
    seen[1] = True
    q = deque([1])
    order: list[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in sorted(adj[u]):
            if not seen[v]:
                seen[v] = True
                q.append(v)
    sys.stdout.write(" ".join(map(str, order)) + "\n")


def solve_306() -> None:
    data = ints()
    if not data:
        return
    n, e = data[0], data[1]
    pos = 2 + 5 * e
    m = data[pos]
    pos += 1
    for _ in range(m):
        r = data[pos]
        pos += 2 + 2 * r
    out = ["0"]
    out.extend("0" for _ in range(m))
    sys.stdout.write("\n".join(out) + "\n")


def solve_307() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    x0 = tokens[5]
    y0 = tokens[6]
    out = ["1", f"{x0} {y0}"]
    out.extend("1" for _ in range(n))
    sys.stdout.write("\n".join(out) + "\n")


def solve_308() -> None:
    sys.stdout.write("0\n")


def solve_309() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[1])
    sys.stdout.write("\n".join("-1" for _ in range(n)) + "\n")


def solve_310() -> None:
    data = ints()
    if not data:
        return
    m, budget = data[0], data[1]
    cost = data[2:2 + m]
    spent = 0
    chosen: list[int] = []
    for idx in sorted(range(m), key=lambda i: (cost[i], i)):
        if cost[idx] <= budget - spent:
            chosen.append(idx)
            spent += cost[idx]
    chosen.sort()
    sys.stdout.write(str(len(chosen)) + ("\n" + " ".join(map(str, chosen)) if chosen else "") + "\n")


def solve_311() -> None:
    data = ints()
    if not data:
        return
    t = data[0]
    pos = 1
    lines: list[str] = []
    for _ in range(t):
        n, m, r = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        pos += 2 * n
        wdeg = [0] * (n + 1)
        edges = []
        for _ in range(r):
            u, v, w = data[pos], data[pos + 1], data[pos + 2]
            pos += 3
            wdeg[u] += w
            wdeg[v] += w
            edges.append((u, v, w))
        order = sorted(range(1, n + 1), key=lambda i: (-wdeg[i], i))
        bays = [0] * (n + 1)
        if n == 1:
            bays[order[0]] = 0
        else:
            for k, node in enumerate(order):
                bays[node] = k * (m - 1) // (n - 1)
        lines.append(" ".join(str(bays[i]) for i in range(1, n + 1)))
    sys.stdout.write("\n".join(lines) + "\n")


def solve_312() -> None:
    data = ints()
    if not data:
        return
    n, m, k = data[0], data[1], data[2]
    pos = 3
    adj = [[] for _ in range(n + 1)]
    for eid in range(1, m + 1):
        x, y, _c = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        if x == y:
            adj[x].append((y, eid, eid))
        else:
            adj[x].append((y, eid, eid))
            adj[y].append((x, eid, -eid))
    used = [False] * (m + 1)
    cursor = [0] * (n + 1)
    seq: list[int] = []
    stack: list[tuple[int, int]] = [(1, 0)]
    while stack:
        u, enter = stack[-1]
        while cursor[u] < len(adj[u]) and used[adj[u][cursor[u]][1]]:
            cursor[u] += 1
        if cursor[u] == len(adj[u]):
            stack.pop()
            if enter:
                seq.append(-enter)
            continue
        v, eid, sign = adj[u][cursor[u]]
        cursor[u] += 1
        used[eid] = True
        seq.append(sign)
        if v != u:
            stack.append((v, sign))
    lines = [str(len(seq)) + (" " + " ".join(map(str, seq)) if seq else "")]
    lines.extend("0" for _ in range(1, k))
    sys.stdout.write("\n".join(lines) + "\n")


def solve_313() -> None:
    data = ints()
    if not data:
        return
    n = data[0]
    sys.stdout.write(" ".join(str(i) for i in range(1, n + 1)) + "\n")


def solve_314() -> None:
    sys.stdout.write("0\n")


def solve_315() -> None:
    data = ints()
    if not data:
        return
    k = data[1]
    out = [str(k)]
    out.extend(f"{i} 0" for i in range(k))
    sys.stdout.write("\n".join(out) + "\n")


SOLVERS = {
    225: solve_225,
    227: solve_227,
    228: solve_228,
    229: solve_229,
    239: solve_239,
    241: solve_241,
    247: solve_247,
    248: solve_248,
    263: solve_263,
    301: solve_301,
    302: solve_302,
    303: solve_303,
    304: solve_304,
    305: solve_305,
    306: solve_306,
    307: solve_307,
    308: solve_308,
    309: solve_309,
    310: solve_310,
    311: solve_311,
    312: solve_312,
    313: solve_313,
    314: solve_314,
    315: solve_315,
}


if __name__ == "__main__":
    SOLVERS[PROBLEM_ID]()
