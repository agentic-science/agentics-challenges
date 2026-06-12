from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MAX_MASS_MG = 20_000_000
MAX_VOLUME_UL = 25_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score treasure packing outputs")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_case_metadata(run: dict[str, Any]) -> dict[str, Any]:
    metadata = run.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"run {run.get('run_name', '<unknown>')} metadata must be an object")
    return metadata


def run_case_required(run: dict[str, Any], key: str) -> Any:
    metadata = run_case_metadata(run)
    if key not in metadata:
        raise ValueError(f"run {run.get('run_name', '<unknown>')} metadata is missing {key}")
    return metadata[key]


def load_run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    try:
        payload = load_json(path)
    except Exception:
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return payload if isinstance(payload, dict) else {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}


def validate_case(case: Any) -> dict[str, tuple[int, int, int, int]]:
    if not isinstance(case, dict):
        raise ValueError("run stdin_json must be an object")
    if len(case) != 12:
        raise ValueError(f"run must contain exactly 12 categories, found {len(case)}")
    items: dict[str, tuple[int, int, int, int]] = {}
    for key, raw_values in case.items():
        if not isinstance(key, str) or not key:
            raise ValueError("category names must be non-empty strings")
        if not isinstance(raw_values, list) or len(raw_values) != 4:
            raise ValueError(f"{key}: value must be [quantity_limit, value, mass_mg, volume_ul]")
        values: list[int] = []
        for raw_value in raw_values:
            if isinstance(raw_value, bool) or not isinstance(raw_value, int) or raw_value <= 0:
                raise ValueError(f"{key}: item metadata must contain positive integers")
            values.append(raw_value)
        items[key] = (values[0], values[1], values[2], values[3])
    return items


def load_output(stdout_path: Path) -> dict[str, int]:
    try:
        payload = json.loads(stdout_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"stdout is not valid JSON: {error.msg}") from error
    if not isinstance(payload, dict):
        raise ValueError("stdout JSON must be an object")
    counts: dict[str, int] = {}
    for key, raw_count in payload.items():
        if not isinstance(key, str):
            raise ValueError("output keys must be strings")
        if isinstance(raw_count, bool) or not isinstance(raw_count, int):
            raise ValueError(f"{key}: count must be an integer")
        counts[key] = raw_count
    return counts


def score_ratio(participant_value: int, baseline_value: int, best_value: int) -> float:
    if best_value <= baseline_value:
        return 1.0 if participant_value >= best_value else 0.0
    return max(0.0, min(1.0, (participant_value - baseline_value) / (best_value - baseline_value)))


def score_run(run: dict[str, Any], solution_runs_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = load_run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    if metadata.get("timed_out") is True:
        return (
            {
                "case_name": run_name,
                "status": "error",
                "score": 0.0,
                "total_value": 0,
                "used_mass_mg": 0,
                "used_volume_ul": 0,
                "wall_time_ms": wall_time_ms,
                "message": "solution timed out",
            },
            [f"{run_name}: solution timed out"],
        )
    if metadata.get("exit_code", 0) != 0:
        return (
            {
                "case_name": run_name,
                "status": "error",
                "score": 0.0,
                "total_value": 0,
                "used_mass_mg": 0,
                "used_volume_ul": 0,
                "wall_time_ms": wall_time_ms,
                "message": f"solution exited with code {metadata.get('exit_code')}",
            },
            [f"{run_name}: nonzero solution exit"],
        )

    stdout_path = run_dir / "stdout.txt"
    if not stdout_path.is_file():
        return (
            {
                "case_name": run_name,
                "status": "error",
                "score": 0.0,
                "total_value": 0,
                "used_mass_mg": 0,
                "used_volume_ul": 0,
                "wall_time_ms": wall_time_ms,
                "message": "missing stdout.txt",
            },
            [f"{run_name}: missing stdout.txt"],
        )

    try:
        items = validate_case(run.get("stdin_json"))
        counts = load_output(stdout_path)
        if set(counts) != set(items):
            missing = sorted(set(items) - set(counts))
            extra = sorted(set(counts) - set(items))
            details = []
            if missing:
                details.append(f"missing keys: {', '.join(missing[:4])}")
            if extra:
                details.append(f"extra keys: {', '.join(extra[:4])}")
            raise ValueError("; ".join(details))

        total_value = 0
        used_mass_mg = 0
        used_volume_ul = 0
        for key, count in counts.items():
            quantity_limit, value, mass_mg, volume_ul = items[key]
            if count < 0:
                raise ValueError(f"{key}: count must be nonnegative")
            if count > quantity_limit:
                raise ValueError(f"{key}: count {count} exceeds limit {quantity_limit}")
            total_value += count * value
            used_mass_mg += count * mass_mg
            used_volume_ul += count * volume_ul
        if used_mass_mg > MAX_MASS_MG:
            raise ValueError(f"total mass {used_mass_mg} exceeds {MAX_MASS_MG} mg")
        if used_volume_ul > MAX_VOLUME_UL:
            raise ValueError(f"total volume {used_volume_ul} exceeds {MAX_VOLUME_UL} ul")

        baseline_value = int(run_case_required(run, "baseline_value"))
        best_value = int(run_case_required(run, "best_value"))
        score = round(100.0 * score_ratio(total_value, baseline_value, best_value), 6)
        result = {
            "case_name": run_name,
            "status": "passed",
            "score": score,
            "total_value": total_value,
            "used_mass_mg": used_mass_mg,
            "used_volume_ul": used_volume_ul,
            "wall_time_ms": wall_time_ms,
            "message": "valid output",
        }
        return result, [f"{run_name}: value={total_value}, score={score}"]
    except Exception as error:
        result = {
            "case_name": run_name,
            "status": "failed",
            "score": 0.0,
            "total_value": 0,
            "used_mass_mg": 0,
            "used_volume_ul": 0,
            "wall_time_ms": wall_time_ms,
            "message": str(error),
        }
        return result, [f"{run_name}: {error}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {
            "score": 0.0,
            "valid_cases": 0,
            "passed": 0,
            "total": 0,
            "total_value": 0,
            "used_mass_mg": 0,
            "used_volume_ul": 0,
        }
    valid_cases = sum(1 for result in results if result["status"] == "passed")
    return {
        "score": round(sum(float(result["score"]) for result in results) / total, 6),
        "valid_cases": valid_cases,
        "passed": valid_cases,
        "total": total,
        "total_value": sum(int(result.get("total_value", 0)) for result in results),
        "used_mass_mg": sum(int(result.get("used_mass_mg", 0)) for result in results),
        "used_volume_ul": sum(int(result.get("used_volume_ul", 0)) for result in results),
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
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_value", "value": summary["total_value"]},
            {"metric_name": "used_mass_mg", "value": summary["used_mass_mg"]},
            {"metric_name": "used_volume_ul", "value": summary["used_volume_ul"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "total_value", "value": result.get("total_value", 0)},
                    {"metric_name": "used_mass_mg", "value": result.get("used_mass_mg", 0)},
                    {"metric_name": "used_volume_ul", "value": result.get("used_volume_ul", 0)},
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
