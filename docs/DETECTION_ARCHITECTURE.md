# Defense-in-Depth Detection and Fast Triage

The fleet uses overlapping but failure-independent diagnostic layers. Contract, build, test,
static analysis, security, runtime, recovery, and independent challenge detectors examine
different failure modes. Duplication is useful only when detectors fail differently.

Findings are deduplicated by repository, code, and component. Independent detector confidence
is combined transparently, while severity, blast radius, recurrence, and corroboration produce
a bounded priority score. The score routes attention; it does not establish root cause.

## Performance strategy

- Scan changed repositories before unchanged repositories.
- Run cheap deterministic checks before expensive AI analysis.
- Cache results by repository commit and tool-policy version.
- Deduplicate before requesting model reviews.
- Limit parallel diagnostics and repair experiments.
- Stop repeated failures at the configured retry boundary.
- Reserve immediate containment for critical exposure.
- Require independent corroboration before closing high-impact findings.

Resilience is preferred over claims of invulnerability. Every detector, repair service, and
workflow can fail; the system must expose degraded coverage and preserve a manual recovery path.
