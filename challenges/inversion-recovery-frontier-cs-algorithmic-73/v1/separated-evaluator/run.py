from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LOG_LIMIT = 300
OUTPUT_LIMIT = 2_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score offline Frontier-CS reference outputs")
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


def clipped(text: str, limit: int = LOG_LIMIT) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "..."


def normalized_tokens(text: str) -> list[str]:
    return text.split()


def expected_text(run: dict[str, Any], challenge_dir: Path) -> str:
    if "answer_text" in run:
        return str(run["answer_text"])
    if "answer_path" in run:
        path = challenge_dir / str(run["answer_path"])
        return path.read_text(encoding="utf-8")
    return ""


def error_result(run_name: str, message: str, wall_time_ms: float) -> tuple[dict[str, Any], str]:
    result = {
        "case_name": run_name,
        "status": "error",
        "score": 0.0,
        "exact_match": 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, f"{run_name}: {message}"


def score_run(run: dict[str, Any], challenge_dir: Path, solution_runs_dir: Path) -> tuple[dict[str, Any], str]:
    run_name = str(run["run_name"])
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
    if stdout_path.stat().st_size > OUTPUT_LIMIT:
        return error_result(run_name, f"stdout exceeds {OUTPUT_LIMIT} bytes", wall_time_ms)

    actual = stdout_path.read_text(encoding="utf-8", errors="replace")
    expected = expected_text(run, challenge_dir)
    actual_tokens = normalized_tokens(actual)
    expected_tokens = normalized_tokens(expected)
    ok = actual_tokens == expected_tokens
    message = "exact reference match" if ok else (
        "expected " + clipped(expected) + "; got " + clipped(actual)
    )
    result = {
        "case_name": run_name,
        "status": "passed" if ok else "failed",
        "score": 100.0 if ok else 0.0,
        "exact_match": 1 if ok else 0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }
    return result, f"{run_name}: {message}"


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for result in results if result.get("status") == "passed")
    score = round(sum(float(result.get("score", 0.0)) for result in results) / total, 6) if total else 0.0
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "valid_cases": passed,
        "total_cases": total,
    }


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    runs = load_json(Path(args.runs_file))["runs"]
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    for run in runs:
        result, log_line = score_run(run, challenge_dir, Path(args.solution_runs_dir))
        results.append(result)
        logs.append(log_line)

    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["passed"] == summary["total"] and summary["total"] > 0 else "failed",
        "mode": args.mode,
        "rank_score": summary["score"],
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_cases", "value": summary["total_cases"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result.get("score", 0.0)},
                    {"metric_name": "valid_cases", "value": result.get("exact_match", 0)},
                ],
            }
            for result in results
        ],
        "public_results": results if args.mode == "validation" else [],
        "logs": logs[:50],
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
