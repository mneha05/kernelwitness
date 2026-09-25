from __future__ import annotations
import re
from .models import Classification

RULES = [
    ("illegal_memory_access", "Illegal memory access", 0.99, [r"illegal memory access", r"invalid __global__ (read|write)", r"out of bounds.*global"]),
    ("device_assert", "Device-side assertion", 0.98, [r"device-side assert", r"device side assert"]),
    ("misaligned_address", "Misaligned address", 0.98, [r"misaligned address"]),
    ("launch_failure", "Kernel launch failure", 0.94, [r"unspecified launch failure", r"launch failed"]),
    ("race", "Data race", 0.97, [r"racecheck", r"hazard", r"data race"]),
    ("sync_error", "Synchronization error", 0.97, [r"synccheck", r"barrier.*error", r"divergent thread"]),
    ("uninitialized", "Uninitialized device memory", 0.96, [r"initcheck", r"uninitialized.*memory"]),
    ("oom", "GPU out of memory", 0.99, [r"cuda out of memory", r"outofmemoryerror", r"failed to allocate.*cuda"]),
    ("timeout", "GPU timeout or hang", 0.87, [r"launch timeout", r"timed out", r"watchdog"]),
    ("numerical_mismatch", "Numerical mismatch", 0.9, [r"kernelwitness numerical mismatch", r"wrong answer", r"mismatch"]),
    ("segfault", "Host segmentation fault", 0.98, [r"segmentation fault", r"sigsegv"]),
]

def classify(stdout: str, stderr: str, returncode: int | None = None, timed_out: bool = False) -> Classification:
    blob = f"{stdout}\n{stderr}".lower()
    if timed_out:
        return Classification("timeout", "Process timeout", 0.99, ["process exceeded configured timeout"])
    for kind, title, confidence, patterns in RULES:
        hits = [p for p in patterns if re.search(p, blob, re.I | re.S)]
        if hits:
            evidence = []
            for line in (stdout + "\n" + stderr).splitlines():
                if any(re.search(p, line, re.I) for p in patterns):
                    evidence.append(line.strip())
            return Classification(kind, title, confidence, evidence[:6])
    if returncode not in (None, 0):
        return Classification("process_failure", f"Process exited {returncode}", 0.75, [f"return code {returncode}"])
    return Classification("success", "No failure detected", 1.0, [])
