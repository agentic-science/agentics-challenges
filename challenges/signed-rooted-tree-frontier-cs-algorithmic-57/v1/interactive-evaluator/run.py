
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


def score_for(q: int, n: int) -> float:
    if q <= n: return 100.0
    if q >= n + 1000: return 0.0
    return 100.0 * (n + 1000 - q) / 1000.0


def build_parent(n: int, edges: list[list[int]], root: int) -> tuple[list[int], list[list[int]]]:
    graph=[[] for _ in range(n+1)]
    for u,v in edges:
        graph[u].append(v); graph[v].append(u)
    parent=[0]*(n+1); order=[root]; parent[root]=-1
    for u in order:
        for v in graph[u]:
            if parent[v] == 0:
                parent[v]=u; order.append(v)
    return parent, graph


def path_sums(n: int, graph: list[list[int]], root: int, values: list[int]) -> list[int]:
    sums=[0]*(n+1); parent=[0]*(n+1); parent[root]=-1; stack=[root]; sums[root]=values[root]
    while stack:
        u=stack.pop()
        for v in graph[u]:
            if parent[v] == 0:
                parent[v]=u; sums[v]=sums[u]+values[v]; stack.append(v)
    return sums


def main() -> int:
    args=parse_args(); output=Path(args.output_path)
    try:
        session=load_session(Path(args.session_file)); name=str(session["session_name"]); cases=session["metadata"]["cases"]
    except Exception as exc: return fail(output,args.mode,"unknown",f"invalid session: {exc}")
    print(len(cases), flush=True)
    total_q=0; solved=0; scores=[]; logs=[]
    for ci, case in enumerate(cases,1):
        n=int(case["n"]); edges=[[int(a),int(b)] for a,b in case["edges"]]; root=int(case["root"])
        values=[0]+[int(x) for x in case["values"]]
        _, graph=build_parent(n, edges, root)
        sums=path_sums(n, graph, root, values)
        print(n, flush=True)
        for u,v in edges: print(u, v, flush=True)
        q=0
        while True:
            line=read_line()
            if line is None: return fail(output,args.mode,name,"participant exited before final answer",total=len(cases),query_count=total_q+q,correctness=solved)
            parts=line.split()
            if not parts: continue
            if parts[0] == "?":
                vals=ints_from_line(" ".join(parts[1:])); q += 1
                if not vals or vals[0] not in (1,2): return fail(output,args.mode,name,"invalid query type",total=len(cases),query_count=total_q+q,correctness=solved)
                if vals[0] == 1:
                    if len(vals) < 2: return fail(output,args.mode,name,"missing type-1 size",total=len(cases),query_count=total_q+q,correctness=solved)
                    m=vals[1]; nodes=vals[2:]
                    if not (1 <= m <= n) or len(nodes) != m or any(x < 1 or x > n for x in nodes): return fail(output,args.mode,name,"invalid type-1 query",total=len(cases),query_count=total_q+q,correctness=solved)
                    print(sum(sums[x] for x in nodes), flush=True)
                else:
                    if len(vals) != 2 or not (1 <= vals[1] <= n): return fail(output,args.mode,name,"invalid toggle query",total=len(cases),query_count=total_q+q,correctness=solved)
                    x=vals[1]; values[x] = -values[x]; sums=path_sums(n, graph, root, values)
            elif parts[0] == "!":
                vals=ints_from_line(" ".join(parts[1:]))
                if len(vals) != n or any(x not in (-1,1) for x in vals): return fail(output,args.mode,name,"invalid final sign vector",total=len(cases),query_count=total_q+q,correctness=solved)
                if vals != values[1:]: return fail(output,args.mode,name,f"wrong signs on case {ci}",total=len(cases),query_count=total_q+q,correctness=solved)
                scores.append(score_for(q,n)); total_q += q; solved += 1; logs.append(f"case {ci}: solved in {q} queries"); break
            else:
                return fail(output,args.mode,name,"unknown command",total=len(cases),query_count=total_q+q,correctness=solved)
    write_result(output,args.mode,name,status="passed",score=min(scores) if scores else 0.0,correctness=solved,total=len(cases),query_count=total_q,protocol_errors=0,logs=logs)
    return 0

if __name__ == "__main__": raise SystemExit(main())
