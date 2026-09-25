from __future__ import annotations
from datetime import datetime, timezone
from .models import *

def sample_report() -> RunReport:
    env=EnvironmentSnapshot("Linux 6.x x86_64","3.12","demo-host","~/demo",{"name":"NVIDIA GB10","driver":"demo","memory":"128 GiB","compute_capability":"12.1"},[
        ToolInfo("nvidia-smi",True,"NVIDIA GB10, demo driver"),ToolInfo("nvcc",True,"CUDA 13.x"),ToolInfo("compute-sanitizer",True,"2026.x"),ToolInfo("cuda-gdb",True,"13.x"),ToolInfo("nsys",True,"available"),ToolInfo("ncu",True,"available")],{"torch":"2.x","triton":"3.x"})
    c=Classification("illegal_memory_access","Illegal memory access",0.99,["CUDA error: an illegal memory access was encountered"])
    at=[Attempt(1,1,.91,"","CUDA error: an illegal memory access was encountered",False,c),Attempt(2,1,.88,"","CUDA error: an illegal memory access was encountered",False,c),Attempt(3,1,.89,"","CUDA error: an illegal memory access was encountered",False,c)]
    f=[SanitizerFinding("memcheck","Invalid __global__ read of size 16","fused_attention_fwd","attention.cu:441","17,0,0","83,0,0")]
    return RunReport("1.0",datetime.now(timezone.utc).isoformat(),["python","crash.py","--seq","257"],env,at,3,3,c,f,"",{"index":1847,"op":"aten::_scaled_dot_product_flash_attention"},[],["demo data"])
