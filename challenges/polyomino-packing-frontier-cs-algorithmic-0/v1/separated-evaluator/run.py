from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COORD_LIMIT = 4_000_000_000_000
MAX_INT64 = 9_223_372_036_854_775_807


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score polyomino packing outputs")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    try:
        payload = load_json(path)
    except Exception:
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return payload if isinstance(payload, dict) else {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}


def parse_integer_tokens(text: str, label: str) -> list[int]:
    tokens: list[int] = []
    for raw_token in text.split():
        try:
            tokens.append(int(raw_token, 10))
        except ValueError as error:
            raise ValueError(f"{label} contains a non-integer token: {raw_token!r}") from error
    return tokens


def parse_case(stdin_text: str) -> tuple[list[list[tuple[int, int]]], int]:
    tokens = parse_integer_tokens(stdin_text, "input")
    if not tokens:
        raise ValueError("input must start with n")
    index = 0
    n = tokens[index]
    index += 1
    if n <= 0:
        raise ValueError("n must be positive")

    shapes: list[list[tuple[int, int]]] = []
    total_cells = 0
    for piece_index in range(n):
        if index >= len(tokens):
            raise ValueError(f"piece {piece_index + 1}: missing k_i")
        k = tokens[index]
        index += 1
        if k < 1 or k > 10:
            raise ValueError(f"piece {piece_index + 1}: k_i must be in 1..10")
        cells: list[tuple[int, int]] = []
        for cell_index in range(k):
            if index + 1 >= len(tokens):
                raise ValueError(f"piece {piece_index + 1}: missing cell {cell_index + 1}")
            cells.append((tokens[index], tokens[index + 1]))
            index += 2
        if len(set(cells)) != len(cells):
            raise ValueError(f"piece {piece_index + 1}: duplicate local cells")
        shapes.append(cells)
        total_cells += k

    if index != len(tokens):
        raise ValueError("input contains extra integer tokens")
    return shapes, total_cells


def parse_output(stdout_text: str, n: int) -> tuple[int, int, list[tuple[int, int, int, int]]]:
    tokens = parse_integer_tokens(stdout_text, "stdout")
    expected = 2 + 4 * n
    if len(tokens) != expected:
        raise ValueError(f"stdout must contain exactly {expected} integers, found {len(tokens)}")
    width, height = tokens[0], tokens[1]
    if width < 1 or width > COORD_LIMIT:
        raise ValueError(f"W must be in 1..{COORD_LIMIT}")
    if height < 1 or height > COORD_LIMIT:
        raise ValueError(f"H must be in 1..{COORD_LIMIT}")
    if width * height > MAX_INT64:
        raise ValueError("W * H exceeds 64-bit area limit")

    placements: list[tuple[int, int, int, int]] = []
    index = 2
    for piece_index in range(n):
        x, y, rotation, reflected = tokens[index : index + 4]
        index += 4
        if x < -COORD_LIMIT or x > COORD_LIMIT:
            raise ValueError(f"piece {piece_index + 1}: X_i is outside allowed range")
        if y < -COORD_LIMIT or y > COORD_LIMIT:
            raise ValueError(f"piece {piece_index + 1}: Y_i is outside allowed range")
        if rotation < 0 or rotation > 3:
            raise ValueError(f"piece {piece_index + 1}: R_i must be in 0..3")
        if reflected not in {0, 1}:
            raise ValueError(f"piece {piece_index + 1}: F_i must be 0 or 1")
        placements.append((x, y, rotation, reflected))
    return width, height, placements


def rotate_clockwise(x: int, y: int, rotation: int) -> tuple[int, int]:
    if rotation == 0:
        return x, y
    if rotation == 1:
        return y, -x
    if rotation == 2:
        return -x, -y
    return -y, x


