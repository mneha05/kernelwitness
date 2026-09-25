from __future__ import annotations
import json, math, subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class DiffResult:
    equal: bool
    max_abs: float
    max_rel: float
    path: str
    candidate: object
    oracle: object

def _last_json(text: str):
    for line in reversed(text.splitlines()):
        line=line.strip()
        if line:
            try: return json.loads(line)
            except json.JSONDecodeError: continue
    raise ValueError("command did not print a JSON value")

def _walk(a,b,path="$"):
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        aa=float(a); bb=float(b); absd=abs(aa-bb); reld=absd/max(abs(bb),1e-12)
        return [(absd,reld,path,a,b)]
    if isinstance(a,list) and isinstance(b,list):
        out=[]
        if len(a)!=len(b): return [(math.inf,math.inf,path+".length",len(a),len(b))]
        for i,(x,y) in enumerate(zip(a,b)): out += _walk(x,y,f"{path}[{i}]")
        return out
    if isinstance(a,dict) and isinstance(b,dict):
        if set(a)!=set(b): return [(math.inf,math.inf,path+".keys",sorted(a),sorted(b))]
        out=[]
        for k in sorted(a): out += _walk(a[k],b[k],f"{path}.{k}")
        return out
    return [(0.0,0.0,path,a,b)] if a==b else [(math.inf,math.inf,path,a,b)]

def compare_commands(candidate: str, oracle: str, atol: float=1e-5, rtol: float=1e-4, timeout: float=120, out_dir: str|Path="kernelwitness-compare") -> DiffResult:
    cp=subprocess.run(candidate,shell=True,text=True,capture_output=True,timeout=timeout)
    op=subprocess.run(oracle,shell=True,text=True,capture_output=True,timeout=timeout)
    if cp.returncode: raise RuntimeError(f"candidate exited {cp.returncode}: {cp.stderr[-1000:]}")
    if op.returncode: raise RuntimeError(f"oracle exited {op.returncode}: {op.stderr[-1000:]}")
    a=_last_json(cp.stdout); b=_last_json(op.stdout); diffs=_walk(a,b)
    worst=max(diffs,key=lambda x:(x[0],x[1])) if diffs else (0,0,"$",a,b)
    equal=all(absd <= atol + rtol*max(abs(float(y)) if isinstance(y,(int,float)) else 0,1e-12) for absd,_,_,_,y in diffs if math.isfinite(absd)) and all(math.isfinite(x[0]) for x in diffs)
    result=DiffResult(equal,worst[0],worst[1],worst[2],worst[3],worst[4])
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    (out/"comparison.json").write_text(json.dumps(asdict(result),indent=2,default=str))
    return result
