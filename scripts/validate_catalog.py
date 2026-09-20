from __future__ import annotations

import json
from pathlib import Path


def validate(root: Path = Path(".")) -> dict[str, int]:
    catalog = json.loads((root / "catalog/diagnostic-playbooks.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "policy/fleet-policy.json").read_text(encoding="utf-8"))
    layers = json.loads((root / "catalog/detection-layers.json").read_text(encoding="utf-8"))
    security = json.loads((root / "catalog/security-controls.json").read_text(encoding="utf-8"))
    incidents = json.loads((root / "policy/incident-state-machine.json").read_text(encoding="utf-8"))
    antimalware = json.loads((root / "catalog/anti-malware-controls.json").read_text(encoding="utf-8"))
    artifacts = json.loads((root / "policy/suspicious-artifact-state-machine.json").read_text(encoding="utf-8"))
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
    detection_layers = layers.get("layers")
    if not isinstance(detection_layers, list) or len(detection_layers) < 8:
        raise ValueError("defense-in-depth registry requires at least eight layers")
    layer_ids = [item.get("id") for item in detection_layers]
    if len(layer_ids) != len(set(layer_ids)):
        raise ValueError("detection layer IDs must be unique")
    families = security.get("control_families")
    if not isinstance(families, list) or len(families) < 10:
        raise ValueError("security registry requires at least ten control families")
    states = incidents.get("states")
    state_names = {item.get("state") for item in states or []}
    required_states = {"suspected", "investigating", "contained", "repairing", "verifying", "resolved"}
    if not required_states.issubset(state_names):
        raise ValueError("incident lifecycle is missing required states")
    if incidents.get("production_authority") != "owner_approval_required":
        raise ValueError("incident production authority must require owner approval")
    malware_controls = antimalware.get("controls")
    if not isinstance(malware_controls, list) or len(malware_controls) < 15:
        raise ValueError("anti-malware registry requires at least fifteen controls")
    artifact_states = {item.get("state") for item in artifacts.get("states", [])}
    if not {"untrusted", "scanning", "suspicious", "unknown", "resolved"}.issubset(artifact_states):
        raise ValueError("suspicious artifact lifecycle is incomplete")
    if artifacts.get("default_for_disagreement") != "unknown":
        raise ValueError("scanner disagreement must default to unknown")
    if artifacts.get("default_for_missing_evidence") != "untrusted":
        raise ValueError("missing evidence must default to untrusted")
    if policy.get("default_mode") != "read_only":
        raise ValueError("default fleet mode must remain read_only")
    if policy.get("repair_mode") != "draft_pull_request_only":
        raise ValueError("repair mode must remain draft_pull_request_only")
    if not policy.get("require_owner_approval"):
        raise ValueError("owner approval must remain required")
    return {"playbooks": len(playbooks), "detection_layers": len(detection_layers), "security_families": len(families), "incident_states": len(states), "anti_malware_controls": len(malware_controls), "artifact_states": len(artifact_states), "prohibited_actions": len(policy.get("prohibited", []))}


if __name__ == "__main__":
    print(json.dumps(validate(), sort_keys=True))
