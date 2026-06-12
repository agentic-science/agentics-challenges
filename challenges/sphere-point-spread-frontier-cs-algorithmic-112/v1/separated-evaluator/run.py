from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score Frontier-CS migrated outputs")
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


def run_case_has(run: dict[str, Any], key: str) -> bool:
    return key in run_case_metadata(run)


def run_case_get(run: dict[str, Any], key: str, default: Any = None) -> Any:
    return run_case_metadata(run).get(key, default)


def run_case_required(run: dict[str, Any], key: str) -> Any:
    metadata = run_case_metadata(run)
    if key not in metadata:
        raise ValueError(f"run {run.get('run_name', '<unknown>')} metadata is missing {key}")
    return metadata[key]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    try:
        payload = load_json(path)
    except Exception:
        return {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}
    return payload if isinstance(payload, dict) else {"exit_code": 1, "timed_out": False, "wall_time_ms": 0}


def ints(text: str) -> list[int]:
    return [int(token) for token in text.split()]


def floats(text: str) -> list[float]:
    return [float(token) for token in text.split()]


def parse_first_int(text: str, default: int = 0) -> int:
    tokens = text.split()
    return int(tokens[0]) if tokens else default


def clamp01(value: float) -> float:
    if not math.isfinite(value):
        return 0.0
    return max(0.0, min(1.0, value))


def score_from_ratio(ratio: float) -> float:
    return round(100.0 * clamp01(ratio), 6)


