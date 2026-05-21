from __future__ import annotations

import json
import subprocess
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
    "private_evaluator_package",
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
    manifest_keywords = required_keywords(manifest, "keywords")
    readme_path = required_safe_path(manifest, "readme_path")
    assert_file(challenge_root / readme_path, f"{challenge_root}: readme_path")
    validate_private_assets(challenge_root, manifest.get("private_assets", []))

    bundle_path = required_safe_path(manifest, "bundle_path")
    bundle_root = challenge_root / bundle_path
    spec = load_json(bundle_root / "spec.json")
    validate_bundle(challenge_root, bundle_root, manifest, manifest_keywords, spec)


def validate_bundle(
    challenge_root: Path,
    bundle_root: Path,
    manifest: dict[str, Any],
    manifest_keywords: list[str],
    spec: dict[str, Any],
) -> None:
    assert_file(bundle_root / "statement.md", f"{bundle_root}: statement.md")
    if spec.get("schema_version") != 1:
        raise ValidationError(f"{bundle_root}: spec schema_version must be 1")
    match_field(spec, "challenge_name", manifest["challenge_name"], bundle_root)
    match_field(spec, "challenge_title", manifest["title"], bundle_root)
    match_localized_text(spec, "summary", manifest["summary"], bundle_root)
    match_keywords(spec, "keywords", manifest_keywords, bundle_root)
    required_str(spec, "starts_at")
    execution = required_object(spec, "execution")
    mode = execution.get("mode")
    if mode not in {"separated_evaluator", "piped_stdio", "coexecuted_benchmark"}:
        raise ValidationError(
            f"{bundle_root}: execution.mode must be separated_evaluator, piped_stdio, or coexecuted_benchmark"
        )
    validate_targets(bundle_root, required_array(spec, "targets"), mode)

    datasets = required_object(spec, "datasets")
    public_dir = required_safe_path(datasets, "public_dir")
    assert_dir(bundle_root / public_dir, f"{bundle_root}: datasets.public_dir")

    if any(target.get("validation_enabled") for target in spec["targets"]):
        if mode == "separated_evaluator" and "validation_runs" in execution:
            runs_path = required_safe_path(execution, "validation_runs")
            ci = manifest.get("ci", {})
            if not isinstance(ci, dict):
                ci = {}
            validate_run_manifest(
                bundle_root,
                bundle_root / runs_path,
                require_expected_outputs=bool(ci.get("smoke_test_public_validation")),
            )
        elif "validation_prepare" not in execution:
            raise ValidationError(
                f"{bundle_root}: validation enabled targets require the mode-specific validation source"
            )

    if datasets.get("private_benchmark_enabled"):
        if mode == "separated_evaluator" and "official_runs" not in execution and "official_prepare" not in execution:
            raise ValidationError(
                f"{bundle_root}: private benchmarks require official_runs or official_prepare"
            )
        if mode == "piped_stdio" and "official_session" not in execution and "official_prepare" not in execution:
            raise ValidationError(
                f"{bundle_root}: private benchmarks require official_session or official_prepare"
            )

    if mode == "coexecuted_benchmark":
        if execution.get("acknowledge_danger") is not True:
            raise ValidationError(
                f"{bundle_root}: coexecuted_benchmark requires acknowledge_danger true"
            )
        for forbidden in ("validation_runs", "official_runs", "validation_session", "official_session"):
            if forbidden in execution:
                raise ValidationError(
                    f"{bundle_root}: coexecuted_benchmark must not declare execution.{forbidden}"
                )
        executor = required_object(execution, "benchmark")
        executor_label = "execution.benchmark.command script"
    elif mode == "piped_stdio":
        executor = required_object(execution, "interactor")
        executor_label = "execution.interactor.command script"
    else:
        executor = required_object(execution, "evaluator")
        executor_label = "execution.evaluator.command script"

    executor_command = required_array(executor, "command")
    for part in executor_command:
        if isinstance(part, str) and part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: {executor_label}")
            break

    if mode == "coexecuted_benchmark":
        validate_coexecuted_prepare(
            bundle_root, execution.get("validation_prepare"), "validation_prepare"
        )
        validate_coexecuted_prepare(
            bundle_root, execution.get("official_prepare"), "official_prepare"
        )
    else:
        validate_prepare(bundle_root, execution.get("validation_prepare"), "validation_prepare")
        validate_prepare(bundle_root, execution.get("official_prepare"), "official_prepare")
    _ = challenge_root


def validate_targets(bundle_root: Path, targets: list[Any], mode: str) -> None:
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
        validate_resource_profile(
            bundle_root, name, required_object(target, "resource_profile"), mode
        )


def validate_resource_profile(
    bundle_root: Path, target_name: str, profile: dict[str, Any], mode: str
) -> None:
    for old_field in (
        "timeout_sec",
        "memory_limit_mb",
        "cpu_limit_millis",
        "disk_limit_mb",
        "setup_network_access",
        "build_network_access",
        "run_network_access",
        "evaluator_network_access",
    ):
        if old_field in profile:
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.{old_field} is not supported"
            )
    solution = required_object(profile, "solution")
    evaluator = required_object(profile, "evaluator")
    for stage in ("setup", "build"):
        validate_stage_profile(
            bundle_root,
            target_name,
            f"solution.{stage}",
            required_object(solution, stage),
        )
    if mode == "coexecuted_benchmark":
        if "run" in solution:
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.solution.run is forbidden for coexecuted_benchmark"
            )
    else:
        validate_stage_profile(
            bundle_root,
            target_name,
            "solution.run",
            required_object(solution, "run"),
        )
    for stage in ("setup", "run"):
        validate_stage_profile(
            bundle_root,
            target_name,
            f"evaluator.{stage}",
            required_object(evaluator, stage),
        )


