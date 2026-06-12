from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
ENV_PROJECT_DIR = "evaluator-env"
PYTHON_INSTALL_DIR = "uv-python"
PYTHON_REQUEST = "3.12"
PYPROJECT = '[project]\nname = "imagenet_2_5m_frontier_cs_imagenet_2_5m"\nversion = "0.1.0"\nrequires-python = ">=3.10,<3.13"\ndependencies = [\n  "torch>=2.2,<2.4",\n  "numpy>=1.24",\n  "tqdm>=4.64",\n]\n\n[tool.uv]\npackage = false\n'

def main() -> int:
    parser = argparse.ArgumentParser(description="Set up evaluator env")
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
    python = Path(sys.executable)
    subprocess.run(["uv", "sync", "--project", str(project_dir), "--python", str(python), "--no-dev", "--no-install-project"], check=True, env=env, timeout=1200)
    (project_dir / "agentics-env.json").write_text(json.dumps({"mode": args.mode, "target": args.target}, indent=2), encoding="utf-8")
    shutil.rmtree(setup_dir / "uv-cache", ignore_errors=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
