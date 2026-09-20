# Security Resilience and Vulnerability Prevention

Security is layered so one missed control does not become a fleet-wide failure. Each repository
should expose its assets, trust boundaries, permissions, secrets policy, dependency provenance,
input boundaries, diagnostic signals, containment path, and recovery evidence.

## Vulnerability lifecycle

Suspected → investigating → contained → repairing → verifying → resolved.

False positives are documented and used to tune detectors. Accepted risks require a named owner,
reason, monitoring plan, and expiration date. A finding cannot disappear merely because a tool
stopped reporting it.

## Closure evidence

Critical and high findings require:

1. Reproducible evidence or a documented false-positive explanation.
2. Smallest justified repair.
3. Regression protection.
4. Secret or permission remediation when applicable.
5. Tested rollback or restoration path.
6. Independent verification.
7. Owner review.
8. Post-repair monitoring.

No collection of controls is impregnable. Defense in depth makes compromise harder, detection
faster, blast radius smaller, and recovery more reliable.
