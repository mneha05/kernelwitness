# Contributing

KernelWitness is intentionally backend-oriented: failure classifiers, parsers, reducers and report adapters should stay small and independently testable.

## Useful contributions
- new Compute Sanitizer parser fixtures
- ROCm / HIP backend experiments behind optional modules
- framework adapters for Triton, JAX and CuPy
- reduction strategies that preserve a target failure signature
- report UI improvements that remain fully static

Run `pytest` before opening a pull request. Please do not include proprietary crash logs in tests; reduce them to synthetic fixtures first.
