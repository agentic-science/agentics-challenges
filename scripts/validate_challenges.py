from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHALLENGES_DIR = ROOT / "challenges"
SUPPORTED_CUDA_VARIANTS = {
    "cu126": "12.6",
    "cu130": "13.0",
    "cu132": "13.2",
}
SUPPORTED_CPU_IMAGE_REPOSITORIES = {
    "agentics-linux-arm64-cpu",
    "ghcr.io/agentic-science/agentics-linux-arm64-cpu",
}
SUPPORTED_CUDA_IMAGE_REPOSITORIES = {
    "agentics-linux-arm64-cuda",
    "ghcr.io/agentic-science/agentics-linux-arm64-cuda",
}
SUPPORTED_LOCAL_IMAGE_REPOSITORIES = {
    "agentics-linux-arm64-cpu",
    "agentics-linux-arm64-cuda",
}
CPU_IMAGE_TAG_PREFIX = "ubuntu26.04-"
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
WARNINGS: list[str] = []


class ValidationError(Exception):
    pass


def main() -> int:
    challenge_roots = sorted(path for path in CHALLENGES_DIR.iterdir() if path.is_dir())
    if not challenge_roots:
        raise ValidationError("repository must contain at least one challenge")
    for challenge_root in challenge_roots:
        validate_challenge(challenge_root)
    for warning in WARNINGS:
        print(f"warning: {warning}", file=sys.stderr)
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
    datasets = required_object(spec, "datasets")
    public_dir = required_safe_path(datasets, "public_dir")
    assert_dir(bundle_root / public_dir, f"{bundle_root}: datasets.public_dir")
    private_benchmark_enabled = bool(datasets.get("private_benchmark_enabled"))
    validate_targets(
        bundle_root,
        required_array(spec, "targets"),
        mode,
        private_benchmark_enabled=private_benchmark_enabled,
    )

    if any(target.get("validation_enabled") for target in spec["targets"]):
        validation_limit = spec.get("validation_submission_limit")
        if not isinstance(validation_limit, int) or validation_limit <= 0:
            raise ValidationError(
                f"{bundle_root}: validation_submission_limit must be a positive integer when any target has validation_enabled true"
            )
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
        elif mode == "piped_stdio" and "validation_session" in execution:
            session_path = required_safe_path(execution, "validation_session")
            validate_session_manifest(bundle_root, bundle_root / session_path)
        elif mode in {"separated_evaluator", "piped_stdio"} and "validation_setup" in execution:
            pass
        elif mode == "coexecuted_benchmark":
            pass
        else:
            raise ValidationError(
                f"{bundle_root}: validation enabled targets require the mode-specific validation source"
            )

    if private_benchmark_enabled:
        uses_static_official = (
            (mode == "separated_evaluator" and "official_runs" in execution)
            or (mode == "piped_stdio" and "official_session" in execution)
        )
        if uses_static_official and "private_benchmark_dir" not in datasets:
            raise ValidationError(
                f"{bundle_root}: datasets.private_benchmark_dir is required for static official run or session manifests"
            )
        if mode == "separated_evaluator" and "official_runs" not in execution and "official_evaluation_setup" not in execution:
            raise ValidationError(
                f"{bundle_root}: private benchmarks require official_runs or official_evaluation_setup"
            )
        if mode == "piped_stdio" and "official_session" not in execution and "official_evaluation_setup" not in execution:
            raise ValidationError(
                f"{bundle_root}: private benchmarks require official_session or official_evaluation_setup"
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
        executor = required_object(execution, "coexecuted_evaluator")
        executor_label = "execution.coexecuted_evaluator.command script"
    elif mode == "piped_stdio":
        if execution.get("acknowledge_stdio_protocol_framing") is not True:
            raise ValidationError(
                f"{bundle_root}: execution.acknowledge_stdio_protocol_framing must be true for piped_stdio: the challenge author must document the stdin/stdout message protocol, including session start and termination, multi-case framing if used, EOF behavior, malformed participant output handling, and trusted evaluator result.json ownership."
            )
        reject_both_execution_fields(bundle_root, execution, "validation_session", "validation_setup")
        reject_both_execution_fields(bundle_root, execution, "official_session", "official_evaluation_setup")
        executor = required_object(execution, "interactive_evaluator")
        executor_label = "execution.interactive_evaluator.command script"
    else:
        reject_both_execution_fields(bundle_root, execution, "validation_runs", "validation_setup")
        reject_both_execution_fields(bundle_root, execution, "official_runs", "official_evaluation_setup")
        executor = required_object(execution, "separated_evaluator")
        executor_label = "execution.separated_evaluator.command script"

    executor_command = required_array(executor, "command")
    result_file = required_safe_path(executor, "result_file")
    if result_file.endswith("/"):
        raise ValidationError(f"{bundle_root}: execution {mode} result_file must be a file")
    for part in executor_command:
        if isinstance(part, str) and part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: {executor_label}")
            break

    if mode == "coexecuted_benchmark":
        validate_coexecuted_setup(
            bundle_root, execution.get("validation_setup"), "validation_setup"
        )
        validate_coexecuted_setup(
            bundle_root, execution.get("official_evaluation_setup"), "official_evaluation_setup"
        )
    elif mode == "piped_stdio":
        validate_setup(
            bundle_root,
            execution.get("validation_setup"),
            "validation_setup",
            "result_session_file",
        )
        validate_setup(
            bundle_root,
            execution.get("official_evaluation_setup"),
            "official_evaluation_setup",
            "result_session_file",
        )
    else:
        validate_setup(
            bundle_root,
            execution.get("validation_setup"),
            "validation_setup",
            "result_runs_file",
        )
        validate_setup(
            bundle_root,
            execution.get("official_evaluation_setup"),
            "official_evaluation_setup",
            "result_runs_file",
        )
    _ = challenge_root


def reject_both_execution_fields(
    bundle_root: Path, execution: dict[str, Any], first: str, second: str
) -> None:
    if first in execution and second in execution:
        raise ValidationError(
            f"{bundle_root}: execution must not declare both {first} and {second}"
        )


def validate_targets(
    bundle_root: Path,
    targets: list[Any],
    mode: str,
    *,
    private_benchmark_enabled: bool,
) -> None:
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
        accelerator, cuda_variant = validate_target_policy(bundle_root, name, target)
        validate_resource_profile(
            bundle_root,
            name,
            required_object(target, "resource_profile"),
            mode,
            accelerator=accelerator,
            cuda_variant=cuda_variant,
            private_benchmark_enabled=private_benchmark_enabled,
        )


def validate_target_policy(
    bundle_root: Path, name: str, target: dict[str, Any]
) -> tuple[Any, str | None]:
    if "accelerator" not in target:
        raise ValidationError(f"{bundle_root}: target {name} must declare accelerator")
    accelerator = target["accelerator"]
    if accelerator not in {None, "gpu"}:
        raise ValidationError(f"{bundle_root}: target {name} accelerator must be null or gpu")

    if name == "linux-arm64-cpu":
        expected_platform = "linux/arm64"
        expected_accelerator = None
    elif name == "linux-arm64-cuda":
        expected_platform = "linux/arm64"
        expected_accelerator = "gpu"
    elif name == "macos-arm64-cpu":
        raise ValidationError(
            f"{bundle_root}: target {name} is a platform-development target and cannot be used for hosted challenge deployment"
        )
    elif name in {"linux-amd64-cpu", "linux-amd64-cuda"}:
        raise ValidationError(f"{bundle_root}: target {name} is reserved for post-MVP support")
    else:
        raise ValidationError(
            f"{bundle_root}: target {name} is not supported for MVP hosted challenge deployment"
        )

    if target.get("docker_platform") != expected_platform:
        raise ValidationError(
            f"{bundle_root}: target {name} must use docker_platform {expected_platform}"
        )
    if accelerator != expected_accelerator:
        expected = "null" if expected_accelerator is None else expected_accelerator
        raise ValidationError(f"{bundle_root}: target {name} accelerator must be {expected}")

    resource_profile = required_object(target, "resource_profile")
    hardware = resource_profile.get("hardware_metadata")
    if accelerator == "gpu":
        return accelerator, validate_cuda_hardware(bundle_root, name, hardware)
    if hardware is not None:
        validate_hardware_metadata(bundle_root, name, hardware)
    return accelerator, None


def validate_resource_profile(
    bundle_root: Path,
    target_name: str,
    profile: dict[str, Any],
    mode: str,
    *,
    accelerator: Any,
    cuda_variant: str | None,
    private_benchmark_enabled: bool,
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
    validate_supported_image(
        bundle_root,
        target_name,
        required_object(profile, "solution_image"),
        accelerator=accelerator,
        cuda_variant=cuda_variant,
        field="solution_image",
    )
    validate_supported_image(
        bundle_root,
        target_name,
        required_object(profile, "evaluator_image"),
        accelerator=accelerator,
        cuda_variant=cuda_variant,
        field="evaluator_image",
    )
    warn_private_network_risk(
        bundle_root,
        target_name,
        mode,
        solution,
        evaluator,
        private_benchmark_enabled=private_benchmark_enabled,
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


def validate_hardware_metadata(bundle_root: Path, target_name: str, hardware: Any) -> None:
    if not isinstance(hardware, dict):
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.hardware_metadata must be an object"
        )
    required_str(hardware, "kind")
    for field in ("gpu_model", "cuda_variant", "cuda_version", "driver_minimum"):
        if field in hardware and not_non_empty_str(hardware[field]):
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.{field} must be a non-empty string"
            )
    for field in ("gpu_count", "gpu_memory_gb"):
        if field in hardware and (not isinstance(hardware[field], int) or hardware[field] <= 0):
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.{field} must be positive"
            )


