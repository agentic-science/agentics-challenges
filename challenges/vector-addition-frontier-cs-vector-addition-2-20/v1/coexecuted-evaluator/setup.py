from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


ENV_PROJECT_DIR = "pytorch-triton-env"
PYTHON_INSTALL_DIR = "uv-python"
PYTHON_REQUEST = "3.12"

PYPROJECT = """\
[project]
name = "agentics-vector-addition-evaluator-env"
version = "0.1.0"
requires-python = ">=3.12,<3.13"
dependencies = [
  "torch>=2.11.0,<2.12.0",
  "triton>=3.5.0,<4",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up the PyTorch/Triton evaluator environment.")
    parser.add_argument("--challenge-dir", required=True)
    parser.add_argument("--setup-dir", required=True)
    parser.add_argument("--mode", choices=["validation", "official"], required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    setup_dir = Path(args.setup_dir)
    project_dir = setup_dir / ENV_PROJECT_DIR
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "pyproject.toml").write_text(PYPROJECT)

    env = os.environ.copy()
    env["UV_CACHE_DIR"] = str(setup_dir / "uv-cache")
    env["UV_LINK_MODE"] = "copy"
    env["UV_PROJECT_ENVIRONMENT"] = str(project_dir / ".venv")
    env["UV_PYTHON_INSTALL_DIR"] = str(setup_dir / PYTHON_INSTALL_DIR)
    subprocess.run(
        ["uv", "python", "install", PYTHON_REQUEST],
        check=True,
        env=env,
        timeout=120,
    )
    managed_python = find_managed_python(env)
    subprocess.run(
        [
            "uv",
            "sync",
            "--project",
            str(project_dir),
            "--python",
            str(managed_python),
            "--no-dev",
            "--no-install-project",
        ],
        check=True,
        env=env,
        timeout=900,
    )

    metadata = inspect_environment(project_dir / ".venv" / "bin" / "python")
    metadata.update({"mode": args.mode, "target": args.target})
    (project_dir / "agentics-env.json").write_text(json.dumps(metadata, indent=2, sort_keys=True))
    shutil.rmtree(setup_dir / "uv-cache", ignore_errors=True)
    return 0


def find_managed_python(env: dict[str, str]) -> Path:
    result = subprocess.run(
        ["uv", "python", "find", PYTHON_REQUEST, "--managed-python", "--resolve-links"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    path = Path(result.stdout.strip())
    if not path.is_file():
        raise RuntimeError(f"managed Python not found at {path}")
    include_dir = path.parent.parent / "include"
    if not any(include_dir.glob("python*/Python.h")):
        raise RuntimeError(f"managed Python headers not found under {include_dir}")
    return path


def inspect_environment(python: Path) -> dict[str, str | bool]:
    result = subprocess.run(
        [
            str(python),
            "-c",
            (
                "import json, torch, triton; "
                "print(json.dumps({"
                "'python_ok': True, "
                "'torch': torch.__version__, "
                "'triton': triton.__version__, "
                "'cuda_available': bool(torch.cuda.is_available())"
                "}))"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise RuntimeError("environment inspection did not return a JSON object")
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
