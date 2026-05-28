from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import sys

SIZE = 30
TURNS = 300

MOVE_DELTAS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
    ".": (0, 0),
}


@dataclass(frozen=True)
class Room:
    top: int
    left: int
    height: int
    width: int

    @property
    def bottom(self) -> int:
        return self.top + self.height - 1

    @property
    def right(self) -> int:
        return self.left + self.width - 1

    @property
    def area(self) -> int:
        return self.height * self.width

    def contains(self, cell: tuple[int, int]) -> bool:
        r, c = cell
        return self.top <= r <= self.bottom and self.left <= c <= self.right

    def distance_to(self, cell: tuple[int, int]) -> int:
        r, c = cell
        clamped_r = min(max(r, self.top), self.bottom)
        clamped_c = min(max(c, self.left), self.right)
        return abs(r - clamped_r) + abs(c - clamped_c)


@dataclass(frozen=True)
class WallTask:
    stand: tuple[int, int]
    action: str
    wall: tuple[int, int]


def read_line() -> str | None:
    line = sys.stdin.readline()
    if line == "":
        return None
    return line.strip()


def update_pets(pets: list[tuple[int, int, int]], line: str) -> list[tuple[int, int, int]]:
    tokens = line.split()
    updated: list[tuple[int, int, int]] = []
    for index, (row, col, kind) in enumerate(pets):
        moves = tokens[index] if index < len(tokens) else "."
        for move in moves:
            dr, dc = MOVE_DELTAS.get(move, (0, 0))
            row += dr
            col += dc
        updated.append((row, col, kind))
    return updated


def choose_room(pets: list[tuple[int, int, int]], humans: list[tuple[int, int]]) -> Room:
    best: tuple[tuple[int, ...], Room] | None = None
    for height in range(6, 12):
        for width in range(6, 13):
            area = height * width
            if area < 80:
                continue
            for top in range(2, SIZE - height - 1):
                bottom = top + height - 1
                if bottom >= SIZE - 2:
                    continue
                for left in range(2, SIZE - width - 1):
                    right = left + width - 1
                    if right >= SIZE - 2:
                        continue
                    room = Room(top, left, height, width)
                    if any(room.contains((row, col)) for row, col, _kind in pets):
                        continue
                    pet_distances = [room.distance_to((row, col)) for row, col, _kind in pets]
                    min_pet_distance = min(pet_distances)
                    near_pets = sum(1 for distance in pet_distances if distance <= 3)
                    human_distances = sorted(room.distance_to(human) for human in humans)
                    travel = sum(human_distances[: min(4, len(human_distances))])
                    perimeter = 2 * (height + width)
                    candidate = (
                        min_pet_distance,
                        -near_pets,
                        area,
                        -travel,
                        -perimeter,
                        -top,
                        -left,
                        -height,
                        -width,
                    )
                    if best is None or candidate > best[0]:
                        best = (candidate, room)
    if best is None:
        return Room(10, 10, 8, 8)
    return best[1]


def make_wall_tasks(room: Room) -> tuple[list[WallTask], list[WallTask]]:
    tasks: list[WallTask] = []
    center_col = room.left + room.width // 2
    gate_cols: list[int] = []
    for offset in [0, -1, 1, -2, 2]:
        col = center_col + offset
        if room.left <= col <= room.right:
            gate_cols.append(col)
    gates = [WallTask((room.bottom, col), "d", (room.bottom + 1, col)) for col in gate_cols]
    gate_walls = {gate.wall for gate in gates}

    for col in range(room.left, room.right + 1):
        tasks.append(WallTask((room.top - 2, col), "d", (room.top - 1, col)))
        task = WallTask((room.bottom + 2, col), "u", (room.bottom + 1, col))
        if task.wall not in gate_walls:
            tasks.append(task)
    for row in range(room.top, room.bottom + 1):
        tasks.append(WallTask((row, room.left - 2), "r", (row, room.left - 1)))
        tasks.append(WallTask((row, room.right + 2), "l", (row, room.right + 1)))
    return tasks, gates


def inner_gate_for_wall(room: Room, wall: tuple[int, int]) -> WallTask:
    row, col = wall
    if row == room.top - 1:
        return WallTask((room.top, col), "u", wall)
    if row == room.bottom + 1:
        return WallTask((room.bottom, col), "d", wall)
    if col == room.left - 1:
        return WallTask((row, room.left), "l", wall)
    return WallTask((row, room.right), "r", wall)


def is_safe_wall(
    wall: tuple[int, int],
    pets: list[tuple[int, int, int]],
    humans: list[tuple[int, int]],
    built: set[tuple[int, int]],
) -> bool:
    row, col = wall
    if not (0 <= row < SIZE and 0 <= col < SIZE):
        return False
    if wall in built:
        return True
    if any((row, col) == (pet_row, pet_col) for pet_row, pet_col, _kind in pets):
        return False
    if any((row, col) == human for human in humans):
        return False
    for pet_row, pet_col, _kind in pets:
        if abs(pet_row - row) + abs(pet_col - col) == 1:
            return False
    return True


