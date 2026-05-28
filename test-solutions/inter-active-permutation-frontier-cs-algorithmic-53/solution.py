from __future__ import annotations

from collections import defaultdict
import random
import sys


BITS = 8
CODE_SEED = 20260528


def ask(order: list[int]) -> int:
    print("? " + " ".join(map(str, order)), flush=True)
    line = sys.stdin.readline()
    if not line:
        raise EOFError("interactor closed before answering a query")
    value = int(line.strip())
    if value == -1:
        raise EOFError("interactor rejected the protocol")
    return value


def make_codes(n: int) -> list[tuple[int, ...]]:
    rng = random.Random(CODE_SEED)
    values = rng.sample(range(1 << BITS), n)
    return [()] + [tuple((value >> bit) & 1 for bit in range(BITS)) for value in values]


def measure_constraints(n: int, codes: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    signatures: list[tuple[int, ...]] = [()]
    labels = list(range(1, n + 1))
    for source in labels:
        signature: list[int] = []
        for bit in range(BITS):
            before = [value for value in labels if value != source and codes[value][bit] == 0]
            after = [value for value in labels if value != source and codes[value][bit] == 1]
            if not before or not after:
                signature.append(0)
                continue
            left = before + [source] + after
            right = before + after + [source]
            signature.append(ask(left) - ask(right))
        signatures.append(tuple(signature))
    return signatures


def build_domains(n: int, codes: list[tuple[int, ...]], signatures: list[tuple[int, ...]]) -> list[list[tuple[int, int]]]:
    pairs_by_signature: dict[tuple[int, ...], list[tuple[int, int]]] = defaultdict(list)
    for successor in range(1, n + 1):
        for predecessor in range(1, n + 1):
            diff = tuple(codes[successor][bit] - codes[predecessor][bit] for bit in range(BITS))
            pairs_by_signature[diff].append((successor, predecessor))

    domains: list[list[tuple[int, int]]] = [[]]
    for node in range(1, n + 1):
        domains.append(
            [
                (successor, predecessor)
                for successor, predecessor in pairs_by_signature.get(signatures[node], [])
                if successor != node and predecessor != node
            ]
        )
    return domains


def solve_domains(domains: list[list[tuple[int, int]]]) -> list[int] | None:
    n = len(domains) - 1
    domain_sets = [set()] + [set(domain) for domain in domains[1:]]
    successor = [0] * (n + 1)
    predecessor = [0] * (n + 1)
    sys.setrecursionlimit(max(10000, 10 * n))

    def assign(kind: str, node: int, value: int, trail: list[tuple[str, int]]) -> bool:
        stack = [(kind, node, value)]
        while stack:
            current_kind, current_node, current_value = stack.pop()
            if current_node == current_value:
                return False
            array = successor if current_kind == "succ" else predecessor
            inverse = predecessor if current_kind == "succ" else successor
            inverse_kind = "pred" if current_kind == "succ" else "succ"
            if array[current_node]:
                if array[current_node] != current_value:
                    return False
                continue
            if inverse[current_value] and inverse[current_value] != current_node:
                return False
            array[current_node] = current_value
            trail.append((current_kind, current_node))
            stack.append((inverse_kind, current_value, current_node))
        return True

    def filtered(node: int) -> list[tuple[int, int]]:
        if successor[node] and predecessor[node]:
            pair = (successor[node], predecessor[node])
            return [pair] if pair in domain_sets[node] else []
        out: list[tuple[int, int]] = []
        for succ, pred in domains[node]:
            if successor[node] and successor[node] != succ:
                continue
            if predecessor[node] and predecessor[node] != pred:
                continue
            if predecessor[succ] and predecessor[succ] != node:
                continue
            if successor[pred] and successor[pred] != node:
                continue
            out.append((succ, pred))
        return out

    def undo(trail: list[tuple[str, int]]) -> None:
        for kind, node in reversed(trail):
            if kind == "succ":
                successor[node] = 0
            else:
                predecessor[node] = 0

    def propagate(trail: list[tuple[str, int]]) -> bool:
        changed = True
        while changed:
            changed = False
            for node in range(1, n + 1):
                options = filtered(node)
                if not options:
                    return False
                if len(options) == 1:
                    succ, pred = options[0]
                    before = len(trail)
                    if not assign("succ", node, succ, trail):
                        return False
                    if not assign("pred", node, pred, trail):
                        return False
                    changed = changed or len(trail) > before
        return True

    def search() -> list[int] | None:
        trail: list[tuple[str, int]] = []
        if not propagate(trail):
            undo(trail)
            return None
        if all(successor[1:]):
            answer = successor[:]
            undo(trail)
            return answer

        choice = 0
        choice_options: list[tuple[int, int]] | None = None
        for node in range(1, n + 1):
            if successor[node] and predecessor[node]:
                continue
            options = filtered(node)
            if choice_options is None or len(options) < len(choice_options):
                choice = node
                choice_options = options

        assert choice_options is not None
        for succ, pred in choice_options:
            branch: list[tuple[str, int]] = []
            if assign("succ", choice, succ, branch) and assign("pred", choice, pred, branch):
                answer = search()
                if answer is not None:
                    undo(branch)
                    undo(trail)
                    return answer
            undo(branch)

        undo(trail)
        return None

    return search()


def fallback_derangement(n: int) -> list[int]:
    return list(range(2, n + 1)) + [1]


def solve_case(n: int) -> list[int]:
    print(n, flush=True)
    codes = make_codes(n)
    signatures = measure_constraints(n, codes)
    domains = build_domains(n, codes, signatures)
    answer = solve_domains(domains)
    return answer[1:] if answer is not None else fallback_derangement(n)


def main() -> int:
    first = sys.stdin.readline()
    if not first:
        return 0
    t = int(first.strip())
    for _ in range(t):
        line = sys.stdin.readline()
        if not line:
            return 0
        n = int(line.strip())
        guess = solve_case(n)
        print("! " + " ".join(map(str, guess)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
