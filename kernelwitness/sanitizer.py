from __future__ import annotations
import re, shutil, subprocess
from .models import SanitizerFinding

ERROR_RE = re.compile(r"^=+\s+(?P<error>Invalid .*|Race reported.*|Uninitialized .*|Barrier error.*|Warp level .*|Program hit .*|CUDA error.*)$", re.I)
KERNEL_RE = re.compile(r"(?:at|by)\s+(?P<kernel>[^\s]+\([^\n]*\)|[^\s]+kernel[^\s]*)", re.I)
SOURCE_RE = re.compile(r"(?P<source>[^\s:]+\.(?:cu|cuh|cpp|cc|py):\d+)")
THREAD_RE = re.compile(r"thread \(([^)]+)\)", re.I)
BLOCK_RE = re.compile(r"block \(([^)]+)\)", re.I)

def available() -> bool:
    return shutil.which("compute-sanitizer") is not None

def run(tool: str, command: list[str], timeout: float, coredump: bool=False) -> tuple[int,str,str,list[SanitizerFinding]]:
    exe=shutil.which("compute-sanitizer")
    if not exe: raise FileNotFoundError("compute-sanitizer is not on PATH")
    cmd=[exe,"--tool",tool,"--error-exitcode","86"]
    if coredump: cmd += ["--generate-coredump","yes"]
    cmd += command
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=timeout)
    raw=(p.stdout or "")+"\n"+(p.stderr or "")
    return p.returncode,p.stdout,p.stderr,parse(tool,raw)

def parse(tool: str, raw: str) -> list[SanitizerFinding]:
    lines=raw.splitlines(); findings=[]
    for i,line in enumerate(lines):
        m=ERROR_RE.match(line.strip())
        if not m: continue
        chunk="\n".join(lines[i:i+12])
        km=KERNEL_RE.search(chunk); sm=SOURCE_RE.search(chunk); tm=THREAD_RE.search(chunk); bm=BLOCK_RE.search(chunk)
        findings.append(SanitizerFinding(
            tool=tool,error=m.group("error").strip(),kernel=km.group("kernel") if km else "",
            source=sm.group("source") if sm else "",thread=tm.group(1) if tm else "",
            block=bm.group(1) if bm else "",raw=chunk[:4000]))
    return findings
