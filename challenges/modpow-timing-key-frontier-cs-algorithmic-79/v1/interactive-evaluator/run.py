from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

MAX_LOG_CHARS = 4000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Frontier-CS Testlib interactor")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--session-input-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    return parser.parse_args()


def cap(text: str, limit: int = MAX_LOG_CHARS) -> str:
    compact = text.replace("\x00", "")
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "...[truncated]"


def load_session(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("session manifest must be an object")
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("session metadata is required")
    cases = metadata.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("session metadata.cases must be a non-empty array")
    return payload


def compile_interactor(challenge_dir: Path, work_dir: Path) -> Path:
    src = challenge_dir / "interactive-evaluator" / "interactor.cpp"
    if not src.is_file():
        raise FileNotFoundError(f"missing interactor source: {src}")
    binary = work_dir / "frontier_cs_interactor"
    cmd = ["g++", "-std=gnu++17", "-O2", "-pipe", str(src), "-o", str(binary)]
    completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        raise RuntimeError("interactor compile failed: " + cap(completed.stderr or completed.stdout))
    return binary


def parse_score(report_text: str) -> tuple[float, str, bool]:
    text = report_text.strip()
    if not text:
        return 0.0, "no Testlib report was produced", False
    first = text.split(maxsplit=1)[0]
    try:
        ratio = float(first)
    except ValueError:
        return 0.0, cap(text), False
    if not math.isfinite(ratio) or ratio < 0.0:
        ratio = 0.0
    return min(ratio, 1.0), cap(text), True


def write_result(output_path: Path, mode: str, session_name: str, case_results: list[dict[str, Any]], logs: list[str]) -> None:
    total = len(case_results)
    protocol_errors = sum(1 for result in case_results if result.get("protocol_error"))
    passed = total - protocol_errors
    source_ratio = round(sum(result["source_ratio"] for result in case_results) / total, 8) if total else 0.0
    score = round(source_ratio * 100.0, 6)
    status = "passed" if total > 0 and protocol_errors == 0 else "failed"
    summary = {
        "score": score,
        "passed": passed,
        "total": total,
        "source_ratio": source_ratio,
        "protocol_errors": protocol_errors,
    }
    payload: dict[str, Any] = {
        "status": status,
        "mode": mode,
        "aggregate_metrics": [
            {"metric_name": "score", "value": score},
            {"metric_name": "source_ratio", "value": source_ratio},
            {"metric_name": "case_count", "value": total},
            {"metric_name": "protocol_errors", "value": protocol_errors},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "source_ratio", "value": result["source_ratio"]},
                    {"metric_name": "protocol_errors", "value": 1 if result.get("protocol_error") else 0},
                ],
            }
            for result in case_results
        ],
        "public_results": [],
        "logs": [cap(entry, 1000) for entry in logs[:8]],
    }
    if mode == "validation":
        payload["validation_summary"] = summary
        payload["public_results"] = [
            {
                "case_name": result["case_name"],
                "status": "passed" if not result.get("protocol_error") else "failed",
                "score": result["score"],
                "message": cap(result["message"], 500),
            }
            for result in case_results
        ]
    else:
        payload["official_summary"] = summary
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def failure_result(output_path: Path, mode: str, session_name: str, message: str) -> None:
    write_result(
        output_path,
        mode,
        session_name,
        [
            {
                "case_name": session_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "protocol_error": True,
                "message": message,
            }
        ],
        [message],
    )


def signal_session_end() -> None:
    try:
        print("0", flush=True)
    except BrokenPipeError:
        pass


def main() -> int:
    args = parse_args()
    output_path = Path(args.output_path)
    try:
        session = load_session(Path(args.session_file))
        session_name = str(session["session_name"])
        cases = session["metadata"]["cases"]
    except Exception as exc:
        failure_result(output_path, args.mode, "unknown", f"invalid session: {exc}")
        signal_session_end()
        return 0

    session_input_dir = Path(args.session_input_dir)
    logs: list[str] = []
    case_results: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="agentics-frontier-cs-") as tmp_name:
        tmp_dir = Path(tmp_name)
        try:
            binary = compile_interactor(Path(args.challenge_dir), tmp_dir)
        except Exception as exc:
            failure_result(output_path, args.mode, session_name, str(exc))
            signal_session_end()
            return 0

        for index, case in enumerate(cases, start=1):
            if not isinstance(case, dict):
                failure_result(output_path, args.mode, session_name, f"case {index} is not an object")
                signal_session_end()
                return 0
            case_name = str(case.get("case_name", f"case-{index}"))
            input_path = session_input_dir / str(case.get("input_path", ""))
            answer_path = session_input_dir / str(case.get("answer_path", ""))
            if not input_path.is_file() or not answer_path.is_file():
                failure_result(output_path, args.mode, session_name, f"case {case_name} is missing input or answer file")
                signal_session_end()
                return 0

            report_path = tmp_dir / f"report-{index}.txt"
            cmd = [str(binary), str(input_path), "/dev/stdout", str(answer_path), str(report_path)]
            completed = subprocess.run(
                cmd,
                stdin=sys.stdin.buffer,
                stdout=sys.stdout.buffer,
                stderr=subprocess.PIPE,
                text=False,
            )
            stderr = completed.stderr.decode("utf-8", errors="replace").strip() if completed.stderr else ""
            report_text = report_path.read_text(encoding="utf-8", errors="replace") if report_path.exists() else ""
            ratio, message, scored = parse_score(report_text)
            protocol_error = not scored
            if stderr and stderr != "See file to check exit message":
                logs.append(f"{case_name} stderr: {cap(stderr, 800)}")
            logs.append(f"{case_name}: {message}")
            case_results.append(
                {
                    "case_name": case_name,
                    "score": round(ratio * 100.0, 6),
                    "source_ratio": round(ratio, 8),
                    "protocol_error": protocol_error,
                    "message": message,
                    "exit_code": completed.returncode,
                }
            )
            if protocol_error:
                break

    signal_session_end()
    write_result(output_path, args.mode, session_name, case_results, logs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
