
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


def runtime_random_case(metadata: dict[str, Any]) -> dict[str, Any] | None:
    policy = metadata.get("runtime_random")
    if not isinstance(policy, dict):
        return None
    if policy.get("kind") != "limited_shuffle_restore":
        raise ValueError("unsupported runtime_random kind")
    n = int(policy["n"])
    if n <= 0:
        raise ValueError("runtime_random n must be positive")
    rng = random.SystemRandom()
    array = list(range(1, n + 1))
    for i in range(n):
        j = rng.randrange(i, min(n - 1, i + 2) + 1)
        array[i], array[j] = array[j], array[i]
    return {"n": n, "array": array}


def main() -> int:
    args=parse_args(); output=Path(args.output_path)
    try:
        session=load_session(Path(args.session_file)); name=str(session["session_name"]); metadata=session["metadata"]; case=runtime_random_case(metadata) or metadata["case"]
    except Exception as exc: return fail(output,args.mode,"unknown",f"invalid session: {exc}")
    n=int(case["n"]); array=[int(x) for x in case["array"]]; limit=n*5//3+5
    print(n, flush=True)
    q=0
    while True:
        line=read_line()
        if line is None: return fail(output,args.mode,name,"participant exited before final answer",query_count=q)
        parts=line.split()
        if not parts: continue
        if parts[0] == "?":
            vals=ints_from_line(" ".join(parts[1:])); q += 1
            if q > limit: return fail(output,args.mode,name,"query limit exceeded",query_count=q)
            if len(vals) != 2 or vals[0] == vals[1] or any(x < 1 or x > n for x in vals): return fail(output,args.mode,name,"invalid comparison query",query_count=q)
            i,j=vals
            print("<" if array[i-1] < array[j-1] else ">", flush=True)
        elif parts[0] == "!":
            vals=ints_from_line(" ".join(parts[1:]))
            if len(vals) != n or sorted(vals) != list(range(1,n+1)): return fail(output,args.mode,name,"final answer is not a permutation",query_count=q)
            if vals != array: return fail(output,args.mode,name,"wrong final array",query_count=q)
            ratio=max(0.2,min(1.0,0.8+0.2*(1.0-q/limit)))
            write_result(output,args.mode,name,status="passed",score=100.0*ratio,correctness=1,total=1,query_count=q,protocol_errors=0,logs=[f"solved in {q} queries"]); return 0
        else:
            return fail(output,args.mode,name,"unknown command",query_count=q)

if __name__ == "__main__": raise SystemExit(main())
