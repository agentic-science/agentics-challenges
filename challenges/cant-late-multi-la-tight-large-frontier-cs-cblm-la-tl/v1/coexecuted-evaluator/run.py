from __future__ import annotations
import argparse,contextlib,importlib.util,io,json,math,os,shutil,sys,tarfile
from pathlib import Path
ENV_PROJECT_DIR='frontier-cs-cpu-env'; ENV_ACTIVE='AGENTICS_FRONTIER_CPU_ENV_ACTIVE'
def reexec(a):
    import os,sys
    from pathlib import Path
    if os.environ.get(ENV_ACTIVE)=="1": return
    if not getattr(a,"setup_dir",None): return
    py=Path(a.setup_dir)/ENV_PROJECT_DIR/".venv/bin/python"
    if not py.is_file(): raise RuntimeError(f"setup environment missing {py}")
    e=os.environ.copy(); e[ENV_ACTIVE]="1"; os.execve(str(py),[str(py),*sys.argv],e)

def imp(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m
def safe_tar(tar,dst):
    base=dst.resolve()
    with tarfile.open(tar,'r:gz') as tf:
        for m in tf.getmembers():
            if m.issym() or m.islnk() or m.name.startswith('/') or '..' in Path(m.name).parts: raise RuntimeError('unsafe tar entry '+m.name)
            target=(dst/m.name).resolve()
            if target!=base and base not in target.parents: raise RuntimeError('tar escape '+m.name)
        tf.extractall(dst)
def finite(x):
    try: v=float(x)
    except Exception: return 0.0
    return v if math.isfinite(v) else 0.0
def cap(s): return [l.strip()[:500] for l in s.splitlines() if l.strip()][:12]
def write(out,mode,raw,logs):
    score=max(0,min(100,finite(raw.get('score',0)))); passed=('error' not in raw and finite(raw.get('runs_successfully',1))>0); key='validation_summary' if mode=='validation' else 'official_summary'; msg=str(raw.get('error','ok'))[:500]
    p={'status':'passed' if passed else 'failed','mode':mode,'aggregate_metrics':[{'metric_name':'score','value':score},{'metric_name':'avg_cost','value':finite(raw.get('avg_cost',raw.get('cost',0)))},{'metric_name':'successful_runs','value':1.0 if passed else 0.0},{'metric_name':'od_anchor','value':finite(raw.get('od_anchor',0))},{'metric_name':'spot_anchor','value':finite(raw.get('spot_anchor',0))}],key:{'score':score,'passed':1 if passed else 0,'total':1},'logs':(logs+([] if msg=='ok' else [msg]))[:12]}
    if mode=='validation': p['public_results']=[{'case_name':'public-smoke','status':'passed' if passed else 'failed','score':score,'message':msg}]
    Path(out).write_text(json.dumps(p,indent=2,sort_keys=True))
def run(a):
    cd=Path(a.challenge_dir); ws=Path(a.workspace_dir); sol=ws/'solution.py'
    if not sol.is_file(): return {'score':0,'runs_successfully':0,'error':'missing solution.py'},[]
    cfg=json.loads((cd/'coexecuted-evaluator/variant-config.json').read_text()); rt=Path(a.output_path).parent/'runtime/common'
    if rt.exists(): shutil.rmtree(rt)
    shutil.copytree(cd/'coexecuted-evaluator/source/common',rt,ignore=shutil.ignore_patterns('__pycache__','*.pyc','data','results','results-*'))
    data=rt/'cant-be-late-simulator/data'; data.mkdir(parents=True,exist_ok=True)
    if a.mode=='validation': shutil.copytree(cd/'public/data',data,dirs_exist_ok=True)
    else: safe_tar(cd/'private-benchmark/real_traces.tar.gz',data)
    sys.path.insert(0,str(rt)); os.environ.setdefault('WANDB_MODE','disabled'); os.environ.setdefault('EVALUATOR_MAX_WORKERS','4'); os.environ.setdefault('EVALUATOR_TIMEOUT','120'); os.environ.setdefault('GEPA_EVAL_TMPDIR',str(Path(a.output_path).parent/'tmp/sim-runs'))
    stream=io.StringIO(); spec=cd/'public/submission_spec.json'
    with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
        mod=imp(rt/'run_evaluator.py','agentics_cbl_eval')
        if cfg['family']=='cant_be_late': raw=mod.evaluate(sol,spec,env_paths=cfg['env_paths'],job_configs=cfg['job_configs'],changeover_delays=cfg['changeover_delays'])
        else: raw=mod.evaluate_solution(sol,spec,cfg['public_scenarios'] if a.mode=='validation' else cfg['official_scenarios'],cfg['deadline_hours'],cfg['restart_overhead_hours'])
    return raw if isinstance(raw,dict) else {'score':0,'error':'bad source result'},cap(stream.getvalue())
def main():
    p=argparse.ArgumentParser(); [p.add_argument(x,required=True) for x in ['--challenge-dir','--workspace-dir','--output-path','--mode','--target']]; p.add_argument('--setup-dir'); a=p.parse_args(); Path(a.output_path).parent.mkdir(parents=True,exist_ok=True); os.environ.setdefault('HOME',str(Path(a.output_path).parent)); os.environ.setdefault('TMPDIR',str(Path(a.output_path).parent/'tmp')); reexec(a)
    try: raw,logs=run(a)
    except Exception as e: raw,logs={'score':0,'runs_successfully':0,'error':str(e)},[]
    write(a.output_path,a.mode,raw,logs); return 0
if __name__=='__main__': raise SystemExit(main())
