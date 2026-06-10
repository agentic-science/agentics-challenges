from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import string
import subprocess
import sys
from pathlib import Path
from typing import Any


ALPHANUMERIC = string.ascii_letters + string.digits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate hello-world-rs submissions")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--workspace-dir", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--setup-dir")
    return parser.parse_args()


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_submission_metadata() -> dict[str, Any]:
    path = Path("/metadata/submission.json")
    if not path.is_file():
        fail("missing trusted submission metadata at /metadata/submission.json")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - evaluator diagnostics for malformed metadata.
        fail(f"invalid trusted submission metadata: {exc}")
    if not isinstance(payload, dict):
        fail("trusted submission metadata must be a JSON object")
    if payload.get("schema_version") != 1:
        fail("unsupported trusted submission metadata schema_version")
    for key in ["artifact_zip_bytes", "artifact_uncompressed_bytes", "artifact_file_count"]:
        value = payload.get(key)
        if not isinstance(value, int) or value < 0:
            fail(f"trusted submission metadata {key} must be a non-negative integer")
    digest = payload.get("artifact_sha256")
    if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
        fail("trusted submission metadata artifact_sha256 must use sha256:<hex>")
    return payload


def cargo_metadata(workspace_dir: Path) -> dict[str, Any]:
    manifest = workspace_dir / "Cargo.toml"
    if not manifest.is_file():
        fail("workspace must contain Cargo.toml at the root")
    completed = subprocess.run(
        [
            "cargo",
            "metadata",
            "--no-deps",
            "--format-version",
            "1",
            "--manifest-path",
            str(manifest),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        fail("cargo metadata failed: " + (completed.stderr or completed.stdout).strip()[:4000])
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cargo metadata produced invalid JSON: {exc}")
    if not isinstance(payload, dict):
        fail("cargo metadata payload must be an object")
    return payload


def binary_name(metadata: dict[str, Any]) -> str:
    packages = metadata.get("packages")
    if not isinstance(packages, list):
        fail("cargo metadata packages must be an array")
    bins: list[str] = []
    for package in packages:
        if not isinstance(package, dict):
            continue
        targets = package.get("targets")
        if not isinstance(targets, list):
            continue
        for target in targets:
            if not isinstance(target, dict):
                continue
            kind = target.get("kind")
            name = target.get("name")
            if isinstance(kind, list) and "bin" in kind and isinstance(name, str):
                bins.append(name)
    if len(bins) != 1:
        fail(f"workspace must define exactly one binary target, found {len(bins)}")
    return bins[0]


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def require_regular_file(path: Path, label: str) -> None:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        fail(f"missing {label}: {path}")
    if not path.is_file() or path.is_symlink():
        fail(f"{label} must be a regular file: {path}")
    if stat.st_size <= 0:
        fail(f"{label} must be non-empty: {path}")


def generated_name(mode: str) -> str:
    if mode == "validation":
        return "Agentics2026"
    length = secrets.randbelow(32) + 1
    return "".join(secrets.choice(ALPHANUMERIC) for _ in range(length))


def run_solution(workspace_dir: Path, output_dir: Path, mode: str) -> Path:
    run_dir = output_dir / "run"
    run_dir.mkdir(parents=True, exist_ok=True)
    target_dir = output_dir / "target"
    source_target = workspace_dir / "target"
    if not source_target.is_dir():
        fail("missing build output directory /workspace/target")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_target, target_dir, symlinks=True)

    metadata = cargo_metadata(workspace_dir)
    name = binary_name(metadata)
    binary = target_dir / "release" / name
    require_regular_file(binary, "pre-built release binary")
    before_size = binary.stat().st_size
    before_hash = file_sha256(binary)

    test_name = generated_name(mode)
    (run_dir / "name.txt").write_text(test_name, encoding="utf-8")
    hello_path = run_dir / "hello.txt"
    if hello_path.exists():
        hello_path.unlink()

    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(target_dir)
    completed = subprocess.run(
        [
            "cargo",
            "run",
            "--release",
            "--manifest-path",
            str(workspace_dir / "Cargo.toml"),
        ],
        cwd=run_dir,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        fail("cargo run failed: " + (completed.stderr or completed.stdout).strip()[:4000])

    require_regular_file(binary, "post-run release binary")
    after_size = binary.stat().st_size
    after_hash = file_sha256(binary)
    if before_size != after_size or before_hash != after_hash:
        fail("release binary changed after cargo run --release")

    if not hello_path.is_file():
        fail("solution did not create hello.txt")
    output = hello_path.read_text(encoding="utf-8", errors="replace")
    if output.endswith("\n"):
        output = output[:-1]
    expected = f"hello {test_name}"
    if output != expected:
        fail(f"hello.txt mismatch: expected {expected!r}, got {output!r}")
    return binary


def write_result(output_path: Path, mode: str, metadata: dict[str, Any], binary: Path) -> None:
    artifact_uncompressed_bytes = int(metadata["artifact_uncompressed_bytes"])
    binary_bytes = binary.stat().st_size
    size_product = artifact_uncompressed_bytes * binary_bytes
    summary = {"score": float(size_product), "passed": 1, "total": 1}
    payload: dict[str, Any] = {
        "status": "passed",
        "mode": mode,
        "aggregate_metrics": [
            {"metric_name": "size_product", "value": float(size_product)},
            {"metric_name": "artifact_uncompressed_bytes", "value": float(artifact_uncompressed_bytes)},
            {"metric_name": "binary_bytes", "value": float(binary_bytes)},
        ],
        "run_metrics": [
            {
                "run_name": "single-run",
                "metrics": [
                    {"metric_name": "size_product", "value": float(size_product)},
                    {"metric_name": "artifact_uncompressed_bytes", "value": float(artifact_uncompressed_bytes)},
                    {"metric_name": "binary_bytes", "value": float(binary_bytes)},
                ],
            }
        ],
        "public_results": [],
        "logs": [
            f"artifact_uncompressed_bytes={artifact_uncompressed_bytes}",
            f"binary_bytes={binary_bytes}",
            f"size_product={size_product}",
        ],
    }
    if mode == "validation":
        payload["validation_summary"] = summary
        payload["public_results"] = [
            {
                "case_name": "public-smoke",
                "status": "passed",
                "score": float(size_product),
                "message": "hello.txt matched the deterministic validation name",
            }
        ]
    else:
        payload["official_summary"] = summary
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    args = parse_args()
    output_path = Path(args.output_path)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = load_submission_metadata()
    binary = run_solution(Path(args.workspace_dir), output_dir, args.mode)
    write_result(output_path, args.mode, metadata, binary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
