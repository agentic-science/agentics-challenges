
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


def main() -> int:
    args=parse_args(); output=Path(args.output_path)
    try:
        session=load_session(Path(args.session_file)); name=str(session["session_name"]); case=session["metadata"]["case"]
    except Exception as exc: return fail(output,args.mode,"unknown",f"invalid session: {exc}")
    n=int(case["n"]); m=int(case["m"]); adj=[[int(x) for x in row] for row in case["adj"]]
    print(m, flush=True)
    marker_type=["center"]*n; marker_pos=[0]*n; current=0; seen=[[False]*m for _ in range(n)]; count=0
    for q in range(50001):
        if count == n*m:
            print("treasure", flush=True)
            ratio=(50000-q)/50000.0
            write_result(output,args.mode,name,status="passed",score=100.0*max(0.0,ratio),correctness=1,total=1,query_count=q,protocol_errors=0,logs=[f"treasure found after {q} moves"]); return 0
        print(marker_type[current], flush=True)
        line=read_line()
        if line is None: return fail(output,args.mode,name,"participant exited before treasure",query_count=q)
        parts=line.split()
        if len(parts) != 3: return fail(output,args.mode,name,"move must be: c side t",query_count=q)
        try:
            c=int(parts[0]); t=int(parts[2])
        except ValueError:
            return fail(output,args.mode,name,"move indices must be integers",query_count=q)
        side=parts[1]
        if not (0 <= c < m) or side not in {"left","right"} or not (0 <= t < m): return fail(output,args.mode,name,"invalid cave move",query_count=q)
        edge=(marker_pos[current]+t)%m
        nxt=adj[current][edge]
        if not (0 <= nxt < n): return fail(output,args.mode,name,"session contains invalid adjacency",query_count=q)
        if not seen[current][edge]: seen[current][edge]=True; count += 1
        marker_type[current]=side; marker_pos[current]=(marker_pos[current]+c)%m; current=nxt
    return fail(output,args.mode,name,"too many moves",query_count=50001)

if __name__ == "__main__": raise SystemExit(main())
