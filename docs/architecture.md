# Architecture

```text
command
  │
  ├─ recorder ── attempts ── failure classifier
  │                              │
  │                              ├─ illegal memory access
  │                              ├─ device assertion
  │                              ├─ OOM / timeout / segfault
  │                              └─ numerical mismatch
  │
  ├─ optional Compute Sanitizer ── memcheck/racecheck/initcheck/synccheck
  │
  ├─ environment doctor ── nvidia-smi/nvcc/cuda-gdb/nsys/ncu/framework versions
  │
  └─ report writer ── HTML + JSON + GitHub Markdown + repro ZIP

parameterized reproducer TOML
  │
  └─ reducer ── candidate search ── same failure signature ── minimized repro.sh
```
