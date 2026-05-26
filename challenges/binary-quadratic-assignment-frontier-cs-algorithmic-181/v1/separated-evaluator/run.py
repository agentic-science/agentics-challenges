from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

POINTS_RE = re.compile(r"\bpoints\s+([-+0-9.eE]+)")
RATIO_RE = re.compile(r"\bRatio:\s*([-+0-9.eE]+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Frontier-CS checker against Agentics stdio outputs")
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


def checker_binary(challenge_dir: Path) -> Path:
    evaluator_dir = challenge_dir / "separated-evaluator"
    source = evaluator_dir / "checker.cc"
    header = evaluator_dir / "testlib.h"
    if not source.is_file() or not header.is_file():
        raise RuntimeError("missing checker.cc or testlib.h")
    digest = hashlib.sha256(source.read_bytes() + header.read_bytes()).hexdigest()[:24]
    cache_dir = Path(tempfile.gettempdir()) / "agentics-frontier-checkers"
    cache_dir.mkdir(parents=True, exist_ok=True)
    binary = cache_dir / f"checker-{digest}.bin"
    if binary.is_file():
        return binary
    tmp_binary = binary.with_suffix(".tmp")
    result = subprocess.run(
        ["g++", "-std=c++17", "-O2", "-pipe", str(source), "-o", str(tmp_binary)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("checker compilation failed: " + (result.stderr or result.stdout).strip())
    os.replace(tmp_binary, binary)
    return binary


def materialize_answer(run: dict[str, Any], challenge_dir: Path, temp_dir: Path) -> Path:
    if "answer_text" in run:
        answer_path = temp_dir / "answer.txt"
        answer_path.write_text(str(run["answer_text"]), encoding="utf-8")
        return answer_path
    if "answer_path" in run:
        return challenge_dir / str(run["answer_path"])
    answer_path = temp_dir / "answer.txt"
    answer_path.write_text("\n", encoding="utf-8")
    return answer_path


def score_from_checker(stderr: str, returncode: int) -> float:
    match = POINTS_RE.search(stderr)
    if match:
        return max(0.0, min(100.0, float(match.group(1))))
    match = RATIO_RE.search(stderr)
    if match:
        return max(0.0, min(100.0, float(match.group(1))))
    return 1.0 if returncode == 0 else 0.0


def score_run(run: dict[str, Any], challenge_dir: Path, solution_runs_dir: Path, checker: Path) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    base = {"case_name": run_name, "wall_time_ms": wall_time_ms}
    if metadata.get("timed_out") is True:
        return {**base, "status": "error", "score": 0.0, "message": "solution timed out"}, [f"{run_name}: solution timed out"]
    if metadata.get("exit_code", 0) != 0:
        return {**base, "status": "error", "score": 0.0, "message": f"solution exited with code {metadata.get('exit_code')}"}, [f"{run_name}: nonzero solution exit"]
    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return {**base, "status": "error", "score": 0.0, "message": "missing stdout.txt"}, [f"{run_name}: missing stdout.txt"]
    with tempfile.TemporaryDirectory(prefix="agentics-frontier-check-") as tmp:
        tmp_dir = Path(tmp)
        input_path = tmp_dir / "input.txt"
        input_path.write_text(str(run.get("stdin_text", "")), encoding="utf-8")
        answer_path = materialize_answer(run, challenge_dir, tmp_dir)
        result = subprocess.run(
            [str(checker), str(input_path), str(stdout_path), str(answer_path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
    checker_log = (result.stderr or result.stdout or "").strip()
    if result.returncode not in (0, 7):
        message = checker_log or f"checker exited with code {result.returncode}"
        return {**base, "status": "failed", "score": 0.0, "ratio": 0.0, "message": message}, [f"{run_name}: {message}"]
    ratio = score_from_checker(checker_log, result.returncode)
    score = round(100.0 * max(0.0, min(1.0, ratio)), 6)
    return {**base, "status": "passed", "score": score, "ratio": round(max(0.0, min(1.0, ratio)), 8), "message": checker_log}, [f"{run_name}: score={score}; {checker_log}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    valid = sum(1 for result in results if result["status"] == "passed")
    score = round(sum(float(result.get("score", 0.0)) for result in results) / total, 6) if total else 0.0
    return {"score": score, "valid_cases": valid, "total_cases": total, "passed": valid, "total": total}


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    runs = load_json(Path(args.runs_file))["runs"]
    checker = checker_binary(challenge_dir)
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    for run in runs:
        result, run_logs = score_run(run, challenge_dir, Path(args.solution_runs_dir), checker)
        results.append(result)
        logs.extend(run_logs)
    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["valid_cases"] == summary["total_cases"] and summary["total_cases"] > 0 else "failed",
        "mode": args.mode,
        "rank_score": summary["score"],
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
