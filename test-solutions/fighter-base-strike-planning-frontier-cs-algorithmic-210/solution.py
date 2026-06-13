from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import sys


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


@dataclass
class BlueBase:
    x: int
    y: int
    fuel: int
    missiles: int


@dataclass
class RedBase:
    x: int
    y: int
    defense: int
    value: int


@dataclass
class Fighter:
    x: int
    y: int
    fuel_cap: int
    missile_cap: int


@dataclass
class Plan:
    fighter_id: int
    path: list[int]
    attack_dir: int
    fuel: int
    missiles: int


def parse_input() -> tuple[int, int, list[str], list[BlueBase], list[RedBase], list[Fighter]]:
    tokens = sys.stdin.read().split()
    if not tokens:
        raise ValueError("empty input")
    pos = 0
    n = int(tokens[pos])
    m = int(tokens[pos + 1])
    pos += 2
    grid = tokens[pos:pos + n]
    pos += n

    blue: list[BlueBase] = []
    blue_count = int(tokens[pos])
    pos += 1
    for _ in range(blue_count):
        x = int(tokens[pos])
        y = int(tokens[pos + 1])
        fuel = int(tokens[pos + 2])
        missiles = int(tokens[pos + 3])
        pos += 6
        blue.append(BlueBase(x, y, fuel, missiles))

    red: list[RedBase] = []
    red_count = int(tokens[pos])
    pos += 1
    for _ in range(red_count):
        x = int(tokens[pos])
        y = int(tokens[pos + 1])
        defense = int(tokens[pos + 4])
        value = int(tokens[pos + 5])
        pos += 6
        red.append(RedBase(x, y, defense, value))

    fighters: list[Fighter] = []
    fighter_count = int(tokens[pos])
    pos += 1
    for _ in range(fighter_count):
        x = int(tokens[pos])
        y = int(tokens[pos + 1])
        fuel_cap = int(tokens[pos + 2])
        missile_cap = int(tokens[pos + 3])
        pos += 4
        fighters.append(Fighter(x, y, fuel_cap, missile_cap))

    return n, m, grid, blue, red, fighters


def bfs(n: int, m: int, grid: list[str], start: tuple[int, int]) -> tuple[list[int], list[int], list[int]]:
    total = n * m
    dist = [-1] * total
    parent = [-1] * total
    parent_dir = [-1] * total

    def cell_id(x: int, y: int) -> int:
        return x * m + y

    start_id = cell_id(*start)
    dist[start_id] = 0
    queue: deque[int] = deque([start_id])

    while queue:
        current = queue.popleft()
        x, y = divmod(current, m)
        for direction, (dx, dy) in enumerate(DIRS):
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < n and 0 <= ny < m):
                continue
            if grid[nx][ny] == "#":
                continue
            nxt = cell_id(nx, ny)
            if dist[nxt] != -1:
                continue
            dist[nxt] = dist[current] + 1
            parent[nxt] = current
            parent_dir[nxt] = direction
            queue.append(nxt)

    return dist, parent, parent_dir


def reconstruct_path(target: int, start: int, parent: list[int], parent_dir: list[int]) -> list[int]:
    path: list[int] = []
    current = target
    while current != start:
        direction = parent_dir[current]
        if direction < 0:
            return []
        path.append(direction)
        current = parent[current]
    path.reverse()
    return path


def choose_plans(
    n: int,
    m: int,
    grid: list[str],
    blue: list[BlueBase],
    red: list[RedBase],
    fighters: list[Fighter],
) -> list[Plan]:
    blue_at = {(base.x, base.y): idx for idx, base in enumerate(blue)}
    remaining_fuel = [base.fuel for base in blue]
    remaining_missiles = [base.missiles for base in blue]
    assigned_red: set[int] = set()
    plans: list[Plan] = []

    for fighter_id, fighter in enumerate(fighters):
        base_id = blue_at.get((fighter.x, fighter.y))
        if base_id is None:
            continue

        dist, parent, parent_dir = bfs(n, m, grid, (fighter.x, fighter.y))
        start_id = fighter.x * m + fighter.y
        best: tuple[float, int, int, int, int] | None = None

        for red_id, target in enumerate(red):
            if red_id in assigned_red or target.defense <= 0 or target.value <= 0:
                continue
            if target.defense > fighter.missile_cap or target.defense > remaining_missiles[base_id]:
                continue

            for attack_dir, (dx, dy) in enumerate(DIRS):
                ax = target.x - dx
                ay = target.y - dy
                if not (0 <= ax < n and 0 <= ay < m):
                    continue
                if grid[ax][ay] == "#":
                    continue
                adj_id = ax * m + ay
                distance = dist[adj_id]
                if distance < 0:
                    continue
                if distance > fighter.fuel_cap or distance > remaining_fuel[base_id]:
                    continue
                score = target.value / (distance + target.defense + 1)
                candidate = (score, target.value, -distance, red_id, attack_dir, adj_id)
                if best is None or candidate > best:
                    best = candidate

        if best is None:
            continue

        _, _value, _neg_distance, red_id, attack_dir, adj_id = best
        path = reconstruct_path(adj_id, start_id, parent, parent_dir)
        fuel = len(path)
        missiles = red[red_id].defense
        remaining_fuel[base_id] -= fuel
        remaining_missiles[base_id] -= missiles
        assigned_red.add(red_id)
        plans.append(Plan(fighter_id, path, attack_dir, fuel, missiles))

    return plans


def emit(plans: list[Plan]) -> None:
    if not plans:
        sys.stdout.write("OK\n")
        return

    max_distance = max((len(plan.path) for plan in plans), default=0)
    frames: list[list[str]] = [[] for _ in range(max_distance + 1)]

    for plan in plans:
        if plan.fuel > 0:
            frames[0].append(f"fuel {plan.fighter_id} {plan.fuel}")
        if plan.missiles > 0:
            frames[0].append(f"missile {plan.fighter_id} {plan.missiles}")
        if not plan.path:
            frames[0].append(f"attack {plan.fighter_id} {plan.attack_dir} {plan.missiles}")
            continue
        for step, direction in enumerate(plan.path, start=1):
            frames[step].append(f"move {plan.fighter_id} {direction}")
            if step == len(plan.path):
                frames[step].append(f"attack {plan.fighter_id} {plan.attack_dir} {plan.missiles}")

    lines: list[str] = []
    for commands in frames:
        lines.extend(commands)
        lines.append("OK")
    sys.stdout.write("\n".join(lines) + "\n")


def main() -> int:
    try:
        n, m, grid, blue, red, fighters = parse_input()
    except ValueError:
        return 0
    emit(choose_plans(n, m, grid, blue, red, fighters))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
