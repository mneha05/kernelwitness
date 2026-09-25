from __future__ import annotations
import shlex, zipfile
from pathlib import Path
from .models import RunReport

def make_bundle(r: RunReport, out_dir: str|Path) -> Path:
    out=Path(out_dir); bundle=out/"kernelwitness-repro.zip"
    (out/"command.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n"+" ".join(shlex.quote(x) for x in r.command)+"\n",encoding="utf-8")
    with zipfile.ZipFile(bundle,"w",zipfile.ZIP_DEFLATED) as z:
        for name in ["index.html","report.json","github.md","command.sh"]:
            p=out/name
            if p.exists(): z.write(p,name)
        for i,a in enumerate(r.attempts,1):
            z.writestr(f"attempts/{i:02d}-stdout.txt",a.stdout)
            z.writestr(f"attempts/{i:02d}-stderr.txt",a.stderr)
        if r.sanitizer_raw: z.writestr("sanitizer.txt",r.sanitizer_raw)
    return bundle
