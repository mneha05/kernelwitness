"""Deterministic CI fixture that behaves like an async CUDA fault."""
import argparse, sys, time
p=argparse.ArgumentParser(); p.add_argument("--seq",type=int,default=4096); p.add_argument("--heads",type=int,default=32); a=p.parse_args()
print(f"launch fused_attention_fwd(seq={a.seq}, heads={a.heads})")
time.sleep(.03)
if a.seq >= 257 and a.heads >= 1:
    print("RuntimeError: CUDA error: an illegal memory access was encountered",file=sys.stderr)
    print("Compile with TORCH_USE_CUDA_DSA to enable device-side assertions.",file=sys.stderr)
    raise SystemExit(1)
print("ok")