def validate_cuda_hardware(bundle_root: Path, target_name: str, hardware: Any) -> str:
    validate_hardware_metadata(bundle_root, target_name, hardware)
    assert isinstance(hardware, dict)
    if hardware.get("kind") != "cuda":
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.kind must be cuda"
        )
    for field in ("gpu_model", "cuda_variant", "cuda_version"):
        if not_non_empty_str(hardware.get(field)):
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.{field} is required for accelerator gpu"
            )
    if not isinstance(hardware.get("gpu_count"), int) or hardware["gpu_count"] <= 0:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.gpu_count must be greater than zero"
        )
    cuda_variant = hardware["cuda_variant"]
    expected_cuda_version = SUPPORTED_CUDA_VARIANTS.get(cuda_variant)
    if expected_cuda_version is None:
        supported = ", ".join(SUPPORTED_CUDA_VARIANTS)
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.cuda_variant {cuda_variant} is not supported; supported variants: {supported}"
        )
    if hardware["cuda_version"] != expected_cuda_version:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.hardware_metadata.cuda_version must be {expected_cuda_version} for cuda_variant {cuda_variant}"
        )
    return cuda_variant


def validate_supported_image(
    bundle_root: Path,
    target_name: str,
    image: dict[str, Any],
    *,
    accelerator: Any,
    cuda_variant: str | None,
    field: str,
) -> None:
    source, reference, repository, tag, _digest = parse_image_reference(
        bundle_root, target_name, image, field
    )
    if accelerator == "gpu":
        supported_repositories = SUPPORTED_CUDA_IMAGE_REPOSITORIES
        expected_prefix = f"{cuda_variant}-"
        target_label = "linux-arm64-cuda"
    else:
        supported_repositories = SUPPORTED_CPU_IMAGE_REPOSITORIES
        expected_prefix = CPU_IMAGE_TAG_PREFIX
        target_label = "linux-arm64-cpu"
    if repository not in supported_repositories:
        supported = ", ".join(sorted(supported_repositories))
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} must use a supported Agentics image repository for {target_label}: {supported}"
        )
    if not tag.startswith(expected_prefix):
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} tag must start with {expected_prefix}"
        )
    if source == "local" and repository != reference.rsplit(":", 1)[0]:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} local image repository mismatch"
        )


