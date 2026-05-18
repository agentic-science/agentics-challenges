from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHALLENGES_DIR = ROOT / "challenges"
PRIVATE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
    "secret",
    "secrets",
    "private",
    "private-benchmark",
    "private_benchmark",
    "heldout",
    "heldout-data",
    "reference-output",
    "reference-outputs",
}
PRIVATE_ASSET_KINDS = {
    "private_benchmark_data",
    "private_scorer_package",
    "private_seeds",
    "private_reference_outputs",
}
class ValidationError(Exception):
    pass


def main() -> int:
    challenge_roots = sorted(path for path in CHALLENGES_DIR.iterdir() if path.is_dir())
    if not challenge_roots:
        raise ValidationError("repository must contain at least one challenge")
    for challenge_root in challenge_roots:
        validate_challenge(challenge_root)
    print(f"validated {len(challenge_roots)} challenge(s)")
    return 0


def validate_challenge(challenge_root: Path) -> None:
    reject_private_files(challenge_root)
    manifest = load_json(challenge_root / "agentics.challenge.json")
    challenge_name = required_str(manifest, "challenge_name")
    if challenge_name != challenge_root.name:
        raise ValidationError(
            f"{challenge_root}: challenge_name must match directory name {challenge_root.name}"
        )
    if manifest.get("schema_version") != 1:
        raise ValidationError(f"{challenge_root}: schema_version must be 1")
    if manifest.get("request") != "new_challenge":
        raise ValidationError(f"{challenge_root}: CI currently validates new_challenge proposals")
    required_str(manifest, "title")
    required_localized_text(manifest, "summary")
    readme_path = required_safe_path(manifest, "readme_path")
    assert_file(challenge_root / readme_path, f"{challenge_root}: readme_path")
    validate_private_assets(challenge_root, manifest.get("private_assets", []))

    bundle_path = required_safe_path(manifest, "bundle_path")
    bundle_root = challenge_root / bundle_path
    spec = load_json(bundle_root / "spec.json")
    validate_bundle(challenge_root, bundle_root, manifest, spec)


def validate_bundle(
    challenge_root: Path,
    bundle_root: Path,
    manifest: dict[str, Any],
    spec: dict[str, Any],
) -> None:
    assert_file(bundle_root / "statement.md", f"{bundle_root}: statement.md")
    if spec.get("schema_version") != 1:
        raise ValidationError(f"{bundle_root}: spec schema_version must be 1")
    match_field(spec, "challenge_name", manifest["challenge_name"], bundle_root)
    match_field(spec, "challenge_title", manifest["title"], bundle_root)
    match_localized_text(spec, "summary", manifest["summary"], bundle_root)
    required_str(spec, "starts_at")
    validate_targets(bundle_root, required_array(spec, "targets"))

    datasets = required_object(spec, "datasets")
    public_dir = required_safe_path(datasets, "public_dir")
    assert_dir(bundle_root / public_dir, f"{bundle_root}: datasets.public_dir")

    execution = required_object(spec, "execution")
    if any(target.get("validation_enabled") for target in spec["targets"]):
        if "validation_runs" in execution:
            runs_path = required_safe_path(execution, "validation_runs")
            validate_run_manifest(bundle_root, bundle_root / runs_path)
        elif "validation_prepare" not in execution:
            raise ValidationError(
                f"{bundle_root}: validation enabled targets require validation_runs or validation_prepare"
            )

    if datasets.get("private_benchmark_enabled"):
        if "official_runs" not in execution and "official_prepare" not in execution:
            raise ValidationError(
                f"{bundle_root}: private benchmarks require official_runs or official_prepare"
            )

    scorer = required_object(spec, "scorer")
    scorer_command = required_array(scorer, "command")
    for part in scorer_command:
        if isinstance(part, str) and part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: scorer.command script")
            break

    validate_prepare(bundle_root, execution.get("validation_prepare"), "validation_prepare")
    validate_prepare(bundle_root, execution.get("official_prepare"), "official_prepare")
    _ = challenge_root


def validate_targets(bundle_root: Path, targets: list[Any]) -> None:
    if not targets:
        raise ValidationError(f"{bundle_root}: targets must not be empty")
    seen = set()
    for target in targets:
        if not isinstance(target, dict):
            raise ValidationError(f"{bundle_root}: target must be an object")
        name = required_str(target, "name")
        if name in seen:
            raise ValidationError(f"{bundle_root}: duplicate target {name}")
        seen.add(name)
        if "accelerator" not in target:
            raise ValidationError(f"{bundle_root}: target {name} must declare accelerator")
        accelerator = target["accelerator"]
        if accelerator not in {None, "gpu"}:
            raise ValidationError(
                f"{bundle_root}: target {name} accelerator must be null or gpu"
            )
        if target.get("docker_platform") != "linux/arm64":
            raise ValidationError(
                f"{bundle_root}: target {name} must use docker_platform linux/arm64"
            )


