from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_PATHS = (
    "catalog/diagnostic-playbooks.json",
    "catalog/detection-layers.json",
    "catalog/security-controls.json",
    "catalog/anti-malware-controls.json",
    "catalog/rnd-enhancements.json",
    "catalog/patcher-roles.json",
    "policy/fleet-policy.json",
    "policy/incident-state-machine.json",
    "policy/suspicious-artifact-state-machine.json",
    "policy/experiment-policy.json",
    "schemas/patch-input.schema.json",
    "schemas/resolution-evidence.schema.json",
)


def assess(root: Path = Path(".")) -> dict[str, Any]:
    checks = []
    for relative in REQUIRED_PATHS:
        path = root / relative
        checks.append({"check": f"file:{relative}", "passed": path.is_file()})
    policy_path = root / "policy/fleet-policy.json"
    if policy_path.is_file():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        checks.extend([
            {"check": "read_only_default", "passed": policy.get("default_mode") == "read_only"},
            {"check": "draft_pr_repairs", "passed": policy.get("repair_mode") == "draft_pull_request_only"},
            {"check": "owner_approval", "passed": policy.get("require_owner_approval") is True},
        ])
    roles_path = root / "catalog/patcher-roles.json"
    if roles_path.is_file():
        roles = json.loads(roles_path.read_text(encoding="utf-8")).get("roles", [])
        authors = [item for item in roles if item.get("may_write_code")]
        unsafe = [item for item in authors if item.get("may_approve")]
        checks.append({"check": "separation_of_duties", "passed": bool(authors) and not unsafe})
    failed = [item for item in checks if not item["passed"]]
    return {
        "status": "application_ready_foundation" if not failed else "not_ready",
        "checks": checks,
        "failed": failed,
        "safe_capabilities": [
            "validate policies", "triage findings", "plan patches",
            "generate resolution evidence", "report R&D coverage gaps",
        ],
        "not_authorized": [
            "automatic code changes", "automatic merge", "automatic deploy",
            "secret operations", "production containment without incident authority",
        ],
        "claim": "Ready foundation means interfaces and safeguards are present; each target repository still needs onboarding and tests.",
    }
