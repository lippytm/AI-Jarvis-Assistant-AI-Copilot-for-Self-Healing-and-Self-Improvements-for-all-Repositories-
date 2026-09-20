from __future__ import annotations

import json
from pathlib import Path


def validate(root: Path = Path(".")) -> dict[str, int]:
    catalog = json.loads((root / "catalog/diagnostic-playbooks.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "policy/fleet-policy.json").read_text(encoding="utf-8"))
    playbooks = catalog.get("playbooks")
    if not isinstance(playbooks, list) or not playbooks:
        raise ValueError("catalog requires at least one playbook")
    ids = [item.get("id") for item in playbooks]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("playbook IDs must be present and unique")
    for item in playbooks:
        if not isinstance(item.get("signals"), list):
            raise ValueError(f"{item['id']} signals must be a list")
        if not isinstance(item.get("diagnostics"), list) or not item["diagnostics"]:
            raise ValueError(f"{item['id']} requires diagnostics")
        if not item.get("repair_gate"):
            raise ValueError(f"{item['id']} requires repair_gate")
    if policy.get("default_mode") != "read_only":
        raise ValueError("default fleet mode must remain read_only")
    if policy.get("repair_mode") != "draft_pull_request_only":
        raise ValueError("repair mode must remain draft_pull_request_only")
    if not policy.get("require_owner_approval"):
        raise ValueError("owner approval must remain required")
    return {"playbooks": len(playbooks), "prohibited_actions": len(policy.get("prohibited", []))}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
