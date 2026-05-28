from __future__ import annotations

import sys


class ParsedForest:
    def __init__(self) -> None:
        self.children: list[list[int]] = []
        self.prefixes: list[list[int]] = []
        self.seq_id: list[int] = []
        self.lo: list[int] = []
        self.hi: list[int] = []
        self.size: list[int] = []
        self.roots: list[int] = []

    def add_node_list(self, children: list[int]) -> int:
        total = 0
        prefix = [0]
        for child in children:
            total += self.size[child]
            prefix.append(total)

        seq_id = len(self.children)
        self.children.append(children)
        self.prefixes.append(prefix)

        node = len(self.size)
        self.seq_id.append(seq_id)
        self.lo.append(0)
        self.hi.append(len(children))
        self.size.append(total + 1)
        return node

    def add_node_view(self, base: int, offset: int) -> int:
        seq_id = self.seq_id[base]
        lo = self.lo[base] + offset
        hi = self.hi[base]
        total = self.prefixes[seq_id][hi] - self.prefixes[seq_id][lo]

        node = len(self.size)
        self.seq_id.append(seq_id)
        self.lo.append(lo)
        self.hi.append(hi)
        self.size.append(total + 1)
        return node

    def child_count(self, node: int) -> int:
        return self.hi[node] - self.lo[node]

    def child_at(self, node: int, offset: int) -> int:
        return self.children[self.seq_id[node]][self.lo[node] + offset]

    def child_slice(self, node: int) -> list[int]:
        return self.children[self.seq_id[node]][self.lo[node] : self.hi[node]]


def parse_forest(sequence: str) -> ParsedForest:
    parsed = ParsedForest()
    stack: list[int] = []
    pending_children: list[list[int]] = []

    for char in sequence:
        if char == "(":
            pending_children.append([])
            stack.append(len(pending_children) - 1)
            continue

        pending_id = stack.pop()
        node = parsed.add_node_list(pending_children[pending_id])
        if stack:
            pending_children[stack[-1]].append(node)
        else:
            parsed.roots.append(node)

    return parsed


def flatten_source(parsed: ParsedForest, original_pairs: int) -> list[tuple[int, int]]:
    operations: list[tuple[int, int]] = [(5, original_pairs * 2)]
    catalyst = parsed.add_node_list([])
    roots = [*parsed.roots, catalyst]

    starts: list[int] = []
    position = 0
    for root in roots:
        starts.append(position)
        position += parsed.size[root] * 2

    doubles: list[int] = []
    stack = [(root, start) for root, start in reversed(list(zip(roots, starts)))]

    while stack:
        node, start = stack.pop()
        child_count = parsed.child_count(node)
        if child_count == 0:
            continue

        first_child = parsed.child_at(node, 0)
        if child_count == 1:
            if parsed.child_count(first_child) == 0:
                doubles.append(start)
            else:
                operations.append((1, start))
                stack.append((first_child, start))
            continue

        second_child = parsed.child_at(node, 1)
        operations.append((2, start))

        merged_children = [first_child]
        merged_children.extend(parsed.child_slice(second_child))
        merged = parsed.add_node_list(merged_children)
        remainder = parsed.add_node_view(node, 2)

        stack.append((remainder, start + parsed.size[merged] * 2))
        stack.append((merged, start))

    doubles.sort()
    operations.extend(reduce_double_atoms(doubles))
    return operations


def reduce_double_atoms(doubles: list[int]) -> list[tuple[int, int]]:
    operations: list[tuple[int, int]] = []

    for index in range(len(doubles) - 1, 0, -1):
        left = doubles[index - 1]
        right = doubles[index]

        position = right - 2
        while position >= left + 4:
            operations.append((3, position))
            position -= 2

        operations.extend(((4, left), (2, left), (1, left)))

    if doubles:
        first = doubles[0]
        operations.append((6, first + 1))
        operations.append((5, first + 2))

    return operations


def build_target(parsed: ParsedForest) -> list[tuple[int, int]]:
    operations: list[tuple[int, int]] = []
    root_starts: list[tuple[int, int]] = []
    position = 0
    for root in parsed.roots:
        root_starts.append((root, position))
        position += parsed.size[root] * 2

    stack: list[tuple[str, int, int]] = [
        ("enter", root, start) for root, start in reversed(root_starts)
    ]

    while stack:
        phase, node, start = stack.pop()
        if phase == "exit":
            child_starts: list[int] = []
            child_position = start
            for offset in range(parsed.child_count(node)):
                child = parsed.child_at(node, offset)
                child_starts.append(child_position)
                child_position += parsed.size[child] * 2
            for child_start in reversed(child_starts):
                operations.append((4, child_start))
            continue

        stack.append(("exit", node, start))
        child_position = start
        children_to_enter: list[tuple[int, int]] = []
        for offset in range(parsed.child_count(node)):
            child = parsed.child_at(node, offset)
            children_to_enter.append((child, child_position))
            child_position += parsed.size[child] * 2
        for child, child_start in reversed(children_to_enter):
            stack.append(("enter", child, child_start))

    return operations


def solve(source: str, target: str) -> list[tuple[int, int]]:
    if source == target:
        return []

    pairs = len(source) // 2
    operations = flatten_source(parse_forest(source), pairs)
    operations.extend(build_target(parse_forest(target)))
    operations.append((6, pairs * 2))
    return operations


def main() -> int:
    data = sys.stdin.read().split()
    if len(data) < 3:
        print(0)
        return 0

    _pairs = int(data[0])
    source = data[1]
    target = data[2]

    operations = solve(source, target)
    output = [str(len(operations))]
    output.extend(f"{operation} {position}" for operation, position in operations)
    sys.stdout.write("\n".join(output))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