def validate_run_manifest(bundle_root: Path, runs_path: Path) -> None:
    manifest = load_json(runs_path)
    runs = required_array(manifest, "runs")
    if not runs:
        raise ValidationError(f"{runs_path}: runs must not be empty")
    seen = set()
    for run in runs:
        if not isinstance(run, dict):
            raise ValidationError(f"{runs_path}: run entries must be objects")
        run_name = required_str(run, "run_name")
        if run_name in seen:
            raise ValidationError(f"{runs_path}: duplicate run_name {run_name}")
        seen.add(run_name)
        for input_file in run.get("input_files", []):
            if not isinstance(input_file, dict):
                raise ValidationError(f"{runs_path}: input_files entries must be objects")
            required_safe_path(input_file, "path")
            source_path = input_file.get("source_path")
            if source_path is not None:
                if not isinstance(source_path, str) or not is_safe_relative_path(source_path):
                    raise ValidationError(f"{runs_path}: unsafe input source_path {source_path}")
                assert_file(bundle_root / source_path, f"{runs_path}: input source_path")


def validate_prepare(bundle_root: Path, prepare: Any, field: str) -> None:
    if prepare is None:
        return
    if not isinstance(prepare, dict):
        raise ValidationError(f"{bundle_root}: execution.{field} must be an object")
    command = required_array(prepare, "command")
    if not command:
        raise ValidationError(f"{bundle_root}: execution.{field}.command must not be empty")
    for part in command:
        if not isinstance(part, str) or not part:
            raise ValidationError(f"{bundle_root}: execution.{field}.command entries must be strings")
        if part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: execution.{field}.command script")
    result_runs_file = required_safe_path(prepare, "result_runs_file")
    if result_runs_file.endswith("/"):
        raise ValidationError(f"{bundle_root}: execution.{field}.result_runs_file must be a file")
    if prepare.get("network_access") not in {"disabled", "loopback", "enabled"}:
        raise ValidationError(
            f"{bundle_root}: execution.{field}.network_access must be disabled, loopback, or enabled"
        )
    for removed in ("external_data", "cache_key_hint"):
        if removed in prepare:
            raise ValidationError(f"{bundle_root}: execution.{field}.{removed} is not supported")


def validate_private_assets(challenge_root: Path, assets: Any) -> None:
    if not isinstance(assets, list):
        raise ValidationError(f"{challenge_root}: private_assets must be an array")
    seen = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValidationError(f"{challenge_root}: private asset entries must be objects")
        asset_name = required_str(asset, "asset_name")
        if asset_name in seen:
            raise ValidationError(f"{challenge_root}: duplicate private asset {asset_name}")
        seen.add(asset_name)
        if asset.get("kind") not in PRIVATE_ASSET_KINDS:
            raise ValidationError(f"{challenge_root}: unsupported private asset kind {asset.get('kind')}")
        if not isinstance(asset.get("required"), bool):
            raise ValidationError(
                f"{challenge_root}: private asset {asset_name} required must be true or false"
            )


def reject_private_files(root: Path) -> None:
    for path in root.rglob("*"):
        name = path.name.lower()
        if name in PRIVATE_NAMES or name.endswith((".pem", ".key", ".p12")):
            raise ValidationError(f"private or secret material must not be committed: {path}")
        if path.is_symlink():
            raise ValidationError(f"symlinks are not allowed in challenge proposals: {path}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            value = json.load(file)
    except FileNotFoundError as error:
        raise ValidationError(f"missing JSON file: {path}") from error
    except json.JSONDecodeError as error:
        raise ValidationError(f"invalid JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: JSON root must be an object")
    return value


def match_field(value: dict[str, Any], field: str, expected: str, location: Path) -> None:
    actual = required_str(value, field)
    if actual != expected:
        raise ValidationError(f"{location}: {field} must be {expected}, got {actual}")


def match_localized_text(
    value: dict[str, Any], field: str, expected: dict[str, str], location: Path
) -> None:
    actual = required_localized_text(value, field)
    if actual != expected:
        raise ValidationError(f"{location}: {field} must match the challenge manifest")


def required_object(value: dict[str, Any], field: str) -> dict[str, Any]:
    item = value.get(field)
    if not isinstance(item, dict):
        raise ValidationError(f"{field} must be an object")
    return item


def required_array(value: dict[str, Any], field: str) -> list[Any]:
    item = value.get(field)
    if not isinstance(item, list):
        raise ValidationError(f"{field} must be an array")
    return item


def required_str(value: dict[str, Any], field: str) -> str:
    item = value.get(field)
    if not isinstance(item, str) or not item.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return item


def required_localized_text(value: dict[str, Any], field: str) -> dict[str, str]:
    item = value.get(field)
    if not isinstance(item, dict):
        raise ValidationError(f"{field} must be an object with en and zh strings")
    for locale in ("en", "zh"):
        text = item.get(locale)
        if not isinstance(text, str) or not text.strip():
            raise ValidationError(f"{field}.{locale} must be a non-empty string")
    return item


def required_safe_path(value: dict[str, Any], field: str) -> str:
    item = required_str(value, field)
    if not is_safe_relative_path(item):
        raise ValidationError(f"{field} must be a safe relative path")
    return item


def is_safe_relative_path(value: str) -> bool:
    if value.startswith("/"):
        return False
    return all(part and part != ".." for part in value.replace("\\", "/").split("/"))


def assert_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise ValidationError(f"{label} must be a file: {path}")


def assert_dir(path: Path, label: str) -> None:
    if not path.is_dir():
        raise ValidationError(f"{label} must be a directory: {path}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
