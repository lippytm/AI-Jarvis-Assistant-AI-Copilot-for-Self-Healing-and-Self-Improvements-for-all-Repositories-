from __future__ import annotations

import unittest

from scripts.readiness import assess


class ReadinessTests(unittest.TestCase):
    def test_repository_foundation_is_application_ready(self) -> None:
        result = assess()
        self.assertEqual("application_ready_foundation", result["status"])
        self.assertEqual([], result["failed"])
        self.assertIn("automatic merge", result["not_authorized"])


if __name__ == "__main__":
    unittest.main()
