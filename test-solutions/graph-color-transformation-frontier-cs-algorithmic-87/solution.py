from __future__ import annotations

from collections import deque
import sys


def main() -> int:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    initial = [int(next(it)) for _ in range(n)]
    target = [int(next(it)) for _ in range(n)]
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it)) - 1; v = int(next(it)) - 1
        adj[u].append(v); adj[v].append(u)
    inf = 10**9
    dist = [[inf] * n for _ in range(2)]
    for color in (0, 1):
        q = deque()
        for i, value in enumerate(initial):
            if value == color:
                dist[color][i] = 0
                q.append(i)
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[color][v] == inf:
                    dist[color][v] = dist[color][u] + 1
                    q.append(v)
    max_steps = max(dist[target[i]][i] for i in range(n))
    if max_steps >= inf:
        max_steps = 0
    states = []
    current = initial[:]
    states.append(current[:])
    for step in range(1, max_steps + 1):
        nxt = current[:]
        for i in range(n):
            if nxt[i] != target[i] and dist[target[i]][i] <= step:
                nxt[i] = target[i]
        states.append(nxt)
        current = nxt
    out = [str(len(states) - 1)]
    out.extend(' '.join(map(str, state)) for state in states)
    sys.stdout.write('\n'.join(out) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
