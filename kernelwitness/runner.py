from __future__ import annotations
import os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from .classifier import classify
from .doctor import snapshot
from .models import Attempt, RunReport, Classification
from .redact import redact_text
from . import sanitizer

FAILURE_KINDS={"illegal_memory_access","device_assert","misaligned_address","launch_failure","race","sync_error","uninitialized","oom","timeout","numerical_mismatch","segfault","process_failure"}

def run_command(command: list[str], attempts: int=3, timeout: float=120, sanitizer_tool: str="none", coredump: bool=False, out_dir: str|Path="kernelwitness-report") -> RunReport:
    env=os.environ.copy()
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    if coredump:
        env["CUDA_ENABLE_COREDUMP_ON_EXCEPTION"]="1"
        env["CUDA_COREDUMP_FILE"]=str(out_dir/"core_%p.nvcudmp")
        env.setdefault("CUDA_COREDUMP_GENERATION_FLAGS","skip_abort")
    rows=[]; reproduced=0
    for i in range(1, attempts+1):
        t=time.perf_counter(); timed_out=False
        try:
            p=subprocess.run(command,text=True,capture_output=True,timeout=timeout,env=env)
            rc=p.returncode; so=p.stdout or ""; se=p.stderr or ""
        except subprocess.TimeoutExpired as e:
            rc=None; so=(e.stdout or "") if isinstance(e.stdout,str) else ""; se=(e.stderr or "") if isinstance(e.stderr,str) else ""; timed_out=True
        duration=time.perf_counter()-t
        so,se=redact_text(so),redact_text(se)
        c=classify(so,se,rc,timed_out)
        if c.kind in FAILURE_KINDS: reproduced+=1
        rows.append(Attempt(i,rc,duration,so[-12000:],se[-12000:],timed_out,c))
    chosen=next((a.classification for a in rows if a.classification and a.classification.kind!="success"), rows[0].classification if rows else Classification("unknown","Unknown",0,[]))
    findings=[]; sanitizer_raw=""; notes=[]; torch_trace={}
    for a in rows:
        for line in a.stderr.splitlines():
            if line.startswith("KERNELWITNESS_OP="):
                try:
                    import json
                    torch_trace=json.loads(line.split("=",1)[1])
                except Exception:
                    pass
    if sanitizer_tool == "auto":
        sanitizer_tool={
            "race":"racecheck", "uninitialized":"initcheck", "sync_error":"synccheck",
            "illegal_memory_access":"memcheck", "misaligned_address":"memcheck",
            "device_assert":"memcheck", "launch_failure":"memcheck"
        }.get(chosen.kind,"memcheck")
    if sanitizer_tool != "none":
        if sanitizer.available():
            try:
                rc,so,se,findings=sanitizer.run(sanitizer_tool,command,timeout,coredump)
                sanitizer_raw=redact_text((so or "")+"\n"+(se or ""))[-30000:]
            except Exception as e:
                notes.append(f"sanitizer run failed: {type(e).__name__}: {e}")
        else:
            notes.append("compute-sanitizer not found; sanitizer phase skipped")
    coredumps=[str(p) for p in out_dir.glob("*.nvcudmp")]
    return RunReport("1.0", datetime.now(timezone.utc).isoformat(), command, snapshot(), rows, reproduced, attempts, chosen, findings, sanitizer_raw, torch_trace, coredumps, notes)
