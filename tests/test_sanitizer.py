from kernelwitness.sanitizer import parse

def test_memcheck_parser():
    raw='''========= Invalid __global__ read of size 16 bytes
=========     at fused_attention_fwd(float*)
=========     by thread (17,0,0) in block (83,0,0)
=========     attention.cu:441
'''
    f=parse("memcheck",raw)
    assert f and "Invalid" in f[0].error
    assert f[0].source=="attention.cu:441"
