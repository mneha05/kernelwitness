from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Classification:
    kind: str
    title: str
    confidence: float
    evidence: list[str] = field(default_factory=list)

@dataclass
class ToolInfo:
    name: str
    available: bool
    version: str = ""
    path: str = ""

@dataclass
class EnvironmentSnapshot:
    platform: str
    python: str
    hostname: str
    cwd: str
    gpu: dict[str, Any] = field(default_factory=dict)
    tools: list[ToolInfo] = field(default_factory=list)
    packages: dict[str, str] = field(default_factory=dict)

@dataclass
class Attempt:
    index: int
    returncode: int | None
    duration_s: float
    stdout: str
    stderr: str
    timed_out: bool = False
    classification: Classification | None = None

@dataclass
class SanitizerFinding:
    tool: str
    error: str
    kernel: str = ""
    source: str = ""
    thread: str = ""
    block: str = ""
    raw: str = ""

@dataclass
class RunReport:
    schema_version: str
    created_at: str
    command: list[str]
    environment: EnvironmentSnapshot
    attempts: list[Attempt]
    reproduced: int
    total_attempts: int
    classification: Classification
    sanitizer_findings: list[SanitizerFinding] = field(default_factory=list)
    sanitizer_raw: str = ""
    torch_trace: dict[str, Any] = field(default_factory=dict)
    coredumps: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
