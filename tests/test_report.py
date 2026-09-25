from kernelwitness.demo import sample_report
from kernelwitness.report import render

def test_report(tmp_path):
    p=render(sample_report(),tmp_path)
    text=p.read_text()
    assert "CUDA FAILURE AUTOPSY" in text
    assert "Invalid __global__ read" in text
