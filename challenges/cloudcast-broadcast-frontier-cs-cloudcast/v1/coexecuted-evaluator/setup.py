from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENV_PROJECT_DIR = "frontier-cs-cpu-env"
PYTHON_INSTALL_DIR = "uv-python"
PYTHON_REQUEST = "3.12"
DEPENDENCIES = ['networkx>=3.2', 'numpy>=1.26', 'pandas>=2.2', 'graphviz>=0.20', 'colorama>=0.4.6']

def find_managed_python(setup_dir: Path, env: dict[str, str]) -> Path:
    install_dir = setup_dir / PYTHON_INSTALL_DIR
    subprocess.run(["uv", "python", "install", PYTHON_REQUEST, "--install-dir", str(install_dir)], check=True, env=env, timeout=900)
    candidates = sorted(install_dir.glob("*/bin/python"))
    if not candidates:
        raise RuntimeError(f"uv did not install a managed Python under {install_dir}")
    return candidates[0]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--setup-dir", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    setup_dir = Path(args.setup_dir)
    project_dir = setup_dir / ENV_PROJECT_DIR
    project_dir.mkdir(parents=True, exist_ok=True)
    deps = "\n".join(f'  "{dep}",' for dep in DEPENDENCIES)
    pyproject = (
        '[project]\n'
        'name = "agentics-frontier-cs-cpu-evaluator-env"\n'
        'version = "0.1.0"\n'
        'requires-python = ">=3.12,<3.13"\n'
        'dependencies = [\n'
        f'{deps}\n'
        ']\n\n'
        '[tool.uv]\n'
        'package = false\n'
    )
    (project_dir / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    env = os.environ.copy()
    env["UV_CACHE_DIR"] = str(setup_dir / "uv-cache")
    env["UV_LINK_MODE"] = "copy"
    env["UV_PROJECT_ENVIRONMENT"] = str(project_dir / ".venv")
    python = find_managed_python(setup_dir, env)
    subprocess.run(
        ["uv", "sync", "--project", str(project_dir), "--python", str(python), "--no-dev", "--no-install-project"],
        check=True,
        env=env,
        timeout=900,
    )
    metadata = {"python_ok": True, "mode": args.mode, "target": args.target}
    (project_dir / "agentics-env.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    shutil.rmtree(setup_dir / "uv-cache", ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
