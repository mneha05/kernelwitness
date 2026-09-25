from __future__ import annotations
import os, re

_SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|authorization)\s*[=:]\s*[^\s,;]+"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]

def redact_text(text: str) -> str:
    if not text:
        return text
    home = os.path.expanduser("~")
    text = text.replace(home, "~") if home and home != "/" else text
    for pat in _SECRET_PATTERNS:
        text = pat.sub(lambda m: m.group(0).split("=")[0].split(":")[0] + "=<redacted>", text)
    return text
