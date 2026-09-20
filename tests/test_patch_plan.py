from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.patch_plan import PatchPlan


class PatchPlanTests(unittest.TestCase):
    def issue(self) -> dict:
        return {
            "repository": "lippytm/example",
            "finding_id": "BUG-42",
            "summary": "Parser rejects valid input",
            "reproducer": "python -m unittest tests.test_parser",
            "suspected_files": ["src/parser.py", "tests/test_parser.py"],
            "hypothesis": "Boundary condition is incorrect.",
        }

    def test_plan_is_deterministic_and_review_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            path.write_text(json.dumps(self.issue()), encoding="utf-8")
            first = PatchPlan().build(path)
            second = PatchPlan().build(path)
            self.assertEqual(first["patch_id"], second["patch_id"])
            self.assertEqual("draft_pull_request_only", first["mode"])
            self.assertIn("weaken_test_to_make_it_pass", first["prohibited"])

    def test_large_patch_surface_trips_circuit_breaker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            issue = self.issue()
            issue["suspected_files"] = [f"file-{number}" for number in range(21)]
            path = Path(directory) / "issue.json"
            path.write_text(json.dumps(issue), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Circuit breaker"):
                PatchPlan().build(path)

    def test_production_write_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            issue = self.issue()
            issue["production_write_required"] = True
            path = Path(directory) / "issue.json"
            path.write_text(json.dumps(issue), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "production"):
                PatchPlan().build(path)


if __name__ == "__main__":
    unittest.main()
