from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MAX_K = 240
INVALID_RATIO = 999.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score world-map grid outputs")
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


def parse_graph(stdin_text: str) -> tuple[int, set[tuple[int, int]]]:
    tokens = parse_integer_tokens(stdin_text, "input")
    if len(tokens) < 2:
        raise ValueError("input must contain N and M")
    n, m = tokens[0], tokens[1]
    if n < 1 or n > 40:
        raise ValueError("N must be in 1..40")
    max_edges = n * (n - 1) // 2
    if m < 0 or m > max_edges:
        raise ValueError(f"M must be in 0..{max_edges}")
    edge_tokens = tokens[2:]
    if len(edge_tokens) != 2 * m:
        raise ValueError(f"input declares {m} edges but contains {len(edge_tokens) // 2}")

    edges: set[tuple[int, int]] = set()
    for index in range(0, len(edge_tokens), 2):
        left, right = edge_tokens[index], edge_tokens[index + 1]
        if not (1 <= left <= n and 1 <= right <= n):
            raise ValueError("edge endpoint is outside 1..N")
        if left >= right:
            raise ValueError("input edges must satisfy A_i < B_i")
        edge = (left, right)
        if edge in edges:
            raise ValueError(f"duplicate edge {left} {right}")
        edges.add(edge)
    return n, edges


def parse_output(stdout_text: str, n: int) -> tuple[int, list[list[int]]]:
    tokens = parse_integer_tokens(stdout_text, "stdout")
    if not tokens:
        raise ValueError("stdout must start with K")
    k = tokens[0]
    if k < 1 or k > MAX_K:
        raise ValueError(f"K must be in 1..{MAX_K}")

    expected_tokens = 1 + k + k * k
    if len(tokens) != expected_tokens:
        raise ValueError(f"stdout must contain exactly {expected_tokens} integers, found {len(tokens)}")

    row_lengths = tokens[1 : 1 + k]
    for row_index, row_length in enumerate(row_lengths, start=1):
        if row_length != k:
            raise ValueError(f"Q_{row_index} must equal K={k}, found {row_length}")

    grid_tokens = tokens[1 + k :]
    grid: list[list[int]] = []
    cursor = 0
    for row_index in range(k):
        row: list[int] = []
        for col_index in range(k):
            color = grid_tokens[cursor]
            cursor += 1
            if color < 1 or color > n:
                raise ValueError(f"cell ({row_index + 1}, {col_index + 1}) color {color} is outside 1..{n}")
            row.append(color)
        grid.append(row)
    return k, grid


def normalized_edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def validate_map(n: int, edges: set[tuple[int, int]], grid: list[list[int]]) -> set[tuple[int, int]]:
    represented: set[tuple[int, int]] = set()
    k = len(grid)
    for row in range(k):
        for col in range(k):
            color = grid[row][col]
            for next_row, next_col in ((row + 1, col), (row, col + 1)):
                if next_row >= k or next_col >= k:
                    continue
                other = grid[next_row][next_col]
                if color == other:
                    continue
                edge = normalized_edge(color, other)
                if edge not in edges:
                    raise ValueError(f"forbidden adjacency between countries {edge[0]} and {edge[1]}")
                represented.add(edge)

    missing_edges = sorted(edges - represented)
    if missing_edges:
        left, right = missing_edges[0]
        raise ValueError(f"required adjacency between countries {left} and {right} is not represented")
    return represented


def score_for_ratio(ratio: float) -> float:
    bounded = max(0.0, min(1.0, (6.0 - ratio) / (6.0 - 1.5)))
    return round(100.0 * bounded, 6)


def error_result(run_name: str, status: str, message: str, wall_time_ms: float) -> tuple[dict[str, Any], list[str]]:
    result = {
        "case_name": run_name,
        "status": status,
        "score": 0.0,
        "ratio": INVALID_RATIO,
        "map_size": 0,
        "total_cells": 0,
        "represented_edges": 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, [f"{run_name}: {message}"]


def score_run(run: dict[str, Any], solution_runs_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    if metadata.get("timed_out") is True:
        return error_result(run_name, "error", "solution timed out", wall_time_ms)
    if metadata.get("exit_code", 0) != 0:
        return error_result(run_name, "error", f"solution exited with code {metadata.get('exit_code')}", wall_time_ms)

    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return error_result(run_name, "error", "missing stdout.txt", wall_time_ms)

    try:
        n, edges = parse_graph(str(run.get("stdin_text", "")))
        k, grid = parse_output(stdout_path.read_text(encoding="utf-8"), n)
        represented = validate_map(n, edges, grid)
        ratio = round(float(k) / float(n), 6)
        score = score_for_ratio(ratio)
        result = {
            "case_name": run_name,
            "status": "passed",
            "score": score,
            "ratio": ratio,
            "map_size": k,
            "total_cells": k * k,
            "represented_edges": len(represented),
            "wall_time_ms": wall_time_ms,
            "message": "valid map",
        }
        return result, [f"{run_name}: K={k}, N={n}, ratio={ratio}, score={score}"]
    except Exception as error:
        return error_result(run_name, "failed", str(error), wall_time_ms)


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"score": 0.0, "valid_cases": 0, "passed": 0, "total": 0, "average_ratio": INVALID_RATIO, "total_cells": 0}
    valid_cases = sum(1 for result in results if result["status"] == "passed")
    return {
        "score": round(sum(float(result["score"]) for result in results) / total, 6),
        "valid_cases": valid_cases,
        "passed": valid_cases,
        "total": total,
        "average_ratio": round(sum(float(result.get("ratio", INVALID_RATIO)) for result in results) / total, 6),
        "total_cells": sum(int(result.get("total_cells", 0)) for result in results),
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
    all_valid = summary["valid_cases"] == summary["total"] and summary["total"] > 0
    payload: dict[str, Any] = {
        "status": "passed" if all_valid else "failed",
        "mode": args.mode,
        "rank_score": summary["score"],
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "average_ratio", "value": summary["average_ratio"]},
            {"metric_name": "total_cells", "value": summary["total_cells"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "average_ratio", "value": result.get("ratio", INVALID_RATIO)},
                    {"metric_name": "total_cells", "value": result.get("total_cells", 0)},
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
