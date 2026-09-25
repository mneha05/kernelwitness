# Security and privacy

KernelWitness treats crash logs as potentially sensitive. Reports redact the current home directory and common secret/token patterns. Environment capture is allowlisted rather than dumping `os.environ`.

Repro bundles do not automatically include application source files. Add source to an issue only after reviewing it yourself.

For security-sensitive vulnerabilities, contact the maintainer privately rather than publishing an exploit reproducer.