def parse_image_reference(
    bundle_root: Path, target_name: str, image: dict[str, Any], field: str
) -> tuple[str, str, str, str, str | None]:
    source = image.get("source")
    reference = image.get("reference")
    if source not in {"local", "registry"} or not_non_empty_str(reference):
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} must declare source local|registry and a non-empty reference"
        )
    assert isinstance(reference, str)
    if source == "local":
        if (
            reference.strip() != reference
            or "/" in reference
            or "@" in reference
            or ":" not in reference
        ):
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.{field} local reference must be a supported tagged Agentics local image"
            )
        repository, tag = reference.rsplit(":", 1)
        if repository not in SUPPORTED_LOCAL_IMAGE_REPOSITORIES or not tag or not is_image_tag(tag):
            raise ValidationError(
                f"{bundle_root}: target {target_name} resource_profile.{field} local reference must be a supported tagged Agentics local image"
            )
        return source, reference, repository, tag, None

    image_without_digest, digest = split_digest(reference)
    registry, repository_path, tag = parse_registry_reference(
        bundle_root, target_name, field, image_without_digest
    )
    if digest is not None and not is_sha256_digest(digest):
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} digest must use sha256:<64 lowercase hex>"
        )
    return source, reference, f"{registry}/{repository_path}", tag, digest


