from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run permutation reconstruction interactor")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--session-input-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    return parser.parse_args()


def load_session(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("session manifest must be an object")
    return payload


def fail_result(
    output_path: Path,
    mode: str,
    session_name: str,
    message: str,
    *,
    query_count: int = 0,
    protocol_errors: int = 1,
) -> None:
    write_result(
        output_path,
        mode,
        session_name,
        score=0.0,
        correctness=0,
        query_count=query_count,
        protocol_errors=protocol_errors,
        status="failed",
        message=message,
    )


def write_result(
    output_path: Path,
    mode: str,
    session_name: str,
    *,
    score: float,
    correctness: int,
    query_count: int,
    protocol_errors: int,
    status: str,
    message: str,
) -> None:
    summary = {
        "score": score,
        "passed": 1 if correctness == 1 else 0,
        "total": 1,
        "query_count": query_count,
        "protocol_errors": protocol_errors,
    }
    result: dict[str, Any] = {
        "status": status,
        "mode": mode,
        "rank_score": score,
        "aggregate_metrics": [
            {"metric_name": "score", "value": score},
            {"metric_name": "correctness", "value": correctness},
            {"metric_name": "query_count", "value": query_count},
            {"metric_name": "protocol_errors", "value": protocol_errors},
        ],
        "run_metrics": [
            {
                "run_name": session_name,
                "metrics": [
                    {"metric_name": "score", "value": score},
                    {"metric_name": "correctness", "value": correctness},
                    {"metric_name": "query_count", "value": query_count},
                    {"metric_name": "protocol_errors", "value": protocol_errors},
                ],
            }
        ],
        "public_results": [],
        "logs": [message],
    }
    if mode == "validation":
        result["validation_summary"] = summary
        result["public_results"] = [
            {
                "case_name": session_name,
                "status": status,
                "score": score,
                "message": message,
                "query_count": query_count,
            }
        ]
    else:
        result["official_summary"] = summary

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


def parse_message(line: str, n: int) -> tuple[int, list[int]]:
    parts = line.strip().split()
    if len(parts) != n + 1:
        raise ValueError(f"expected {n + 1} integers, got {len(parts)}")
    try:
        values = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError("message must contain only integers") from exc
    action = values[0]
    payload = values[1:]
    if action not in {0, 1}:
        raise ValueError("action must be 0 for query or 1 for final answer")
    if any(value < 1 or value > n for value in payload):
        raise ValueError(f"all payload values must be in [1, {n}]")
    return action, payload


def is_permutation(values: list[int], n: int) -> bool:
    return sorted(values) == list(range(1, n + 1))


def main() -> int:
    args = parse_args()
    output_path = Path(args.output_path)
    try:
        session = load_session(Path(args.session_file))
        metadata = session.get("metadata")
        if not isinstance(metadata, dict):
            raise ValueError("session metadata is required")
        session_name = str(session["session_name"])
        n = int(metadata["n"])
        permutation = [int(value) for value in metadata["permutation"]]
        best_queries = int(metadata["best_queries"])
        max_queries = int(metadata.get("max_queries", 10000))
        if n <= 0 or len(permutation) != n or not is_permutation(permutation, n):
            raise ValueError("invalid hidden permutation metadata")
        if best_queries >= max_queries:
            raise ValueError("best_queries must be smaller than max_queries")
    except Exception as exc:
        fail_result(output_path, args.mode, "unknown", f"invalid session: {exc}")
        return 0

    query_count = 0
    print(n, flush=True)

    while True:
        line = sys.stdin.readline()
        if line == "":
            fail_result(output_path, args.mode, session_name, "participant exited before final answer", query_count=query_count)
            return 0
        try:
            action, payload = parse_message(line, n)
        except Exception as exc:
            fail_result(output_path, args.mode, session_name, f"protocol error: {exc}", query_count=query_count)
            return 0

        if action == 0:
            query_count += 1
            if query_count > max_queries:
                fail_result(output_path, args.mode, session_name, "query limit exceeded", query_count=query_count)
                return 0
            matches = sum(1 for actual, proposed in zip(permutation, payload, strict=True) if actual == proposed)
            print(matches, flush=True)
            continue

        if not is_permutation(payload, n):
            fail_result(output_path, args.mode, session_name, "final answer is not a permutation", query_count=query_count)
            return 0

        if payload != permutation:
            write_result(
                output_path,
                args.mode,
                session_name,
                score=0.0,
                correctness=0,
                query_count=query_count,
                protocol_errors=0,
                status="failed",
                message="wrong final permutation",
            )
            return 0

        denominator = max_queries - best_queries
        ratio = (max_queries - query_count) / denominator
        score = round(100.0 * max(0.0, min(1.0, ratio)), 4)
        write_result(
            output_path,
            args.mode,
            session_name,
            score=score,
            correctness=1,
            query_count=query_count,
            protocol_errors=0,
            status="passed",
            message=f"correct permutation in {query_count} queries",
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
