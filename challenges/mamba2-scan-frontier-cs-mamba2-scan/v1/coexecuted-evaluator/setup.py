from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENV_PROJECT_DIR = "evaluator-env"
PYTHON_INSTALL_DIR = "uv-python"
PYTHON_REQUEST = "3.12"
PYPROJECT = """[project]
name = "mamba2_scan_frontier_cs_mamba2_scan"
version = "0.1.0"
requires-python = ">=3.12,<3.13"
dependencies = [
  "torch>=2.11.0,<2.12.0",
  "triton>=3.5.0,<4",
  "numpy>=1.26",
]

[tool.uv]
package = false

[tool.uv.sources]
torch = [
  { index = "pytorch-cu130", marker = "sys_platform == 'linux'" },
]

[[tool.uv.index]]
name = "pytorch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true
"""

def find_managed_python(setup_dir: Path, env: dict[str, str]) -> Path:
    install_dir = setup_dir / PYTHON_INSTALL_DIR
    subprocess.run(["uv", "python", "install", PYTHON_REQUEST, "--install-dir", str(install_dir)], check=True, env=env, timeout=900)
    candidates = sorted(install_dir.glob("*/bin/python"))
    if not candidates:
        raise RuntimeError(f"uv did not install a managed Python under {install_dir}")
    return candidates[0]

def main() -> int:
    parser = argparse.ArgumentParser(description="Set up the Mamba2 scan evaluator environment")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--setup-dir", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    setup_dir = Path(args.setup_dir)
    project_dir = setup_dir / ENV_PROJECT_DIR
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    env = os.environ.copy()
    env["UV_CACHE_DIR"] = str(setup_dir / "uv-cache")
    env["UV_LINK_MODE"] = "copy"
    env["UV_PROJECT_ENVIRONMENT"] = str(project_dir / ".venv")
    python = find_managed_python(setup_dir, env)
    subprocess.run(
        ["uv", "sync", "--project", str(project_dir), "--python", str(python), "--no-dev", "--no-install-project"],
        check=True,
        env=env,
        timeout=1200,
    )
    (project_dir / "agentics-env.json").write_text(json.dumps({"mode": args.mode, "target": args.target}, indent=2), encoding="utf-8")
    shutil.rmtree(setup_dir / "uv-cache", ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
