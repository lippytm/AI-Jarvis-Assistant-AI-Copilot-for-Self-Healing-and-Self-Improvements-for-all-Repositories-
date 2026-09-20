from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_catalog import validate


class CatalogValidationTests(unittest.TestCase):
    def test_repository_catalog_is_valid(self) -> None:
        result = validate()
        self.assertGreaterEqual(result["playbooks"], 7)
        self.assertGreaterEqual(result["prohibited_actions"], 8)

    def test_duplicate_playbook_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "catalog").mkdir()
            (root / "policy").mkdir()
            playbook = {"id": "same", "signals": [], "diagnostics": ["test"], "repair_gate": "review"}
            (root / "catalog/diagnostic-playbooks.json").write_text(
                json.dumps({"playbooks": [playbook, playbook]}), encoding="utf-8"
            )
            (root / "catalog/detection-layers.json").write_text(json.dumps({
                "layers": [{"id": f"L{number}"} for number in range(8)]
            }), encoding="utf-8")
            (root / "catalog/security-controls.json").write_text(json.dumps({
                "control_families": [{"id": f"SEC-{number}"} for number in range(10)]
            }), encoding="utf-8")
            (root / "policy/incident-state-machine.json").write_text(json.dumps({
                "production_authority": "owner_approval_required",
                "states": [{"state": state} for state in [
                    "suspected", "investigating", "contained", "repairing", "verifying", "resolved"
                ]]
            }), encoding="utf-8")
            (root / "policy/fleet-policy.json").write_text(json.dumps({
                "default_mode": "read_only",
                "repair_mode": "draft_pull_request_only",
                "require_owner_approval": True,
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique"):
                validate(root)


if __name__ == "__main__":
    unittest.main()
