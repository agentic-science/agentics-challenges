from __future__ import annotations

import sys


def query(a: list[int], b: list[int]) -> int:
    print("1")
    print(len(a))
    print(" ".join(str(value) for value in a))
    print(" ".join(str(value) for value in b))
    sys.stdout.flush()

    response = sys.stdin.readline()
    if not response:
        raise EOFError("interactor closed before answering a query")
    return int(response.strip())


def ask_position(index: int) -> str:
    m = index + 3
    zero_state = index + 1
    one_state = index + 2

    a = list(range(m))
    b = list(range(m))
    for state in range(index):
        a[state] = state + 1
        b[state] = state + 1

    a[index] = zero_state
    b[index] = one_state
    a[zero_state] = zero_state
    b[zero_state] = zero_state
    a[one_state] = one_state
    b[one_state] = one_state

    result = query(a, b)
    if result == zero_state:
        return "0"
    if result == one_state:
        return "1"
    raise ValueError(f"unexpected query response {result}")


def build_suffix_automaton(pattern: str) -> tuple[list[int], list[int]]:
    states = len(pattern) + 1
    a = [0] * states
    b = [0] * states
    for state in range(states):
        prefix = pattern[:state]
        for bit, transitions in (("0", a), ("1", b)):
            candidate = prefix + bit
            next_state = min(len(pattern), len(candidate))
            while next_state > 0 and not candidate.endswith(pattern[:next_state]):
                next_state -= 1
            transitions[state] = next_state
    return a, b


def suffix_matches(pattern: str) -> bool:
    a, b = build_suffix_automaton(pattern)
    return query(a, b) == len(pattern)


def recover_suffix(length: int) -> str:
    suffix = ""
    for _ in range(length):
        candidate = "0" + suffix
        suffix = candidate if suffix_matches(candidate) else "1" + suffix
    return suffix


def solve_case(n: int) -> None:
    if n <= 20:
        guess = "".join(ask_position(index) for index in range(n))
    else:
        prefix_length = n // 2
        prefix = "".join(ask_position(index) for index in range(prefix_length))
        suffix = recover_suffix(n - prefix_length)
        guess = prefix + suffix

    print("0")
    print(guess, flush=True)


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        stripped = line.strip()
        if not stripped:
            continue
        n = int(stripped)
        if n <= 0:
            return 0
        solve_case(n)


if __name__ == "__main__":
    raise SystemExit(main())
