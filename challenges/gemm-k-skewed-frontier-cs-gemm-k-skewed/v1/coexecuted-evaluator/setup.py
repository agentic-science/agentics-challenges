from __future__ import annotations
import argparse,json,os,shutil,subprocess
from pathlib import Path
ENV_PROJECT_DIR="pytorch-triton-env"; PYTHON_INSTALL_DIR="uv-python"; PYTHON_REQUEST="3.12"
PYPROJECT="""[project]
name="agentics-frontier-cs-cuda-evaluator-env"
version="0.1.0"
requires-python=">=3.12,<3.13"
dependencies=["torch>=2.11.0,<2.12.0","triton>=3.5.0,<4","numpy>=1.26","tqdm>=4.66"]
[tool.uv]
package=false
[tool.uv.sources]
torch=[{ index="pytorch-cu130", marker="sys_platform == 'linux'" }]
[[tool.uv.index]]
name="pytorch-cu130"
url="https://download.pytorch.org/whl/cu130"
explicit=true
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--challenge-dir",required=True); p.add_argument("--setup-dir",required=True); p.add_argument("--mode",required=True); p.add_argument("--target",required=True); a=p.parse_args(); sd=Path(a.setup_dir); pd=sd/ENV_PROJECT_DIR; pd.mkdir(parents=True,exist_ok=True); (pd/"pyproject.toml").write_text(PYPROJECT)
    env=os.environ.copy(); env["UV_CACHE_DIR"]=str(sd/"uv-cache"); env["UV_LINK_MODE"]="copy"; env["UV_PROJECT_ENVIRONMENT"]=str(pd/".venv"); env["UV_PYTHON_INSTALL_DIR"]=str(sd/PYTHON_INSTALL_DIR)
    subprocess.run(["uv","python","install",PYTHON_REQUEST],check=True,env=env,timeout=120); py=Path(subprocess.run(["uv","python","find",PYTHON_REQUEST,"--managed-python","--resolve-links"],check=True,capture_output=True,text=True,env=env,timeout=30).stdout.strip())
    subprocess.run(["uv","sync","--project",str(pd),"--python",str(py),"--no-dev","--no-install-project"],check=True,env=env,timeout=900); r=subprocess.run([str(pd/".venv/bin/python"),"-c","import json,torch,triton; print(json.dumps({'python_ok':True,'torch':torch.__version__,'triton':triton.__version__,'cuda_available':bool(torch.cuda.is_available())}))"],check=True,capture_output=True,text=True,timeout=60); (pd/"agentics-env.json").write_text(r.stdout); shutil.rmtree(sd/"uv-cache",ignore_errors=True); return 0
if __name__=="__main__": raise SystemExit(main())
