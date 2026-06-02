
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import deque
from pathlib import Path
from typing import Any

LINE_LIMIT = 200000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--session-input-dir", required=False)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=False)
    return parser.parse_args()


def load_session(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("session root must be an object")
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("session metadata must be an object")
    return payload


def read_line() -> str | None:
    line = sys.stdin.readline(LINE_LIMIT + 1)
    if line == "":
        return None
    if len(line) > LINE_LIMIT:
        raise ValueError("participant line is too long")
    return line.strip()


def ints_from_line(line: str) -> list[int]:
    parts = line.split()
    try:
        return [int(part, 10) for part in parts]
    except ValueError as exc:
        raise ValueError("expected integer tokens") from exc


def clipped(message: str, limit: int = 300) -> str:
    compact = " ".join(str(message).split())
    return compact if len(compact) <= limit else compact[:limit] + "..."


def write_result(output_path: Path, mode: str, session_name: str, *, status: str, score: float, correctness: int, total: int, query_count: int, protocol_errors: int, logs: list[str]) -> None:
    score = round(float(score), 6)
    summary = {"score": score, "passed": correctness, "total": total, "query_count": query_count, "protocol_errors": protocol_errors}
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
        "run_metrics": [{"run_name": session_name, "metrics": [{"metric_name": "score", "value": score}, {"metric_name": "correctness", "value": correctness}, {"metric_name": "query_count", "value": query_count}, {"metric_name": "protocol_errors", "value": protocol_errors}]}],
        "public_results": [],
        "logs": [clipped(line) for line in logs[:50]],
    }
    if mode == "validation":
        result["validation_summary"] = summary
        result["public_results"] = [{"case_name": session_name, "status": status, "score": score, "message": clipped(logs[-1] if logs else status), "query_count": query_count}]
    else:
        result["official_summary"] = summary
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


def fail(output_path: Path, mode: str, session_name: str, message: str, *, total: int = 1, query_count: int = 0, correctness: int = 0) -> int:
    write_result(output_path, mode, session_name, status="failed", score=0.0, correctness=correctness, total=total, query_count=query_count, protocol_errors=1, logs=[message])
    return 0


def case_score(q: int) -> float:
    if q <= 500:
        return 100.0
    if q >= 5000:
        return 0.0
    return 100.0 * (5000.0 - q) / 4500.0


def runtime_random_cases(metadata: dict[str, Any]) -> list[dict[str, Any]] | None:
    policy = metadata.get("runtime_random")
    if not isinstance(policy, dict):
        return None
    if policy.get("kind") != "duplicate_position_search":
        raise ValueError("unsupported runtime_random kind")
    case_count = int(policy.get("case_count", 20))
    n = int(policy.get("n", 300))
    if case_count <= 0 or n <= 0:
        raise ValueError("runtime_random case_count and n must be positive")
    rng = random.SystemRandom()
    cases: list[dict[str, Any]] = []
    for _ in range(case_count):
        pos = rng.randrange(1, n + 1)
        array = list(range(1, n + 1))
        array.extend(value for value in range(1, n + 1) if value != pos)
        rng.shuffle(array)
        cases.append({"n": n, "pos": pos, "array": array})
    return cases


def main() -> int:
    args = parse_args(); output = Path(args.output_path)
    try:
        session = load_session(Path(args.session_file)); name = str(session["session_name"]); metadata = session["metadata"]; cases = runtime_random_cases(metadata) or metadata["cases"]
    except Exception as exc:
        return fail(output, args.mode, "unknown", f"invalid session: {exc}")
    print(len(cases), flush=True)
    scores=[]; total_q=0; solved=0; logs=[]
    for ci, case in enumerate(cases, 1):
        n=int(case["n"]); pos=int(case["pos"]); array=[int(x) for x in case["array"]]
        print(n, flush=True)
        q=0
        while True:
            line=read_line()
            if line is None: return fail(output,args.mode,name,"participant exited before final answer",total=len(cases),query_count=total_q+q,correctness=solved)
            parts=line.split()
            if not parts: continue
            if parts[0] == "?":
                q += 1
                if q > 5000: return fail(output,args.mode,name,"query limit exceeded",total=len(cases),query_count=total_q+q,correctness=solved)
                vals=ints_from_line(" ".join(parts[1:]))
                if len(vals) < 2: return fail(output,args.mode,name,"query must contain x, m, and indices",total=len(cases),query_count=total_q+q,correctness=solved)
                x,m=vals[0],vals[1]; idxs=vals[2:]
                if not (1 <= x <= n) or not (1 <= m <= 2*n-1) or len(idxs) != m or any(i < 1 or i > 2*n-1 for i in idxs):
                    return fail(output,args.mode,name,"invalid membership query",total=len(cases),query_count=total_q+q,correctness=solved)
                print(1 if any(array[i-1] == x for i in idxs) else 0, flush=True)
            elif parts[0] == "!":
                vals=ints_from_line(" ".join(parts[1:]))
                if len(vals) != 1 or not (1 <= vals[0] <= n): return fail(output,args.mode,name,"invalid final answer",total=len(cases),query_count=total_q+q,correctness=solved)
                if vals[0] != pos: return fail(output,args.mode,name,f"wrong singleton on case {ci}",total=len(cases),query_count=total_q+q,correctness=solved)
                scores.append(case_score(q)); total_q += q; solved += 1; logs.append(f"case {ci}: solved in {q} queries"); break
            else:
                return fail(output,args.mode,name,"unknown command",total=len(cases),query_count=total_q+q,correctness=solved)
    score=min(scores) if scores else 0.0
    write_result(output,args.mode,name,status="passed",score=score,correctness=solved,total=len(cases),query_count=total_q,protocol_errors=0,logs=logs)
    return 0

if __name__ == "__main__": raise SystemExit(main())
