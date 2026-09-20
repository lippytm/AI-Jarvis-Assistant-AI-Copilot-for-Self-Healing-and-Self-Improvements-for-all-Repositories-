from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.resolution_evidence import ResolutionEvidence, build_files


class ResolutionEvidenceTests(unittest.TestCase):
    def record(self) -> dict:
        return {
            "repository": "lippytm/example",
            "commit_before": "a" * 40,
            "commit_after": "b" * 40,
            "finding_id": "BUG-1",
            "reproducer_before": {"status": "failed", "command": "python -m unittest"},
            "reproducer_after": {"status": "passed", "command": "python -m unittest"},
            "tests": [{"name": "regression", "status": "passed"}],
            "rollback": "Revert the repair commit.",
            "monitoring": "Watch the error metric for seven days.",
            "owner_approval": True,
            "residual_risk": ["External dependency behavior remains outside this test."],
        }

    def test_complete_evidence_is_verified_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "record.json"
            source.write_text(json.dumps(self.record()), encoding="utf-8")
            result = build_files(source, root / "out")
            self.assertEqual("verified_candidate", result["status"])
            self.assertTrue(Path(result["json"]).exists())
            self.assertTrue(Path(result["markdown"]).exists())

    def test_failed_test_blocks_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = self.record()
            record["tests"].append({"name": "integration", "status": "failed"})
            source = root / "record.json"
            source.write_text(json.dumps(record), encoding="utf-8")
            manifest = ResolutionEvidence().build(source)
            self.assertEqual("not_verified", manifest["status"])
            self.assertFalse(manifest["gates"]["all_tests_passed"])

    def test_missing_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "record.json"
            source.write_text('{"repository":"x"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing"):
                ResolutionEvidence().build(source)


if __name__ == "__main__":
    unittest.main()
