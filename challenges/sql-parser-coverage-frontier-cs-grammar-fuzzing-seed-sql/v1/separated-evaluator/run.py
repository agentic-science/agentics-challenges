from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from types import FrameType
from typing import Any


FEATURE_PATTERNS = {
    "create": re.compile(r"\bCREATE\s+TABLE\b", re.IGNORECASE),
    "insert": re.compile(r"\bINSERT\s+INTO\b", re.IGNORECASE),
    "select": re.compile(r"\bSELECT\b", re.IGNORECASE),
    "update": re.compile(r"\bUPDATE\b", re.IGNORECASE),
    "delete": re.compile(r"\bDELETE\s+FROM\b", re.IGNORECASE),
    "where": re.compile(r"\bWHERE\b", re.IGNORECASE),
    "join": re.compile(r"\bJOIN\b", re.IGNORECASE),
    "group_by": re.compile(r"\bGROUP\s+BY\b", re.IGNORECASE),
    "order_by": re.compile(r"\bORDER\s+BY\b", re.IGNORECASE),
    "limit": re.compile(r"\bLIMIT\b", re.IGNORECASE),
    "between": re.compile(r"\bBETWEEN\b", re.IGNORECASE),
    "in": re.compile(r"\bIN\s*\(", re.IGNORECASE),
    "function": re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\s*\(", re.IGNORECASE),
}

TARGET_MODULES = ("parser.py", "tokenizer.py", "ast_nodes.py")
DEFAULT_STATEMENT_LIMIT = 100
DEFAULT_MAX_STATEMENT_BYTES = 4096


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score SQL parser coverage runs")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--solution-runs-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def executable_lines(target_files: set[Path]) -> set[tuple[str, int]]:
    lines: set[tuple[str, int]] = set()
    for path in target_files:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
                lines.add((str(path), lineno))
    return lines


def load_statements(path: Path) -> list[str]:
    payload = load_json(path)
    if isinstance(payload, list):
        statements = payload
    elif isinstance(payload, dict):
        statements = payload.get("statements")
    else:
        raise ValueError("statements.json must be a JSON array or object")
    if not isinstance(statements, list):
        raise ValueError("statements must be an array")
    if not all(isinstance(statement, str) for statement in statements):
        raise ValueError("every statement must be a string")
    return statements


def run_metadata(run_root: Path) -> dict[str, Any]:
    metadata_path = run_root / "agentics-run.json"
    if not metadata_path.is_file():
        return {}
    try:
        metadata = load_json(metadata_path)
    except Exception:
        return {}
    return metadata if isinstance(metadata, dict) else {}


def load_case(run_root: Path, run: dict[str, Any]) -> dict[str, Any]:
    case_path = run_root / "input" / "case.json"
    if not case_path.is_file():
        return {
            "case_id": run["run_name"],
            "statement_limit": DEFAULT_STATEMENT_LIMIT,
            "max_statement_bytes": DEFAULT_MAX_STATEMENT_BYTES,
        }
    case = load_json(case_path)
    if not isinstance(case, dict):
        raise ValueError("case.json must be an object")
    return case


def parse_with_trace(
    parse_sql: Any,
    statements: list[str],
    target_files: set[Path],
) -> tuple[int, int, set[tuple[str, int]], list[str]]:
    target_file_names = {str(path) for path in target_files}
    executed: set[tuple[str, int]] = set()
    logs: list[str] = []
    valid = 0
    invalid = 0

    def tracer(frame: FrameType, event: str, _arg: Any) -> Any:
        if event == "line" and frame.f_code.co_filename in target_file_names:
            executed.add((frame.f_code.co_filename, frame.f_lineno))
        return tracer

    for statement in statements:
        sys.settrace(tracer)
        try:
            parse_sql(statement)
        except Exception as exc:
            invalid += 1
            if len(logs) < 8:
                logs.append(f"invalid SQL ignored: {str(exc)[:160]}")
        else:
            valid += 1
        finally:
            sys.settrace(None)

    return valid, invalid, executed, logs


def detected_features(statements: list[str]) -> set[str]:
    joined = "\n".join(statements)
    return {feature for feature, pattern in FEATURE_PATTERNS.items() if pattern.search(joined)}


def score_run(
    run: dict[str, Any],
    solution_runs_dir: Path,
    resources_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_root = solution_runs_dir / run_name
    metadata = run_metadata(run_root)
    if metadata.get("timed_out") is True:
        return (
            {"case_name": run_name, "status": "error", "score": 0, "message": "solution timed out"},
            [f"{run_name}: solution timed out"],
        )
    if metadata.get("exit_code", 0) != 0:
        return (
            {
                "case_name": run_name,
                "status": "error",
                "score": 0,
                "message": f"solution exited with code {metadata.get('exit_code')}",
            },
            [f"{run_name}: nonzero solution exit"],
        )

    output_path = run_root / "output" / "statements.json"
    if not output_path.is_file():
        return (
            {"case_name": run_name, "status": "error", "score": 0, "message": "missing statements.json"},
            [f"{run_name}: missing output/statements.json"],
        )

    try:
        case = load_case(run_root, run)
        statement_limit = int(case.get("statement_limit", DEFAULT_STATEMENT_LIMIT))
        max_statement_bytes = int(case.get("max_statement_bytes", DEFAULT_MAX_STATEMENT_BYTES))
        statements = load_statements(output_path)
        if not statements:
            raise ValueError("at least one statement is required")
        if len(statements) > statement_limit:
            raise ValueError(f"too many statements: {len(statements)} > {statement_limit}")
        for index, statement in enumerate(statements):
            if len(statement.encode("utf-8")) > max_statement_bytes:
                raise ValueError(f"statement {index} exceeds {max_statement_bytes} bytes")
    except Exception as exc:
        return (
            {"case_name": run_name, "status": "error", "score": 0, "message": str(exc)},
            [f"{run_name}: {exc}"],
        )

    sys.path.insert(0, str(resources_dir))
    from sql_engine import parse_sql  # type: ignore

    target_files = {resources_dir / "sql_engine" / name for name in TARGET_MODULES}
    covered_total = executable_lines(target_files)
    valid, invalid, executed, parse_logs = parse_with_trace(parse_sql, statements, target_files)
    features = detected_features(statements)
    line_coverage = 100.0 * len(executed & covered_total) / max(len(covered_total), 1)
    feature_coverage = 100.0 * len(features) / len(FEATURE_PATTERNS)
    score = round(0.7 * line_coverage + 0.3 * feature_coverage, 4)

    status = "passed" if valid > 0 else "failed"
    result = {
        "case_name": run_name,
        "status": status,
        "score": score,
        "line_coverage": round(line_coverage, 4),
        "feature_coverage": round(feature_coverage, 4),
        "valid_statements": valid,
        "invalid_statements": invalid,
        "features": sorted(features),
    }
    return result, [f"{run_name}: valid={valid}, invalid={invalid}, score={score}", *parse_logs]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if total == 0:
        return {
            "score": 0.0,
            "line_coverage": 0.0,
            "feature_coverage": 0.0,
            "valid_statements": 0,
            "passed": 0,
            "total": 0,
        }
    return {
        "score": round(sum(float(result["score"]) for result in results) / total, 4),
        "line_coverage": round(sum(float(result.get("line_coverage", 0)) for result in results) / total, 4),
        "feature_coverage": round(sum(float(result.get("feature_coverage", 0)) for result in results) / total, 4),
        "valid_statements": sum(int(result.get("valid_statements", 0)) for result in results),
        "passed": sum(1 for result in results if result["status"] == "passed"),
        "total": total,
    }


def main() -> int:
    args = parse_args()
    runs = load_json(Path(args.runs_file))["runs"]
    resources_dir = (Path(args.challenge_dir) / "resources").resolve()
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    for run in runs:
        result, run_logs = score_run(run, Path(args.solution_runs_dir), resources_dir)
        results.append(result)
        logs.extend(run_logs)

    summary = aggregate(results)
    status = "passed" if any(result["status"] == "passed" for result in results) else "failed"
    payload: dict[str, Any] = {
        "status": status,
        "mode": args.mode,
        "rank_score": summary["score"],
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "line_coverage", "value": summary["line_coverage"]},
            {"metric_name": "feature_coverage", "value": summary["feature_coverage"]},
            {"metric_name": "valid_statements", "value": summary["valid_statements"]},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "line_coverage", "value": result.get("line_coverage", 0)},
                    {"metric_name": "feature_coverage", "value": result.get("feature_coverage", 0)},
                    {"metric_name": "valid_statements", "value": result.get("valid_statements", 0)},
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
