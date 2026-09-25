from __future__ import annotations
import json, runpy, sys, traceback

def run_script(script: str, argv: list[str]) -> int:
    try:
        import torch
        from torch.utils._python_dispatch import TorchDispatchMode
    except Exception as e:
        print(f"KernelWitness torch trace unavailable: {e}", file=sys.stderr); return 2
    class SyncEveryOp(TorchDispatchMode):
        def __init__(self): self.i=0
        def __torch_dispatch__(self, func, types, args=(), kwargs=None):
            kwargs=kwargs or {}; self.i+=1
            try:
                out=func(*args,**kwargs)
                if torch.cuda.is_available(): torch.cuda.synchronize()
                return out
            except Exception:
                marker={"index":self.i,"op":str(func)}
                print("KERNELWITNESS_OP="+json.dumps(marker),file=sys.stderr,flush=True)
                raise
    old=sys.argv; sys.argv=[script]+argv
    try:
        with SyncEveryOp(): runpy.run_path(script,run_name="__main__")
        return 0
    except SystemExit as e:
        return int(e.code or 0)
    except Exception:
        traceback.print_exc(); return 1
    finally: sys.argv=old
