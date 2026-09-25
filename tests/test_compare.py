from kernelwitness.compare import _walk

def test_numeric_walk():
    d=_walk([1.0,2.1],[1.0,2.0])
    assert max(x[0] for x in d) > .09
