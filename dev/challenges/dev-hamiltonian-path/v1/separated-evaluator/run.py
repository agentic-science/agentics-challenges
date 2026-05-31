from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score Hamiltonian path outputs")
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


def parse_graph(stdin_text: str) -> tuple[int, list[int], set[tuple[int, int]]]:
    tokens = parse_integer_tokens(stdin_text, "input")
    if len(tokens) < 12:
        raise ValueError("input must contain n, m, and ten thresholds")
    n, m = tokens[0], tokens[1]
    if n <= 0 or m < 0:
        raise ValueError("n must be positive and m must be nonnegative")
    thresholds = tokens[2:12]
    if any(threshold < 1 or threshold > n for threshold in thresholds):
        raise ValueError("all thresholds must be in 1..n")
    edge_tokens = tokens[12:]
    if len(edge_tokens) != 2 * m:
        raise ValueError(f"input declares {m} edges but contains {len(edge_tokens) // 2}")
    edges: set[tuple[int, int]] = set()
    for index in range(0, len(edge_tokens), 2):
        u, v = edge_tokens[index], edge_tokens[index + 1]
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError("edge endpoint is out of range")
        if u == v:
            raise ValueError("self-loops are not allowed")
        edges.add((u, v))
    return n, thresholds, edges


def parse_path(stdout_text: str, n: int) -> list[int]:
    tokens = parse_integer_tokens(stdout_text, "stdout")
    if not tokens:
        raise ValueError("stdout must start with path length k")
    k = tokens[0]
    if k <= 0:
        raise ValueError("path length k must be positive")
    path = tokens[1:]
    if len(path) != k:
        raise ValueError(f"declared k={k}, but found {len(path)} path vertices")
    for vertex in path:
        if vertex < 1 or vertex > n:
            raise ValueError(f"vertex {vertex} is outside 1..{n}")
    if len(set(path)) != len(path):
        raise ValueError("path repeats a vertex")
    return path


def threshold_score(path_length: int, thresholds: list[int]) -> float:
    return 10.0 * sum(1 for threshold in thresholds if path_length >= threshold)


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
        n, thresholds, edges = parse_graph(str(run.get("stdin_text", "")))
        path = parse_path(stdout_path.read_text(encoding="utf-8"), n)
        for left, right in zip(path, path[1:]):
            if (left, right) not in edges:
                raise ValueError(f"missing directed edge {left} -> {right}")
        score = threshold_score(len(path), thresholds)
        result = {
            "case_name": run_name,
            "status": "passed",
            "score": score,
            "path_length": len(path),
            "wall_time_ms": wall_time_ms,
            "message": "valid path",
        }
        return result, [f"{run_name}: path_length={len(path)}, score={score}"]
    except Exception as error:
        result = {
            "case_name": run_name,
            "status": "failed",
            "score": 0.0,
            "path_length": 0,
            "wall_time_ms": wall_time_ms,
            "message": str(error),
        }
        return result, [f"{run_name}: {error}"]


def error_result(run_name: str, message: str, wall_time_ms: float) -> tuple[dict[str, Any], list[str]]:
    result = {
        "case_name": run_name,
        "status": "error",
        "score": 0.0,
        "path_length": 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, [f"{run_name}: {message}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"score": 0.0, "valid_cases": 0, "passed": 0, "total": 0, "total_path_length": 0}
    valid_cases = sum(1 for result in results if result["status"] == "passed")
    return {
        "score": round(sum(float(result["score"]) for result in results) / total, 6),
        "valid_cases": valid_cases,
        "passed": valid_cases,
        "total": total,
        "total_path_length": sum(int(result.get("path_length", 0)) for result in results),
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
            {"metric_name": "total_path_length", "value": summary["total_path_length"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "total_path_length", "value": result.get("path_length", 0)},
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
