from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


RATIO_RE = re.compile(r"Ratio:\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")
POINTS_RE = re.compile(r"points\s+([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score Frontier-CS checker-based stdio outputs")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    try:
        payload = load_json(path)
    except Exception:
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return payload if isinstance(payload, dict) else {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}


def clamp_ratio(value: float) -> float:
    if not math.isfinite(value):
        return 0.0
    return max(0.0, min(1.0, value))


def parse_ratio(message: str) -> float:
    match = RATIO_RE.search(message)
    if match:
        return clamp_ratio(float(match.group(1)))
    match = POINTS_RE.search(message)
    if match:
        return clamp_ratio(float(match.group(1)))
    return 1.0


def compile_checker(challenge_dir: Path, work_dir: Path) -> Path:
    checker_src = challenge_dir / "separated-evaluator" / "checker.cpp"
    include_dir = challenge_dir / "separated-evaluator"
    checker_bin = work_dir / "frontier_checker"
    command = ["g++", str(checker_src), "-O2", "-pipe", "-std=gnu++17", "-I", str(include_dir), "-o", str(checker_bin)]
    try:
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("checker compilation timed out") from error
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"checker compilation failed: {detail[:4000]}")
    return checker_bin


def run_checker(checker_bin: Path, input_text: str, output_text: str, answer_text: str, work_dir: Path, run_name: str) -> tuple[int, str]:
    case_dir = work_dir / run_name
    case_dir.mkdir(parents=True, exist_ok=True)
    input_path = case_dir / "input.txt"
    output_path = case_dir / "stdout.txt"
    answer_path = case_dir / "answer.txt"
    input_path.write_text(input_text, encoding="utf-8")
    output_path.write_text(output_text, encoding="utf-8")
    answer_path.write_text(answer_text, encoding="utf-8")
    completed = subprocess.run(
        [str(checker_bin), str(input_path), str(output_path), str(answer_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
    )
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def score_run(run: dict[str, Any], challenge_dir: Path, solution_runs_dir: Path, checker_bin: Path, work_dir: Path) -> tuple[dict[str, Any], str]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    base = {"case_name": run_name, "wall_time_ms": wall_time_ms}
    if metadata.get("timed_out") is True:
        return {**base, "status": "error", "score": 0.0, "ratio": 0.0, "message": "solution timed out"}, f"{run_name}: solution timed out"
    if metadata.get("exit_code", 0) != 0:
        return {**base, "status": "error", "score": 0.0, "ratio": 0.0, "message": f"solution exited with code {metadata.get('exit_code')}"}, f"{run_name}: nonzero solution exit"
    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return {**base, "status": "error", "score": 0.0, "ratio": 0.0, "message": "missing stdout.txt"}, f"{run_name}: missing stdout.txt"
    input_text = str(run.get("stdin_text", ""))
    answer_text = (challenge_dir / run["answer_path"]).read_text(encoding="utf-8")
    output_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    try:
        code, message = run_checker(checker_bin, input_text, output_text, answer_text, work_dir, run_name)
    except subprocess.TimeoutExpired:
        return {**base, "status": "failed", "score": 0.0, "ratio": 0.0, "message": "checker timed out"}, f"{run_name}: checker timed out"
    except Exception as error:
        return {**base, "status": "failed", "score": 0.0, "ratio": 0.0, "message": str(error)}, f"{run_name}: {error}"
    if code not in (0, 7):
        return {**base, "status": "failed", "score": 0.0, "ratio": 0.0, "message": message[:1000]}, f"{run_name}: checker rejected output: {message[:300]}"
    ratio = parse_ratio(message)
    score = round(100.0 * ratio, 6)
    return {**base, "status": "passed", "score": score, "ratio": round(ratio, 8), "message": message[:1000]}, f"{run_name}: score={score}; {message[:240]}"


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    valid = sum(1 for result in results if result["status"] == "passed")
    score = round(sum(float(result.get("score", 0.0)) for result in results) / total, 6) if total else 0.0
    return {"score": score, "valid_cases": valid, "total_cases": total, "passed": valid, "total": total}


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    solution_runs_dir = Path(args.solution_runs_dir)
    runs = load_json(Path(args.runs_file))["runs"]
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    with tempfile.TemporaryDirectory(prefix="frontier-checker-") as tmp:
        checker_bin = compile_checker(challenge_dir, Path(tmp))
        for run in runs:
            result, log = score_run(run, challenge_dir, solution_runs_dir, checker_bin, Path(tmp))
            results.append(result)
            logs.append(log)
    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["valid_cases"] == summary["total_cases"] and summary["total_cases"] > 0 else "failed",
        "mode": args.mode,
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_cases", "value": summary["total_cases"]},
        ],
        "run_metrics": [
            {"run_name": result["case_name"], "metrics": [{"metric_name": "score", "value": result.get("score", 0.0)}]}
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
