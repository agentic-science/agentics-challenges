from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any

RATIO_RE = re.compile(r"Ratio: ([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")
UNBOUNDED_RE = re.compile(r"RatioUnbounded[=:] ?([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)")
SCORE_RE = re.compile(r"score=([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)/100")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a migrated Frontier-CS Testlib checker")
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


def compile_checker(evaluator_dir: Path, work_dir: Path) -> Path:
    checker = evaluator_dir / "checker.cpp"
    binary = work_dir / "checker"
    command = [
        "g++",
        str(checker),
        "-O2",
        "-std=gnu++17",
        "-U_FORTIFY_SOURCE",
        "-D_FORTIFY_SOURCE=0",
        "-I",
        str(evaluator_dir),
        "-o",
        str(binary),
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError("checker compile failed: " + (result.stderr or result.stdout)[-2000:])
    return binary


def parse_ratio(message: str, returncode: int) -> tuple[float | None, float | None]:
    ratio_match = RATIO_RE.search(message)
    score_match = SCORE_RE.search(message)
    if ratio_match:
        ratio = float(ratio_match.group(1))
    elif score_match:
        ratio = float(score_match.group(1)) / 100.0
    elif returncode == 0:
        ratio = 1.0
    else:
        ratio = None

    unbounded_match = UNBOUNDED_RE.search(message)
    unbounded = float(unbounded_match.group(1)) if unbounded_match else ratio
    if ratio is not None:
        ratio = max(0.0, min(1.0, ratio))
    if unbounded is not None:
        unbounded = max(0.0, unbounded)
    return ratio, unbounded


def error_case(run_name: str, status: str, message: str, wall_time_ms: float) -> dict[str, Any]:
    return {
        "case_name": run_name,
        "status": status,
        "score": 0.0,
        "ratio": 0.0,
        "unbounded_ratio": 0.0,
        "wall_time_ms": wall_time_ms,
        "message": message,
    }


def score_run(run: dict[str, Any], solution_runs_dir: Path, checker_bin: Path, work_dir: Path) -> dict[str, Any]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    if metadata.get("timed_out") is True:
        return error_case(run_name, "error", "solution timed out", wall_time_ms)
    if metadata.get("exit_code", 0) != 0:
        return error_case(run_name, "error", f"solution exited with code {metadata.get('exit_code')}", wall_time_ms)

    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return error_case(run_name, "error", "missing stdout.txt", wall_time_ms)

    case_dir = work_dir / run_name
    case_dir.mkdir(parents=True, exist_ok=True)
    input_path = case_dir / "input.txt"
    output_path = case_dir / "output.txt"
    answer_path = case_dir / "answer.txt"
    input_path.write_text(str(run.get("stdin_text", "")), encoding="utf-8")
    output_path.write_text(stdout_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    answer_path.write_text(str(run.get("answer_text", "")), encoding="utf-8")

    try:
        result = subprocess.run(
            [str(checker_bin), str(input_path), str(output_path), str(answer_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return error_case(run_name, "failed", "checker timed out", wall_time_ms)

    message = (result.stdout + result.stderr).strip()
    ratio, unbounded = parse_ratio(message, result.returncode)
    if ratio is None:
        return error_case(run_name, "failed", message or f"checker exited with code {result.returncode}", wall_time_ms)

    score = round(ratio * 100.0, 6)
    return {
        "case_name": run_name,
        "status": "passed" if ratio > 0.0 or result.returncode == 0 else "failed",
        "score": score,
        "ratio": round(ratio, 8),
        "unbounded_ratio": round(unbounded if unbounded is not None else ratio, 8),
        "checker_exit_code": result.returncode,
        "wall_time_ms": wall_time_ms,
        "message": message[:1000],
    }


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"score": 0.0, "accepted_cases": 0, "total_cases": 0, "average_ratio": 0.0, "unbounded_score": 0.0}
    accepted = sum(1 for result in results if result["status"] == "passed")
    return {
        "score": round(sum(float(result["score"]) for result in results) / total, 6),
        "accepted_cases": accepted,
        "total_cases": total,
        "average_ratio": round(sum(float(result.get("ratio", 0.0)) for result in results) / total, 8),
        "unbounded_score": round(100.0 * sum(float(result.get("unbounded_ratio", 0.0)) for result in results) / total, 6),
    }


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    evaluator_dir = challenge_dir / "separated-evaluator"
    runs = load_json(Path(args.runs_file))["runs"]
    logs: list[str] = []
    with tempfile.TemporaryDirectory(prefix="frontier-cs-checker-") as tmp:
        work_dir = Path(tmp)
        try:
            checker_bin = compile_checker(evaluator_dir, work_dir)
        except Exception as error:
            payload = {
                "status": "failed",
                "mode": args.mode,
                "rank_score": 0.0,
                "aggregate_metrics": [
                    {"metric_name": "score", "value": 0.0},
                    {"metric_name": "accepted_cases", "value": 0},
                    {"metric_name": "average_ratio", "value": 0.0},
                    {"metric_name": "unbounded_score", "value": 0.0},
                ],
                "run_metrics": [],
                "public_results": [],
                "logs": [str(error)],
            }
            Path(args.output_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return 0

        results = [score_run(run, Path(args.solution_runs_dir), checker_bin, work_dir) for run in runs]

    summary = aggregate(results)
    for result in results:
        logs.append(f"{result['case_name']}: ratio={result.get('ratio', 0.0)} status={result['status']} {result.get('message', '')[:160]}")

    passed = summary["accepted_cases"] == summary["total_cases"] and summary["total_cases"] > 0
    payload: dict[str, Any] = {
        "status": "passed" if passed else "failed",
        "mode": args.mode,
        "rank_score": summary["score"],
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "accepted_cases", "value": summary["accepted_cases"]},
            {"metric_name": "average_ratio", "value": summary["average_ratio"]},
            {"metric_name": "unbounded_score", "value": summary["unbounded_score"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "average_ratio", "value": result.get("ratio", 0.0)},
                    {"metric_name": "unbounded_score", "value": 100.0 * result.get("unbounded_ratio", 0.0)},
                ],
            }
            for result in results
        ],
        "public_results": results if args.mode == "validation" else [],
        "logs": logs,
    }
    payload["validation_summary" if args.mode == "validation" else "official_summary"] = summary
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