def validate_knight_path(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    data = ints(input_text)
    if len(data) < 3:
        raise ValueError("input must contain N r c")
    n, r0, c0 = data[:3]
    best_len = max(1, parse_first_int(answer_text, 1))
    out = ints(output_text)
    if not out:
        return 0.0, {"path_length": 0, "reference_length": best_len}, "empty output"
    length = out[0]
    if length < 0 or length > n * n:
        raise ValueError(f"invalid path length {length}")
    coords = out[1:]
    if len(coords) < 2 * length:
        raise ValueError(f"declared {length} cells but output ended early")
    if length == 0:
        return 0.0, {"path_length": 0, "reference_length": best_len}, "valid zero-length path"
    path = [(coords[i], coords[i + 1]) for i in range(0, 2 * length, 2)]
    if path[0] != (r0, c0):
        raise ValueError(f"path starts at {path[0]}, expected {(r0, c0)}")
    seen: set[tuple[int, int]] = set()
    for idx, (r, c) in enumerate(path):
        if r < 1 or r > n or c < 1 or c > n:
            raise ValueError(f"cell {(r, c)} at step {idx + 1} is out of bounds")
        if (r, c) in seen:
            raise ValueError(f"cell {(r, c)} is revisited")
        seen.add((r, c))
        if idx:
            pr, pc = path[idx - 1]
            dr, dc = abs(r - pr), abs(c - pc)
            if not ((dr == 1 and dc == 2) or (dr == 2 and dc == 1)):
                raise ValueError(f"illegal knight move from {(pr, pc)} to {(r, c)}")
    ratio = length / best_len if best_len else 0.0
    return ratio, {"path_length": length, "reference_length": best_len}, "valid knight path"


DIGIT_H = 8
DIGIT_W = 14
DIGIT_NEIGHBORS: list[list[int]] = []
for y in range(DIGIT_H):
    for x in range(DIGIT_W):
        here: list[int] = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < DIGIT_H and 0 <= nx < DIGIT_W:
                    here.append(ny * DIGIT_W + nx)
        DIGIT_NEIGHBORS.append(here)


def parse_digit_grid(text: str) -> list[str]:
    rows = text.split()
    if len(rows) < DIGIT_H:
        raise ValueError(f"expected {DIGIT_H} digit rows, found {len(rows)}")
    rows = rows[:DIGIT_H]
    for idx, row in enumerate(rows):
        if len(row) != DIGIT_W or any(ch < '0' or ch > '9' for ch in row):
            raise ValueError(f"row {idx + 1} must contain exactly {DIGIT_W} digits")
    return rows


def digit_prefix_score(rows: list[str], cap: int | None = None) -> int:
    flat = ''.join(rows)
    by_digit = {str(d): [idx for idx, ch in enumerate(flat) if ch == str(d)] for d in range(10)}

    def can_read(s: str) -> bool:
        frontier = set(by_digit.get(s[0], []))
        if not frontier:
            return False
        for ch in s[1:]:
            need = by_digit.get(ch, [])
            if not need:
                return False
            need_set = set(need)
            nxt: set[int] = set()
            for u in frontier:
                for v in DIGIT_NEIGHBORS[u]:
                    if v in need_set:
                        nxt.add(v)
            if not nxt:
                return False
            frontier = nxt
        return True

    x = 0
    k = 1
    while True:
        if cap is not None and k > cap:
            return cap
        if can_read(str(k)):
            x = k
            k += 1
        else:
            return x


def validate_digit_grid(_input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    best = digit_prefix_score(parse_digit_grid(answer_text))
    yours = digit_prefix_score(parse_digit_grid(output_text), best)
    ratio = 1.0 if best == 0 and yours == 0 else (yours / best if best else 0.0)
    return ratio, {"readable_prefix": yours, "reference_prefix": best}, "valid digit grid"


def validate_xor_set(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n = ints(input_text)[0]
    best = max(1, parse_first_int(answer_text, 1))
    out = ints(output_text)
    if not out:
        raise ValueError("missing set size")
    m = out[0]
    if m < 0 or m > n:
        raise ValueError(f"invalid set size {m}")
    values = out[1:1 + m]
    if len(values) < m:
        raise ValueError(f"declared {m} values but output ended early")
    if len(set(values)) != len(values):
        raise ValueError("set contains duplicate values")
    if any(value < 1 or value > n for value in values):
        raise ValueError("set value outside 1..n")
    seen: set[int] = set()
    for i, a in enumerate(values):
        for b in values[i + 1:]:
            x = a ^ b
            if x in seen:
                raise ValueError(f"duplicate pairwise xor {x}")
            seen.add(x)
    ratio = m / best if best else 0.0
    return ratio, {"set_size": m, "reference_size": best}, "valid XOR-distinct set"


def validate_sphere_spread(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n = ints(input_text)[0]
    ref = max(float(answer_text.split()[0]), 1e-12)
    values = floats(output_text)
    expected_values = 1 + 3 * n
    if len(values) != expected_values:
        raise ValueError(f"expected exactly {expected_values} numeric values, found {len(values)}")
    claimed = values[0]
    if claimed < 0:
        raise ValueError("claimed minimum distance cannot be negative")
    pts = [(values[1 + 3 * i], values[2 + 3 * i], values[3 + 3 * i]) for i in range(n)]
    for idx, (x, y, z) in enumerate(pts):
        if x * x + y * y + z * z > 1.0 + 1e-9:
            raise ValueError(f"point {idx + 1} lies outside the unit sphere")
    actual = float('inf')
    for i, (x1, y1, z1) in enumerate(pts):
        for x2, y2, z2 in pts[i + 1:]:
            actual = min(actual, math.dist((x1, y1, z1), (x2, y2, z2)))
    if actual == float('inf'):
        actual = 0.0
    if abs(actual - claimed) > 1e-6 * max(1.0, abs(actual), abs(claimed)):
        raise ValueError(f"claimed distance {claimed:.10f} does not match actual {actual:.10f}")
    return claimed / ref, {"min_distance": claimed, "reference_distance": ref}, "valid sphere placement"


def graph_from_input(input_text: str) -> tuple[int, list[tuple[int, int]]]:
    data = ints(input_text)
    if len(data) < 2:
        raise ValueError("graph input must start with N M")
    n, m = data[:2]
    raw_edges = data[2:]
    if len(raw_edges) < 2 * m:
        raise ValueError("graph input ended before all edges")
    edges = [(raw_edges[2 * i], raw_edges[2 * i + 1]) for i in range(m)]
    return n, edges


def read_binary_vector(output_text: str, n: int) -> list[int]:
    values = ints(output_text)
    if len(values) < n:
        raise ValueError(f"expected {n} binary values, found {len(values)}")
    values = values[:n]
    if any(value not in (0, 1) for value in values):
        raise ValueError("output values must be 0 or 1")
    return values


def validate_vertex_cover(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n, edges = graph_from_input(input_text)
    sol = read_binary_vector(output_text, n)
    for u, v in edges:
        if sol[u - 1] == 0 and sol[v - 1] == 0:
            raise ValueError(f"edge {u}-{v} is uncovered")
    k = sum(sol)
    ref = max(1, parse_first_int(answer_text, 1))
    ratio = ref / k if k else (1.0 if not edges else 0.0)
    return ratio, {"selected_vertices": k, "reference_vertices": ref}, "valid vertex cover"


def validate_independent_set(input_text: str, answer_text: str, output_text: str, complement_score: bool) -> tuple[float, dict[str, Any], str]:
    n, edges = graph_from_input(input_text)
    sol = read_binary_vector(output_text, n)
    for u, v in edges:
        if sol[u - 1] == 1 and sol[v - 1] == 1:
            raise ValueError(f"edge {u}-{v} has both endpoints selected")
    k = sum(sol)
    ref = parse_first_int(answer_text, 0)
    if complement_score:
        denom = n - k
        ratio = (n - ref) / denom if denom else 0.0
    else:
        ratio = k / ref if ref else (1.0 if k == 0 else 0.0)
    return ratio, {"selected_vertices": k, "reference_vertices": ref}, "valid independent set"


def validate_clique(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n, edges = graph_from_input(input_text)
    edge_set = {tuple(sorted(edge)) for edge in edges}
    sol = read_binary_vector(output_text, n)
    selected = [idx + 1 for idx, value in enumerate(sol) if value == 1]
    for i, u in enumerate(selected):
        for v in selected[i + 1:]:
            if tuple(sorted((u, v))) not in edge_set:
                raise ValueError(f"selected vertices {u} and {v} are not adjacent")
    ref = parse_first_int(answer_text, 0)
    ratio = len(selected) / ref if ref else (1.0 if not selected else 0.0)
    return ratio, {"selected_vertices": len(selected), "reference_vertices": ref}, "valid clique"


def validate_coloring(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n, edges = graph_from_input(input_text)
    colors = ints(output_text)
    if len(colors) < n:
        raise ValueError(f"expected {n} colors, found {len(colors)}")
    colors = colors[:n]
    for u, v in edges:
        if colors[u - 1] == colors[v - 1]:
            raise ValueError(f"adjacent vertices {u} and {v} share a color")
    used = len(set(colors))
    ref = max(1, parse_first_int(answer_text, 1))
    return ref / used, {"used_colors": used, "reference_colors": ref}, "valid coloring"


def validate_clique_cover(input_text: str, answer_text: str, output_text: str) -> tuple[float, dict[str, Any], str]:
    n, edges = graph_from_input(input_text)
    edge_set = {tuple(sorted(edge)) for edge in edges}
    group_ids = ints(output_text)
    if len(group_ids) < n:
        raise ValueError(f"expected {n} clique ids, found {len(group_ids)}")
    group_ids = group_ids[:n]
    groups: dict[int, list[int]] = {}
    for vertex, group_id in enumerate(group_ids, start=1):
        groups.setdefault(group_id, []).append(vertex)
    for group_id, nodes in groups.items():
        for i, u in enumerate(nodes):
            for v in nodes[i + 1:]:
                if tuple(sorted((u, v))) not in edge_set:
                    raise ValueError(f"vertices {u} and {v} in group {group_id} are not adjacent")
    used = len(groups)
    ref = max(1, parse_first_int(answer_text, 1))
    return ref / used, {"used_cliques": used, "reference_cliques": ref}, "valid clique cover"


VALIDATORS = {
    "knight_path": lambda i, a, o: validate_knight_path(i, a, o),
    "digit_grid_prefix": lambda i, a, o: validate_digit_grid(i, a, o),
    "distinct_xor_set": lambda i, a, o: validate_xor_set(i, a, o),
    "sphere_spread": lambda i, a, o: validate_sphere_spread(i, a, o),
    "vertex_cover": lambda i, a, o: validate_vertex_cover(i, a, o),
    "independent_set_complement": lambda i, a, o: validate_independent_set(i, a, o, True),
    "maximum_independent_set": lambda i, a, o: validate_independent_set(i, a, o, False),
    "maximum_clique": lambda i, a, o: validate_clique(i, a, o),
    "graph_coloring": lambda i, a, o: validate_coloring(i, a, o),
    "clique_cover": lambda i, a, o: validate_clique_cover(i, a, o),
}


def score_run(run: dict[str, Any], challenge_dir: Path, solution_runs_dir: Path) -> tuple[dict[str, Any], list[str]]:
    run_name = run["run_name"]
    run_dir = solution_runs_dir / run_name
    metadata = run_metadata(run_dir / "agentics-run.json")
    wall_time_ms = float(metadata.get("wall_time_ms", 0))
    base = {"case_name": run_name, "wall_time_ms": wall_time_ms}
    if metadata.get("timed_out") is True:
        return {**base, "status": "error", "score": 0.0, "message": "solution timed out"}, [f"{run_name}: solution timed out"]
    if metadata.get("exit_code", 0) != 0:
        return {**base, "status": "error", "score": 0.0, "message": f"solution exited with code {metadata.get('exit_code')}"}, [f"{run_name}: nonzero solution exit"]
    output_path = run_dir / "output" / "answer.txt"
    if not output_path.is_file():
        return {**base, "status": "error", "score": 0.0, "message": "missing output/answer.txt"}, [f"{run_name}: missing output/answer.txt"]
    try:
        input_text = load_text(challenge_dir / str(run_case_required(run, "input_path")))
        answer_text = load_text(challenge_dir / str(run_case_required(run, "answer_path")))
        output_text = load_text(output_path)
        ratio, details, message = VALIDATORS[str(run_case_required(run, "task_type"))](input_text, answer_text, output_text)
        score = score_from_ratio(ratio)
        return {**base, "status": "passed", "score": score, "ratio": round(clamp01(ratio), 8), "message": message, **details}, [f"{run_name}: {message}; score={score}"]
    except Exception as error:
        return {**base, "status": "failed", "score": 0.0, "ratio": 0.0, "message": str(error)}, [f"{run_name}: {error}"]


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    valid = sum(1 for result in results if result["status"] == "passed")
    score = round(sum(float(result.get("score", 0.0)) for result in results) / total, 6) if total else 0.0
    return {"score": score, "valid_cases": valid, "total_cases": total, "passed": valid, "total": total}


def main() -> int:
    args = parse_args()
    runs = load_json(Path(args.runs_file))["runs"]
    results: list[dict[str, Any]] = []
    logs: list[str] = []
    for run in runs:
        result, run_logs = score_run(run, Path(args.challenge_dir), Path(args.solution_runs_dir))
        results.append(result)
        logs.extend(run_logs)
    summary = aggregate(results)
    payload: dict[str, Any] = {
        "status": "passed" if summary["valid_cases"] == summary["total_cases"] and summary["total_cases"] > 0 else "failed",
        "mode": args.mode,
        "aggregate_metrics": [
            {"metric_name": "score", "value": summary["score"]},
            {"metric_name": "valid_cases", "value": summary["valid_cases"]},
            {"metric_name": "total_cases", "value": summary["total_cases"]},
        ],
        "run_metrics": [
            {"run_name": result["case_name"], "metrics": [{"metric_name": "score", "value": result.get("score", 0.0)}]}
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
