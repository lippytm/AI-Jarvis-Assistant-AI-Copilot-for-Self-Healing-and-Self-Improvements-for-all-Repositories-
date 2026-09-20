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
            playbook = {"id": "same", "signals": [], "diagnostics": ["test"], "repair_gate": "review"}
            (root / "catalog/diagnostic-playbooks.json").write_text(
                json.dumps({"playbooks": [playbook, playbook]}), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "unique"):
                validate(root)


if __name__ == "__main__":
    unittest.main()