def validate_placement(
    shapes: list[list[tuple[int, int]]],
    width: int,
    height: int,
    placements: list[tuple[int, int, int, int]],
) -> None:
    occupied: set[tuple[int, int]] = set()
    for piece_index, (shape, placement) in enumerate(zip(shapes, placements), start=1):
        translate_x, translate_y, rotation, reflected = placement
        for source_x, source_y in shape:
            reflected_x = -source_x if reflected == 1 else source_x
            reflected_y = source_y
            rotated_x, rotated_y = rotate_clockwise(reflected_x, reflected_y, rotation)
            placed_x = rotated_x + translate_x
            placed_y = rotated_y + translate_y
            if placed_x < 0 or placed_x >= width or placed_y < 0 or placed_y >= height:
                raise ValueError(
                    f"piece {piece_index}: transformed cell ({placed_x}, {placed_y}) is out of bounds"
                )
            cell = (placed_x, placed_y)
            if cell in occupied:
                raise ValueError(f"piece {piece_index}: overlap at cell ({placed_x}, {placed_y})")
            occupied.add(cell)


def score_run(run: dict[str, Any], solution_runs_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    if metadata.get("timed_out") is True:
        return error_result(run_name, "solution timed out", wall_time_ms)
    if metadata.get("exit_code", 0) != 0:
        return error_result(run_name, f"solution exited with code {metadata.get('exit_code')}", wall_time_ms)

    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return error_result(run_name, "missing stdout.txt", wall_time_ms)

    try:
        shapes, total_cells = parse_case(str(run.get("stdin_text", "")))
        width, height, placements = parse_output(stdout_path.read_text(encoding="utf-8"), len(shapes))
        validate_placement(shapes, width, height, placements)
        total_area = width * height
        score = round(100.0 * float(total_cells) / float(total_area), 6)
        result = {
            "case_name": run_name,
            "status": "passed",
            "score": score,
            "total_cells": total_cells,
            "total_area": total_area,
            "width": width,
            "height": height,
            "wall_time_ms": wall_time_ms,
            "message": "valid placement",
        }
        return result, [f"{run_name}: cells={total_cells}, area={total_area}, score={score}"]
    except Exception as error:
        result = {
            "case_name": run_name,
            "status": "failed",
            "score": 0.0,
            "total_cells": 0,
            "total_area": 0,
            "width": 0,
            "height": 0,
            "wall_time_ms": wall_time_ms,
            "message": str(error),
        }
        return result, [f"{run_name}: {error}"]


def error_result(run_name: str, message: str, wall_time_ms: float) -> tuple[dict[str, Any], list[str]]:
    result = {
        "case_name": run_name,
        "status": "error",
        "score": 0.0,
        "total_cells": 0,
        "total_area": 0,
        "width": 0,
        "height": 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, [f"{run_name}: {message}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"score": 0.0, "valid_cases": 0, "passed": 0, "total": 0, "total_cells": 0, "total_area": 0}
    valid_cases = sum(1 for result in results if result["status"] == "passed")
    average_score = round(sum(float(result["score"]) for result in results) / total, 6)
    return {
        "score": average_score,
        "valid_cases": valid_cases,
        "passed": valid_cases,
        "total": total,
        "total_cells": sum(int(result.get("total_cells", 0)) for result in results),
        "total_area": sum(int(result.get("total_area", 0)) for result in results),
    }


def main() -> int:
    args = parse_args()
    runs = load_json(Path(args.runs_file))["runs"]
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    for run in runs:
        result, run_logs = score_run(run, Path(args.solution_runs_dir))
        results.append(result)
        logs.extend(run_logs)

    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["total"] > 0 else "failed",
        "mode": args.mode,
        "rank_score": summary["score"],
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_cells", "value": summary["total_cells"]},
            {"metric_name": "total_area", "value": summary["total_area"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "total_cells", "value": result.get("total_cells", 0)},
                    {"metric_name": "total_area", "value": result.get("total_area", 0)},
                ],
            }
            for result in results
        ],
        "public_results": results if args.mode == "validation" else [],
        "logs": logs,
    }
    if args.mode == "validation":
        payload["validation_summary"] = summary
    else:
        payload["official_summary"] = summary

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