def validate_stage_profile(
    bundle_root: Path, target_name: str, field: str, stage: dict[str, Any]
) -> None:
    for key in ("timeout_sec", "memory_limit_mb", "cpu_limit_millis", "disk_limit_mb"):
        value = stage.get(key)
        if not isinstance(value, int) or value <= 0:
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.{field}.{key} must be a positive integer"
            )
    if stage.get("network_access") not in {"disabled", "loopback", "enabled"}:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field}.network_access must be disabled, loopback, or enabled"
        )


def validate_run_manifest(
    bundle_root: Path, runs_path: Path, *, require_expected_outputs: bool = False
) -> None:
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
        for output_file in run.get("output_files", []):
            if not isinstance(output_file, str) or not is_safe_relative_path(output_file):
                raise ValidationError(f"{runs_path}: unsafe output_files path {output_file}")
        expected_output = run.get("expected_output_source_path")
        if expected_output is None:
            if require_expected_outputs:
                raise ValidationError(
                    f"{runs_path}: smoke_test_public_validation requires expected_output_source_path for {run_name}"
                )
        elif not isinstance(expected_output, str) or not is_safe_relative_path(expected_output):
            raise ValidationError(
                f"{runs_path}: unsafe expected_output_source_path {expected_output}"
            )
        else:
            assert_file(
                bundle_root / expected_output,
                f"{runs_path}: expected_output_source_path",
            )


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
    for removed in ("external_data", "cache_key_hint", "network_access"):
        if removed in prepare:
            raise ValidationError(f"{bundle_root}: execution.{field}.{removed} is not supported")


def validate_coexecuted_prepare(bundle_root: Path, prepare: Any, field: str) -> None:
    if prepare is None:
        return
    if not isinstance(prepare, dict):
        raise ValidationError(f"{bundle_root}: execution.{field} must be an object")
    command = required_array(prepare, "command")
    if not command:
        raise ValidationError(f"{bundle_root}: execution.{field}.command must not be empty")
    for part in command:
        if not isinstance(part, str) or not part:
            raise ValidationError(
                f"{bundle_root}: execution.{field}.command entries must be strings"
            )
        if part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: execution.{field}.command script")
    for removed in (
        "external_data",
        "cache_key_hint",
        "network_access",
        "result_runs_file",
        "result_session_file",
    ):
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
        required_paths = asset.get("required_paths", [])
        if not isinstance(required_paths, list):
            raise ValidationError(
                f"{challenge_root}: private asset {asset_name} required_paths must be an array"
            )
        seen_paths: set[str] = set()
        for index, required_path in enumerate(required_paths):
            if not isinstance(required_path, str) or not is_safe_relative_path(required_path):
                raise ValidationError(
                    f"{challenge_root}: private asset {asset_name} required_paths[{index}] must be a safe relative path"
                )
            if required_path in seen_paths:
                raise ValidationError(
                    f"{challenge_root}: private asset {asset_name} contains duplicate required path {required_path}"
                )
            seen_paths.add(required_path)


def reject_private_files(root: Path) -> None:
    for path in root.rglob("*"):
        if is_git_ignored(path):
            continue
        name = path.name.lower()
        if name in PRIVATE_NAMES or name.endswith((".pem", ".key", ".p12")):
            raise ValidationError(f"private or secret material must not be committed: {path}")
        if path.is_symlink():
            raise ValidationError(f"symlinks are not allowed in challenge proposals: {path}")


def is_git_ignored(path: Path) -> bool:
    try:
        checked_path = path.relative_to(ROOT)
    except ValueError:
        checked_path = path
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "-q", str(checked_path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return False
    return result.returncode == 0


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


def match_keywords(
    value: dict[str, Any], field: str, expected: list[str], location: Path
) -> None:
    actual = required_keywords(value, field)
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


def required_keywords(value: dict[str, Any], field: str) -> list[str]:
    item = value.get(field)
    if not isinstance(item, list):
        raise ValidationError(f"{field} must be an array")
    if not 1 <= len(item) <= 6:
        raise ValidationError(f"{field} must contain between 1 and 6 entries")
    keywords: list[str] = []
    seen: set[str] = set()
    for index, keyword in enumerate(item):
        if not isinstance(keyword, str):
            raise ValidationError(f"{field}[{index}] must be a string")
        normalized = keyword.strip()
        if not normalized:
            raise ValidationError(f"{field}[{index}] must be non-empty after trimming")
        if len(normalized.encode("utf-8")) > 30:
            raise ValidationError(f"{field}[{index}] must be at most 30 UTF-8 bytes")
        if any(ord(char) < 32 or ord(char) == 127 for char in normalized):
            raise ValidationError(f"{field}[{index}] must not contain control characters")
        case_key = normalized.casefold()
        if case_key in seen:
            raise ValidationError(f"{field} contains duplicate keyword {normalized!r}")
        seen.add(case_key)
        keywords.append(normalized)
    return keywords


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
