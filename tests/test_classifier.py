from kernelwitness.classifier import classify

def test_illegal_memory_access():
    c=classify("","RuntimeError: CUDA error: an illegal memory access was encountered",1)
    assert c.kind=="illegal_memory_access"

def test_success():
    assert classify("ok","",0).kind=="success"
