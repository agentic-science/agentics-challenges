from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


MAX_CELLS = 100_000
HEAVY_ROW_THRESHOLD = 300


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score rectangle-free point sets")
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


def parse_case(stdin_text: str) -> tuple[int, int]:
    tokens = parse_integer_tokens(stdin_text, "input")
    if len(tokens) != 2:
        raise ValueError(f"input must contain exactly 2 integers, found {len(tokens)}")
    n, m = tokens
    if n < 1 or m < 1:
        raise ValueError("n and m must be positive")
    if n * m > MAX_CELLS:
        raise ValueError(f"n * m must not exceed {MAX_CELLS}")
    return n, m


def parse_output(stdout_text: str, n: int, m: int) -> list[tuple[int, int]]:
    tokens = parse_integer_tokens(stdout_text, "stdout")
    if not tokens:
        raise ValueError("stdout must start with k")
    k = tokens[0]
    if k < 0 or k > n * m:
        raise ValueError(f"k must be in 0..{n * m}")
    expected = 1 + 2 * k
    if len(tokens) != expected:
        raise ValueError(f"stdout must contain exactly {expected} integers, found {len(tokens)}")

    points: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    index = 1
    for point_index in range(k):
        row, col = tokens[index], tokens[index + 1]
        index += 2
        if row < 1 or row > n:
            raise ValueError(f"point {point_index + 1}: row {row} is outside 1..{n}")
        if col < 1 or col > m:
            raise ValueError(f"point {point_index + 1}: column {col} is outside 1..{m}")
        point = (row, col)
        if point in seen:
            raise ValueError(f"point {point_index + 1}: duplicate coordinate ({row}, {col})")
        seen.add(point)
        points.append(point)
    return points


def validate_rectangle_free(n: int, m: int, points: list[tuple[int, int]]) -> None:
    if len(points) <= 1 or n == 1 or m == 1:
        return

    rows: dict[int, list[int]] = defaultdict(list)
    cols: dict[int, list[int]] = defaultdict(list)
    for row, col in points:
        rows[row].append(col)
        cols[col].append(row)

    for row_cols in rows.values():
        row_cols.sort()

    heavy_rows = [row for row, row_cols in rows.items() if len(row_cols) > HEAVY_ROW_THRESHOLD]
    for heavy_row in heavy_rows:
        counts: dict[int, int] = {}
        for col in rows[heavy_row]:
            for other_row in cols[col]:
                if other_row == heavy_row:
                    continue
                counts[other_row] = counts.get(other_row, 0) + 1
                if counts[other_row] >= 2:
                    raise ValueError(f"rectangle found using rows {heavy_row} and {other_row}")

    seen_column_pairs: set[tuple[int, int]] = set()
    for row, row_cols in rows.items():
        degree = len(row_cols)
        if degree < 2 or degree > HEAVY_ROW_THRESHOLD:
            continue
        for left_index in range(degree):
            left = row_cols[left_index]
            for right in row_cols[left_index + 1 :]:
                pair = (left, right)
                if pair in seen_column_pairs:
                    raise ValueError(f"rectangle found using columns {left} and {right}")
                seen_column_pairs.add(pair)


def upper_bound(n: int, m: int) -> int:
    return int(math.floor(min(n * math.sqrt(m) + m, m * math.sqrt(n) + n, n * m)))


def score_for_case(n: int, m: int, k: int) -> float:
    bound = upper_bound(n, m)
    if bound <= 0:
        return 100.0 if k > 0 else 0.0
    return round(100.0 * min(float(k) / (1.5 * float(bound)), 1.0), 6)


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
        n, m = parse_case(str(run.get("stdin_text", "")))
        points = parse_output(stdout_path.read_text(encoding="utf-8"), n, m)
        validate_rectangle_free(n, m, points)
        bound = upper_bound(n, m)
        score = score_for_case(n, m, len(points))
        result = {
            "case_name": run_name,
            "status": "passed",
            "score": score,
            "points": len(points),
            "upper_bound": bound,
            "n": n,
            "m": m,
            "wall_time_ms": wall_time_ms,
            "message": "valid rectangle-free point set",
        }
        return result, [f"{run_name}: points={len(points)}, upper_bound={bound}, score={score}"]
    except Exception as error:
        result = {
            "case_name": run_name,
            "status": "failed",
            "score": 0.0,
            "points": 0,
            "upper_bound": 0,
            "n": 0,
            "m": 0,
            "wall_time_ms": wall_time_ms,
            "message": str(error),
        }
        return result, [f"{run_name}: {error}"]


def error_result(run_name: str, message: str, wall_time_ms: float) -> tuple[dict[str, Any], list[str]]:
    result = {
        "case_name": run_name,
        "status": "error",
        "score": 0.0,
        "points": 0,
        "upper_bound": 0,
        "n": 0,
        "m": 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, [f"{run_name}: {message}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"score": 0.0, "valid_cases": 0, "passed": 0, "total": 0, "total_points": 0, "upper_bound": 0}
    valid_cases = sum(1 for result in results if result["status"] == "passed")
    average_score = round(sum(float(result["score"]) for result in results) / total, 6)
    return {
        "score": average_score,
        "valid_cases": valid_cases,
        "passed": valid_cases,
        "total": total,
        "total_points": sum(int(result.get("points", 0)) for result in results),
        "upper_bound": sum(int(result.get("upper_bound", 0)) for result in results),
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
            {"metric_name": "total_points", "value": summary["total_points"]},
            {"metric_name": "upper_bound", "value": summary["upper_bound"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "total_points", "value": result.get("points", 0)},
                    {"metric_name": "upper_bound", "value": result.get("upper_bound", 0)},
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
