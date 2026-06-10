from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

MAX_LINE_CHARS = 200000
MAX_LOG_CHARS = 4000
N_SOURCE = 5000
QUERY_LIMIT = 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Frontier-CS moving mole interactor logic")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--session-input-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    return parser.parse_args()


def cap(text: str, limit: int = MAX_LOG_CHARS) -> str:
    text = text.replace("\x00", "")
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


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


def read_line() -> str | None:
    line = sys.stdin.readline(MAX_LINE_CHARS + 1)
    if line == "":
        return None
    if len(line) > MAX_LINE_CHARS:
        raise ValueError("participant line is too long")
    return line.rstrip("\n")


def parse_source_case(input_text: str, answer_text: str) -> tuple[int, list[tuple[int, int]], int, int]:
    tokens = input_text.split()
    if not tokens:
        raise ValueError("empty source input")
    pos = 0
    t = int(tokens[pos])
    pos += 1
    if t != 1:
        raise ValueError(f"source interactor expects t=1, got {t}")
    n = int(tokens[pos])
    pos += 1
    if n != N_SOURCE:
        raise ValueError(f"source interactor expects n={N_SOURCE}, got {n}")
    edges: list[tuple[int, int]] = []
    for _ in range(n - 1):
        x = int(tokens[pos])
        y = int(tokens[pos + 1])
        pos += 2
        if not (1 <= x <= n and 1 <= y <= n):
            raise ValueError("edge endpoint is out of range")
        edges.append((x, y))
    target = int(tokens[pos])
    if not (1 <= target <= n):
        raise ValueError("hidden target is out of range")
    answer_tokens = answer_text.split()
    if not answer_tokens:
        raise ValueError("missing source best-depth answer")
    best = int(answer_tokens[0])
    if best <= 0:
        raise ValueError("source best-depth answer must be positive")
    return n, edges, target, best


def generated_source_case(config: dict[str, Any]) -> tuple[int, list[tuple[int, int]], int, int]:
    kind = config.get("kind")
    if kind != "two_branch_smoke":
        raise ValueError(f"unsupported generated source case kind {kind!r}")
    target = int(config.get("target", 2))
    best = int(config.get("best", 1))
    # A deterministic 5000-node tree matching the source interactor's exact n.
    # Node 2 is a leaf child of root; nodes 3..5000 form a separate chain.
    edges = [(1, 2), (1, 3)]
    edges.extend((node - 1, node) for node in range(4, N_SOURCE + 1))
    return N_SOURCE, edges, target, best


def load_case(case: dict[str, Any], session_input_dir: Path) -> tuple[int, list[tuple[int, int]], int, int]:
    generated = case.get("generated_input")
    if isinstance(generated, dict):
        return generated_source_case(generated)
    input_path = session_input_dir / str(case.get("input_path", ""))
    answer_path = session_input_dir / str(case.get("answer_path", ""))
    if not input_path.is_file() or not answer_path.is_file():
        raise FileNotFoundError("case is missing input or answer file")
    return parse_source_case(
        input_path.read_text(encoding="utf-8"),
        answer_path.read_text(encoding="utf-8"),
    )


