from __future__ import annotations

from collections import Counter
import sys


def is_solid(hands: list[Counter[int]], n: int) -> bool:
    return all(hands[player].get(player, 0) == n for player in range(1, n + 1))


def solve_two_players(hands: list[Counter[int]]) -> list[list[int]]:
    operations = []
    while hands[1].get(2, 0) > 0:
        operations.append([2, 1])
        hands[1][2] -= 1
        hands[2][1] -= 1
        hands[1][1] += 1
        hands[2][2] += 1
    return operations


def greedy_route(hands: list[Counter[int]], n: int) -> list[list[int]] | None:
    operations = []
    limit = n * n - n
    while not is_solid(hands, n) and len(operations) < limit:
        passed = [0] * (n + 1)
        for player in range(1, n + 1):
            candidates = [
                ((card - player) % n, card)
                for card, count in hands[player].items()
                if count > 0 and card != player
            ]
            if candidates:
                _, card = max(candidates)
            else:
                card = player
            passed[player] = card
            hands[player][card] -= 1
        for player in range(1, n + 1):
            hands[player % n + 1][passed[player]] += 1
        operations.append(passed[1:])
    return operations if is_solid(hands, n) else None


def main() -> int:
    data = [int(token) for token in sys.stdin.read().split()]
    if not data:
        return 0
    n = data[0]
    hands = [Counter() for _ in range(n + 1)]
    pos = 1
    for player in range(1, n + 1):
        for _ in range(n):
            if pos < len(data):
                hands[player][data[pos]] += 1
            pos += 1

    if is_solid(hands, n):
        print(0)
        return 0
    if n == 2:
        operations = solve_two_players(hands)
    else:
        operations = greedy_route([Counter()]+[Counter(hands[i]) for i in range(1, n + 1)], n)
        if operations is None:
            print(0)
            return 0

    print(len(operations))
    for row in operations:
        print(" ".join(map(str, row)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