def split_digest(reference: str) -> tuple[str, str | None]:
    if "@" not in reference:
        return reference, None
    image, digest = reference.split("@", 1)
    return image, digest


def parse_registry_reference(
    bundle_root: Path, target_name: str, field: str, image_without_digest: str
) -> tuple[str, str, str]:
    if image_without_digest.strip() != image_without_digest or "/" not in image_without_digest:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} registry reference must include explicit registry, repository, and tag"
        )
    registry, remainder = image_without_digest.split("/", 1)
    if registry != "localhost" and "." not in registry and ":" not in registry:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} registry reference must include explicit registry"
        )
    tag_separator = remainder.rfind(":")
    if tag_separator <= 0 or tag_separator == len(remainder) - 1:
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} registry reference must include explicit tag"
        )
    repository_path = remainder[:tag_separator]
    tag = remainder[tag_separator + 1 :]
    if not repository_path or any(not part for part in repository_path.split("/")) or not is_image_tag(tag):
        raise ValidationError(
            f"{bundle_root}: target {target_name} resource_profile.{field} registry reference must include explicit repository and valid tag"
        )
    return registry, repository_path, tag


def is_image_tag(value: str) -> bool:
    return bool(value) and all(
        char.isascii() and (char.isalnum() or char in "_.-") for char in value
    )


def is_sha256_digest(value: str) -> bool:
    prefix = "sha256:"
    if not value.startswith(prefix):
        return False
    digest = value[len(prefix) :]
    return len(digest) == 64 and all(char in "0123456789abcdef" for char in digest)


