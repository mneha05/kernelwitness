from __future__ import annotations
import importlib.metadata, json, platform, shutil, socket, subprocess, sys
from pathlib import Path
from .models import EnvironmentSnapshot, ToolInfo
from .redact import redact_text

TOOLS = ["nvidia-smi", "nvcc", "compute-sanitizer", "cuda-gdb", "nsys", "ncu"]

def _version(cmd: str) -> tuple[bool, str, str]:
    path = shutil.which(cmd)
    if not path:
        return False, "", ""
    args = [path, "--version"]
    if cmd == "nvidia-smi": args = [path, "--query-gpu=name,driver_version,memory.total,compute_cap", "--format=csv,noheader"]
    try:
        p = subprocess.run(args, text=True, capture_output=True, timeout=4)
        text = (p.stdout or p.stderr).strip().splitlines()
        return True, redact_text(text[0] if text else "available"), path
    except Exception as e:
        return True, f"available ({type(e).__name__})", path

def snapshot() -> EnvironmentSnapshot:
    tools=[]; gpu={}
    for name in TOOLS:
        ok, ver, path = _version(name)
        tools.append(ToolInfo(name, ok, ver, path))
        if name == "nvidia-smi" and ok:
            parts=[x.strip() for x in ver.split(",")]
            if parts: gpu["name"] = parts[0]
            if len(parts)>1: gpu["driver"] = parts[1]
            if len(parts)>2: gpu["memory"] = parts[2]
            if len(parts)>3: gpu["compute_capability"] = parts[3]
    pkgs={}
    for name in ["torch", "triton", "numpy", "cupy-cuda12x", "jax", "jaxlib"]:
        try: pkgs[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: pass
    return EnvironmentSnapshot(
        platform=f"{platform.system()} {platform.release()} {platform.machine()}",
        python=sys.version.split()[0], hostname=socket.gethostname(), cwd=redact_text(str(Path.cwd())),
        gpu=gpu, tools=tools, packages=pkgs,
    )

def as_json() -> str:
    from dataclasses import asdict
    return json.dumps(asdict(snapshot()), indent=2)
