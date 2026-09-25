from pathlib import Path
from kernelwitness.minimize import minimize_spec

def test_minimize(tmp_path, monkeypatch):
    root=Path(__file__).parents[1]
    monkeypatch.chdir(root)
    r=minimize_spec(root/"examples/kernelwitness.toml",tmp_path)
    assert r.parameters["seq"]==257
    assert r.parameters["heads"]==1