def step_toward(
    start: tuple[int, int],
    target: tuple[int, int],
    built: set[tuple[int, int]],
    room: Room | None = None,
) -> tuple[str, tuple[int, int]]:
    if start == target:
        return ".", start
    queue: deque[tuple[int, int]] = deque([start])
    parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
    seen = {start}
    while queue:
        cell = queue.popleft()
        if cell == target:
            break
        row, col = cell
        for action, (dr, dc) in MOVE_DELTAS.items():
            if action == ".":
                continue
            next_cell = (row + dr, col + dc)
            next_row, next_col = next_cell
            if not (0 <= next_row < SIZE and 0 <= next_col < SIZE):
                continue
            if next_cell in built or next_cell in seen:
                continue
            if room is not None and not room.contains(next_cell):
                continue
            seen.add(next_cell)
            parent[next_cell] = (cell, action)
            queue.append(next_cell)
    if target not in seen:
        return ".", start
    cell = target
    action = "."
    while parent[cell][0] != start:
        cell, action = parent[cell]
    return parent[cell][1], cell


def assign_targets(
    humans: list[tuple[int, int]],
    tasks: list[WallTask],
    reserved: set[tuple[int, int]],
) -> list[WallTask | None]:
    assignments: list[WallTask | None] = [None] * len(humans)
    available = [task for task in tasks if task.wall not in reserved]
    for index, human in enumerate(humans):
        if not available:
            break
        best_index = min(
            range(len(available)),
            key=lambda task_index: (
                abs(human[0] - available[task_index].stand[0])
                + abs(human[1] - available[task_index].stand[1]),
                available[task_index].wall,
            ),
        )
        assignments[index] = available.pop(best_index)
    return assignments


def solve_session(first_line: str) -> bool:
    pet_count = int(first_line)
    pets: list[tuple[int, int, int]] = []
    for _ in range(pet_count):
        line = read_line()
        if line is None:
            return False
        row, col, kind = map(int, line.split())
        pets.append((row - 1, col - 1, kind))

    line = read_line()
    if line is None:
        return False
    human_count = int(line)
    humans: list[tuple[int, int]] = []
    for _ in range(human_count):
        line = read_line()
        if line is None:
            return False
        row, col = map(int, line.split())
        humans.append((row - 1, col - 1))

    room = choose_room(pets, humans)
    wall_tasks, gates = make_wall_tasks(room)
    remaining = {task.wall: task for task in wall_tasks}
    open_gates = {gate.wall: gate for gate in gates}
    built: set[tuple[int, int]] = set()

    entry_target = gates[len(gates) // 2].stand
    outside_wait = (room.bottom + 2, entry_target[1])

    for _turn in range(TURNS):
        actions = ["."] * human_count
        planned_walls: set[tuple[int, int]] = set()

        if remaining:
            if _turn >= 120 and len(remaining) <= 3:
                for wall in list(remaining):
                    open_gates[wall] = inner_gate_for_wall(room, wall)
                    remaining.pop(wall, None)
            if not remaining:
                print("".join(actions), flush=True)
                line = read_line()
                if line is None:
                    return False
                pets = update_pets(pets, line)
                continue
            assignments = assign_targets(humans, list(remaining.values()), planned_walls)
            for index, task in enumerate(assignments):
                if task is None:
                    continue
                human = humans[index]
                if human == task.stand:
                    if task.wall not in planned_walls and is_safe_wall(task.wall, pets, humans, built):
                        actions[index] = task.action
                        planned_walls.add(task.wall)
                        built.add(task.wall)
                        remaining.pop(task.wall, None)
                else:
                    action, next_cell = step_toward(human, task.stand, built)
                    actions[index] = action
                    humans[index] = next_cell
        elif open_gates:
            pets_inside = sum(1 for row, col, _kind in pets if room.contains((row, col)))
            all_inside = all(room.contains(human) for human in humans)
            if pets_inside > 1:
                for index, human in enumerate(humans):
                    if human == outside_wait:
                        continue
                    action, next_cell = step_toward(human, outside_wait, built)
                    actions[index] = action
                    humans[index] = next_cell
            elif all_inside:
                assignments = assign_targets(humans, list(open_gates.values()), planned_walls)
                for index, task in enumerate(assignments):
                    if task is None:
                        continue
                    human = humans[index]
                    if human == task.stand:
                        if task.wall not in planned_walls and is_safe_wall(task.wall, pets, humans, built):
                            actions[index] = task.action
                            planned_walls.add(task.wall)
                            built.add(task.wall)
                            open_gates.pop(task.wall, None)
                    else:
                        action, next_cell = step_toward(human, task.stand, built, room)
                        actions[index] = action
                        humans[index] = next_cell
            else:
                closer = sorted(
                    range(human_count),
                    key=lambda index: abs(humans[index][0] - entry_target[0]) + abs(humans[index][1] - entry_target[1]),
                )
                for index in closer:
                    human = humans[index]
                    if room.contains(human):
                        continue
                    action, next_cell = step_toward(human, entry_target, built)
                    actions[index] = action
                    humans[index] = next_cell

        print("".join(actions), flush=True)
        line = read_line()
        if line is None:
            return False
        pets = update_pets(pets, line)

    return True


def main() -> int:
    line = read_line()
    while line is not None:
        if not solve_session(line):
            return 0
        line = read_line()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
