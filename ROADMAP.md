# Roadmap

## 0.1 — reproducibility core
- [x] command recorder and failure classifier
- [x] NVIDIA environment doctor
- [x] Compute Sanitizer orchestration and structured parsing
- [x] GPU coredump environment configuration
- [x] failure-preserving parameter minimizer
- [x] PyTorch per-op synchronization tracer
- [x] candidate/oracle numerical comparison
- [x] static HTML/JSON/GitHub report bundle
- [x] privacy redaction

## 0.2 — framework adapters
- [ ] first-class Triton JIT metadata capture
- [ ] JAX/XLA crash context
- [ ] CuPy RawKernel launch context
- [ ] `torch.compile` / Inductor generated-source capture hooks
- [ ] CUDA Graph on/off matrix runner

## 0.3 — reducers
- [ ] Python file ddmin reducer
- [ ] tensor-shape reducer API
- [ ] dtype/layout reducer
- [ ] environment/config reducer
- [ ] multi-GPU topology reducer

## Long-term
- [ ] plugin interface for external crash classifiers
- [ ] report schema stabilization
- [ ] issue-template integrations for major GPU OSS projects
- [ ] optional ROCm backend without weakening CUDA-native tooling