def warn_private_network_risk(
    bundle_root: Path,
    target_name: str,
    mode: str,
    solution: dict[str, Any],
    evaluator: dict[str, Any],
    *,
    private_benchmark_enabled: bool,
) -> None:
    if not private_benchmark_enabled:
        return
    risky: list[str] = []
    if mode in {"separated_evaluator", "piped_stdio"}:
        run = solution.get("run")
        if isinstance(run, dict) and run.get("network_access") != "disabled":
            risky.append("resource_profile.solution.run")
    if mode == "coexecuted_benchmark":
        evaluator_run = evaluator.get("run")
        if isinstance(evaluator_run, dict) and evaluator_run.get("network_access") != "disabled":
            risky.append("resource_profile.evaluator.run")
    for field in risky:
        WARNINGS.append(
            f"{bundle_root}: target {target_name} enables {field}.network_access while private benchmarks are enabled; participant-containing official stages can exfiltrate private benchmark data"
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
        if not is_run_name(run_name):
            raise ValidationError(f"{runs_path}: run_name {run_name} is invalid")
        if run_name in seen:
            raise ValidationError(f"{runs_path}: duplicate run_name {run_name}")
        seen.add(run_name)
        validate_input_files(bundle_root, runs_path, run.get("input_files", []))
        seen_outputs: set[str] = set()
        for output_file in run.get("output_files", []):
            if not isinstance(output_file, str) or not is_safe_relative_path(output_file):
                raise ValidationError(f"{runs_path}: unsafe output_files path {output_file}")
            if output_file in seen_outputs:
                raise ValidationError(f"{runs_path}: duplicate output_files path {output_file}")
            seen_outputs.add(output_file)
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


def validate_session_manifest(bundle_root: Path, session_path: Path) -> None:
    manifest = load_json(session_path)
    session_name = required_str(manifest, "session_name")
    if not is_run_name(session_name):
        raise ValidationError(f"{session_path}: session_name {session_name} is invalid")
    validate_input_files(bundle_root, session_path, manifest.get("input_files", []))
    metadata = manifest.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValidationError(f"{session_path}: metadata must be an object")


def validate_input_files(bundle_root: Path, manifest_path: Path, input_files: Any) -> None:
    if not isinstance(input_files, list):
        raise ValidationError(f"{manifest_path}: input_files must be an array")
    seen_paths: set[str] = set()
    for input_file in input_files:
        if not isinstance(input_file, dict):
            raise ValidationError(f"{manifest_path}: input_files entries must be objects")
        materialized_path = required_safe_path(input_file, "path")
        if materialized_path in seen_paths:
            raise ValidationError(
                f"{manifest_path}: duplicate input_files path {materialized_path}"
            )
        seen_paths.add(materialized_path)
        source_fields = [
            key for key in ("source_path", "content", "content_json") if key in input_file
        ]
        if len(source_fields) != 1:
            raise ValidationError(
                f"{manifest_path}: input_files entries must declare exactly one of source_path, content, or content_json"
            )
        source_path = input_file.get("source_path")
        if source_path is not None:
            if not isinstance(source_path, str) or not is_safe_relative_path(source_path):
                raise ValidationError(f"{manifest_path}: unsafe input source_path {source_path}")
            assert_file(bundle_root / source_path, f"{manifest_path}: input source_path")


def validate_setup(bundle_root: Path, setup: Any, field: str, result_locator: str) -> None:
    if setup is None:
        return
    if not isinstance(setup, dict):
        raise ValidationError(f"{bundle_root}: execution.{field} must be an object")
    command = required_array(setup, "command")
    if not command:
        raise ValidationError(f"{bundle_root}: execution.{field}.command must not be empty")
    for part in command:
        if not isinstance(part, str) or not part:
            raise ValidationError(f"{bundle_root}: execution.{field}.command entries must be strings")
        if part.endswith(".py") and is_safe_relative_path(part):
            assert_file(bundle_root / part, f"{bundle_root}: execution.{field}.command script")
    result_file = required_safe_path(setup, result_locator)
    if result_file.endswith("/"):
        raise ValidationError(f"{bundle_root}: execution.{field}.{result_locator} must be a file")
    for removed in ("external_data", "cache_key_hint", "network_access"):
        if removed in setup:
            raise ValidationError(f"{bundle_root}: execution.{field}.{removed} is not supported")


def validate_coexecuted_setup(bundle_root: Path, setup: Any, field: str) -> None:
    if setup is None:
        return
    if not isinstance(setup, dict):
        raise ValidationError(f"{bundle_root}: execution.{field} must be an object")
    command = required_array(setup, "command")
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
        if removed in setup:
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
    if not_non_empty_str(item):
        raise ValidationError(f"{field} must be a non-empty string")
    return item


def not_non_empty_str(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


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
    if (
        not value
        or value.strip() != value
        or value.startswith("/")
        or value.endswith("/")
        or "\\" in value
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        return False
    parts = value.split("/")
    return all(
        part
        and part not in {".", ".."}
        and all(char.isascii() and (char.isalnum() or char in "_.-") for char in part)
        for part in parts
    ) and "/".join(parts) == value


def is_run_name(value: str) -> bool:
    return (
        bool(value)
        and value not in {".", ".."}
        and all(char.isascii() and (char.isalnum() or char in "_.-") for char in value)
    )


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
