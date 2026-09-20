from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.coverage_gap import CoverageGap


class CoverageGapTests(unittest.TestCase):
    def test_gap_report_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "registry.json"
            evidence = root / "evidence.json"
            registry.write_text(json.dumps({"enhancements": [
                {"id": "A", "name": "a", "phase": "pilot", "evidence": "x", "gate": "g"},
                {"id": "B", "name": "b", "phase": "research", "evidence": "y", "gate": "g"},
            ]}), encoding="utf-8")
            evidence.write_text(json.dumps({"completed": ["A"], "active": []}), encoding="utf-8")
            result = CoverageGap().analyze(registry, evidence)
            self.assertEqual(50, result["coverage_percent"])
            self.assertEqual("B", result["gaps"][0]["id"])

    def test_unknown_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "registry.json"
            evidence = root / "evidence.json"
            registry.write_text('{"enhancements":[]}', encoding="utf-8")
            evidence.write_text('{"completed":["X"]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unknown"):
                CoverageGap().analyze(registry, evidence)


if __name__ == "__main__":
    unittest.main()