def parent_and_depth(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    adj = [[] for _ in range(n + 1)]
    for x, y in edges:
        adj[x].append(y)
        adj[y].append(x)
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    parent[1] = 1
    queue: deque[int] = deque([1])
    seen = [False] * (n + 1)
    seen[1] = True
    while queue:
        node = queue.popleft()
        for nxt in adj[node]:
            if seen[nxt]:
                continue
            seen[nxt] = True
            parent[nxt] = node
            depth[nxt] = depth[node] + 1
            queue.append(nxt)
    if not all(seen[1:]):
        raise ValueError("source input is not connected")
    return parent, depth


def in_current_subtree(parent: list[int], target: int, query: int) -> bool:
    node = target
    while node != 1 and node != query:
        node = parent[node]
    return node == query


def source_score(best: int, depth_cost: int) -> tuple[float, float]:
    raw = (3.0 * best - float(depth_cost)) / (2.0 * best)
    unbounded = max(0.0, raw)
    bounded = min(1.0, max(0.0, raw))
    return bounded, unbounded


def write_result(
    output_path: Path,
    mode: str,
    session_name: str,
    case_results: list[dict[str, Any]],
    logs: list[str],
) -> None:
    total = len(case_results)
    passed = sum(1 for result in case_results if not result.get("protocol_error"))
    score = round(sum(result["score"] for result in case_results) / total, 6) if total else 0.0
    source_ratio = round(score / 100.0, 8)
    protocol_errors = sum(1 for result in case_results if result.get("protocol_error"))
    query_count = sum(float(result.get("query_count", 0.0)) for result in case_results)
    depth_cost = sum(float(result.get("depth_cost", 0.0)) for result in case_results)
    status = "passed" if total > 0 and protocol_errors == 0 else "failed"
    summary = {
        "score": score,
        "passed": passed,
        "total": total,
        "protocol_errors": protocol_errors,
        "query_count": query_count,
        "depth_cost": depth_cost,
    }
    payload: dict[str, Any] = {
        "status": status,
        "mode": mode,
        "aggregate_metrics": [
            {"metric_name": "score", "value": score},
            {"metric_name": "source_ratio", "value": source_ratio},
            {"metric_name": "case_count", "value": total},
            {"metric_name": "protocol_errors", "value": protocol_errors},
            {"metric_name": "query_count", "value": query_count},
            {"metric_name": "depth_cost", "value": depth_cost},
        ],
        "run_metrics": [
            {
                "run_name": result["case_name"],
                "metrics": [
                    {"metric_name": "score", "value": result["score"]},
                    {"metric_name": "source_ratio", "value": result["source_ratio"]},
                    {"metric_name": "protocol_errors", "value": 1 if result.get("protocol_error") else 0},
                    {"metric_name": "query_count", "value": result.get("query_count", 0.0)},
                    {"metric_name": "depth_cost", "value": result.get("depth_cost", 0.0)},
                ],
            }
            for result in case_results
        ],
        "public_results": [],
        "logs": [cap(entry, 1000) for entry in logs[:12]],
    }
    if mode == "validation":
        payload["validation_summary"] = summary
        payload["public_results"] = [
            {
                "case_name": result["case_name"],
                "status": "failed" if result.get("protocol_error") else "passed",
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
                "query_count": 0.0,
                "depth_cost": 0.0,
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


def run_case(case_name: str, n: int, edges: list[tuple[int, int]], target: int, best: int) -> dict[str, Any]:
    parent, depth = parent_and_depth(n, edges)
    print(1, flush=True)
    print(n, flush=True)
    for x, y in edges:
        print(f"{x} {y}", flush=True)

    query_count = 0
    depth_cost = 0
    current = target
    while True:
        line = read_line()
        if line is None:
            return {
                "case_name": case_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "query_count": query_count,
                "depth_cost": depth_cost,
                "protocol_error": True,
                "message": "participant exited before final answer",
            }
        parts = line.split()
        if len(parts) != 2 or parts[0] not in {"?", "!"}:
            return {
                "case_name": case_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "query_count": query_count,
                "depth_cost": depth_cost,
                "protocol_error": True,
                "message": f"invalid operation line: {cap(line, 120)}",
            }
        try:
            value = int(parts[1])
        except ValueError:
            return {
                "case_name": case_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "query_count": query_count,
                "depth_cost": depth_cost,
                "protocol_error": True,
                "message": "operation argument must be an integer",
            }
        if not (1 <= value <= n):
            return {
                "case_name": case_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "query_count": query_count,
                "depth_cost": depth_cost,
                "protocol_error": True,
                "message": "operation argument is out of range",
            }
        if parts[0] == "?":
            query_count += 1
            if query_count > QUERY_LIMIT:
                return {
                    "case_name": case_name,
                    "score": 0.0,
                    "source_ratio": 0.0,
                    "query_count": query_count,
                    "depth_cost": depth_cost,
                    "protocol_error": True,
                    "message": "too many queries",
                }
            depth_cost += depth[value]
            if in_current_subtree(parent, current, value):
                print(1, flush=True)
            else:
                print(0, flush=True)
                current = parent[current]
            continue

        if value != current:
            return {
                "case_name": case_name,
                "score": 0.0,
                "source_ratio": 0.0,
                "query_count": query_count,
                "depth_cost": depth_cost,
                "protocol_error": True,
                "message": f"wrong node, expected {current}, output {value}",
            }
        bounded, unbounded = source_score(best, depth_cost)
        score = round(100.0 * bounded, 6)
        return {
            "case_name": case_name,
            "score": score,
            "source_ratio": round(bounded, 8),
            "query_count": query_count,
            "depth_cost": depth_cost,
            "protocol_error": False,
            "message": f"Ratio: {bounded:.3f}, RatioUnbounded: {unbounded:.3f}",
        }


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

    logs: list[str] = []
    case_results: list[dict[str, Any]] = []
    session_input_dir = Path(args.session_input_dir)
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            failure_result(output_path, args.mode, session_name, f"case {index} is not an object")
            signal_session_end()
            return 0
        case_name = str(case.get("case_name", f"case-{index}"))
        try:
            n, edges, target, best = load_case(case, session_input_dir)
        except Exception as exc:
            failure_result(output_path, args.mode, session_name, f"case {case_name} is invalid: {exc}")
            signal_session_end()
            return 0
        result = run_case(case_name, n, edges, target, best)
        case_results.append(result)
        logs.append(f"{case_name}: {result['message']}")
        if result.get("protocol_error"):
            break

    signal_session_end()
    write_result(output_path, args.mode, session_name, case_results, logs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
