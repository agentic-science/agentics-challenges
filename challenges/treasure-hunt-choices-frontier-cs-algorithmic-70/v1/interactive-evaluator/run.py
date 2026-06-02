
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


def uses_runtime_random(metadata: dict[str, Any]) -> bool:
    policy = metadata.get("runtime_random")
    if not isinstance(policy, dict):
        return False
    if policy.get("kind") != "treasure_hunt_choices":
        raise ValueError("unsupported runtime_random kind")
    return True


def main() -> int:
    args=parse_args(); output=Path(args.output_path)
    try:
        session=load_session(Path(args.session_file)); name=str(session["session_name"]); metadata=session["metadata"]; cases=metadata["cases"]; runtime_random=uses_runtime_random(metadata)
    except Exception as exc: return fail(output,args.mode,"unknown",f"invalid session: {exc}")
    print(len(cases), flush=True)
    total_moves=0; solved=0; score_sum=0.0; logs=[]
    for ci, case in enumerate(cases,1):
        n=int(case["n"]); m=int(case["m"]); start=int(case["start"]); base=int(case["base_move_count"]); seed=int(case.get("shuffle_seed", ci))
        edges=[[int(a),int(b)] for a,b in case["edges"]]
        print(n, m, start, base, flush=True)
        adj=[[] for _ in range(n+1)]
        for u,v in edges:
            adj[u].append(v); adj[v].append(u); print(u, v, flush=True)
        degrees=[0]+[len(adj[i]) for i in range(1,n+1)]
        rng=random.SystemRandom() if runtime_random else random.Random(seed); curr=start; visited=[False]*(n+1); visited[curr]=True; seen=1; moves=0; limit=2*base
        while moves < limit and seen < n:
            neigh=list(adj[curr]); rng.shuffle(neigh)
            fields=[str(len(neigh))]
            for node in neigh: fields.extend([str(degrees[node]), "1" if visited[node] else "0"])
            print(" ".join(fields), flush=True)
            line=read_line()
            if line is None: return fail(output,args.mode,name,"participant exited during traversal",total=len(cases),query_count=total_moves+moves,correctness=solved)
            vals=ints_from_line(line)
            if len(vals) != 1 or not (1 <= vals[0] <= len(neigh)): return fail(output,args.mode,name,"invalid choice index",total=len(cases),query_count=total_moves+moves,correctness=solved)
            curr=neigh[vals[0]-1]; moves += 1
            if not visited[curr]: visited[curr]=True; seen += 1
        total_moves += moves
        if seen == n:
            print("AC", flush=True); solved += 1
            if moves <= base: score=1.0
            elif moves <= 2*base: score=((2.0*base-moves)/base)**2
            else: score=0.0
            score_sum += max(0.0,min(1.0,score)); logs.append(f"case {ci}: visited all vertices in {moves} moves")
        else:
            print("F", flush=True); logs.append(f"case {ci}: failed after {moves} moves")
    status="passed" if solved == len(cases) else "failed"
    write_result(output,args.mode,name,status=status,score=100.0*score_sum/len(cases) if cases else 0.0,correctness=solved,total=len(cases),query_count=total_moves,protocol_errors=0,logs=logs)
    return 0

if __name__ == "__main__": raise SystemExit(main())
