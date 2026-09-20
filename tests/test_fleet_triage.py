from __future__ import annotations

import unittest

from scripts.fleet_triage import FleetTriage


class FleetTriageTests(unittest.TestCase):
    def finding(self, detector: str, severity: str = "high", confidence: float = 0.8) -> dict:
        return {
            "repository": "lippytm/example",
            "detector": detector,
            "code": "dependency-risk",
            "severity": severity,
            "confidence": confidence,
            "component": "requirements.txt",
            "evidence": f"{detector}-evidence",
            "blast_radius": 4,
            "recurrence": 3,
        }

    def test_overlapping_detectors_are_deduplicated_and_corroborated(self) -> None:
        result = FleetTriage().analyze([
            self.finding("scanner-a", confidence=0.7),
            self.finding("scanner-b", confidence=0.8),
        ])
        self.assertEqual(2, result["raw_finding_count"])
        self.assertEqual(1, result["deduplicated_count"])
        item = result["queue"][0]
        self.assertEqual(2, item["detector_count"])
        self.assertAlmostEqual(0.94, item["corroborated_confidence"])
        self.assertIn("isolated", item["next_action"])

    def test_critical_finding_routes_to_containment(self) -> None:
        result = FleetTriage().analyze([self.finding("scanner", "critical", 0.9)])
        self.assertIn("Contain", result["queue"][0]["next_action"])

    def test_invalid_confidence_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "confidence"):
            FleetTriage().analyze([self.finding("scanner", confidence=2.0)])

    def test_order_is_deterministic(self) -> None:
        first = self.finding("a", "medium", 0.7)
        second = {
            **self.finding("b", "critical", 0.9),
            "repository": "lippytm/urgent",
            "code": "secret-exposure",
            "component": ".env",
        }
        result = FleetTriage().analyze([first, second])
        self.assertEqual("lippytm/urgent", result["queue"][0]["repository"])


if __name__ == "__main__":
    unittest.main()
