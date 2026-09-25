from __future__ import annotations
import json, shlex, subprocess, time, tomllib
from dataclasses import dataclass, asdict
from pathlib import Path
from .classifier import classify

@dataclass
class ReductionStep:
    parameter: str
    before: object
    candidate: object
    kept: bool
    kind: str
    duration_s: float

@dataclass
class ReductionResult:
    expected: str
    parameters: dict[str, object]
    command: list[str]
    history: list[ReductionStep]

def _format(command: list[str], values: dict[str, object]) -> list[str]:
    return [str(part).format(**values) for part in command]

def _fails(command: list[str], expected: str, timeout: float) -> tuple[bool,str,float]:
    t=time.perf_counter()
    try:
        p=subprocess.run(command,text=True,capture_output=True,timeout=timeout)
        c=classify(p.stdout or "",p.stderr or "",p.returncode,False)
    except subprocess.TimeoutExpired:
        c=classify("","",None,True)
    return c.kind==expected,c.kind,time.perf_counter()-t

def minimize_spec(path: str|Path, out_dir: str|Path="kernelwitness-minimized") -> ReductionResult:
    cfg=tomllib.loads(Path(path).read_text(encoding="utf-8"))
    repro=cfg["repro"]; params=cfg["parameters"]
    command=list(repro["command"]); expected=repro["expected"]; timeout=float(repro.get("timeout",60))
    current={k:(cfg.get("initial",{}).get(k,v[-1])) for k,v in params.items()}
    initial_cmd=_format(command,current)
    ok,kind,_=_fails(initial_cmd,expected,timeout)
    if not ok: raise RuntimeError(f"initial command does not reproduce {expected}; saw {kind}")
    history=[]; changed=True
    while changed:
        changed=False
        for name,candidates in params.items():
            ordered=list(candidates)
            try:
                current_index=ordered.index(current[name])
                smaller=ordered[:current_index]
            except ValueError:
                smaller=ordered
            for candidate in smaller:
                trial=dict(current); trial[name]=candidate
                ok,kind,dur=_fails(_format(command,trial),expected,timeout)
                history.append(ReductionStep(name,current[name],candidate,ok,kind,dur))
                if ok:
                    current[name]=candidate; changed=True; break
    final=_format(command,current)
    result=ReductionResult(expected,current,final,history)
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    (out/"reduction.json").write_text(json.dumps({"expected":expected,"parameters":current,"command":final,"history":[asdict(x) for x in history]},indent=2),encoding="utf-8")
    (out/"repro.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n"+" ".join(shlex.quote(x) for x in final)+"\n",encoding="utf-8")
    lines=["[repro]",f'expected = "{expected}"',"command = ["+", ".join(json.dumps(x) for x in command)+"]","","[parameters]"]
    for k,v in current.items(): lines.append(f"{k} = [{json.dumps(v)}]")
    (out/"minimized.toml").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return result
