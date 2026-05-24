from __future__ import annotations

import argparse
import json
import random
import struct
import subprocess
import sys
from pathlib import Path
from typing import Iterable

INPUT_MAGIC = b"AGMMIN1\0"
OUTPUT_MAGIC = b"AGMMOUT1"
INPUT_HEADER = struct.Struct("<8sIIII")
OUTPUT_HEADER = struct.Struct("<8sIII")
NUMPY_VERSION = "2.2.6"
PYTHON_GENERATOR_WORK_LIMIT = 5_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set up official matrix multiplication benchmark files."
    )
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--setup-dir", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--runs-file", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    challenge_dir = Path(args.challenge_dir)
    setup_dir = Path(args.setup_dir)
    runs_file = Path(args.runs_file)

    config = load_config(challenge_dir)
    generated_runs = []
    for run in config["runs"]:
        run_name = run["run_name"]
        input_path = setup_dir / "inputs" / f"{run_name}.bin"
        expected_path = setup_dir / "expected" / f"{run_name}.bin"
        generate_dataset(
            input_path,
            expected_path,
            cases=int(run["cases"]),
            m=int(run["m"]),
            k=int(run["k"]),
            n=int(run["n"]),
            seed=int(run["seed"]),
        )
        generated_runs.append(
            {
                "run_name": run_name,
                "interface": "file_system",
                "input_files": [
                    {"path": "input.bin", "source_path": f"inputs/{run_name}.bin"}
                ],
                "output_files": ["output.bin"],
                "expected_output_source_path": f"/setup/expected/{run_name}.bin",
                "tolerance_abs": float(run.get("tolerance_abs", 0.001)),
                "tolerance_rel": float(run.get("tolerance_rel", 0.0001)),
            }
        )

    runs_file.parent.mkdir(parents=True, exist_ok=True)
    runs_file.write_text(json.dumps({"runs": generated_runs}, indent=2), encoding="utf-8")
    return 0


def load_config(challenge_dir: Path) -> dict[str, object]:
    config_path = challenge_dir / "private-benchmark" / "config.json"
    if not config_path.is_file():
        raise FileNotFoundError(
            "official preparation requires private-benchmark/config.json from the private seed overlay"
        )
    loaded = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or not isinstance(loaded.get("runs"), list):
        raise ValueError("private-benchmark/config.json must contain a runs array")
    return loaded


def generate_dataset(
    input_path: Path,
    expected_path: Path,
    *,
    cases: int,
    m: int,
    k: int,
    n: int,
    seed: int,
) -> None:
    input_path.parent.mkdir(parents=True, exist_ok=True)
    expected_path.parent.mkdir(parents=True, exist_ok=True)

    np = load_numpy_if_needed(cases * m * k * n)
    if np is not None:
        generate_dataset_numpy(input_path, expected_path, cases, m, k, n, seed, np)
    else:
        generate_dataset_python(input_path, expected_path, cases, m, k, n, seed)


def load_numpy_if_needed(work: int):
    try:
        import numpy as np

        return np
    except ModuleNotFoundError:
        if work <= PYTHON_GENERATOR_WORK_LIMIT:
            return None

    subprocess.run(
        [sys.executable, "-m", "pip", "install", f"numpy=={NUMPY_VERSION}"],
        check=True,
    )
    import numpy as np

    return np


def generate_dataset_numpy(
    input_path: Path,
    expected_path: Path,
    cases: int,
    m: int,
    k: int,
    n: int,
    seed: int,
    np: object,
) -> None:
    rng = np.random.default_rng(seed)
    batch_size = max(1, min(128, cases))
    with input_path.open("wb") as input_file, expected_path.open("wb") as expected_file:
        input_file.write(INPUT_HEADER.pack(INPUT_MAGIC, cases, m, k, n))
        expected_file.write(OUTPUT_HEADER.pack(OUTPUT_MAGIC, cases, m, n))
        for start in range(0, cases, batch_size):
            count = min(batch_size, cases - start)
            a = rng.uniform(-1.0, 1.0, size=(count, m, k)).astype("<f4")
            b = rng.uniform(-1.0, 1.0, size=(count, k, n)).astype("<f4")
            c = (a @ b).astype("<f4")
            a.tofile(input_file)
            b.tofile(input_file)
            c.tofile(expected_file)


def generate_dataset_python(
    input_path: Path,
    expected_path: Path,
    cases: int,
    m: int,
    k: int,
    n: int,
    seed: int,
) -> None:
    rng = random.Random(seed)
    with input_path.open("wb") as input_file, expected_path.open("wb") as expected_file:
        input_file.write(INPUT_HEADER.pack(INPUT_MAGIC, cases, m, k, n))
        expected_file.write(OUTPUT_HEADER.pack(OUTPUT_MAGIC, cases, m, n))
        for _ in range(cases):
            a = [rng.uniform(-1.0, 1.0) for _ in range(m * k)]
            b = [rng.uniform(-1.0, 1.0) for _ in range(k * n)]
            input_file.write(pack_f32(a))
            input_file.write(pack_f32(b))
            expected_file.write(pack_f32(matmul(a, b, m, k, n)))


def matmul(a: list[float], b: list[float], m: int, k: int, n: int) -> Iterable[float]:
    out: list[float] = []
    for row in range(m):
        row_offset = row * k
        for col in range(n):
            acc = 0.0
            for inner in range(k):
                acc += a[row_offset + inner] * b[inner * n + col]
            out.append(acc)
    return out


def pack_f32(values: Iterable[float]) -> bytes:
    values = list(values)
    return struct.pack(f"<{len(values)}f", *values)


if __name__ == "__main__":
    raise SystemExit(main())
