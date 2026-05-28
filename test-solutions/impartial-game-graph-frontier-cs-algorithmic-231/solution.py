from __future__ import annotations

from collections import Counter, defaultdict, deque
import sys


BASIS_SIZE = 56


def read_nonempty() -> str | None:
    while True:
        line = sys.stdin.readline()
        if line == "":
            return None
        stripped = line.strip()
        if stripped:
            return stripped


def compute_game(n: int, edges: set[tuple[int, int]]) -> tuple[list[list[int]], list[int], list[int]]:
    adj = [[] for _ in range(n + 1)]
    outdeg = [0] * (n + 1)
    for u, v in edges:
        adj[u].append(v)
        outdeg[u] += 1

    state = [-1] * (n + 1)
    for node in range(1, n + 1):
        if any(child == node for child in adj[node]):
            state[node] = 2

    radj = [[] for _ in range(n + 1)]
    undecided = [0] * (n + 1)
    queue: deque[int] = deque()
    for node in range(1, n + 1):
        if state[node] != 2 and outdeg[node] == 0:
            state[node] = 0
            queue.append(node)

    for node in range(1, n + 1):
        for child in adj[node]:
            if child == node:
                continue
            radj[child].append(node)
            if state[child] != 2:
                undecided[node] += 1

    while queue:
        node = queue.popleft()
        for parent in radj[node]:
            if state[parent] != -1:
                continue
            if state[node] == 0:
                state[parent] = 1
                queue.append(parent)
            elif state[node] == 1:
                undecided[parent] -= 1
                if undecided[parent] == 0:
                    state[parent] = 0
                    queue.append(parent)

    for node in range(1, n + 1):
        if state[node] != -1:
            continue
        all_draw = True
        for child in adj[node]:
            if child != node and state[child] not in (2, -1):
                all_draw = False
                break
        if all_draw and outdeg[node] > 0:
            state[node] = 2
        elif undecided[node] == 0 and outdeg[node] > 0:
            state[node] = 2
        else:
            state[node] = 0

    nimber = [-1] * (n + 1)
    non_draw_out = [0] * (n + 1)
    queue.clear()
    for node in range(1, n + 1):
        if state[node] == 2:
            continue
        for child in adj[node]:
            if state[child] != 2:
                non_draw_out[node] += 1
    for node in range(1, n + 1):
        if state[node] != 2 and non_draw_out[node] == 0:
            nimber[node] = 0
            queue.append(node)

    while queue:
        child = queue.popleft()
        for node in radj[child]:
            if state[node] == 2:
                continue
            non_draw_out[node] -= 1
            if non_draw_out[node] != 0 or nimber[node] != -1:
                continue
            seen = {
                nimber[next_node]
                for next_node in adj[node]
                if state[next_node] != 2 and nimber[next_node] >= 0
            }
            mex = 0
            while mex in seen:
                mex += 1
            nimber[node] = mex
            queue.append(node)

    for node in range(1, n + 1):
        if state[node] != 2 and nimber[node] == -1:
            nimber[node] = 0
    return adj, state, nimber


def game_result(tokens: list[int], adj: list[list[int]], state: list[int], nimber: list[int]) -> str:
    if not tokens:
        return "Lose"

    draw_tokens = [node for node in tokens if state[node] == 2]
    xor_value = 0
    for node in tokens:
        if state[node] != 2 and nimber[node] >= 0:
            xor_value ^= nimber[node]

    if not draw_tokens:
        return "Lose" if xor_value == 0 else "Win"

    for draw in draw_tokens:
        for child in adj[draw]:
            if child == draw or state[child] == 2:
                continue
            if nimber[child] >= 0 and (xor_value ^ nimber[child]) == 0:
                return "Win"
    return "Draw"


def choose_basis(n: int, edges: set[tuple[int, int]]) -> list[int]:
    indegree = Counter(v for _, v in edges)
    outdegree = Counter(u for u, _ in edges)
    root = min(range(1, n + 1), key=lambda node: (outdegree[node], -indegree[node], node))
    size = min(BASIS_SIZE, n)
    candidates = sorted(
        ((indegree[node], node) for node in range(1, n + 1) if node != root)
    )
    return [root] + [node for _, node in candidates[-(size - 1) :]]


def build_modified_graph(n: int, edges: set[tuple[int, int]], basis: list[int]) -> tuple[set[tuple[int, int]], list[tuple[str, int, int]]]:
    basis_set = set(basis)
    position = {node: index for index, node in enumerate(basis)}
    modified = set(edges)
    operations: list[tuple[str, int, int]] = []

    def add_edge(u: int, v: int) -> None:
        if (u, v) not in modified:
            modified.add((u, v))
            operations.append(("+", u, v))

    def remove_edge(u: int, v: int) -> None:
        if (u, v) in modified:
            modified.remove((u, v))
            operations.append(("-", u, v))

    for node in range(1, n + 1):
        if node not in basis_set:
            add_edge(node, node)

    root = basis[0]
    for u, v in list(modified):
        if u == root:
            remove_edge(u, v)

    for node in basis[1:]:
        for other in basis:
            if other == node or position[other] > position[node]:
                remove_edge(node, other)
            elif position[other] < position[node]:
                add_edge(node, other)

    return modified, operations


def query(tokens: list[int]) -> str:
    if tokens:
        print("? " + str(len(tokens)) + " " + " ".join(map(str, tokens)), flush=True)
    else:
        print("? 0", flush=True)
    line = read_nonempty()
    if line is None:
        raise EOFError("interactor closed during a round")
    return line


def solve_case(n: int, m: int, rounds: int) -> bool:
    edges: set[tuple[int, int]] = set()
    for _ in range(m):
        line = read_nonempty()
        if line is None:
            return False
        u, v = map(int, line.split())
        edges.add((u, v))

    basis = choose_basis(n, edges)
    modified_edges, operations = build_modified_graph(n, edges, basis)
    adj, state, nimber = compute_game(n, modified_edges)

    nimber_token: dict[int, int] = {}
    for node in range(1, n + 1):
        if state[node] != 2 and nimber[node] >= 0:
            nimber_token.setdefault(nimber[node], node)
    query_plan = sorted(nimber_token)
    query_tokens = {value: ([] if value == 0 else [nimber_token[value]]) for value in query_plan}
    outcome = {
        value: {
            vertex: game_result(query_tokens[value] + [vertex], adj, state, nimber)
            for vertex in range(1, n + 1)
        }
        for value in query_plan
    }

    print(len(operations), flush=True)
    for op, u, v in operations:
        print(f"{op} {u} {v}", flush=True)

    all_vertices = set(range(1, n + 1))
    for _ in range(rounds):
        possible = set(all_vertices)
        for value in query_plan:
            if len(possible) == 1:
                break
            tokens = query_tokens[value]
            answer = query(tokens)
            answers = outcome[value]
            possible = {vertex for vertex in possible if answers[vertex] == answer}
        guess = min(possible) if possible else 1
        print(f"! {guess}", flush=True)
        verdict = read_nonempty()
        if verdict != "Correct":
            return False
    return True


def main() -> int:
    while True:
        header = read_nonempty()
        if header is None:
            return 0
        n, m, rounds = map(int, header.split())
        if not solve_case(n, m, rounds):
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
