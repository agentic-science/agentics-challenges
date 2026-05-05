from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path
from typing import Any, BinaryIO

INPUT_MAGIC = b"AGMMIN1\0"
OUTPUT_MAGIC = b"AGMMOUT1"
OUTPUT_HEADER = struct.Struct("<8sIII")
F32_SIZE = 4
CHUNK_VALUES = 262_144
FAILED_RANK_BASE = 1_000_000_000_000.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score matrix multiplication outputs")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    solution_runs_dir = Path(args.solution_runs_dir)
    runs = load_json(Path(args.runs_file))["runs"]

    public_results: list[dict[str, Any]] = []
    run_metric_rows: list[dict[str, Any]] = []
    logs: list[str] = []
    total_wall_time_ms = 0.0
    max_abs_error = 0.0
    failed_values = 0
    passed = 0

    for run in runs:
        result = score_run(challenge_dir, solution_runs_dir, run)
        total_wall_time_ms += result["wall_time_ms"]
        max_abs_error = max(max_abs_error, result["max_abs_error"])
        failed_values += result["failed_values"]
        if result["status"] == "passed":
            passed += 1
        else:
            logs.append(f"{result['run_id']}: {result['message']}")

        run_metric_rows.append(
            {
                "run_id": result["run_id"],
                "metrics": [
                    {"metric_id": "correctness", "value": result["score"]},
                    {"metric_id": "wall_time_ms", "value": result["wall_time_ms"]},
                    {"metric_id": "max_abs_error", "value": result["max_abs_error"]},
                    {"metric_id": "failed_values", "value": result["failed_values"]},
                ],
            }
        )
        public_results.append(
            {
                "case_id": result["run_id"],
                "status": result["status"],
                "score": result["score"],
                "message": result["message"],
            }
        )

    total = len(runs)
    correctness = 0.0 if total == 0 else passed / total
    summary = {"score": correctness, "passed": passed, "total": total}
    rank_score = -total_wall_time_ms if passed == total else -FAILED_RANK_BASE - total_wall_time_ms
    payload: dict[str, Any] = {
        "status": "passed" if passed == total else "failed",
        "mode": args.mode,
        "primary_score": correctness,
        "rank_score": rank_score,
        "aggregate_metrics": [
            {"metric_id": "correctness", "value": correctness},
            {"metric_id": "total_wall_time_ms", "value": total_wall_time_ms},
            {"metric_id": "max_abs_error", "value": max_abs_error},
            {"metric_id": "failed_values", "value": float(failed_values)},
        ],
        "run_metrics": run_metric_rows,
        "public_results": public_results if args.mode == "validation" else [],
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


def score_run(
    challenge_dir: Path, solution_runs_dir: Path, run: dict[str, Any]
) -> dict[str, Any]:
    run_id = run["run_id"]
    run_dir = solution_runs_dir / run_id
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    output_path = run_dir / "output" / "output.bin"
    expected_path = challenge_dir / run["expected_output_source_path"]
    tolerance_abs = float(run.get("tolerance_abs", 0.001))
    tolerance_rel = float(run.get("tolerance_rel", 0.0001))

    result = {
        "run_id": run_id,
        "status": "failed",
        "score": 0.0,
        "wall_time_ms": float(metadata.get("wall_time_ms", 0)),
        "max_abs_error": 0.0,
        "failed_values": 0,
        "message": "",
    }
    if metadata.get("exit_code") != 0 or metadata.get("timed_out"):
        result["status"] = "error"
        result["message"] = "solution run did not exit successfully"
        return result
    if not output_path.is_file():
        result["status"] = "error"
        result["message"] = "missing output/output.bin"
        return result

    try:
        comparison = compare_output(output_path, expected_path, tolerance_abs, tolerance_rel)
    except ValueError as error:
        result["message"] = str(error)
        return result

    result["max_abs_error"] = comparison["max_abs_error"]
    result["failed_values"] = comparison["failed_values"]
    if comparison["failed_values"] == 0:
        result["status"] = "passed"
        result["score"] = 1.0
        result["message"] = "passed"
    else:
        result["message"] = f"{comparison['failed_values']} values outside tolerance"
    return result


def load_run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return load_json(path)


def compare_output(
    output_path: Path,
    expected_path: Path,
    tolerance_abs: float,
    tolerance_rel: float,
) -> dict[str, Any]:
    with output_path.open("rb") as output_file, expected_path.open("rb") as expected_file:
        output_count = read_output_header(output_file, "solution output")
        expected_count = read_output_header(expected_file, "expected output")
        if output_count != expected_count:
            raise ValueError(
                f"output header mismatch: expected {expected_count}, got {output_count}"
            )

        max_abs_error = 0.0
        failed_values = 0
        values_remaining = output_count[0] * output_count[1] * output_count[2]
        while values_remaining > 0:
            chunk_values = min(CHUNK_VALUES, values_remaining)
            output_values = read_f32_values(output_file, chunk_values, "solution output")
            expected_values = read_f32_values(expected_file, chunk_values, "expected output")
            for actual, expected in zip(output_values, expected_values, strict=True):
                abs_error = abs(actual - expected)
                max_abs_error = max(max_abs_error, abs_error)
                allowed = tolerance_abs + tolerance_rel * abs(expected)
                if not math.isfinite(actual) or abs_error > allowed:
                    failed_values += 1
            values_remaining -= chunk_values

        if output_file.read(1):
            raise ValueError("solution output has trailing bytes")
        if expected_file.read(1):
            raise ValueError("expected output has trailing bytes")

    return {"max_abs_error": max_abs_error, "failed_values": failed_values}


def read_output_header(file: BinaryIO, label: str) -> tuple[int, int, int]:
    raw = file.read(OUTPUT_HEADER.size)
    if len(raw) != OUTPUT_HEADER.size:
        raise ValueError(f"{label} header is truncated")
    magic, cases, m, n = OUTPUT_HEADER.unpack(raw)
    if magic != OUTPUT_MAGIC:
        raise ValueError(f"{label} has invalid magic")
    return cases, m, n


def read_f32_values(file: BinaryIO, count: int, label: str) -> tuple[float, ...]:
    raw = file.read(count * F32_SIZE)
    if len(raw) != count * F32_SIZE:
        raise ValueError(f"{label} is truncated")
    return struct.unpack(f"<{count}f", raw)


if __name__ == "__main__":
    raise SystemExit(main())
