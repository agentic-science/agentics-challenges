from __future__ import annotations

import argparse
import json
import random
import struct
import zipfile
from pathlib import Path
from typing import Iterable

INPUT_MAGIC = b"AGMMIN1\0"
OUTPUT_MAGIC = b"AGMMOUT1"
INPUT_HEADER = struct.Struct("<8sIIII")
OUTPUT_HEADER = struct.Struct("<8sIII")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate matrix multiplication validation data and private benchmark overlays."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="challenge root containing v1/",
    )
    parser.add_argument(
        "--preset",
        choices=["public", "official-config"],
        required=True,
        help="public writes committed validation data; official-config writes the private seed/config overlay",
    )
    parser.add_argument(
        "--square-cases",
        type=int,
        default=None,
        help="override case count for the square official run",
    )
    parser.add_argument(
        "--rect-cases",
        type=int,
        default=None,
        help="override case count for the rectangular official run",
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=None,
        help="optional path for a private benchmark ZIP overlay",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    challenge_root = args.root.resolve()
    if args.preset == "public":
        generate_public(challenge_root)
    else:
        generate_official_config(
            challenge_root,
            square_cases=args.square_cases or 5000,
            rect_cases=args.rect_cases or 5000,
        )
        if args.zip is not None:
            write_private_zip(challenge_root, args.zip)
    return 0


def generate_public(challenge_root: Path) -> None:
    version_root = challenge_root / "v1"
    generate_dataset(
        version_root / "public" / "inputs" / "public_square.bin",
        version_root / "public" / "expected" / "public_square.bin",
        cases=3,
        m=4,
        k=4,
        n=4,
        seed=101,
    )
    generate_dataset(
        version_root / "public" / "inputs" / "public_rectangular.bin",
        version_root / "public" / "expected" / "public_rectangular.bin",
        cases=3,
        m=3,
        k=2,
        n=5,
        seed=202,
    )


def generate_official_config(challenge_root: Path, square_cases: int, rect_cases: int) -> None:
    version_root = challenge_root / "v1"
    private_root = version_root / "private-benchmark"
    config = {
        "runs": [
            {
                "run_name": "square_100x100",
                "cases": square_cases,
                "m": 100,
                "k": 100,
                "n": 100,
                "seed": 1001,
                "tolerance_abs": 0.001,
                "tolerance_rel": 0.0001,
            },
            {
                "run_name": "rect_50x10_10x500",
                "cases": rect_cases,
                "m": 50,
                "k": 10,
                "n": 500,
                "seed": 2002,
                "tolerance_abs": 0.001,
                "tolerance_rel": 0.0001,
            },
        ]
    }
    (private_root).mkdir(parents=True, exist_ok=True)
    (private_root / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")


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

    try:
        import numpy as np
    except ModuleNotFoundError:
        np = None

    if np is not None:
        generate_dataset_numpy(input_path, expected_path, cases, m, k, n, seed, np)
        return

    work = cases * m * k * n
    if work > 5_000_000:
        raise SystemExit(
            "NumPy is required for large benchmark generation. Install numpy or use a small smoke case."
        )
    generate_dataset_python(input_path, expected_path, cases, m, k, n, seed)


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


def write_private_zip(challenge_root: Path, output_path: Path) -> None:
    private_root = challenge_root / "v1" / "private-benchmark"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(private_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(challenge_root / "v1"))


if __name__ == "__main__":
    raise SystemExit(main())
