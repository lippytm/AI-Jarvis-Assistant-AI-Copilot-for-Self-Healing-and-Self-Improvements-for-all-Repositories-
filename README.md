# AI Jarvis Repository Self-Healing Copilot

Fleet control plane for continuous diagnosis, tested repair proposals, and measurable software
quality across the lippytm repository portfolio.

## Operating loop

Inventory → classify → reproduce → diagnose → propose → sandbox → test → draft PR → approve →
merge → monitor → learn.

## Safety contract

- Read-only discovery is automatic.
- Every repair uses a dedicated branch and draft pull request.
- Tests, static analysis, dependency checks, secret scanning, and rollback evidence are required.
- Jarvis never force-pushes, merges, deploys, publishes, deletes, rotates secrets, or spends
  money without explicit owner approval.
- A passing check reduces known risk; it never proves that a repository is bug-free.
- Language-specific tools are selected from a versioned catalog and run only when their
  configuration or a reviewed default is present.

## Foundation

- `policy/fleet-policy.json` defines fleet limits and approval boundaries.
- `catalog/diagnostic-playbooks.json` maps repository evidence to diagnostic tools.
- `docs/REPAIR_PROTOCOL.md` defines reproducibility, repair, validation, rollback, and learning.
- `catalog/detection-layers.json` defines eight failure-independent detection layers.
- `scripts/fleet_triage.py` deduplicates, corroborates, and prioritizes fleet findings.
- `docs/DETECTION_ARCHITECTURE.md` defines fast scanning, caching, containment, and degraded-mode transparency.
- `catalog/security-controls.json` defines layered vulnerability-prevention and recovery controls.
- `policy/incident-state-machine.json` makes security finding status changes auditable.
- `docs/SECURITY_RESILIENCE.md` defines evidence required before high-impact findings close.
- Development stays on review branches; `main` remains the approved baseline.
