from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any


SEVERITY = {"critical": 100, "high": 70, "medium": 40, "low": 15, "info": 0}


@dataclass(frozen=True)
class Finding:
    repository: str
    detector: str
    code: str
    severity: str
    confidence: float
    component: str
    evidence: str
    blast_radius: int = 1
    recurrence: int = 1

    @classmethod
    def from_dict(cls, item: dict[str, Any]) -> "Finding":
        severity = str(item.get("severity", "")).lower()
        if severity not in SEVERITY:
            raise ValueError(f"Unsupported severity: {severity}")
        confidence = float(item.get("confidence", 0))
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        blast = int(item.get("blast_radius", 1))
        recurrence = int(item.get("recurrence", 1))
        if not 1 <= blast <= 100 or not 1 <= recurrence <= 1000:
            raise ValueError("blast_radius or recurrence outside policy limits")
        required = ("repository", "detector", "code", "component", "evidence")
        if any(not str(item.get(key, "")).strip() for key in required):
            raise ValueError("finding is missing required identity or evidence")
        return cls(
            repository=str(item["repository"]), detector=str(item["detector"]),
            code=str(item["code"]), severity=severity, confidence=confidence,
            component=str(item["component"]), evidence=str(item["evidence"]),
            blast_radius=blast, recurrence=recurrence,
        )

    def fingerprint(self) -> str:
        identity = f"{self.repository}\0{self.code}\0{self.component}".encode()
        return hashlib.sha256(identity).hexdigest()[:20]


class FleetTriage:
    """Deduplicate and prioritize corroborated findings without changing repositories."""

    def analyze(self, raw_findings: list[dict[str, Any]]) -> dict[str, Any]:
        findings = [Finding.from_dict(item) for item in raw_findings]
        groups: dict[str, list[Finding]] = defaultdict(list)
        for finding in findings:
            groups[finding.fingerprint()].append(finding)
        queue = []
        for fingerprint, matches in groups.items():
            detectors = sorted({item.detector for item in matches})
            strongest = max(matches, key=lambda item: SEVERITY[item.severity])
            confidence = 1.0
            for item in matches:
                confidence *= 1 - item.confidence
            corroborated_confidence = round(1 - confidence, 4)
            score = self._score(
                strongest.severity,
                corroborated_confidence,
                max(item.blast_radius for item in matches),
                max(item.recurrence for item in matches),
                len(detectors),
            )
            queue.append({
                "fingerprint": fingerprint,
                "repository": strongest.repository,
                "component": strongest.component,
                "code": strongest.code,
                "severity": strongest.severity,
                "priority_score": score,
                "corroborated_confidence": corroborated_confidence,
                "detectors": detectors,
                "detector_count": len(detectors),
                "evidence": sorted({item.evidence for item in matches}),
                "mode": "diagnose_only",
                "next_action": self._next_action(strongest.severity, len(detectors)),
            })
        queue.sort(key=lambda item: (-item["priority_score"], item["repository"], item["code"]))
        return {
            "raw_finding_count": len(findings),
            "deduplicated_count": len(queue),
            "queue": queue,
            "claim": "Priority is a transparent routing aid, not proof of root cause.",
        }

    @staticmethod
    def _score(severity: str, confidence: float, blast: int, recurrence: int,
               detector_count: int) -> int:
        base = SEVERITY[severity]
        value = base + confidence * 20 + min(blast, 20) + min(recurrence, 10)
        value += min(max(detector_count - 1, 0) * 5, 15)
        return min(100, round(value))

    @staticmethod
    def _next_action(severity: str, detector_count: int) -> str:
        if severity == "critical":
            return "Contain exposure, preserve evidence, and request immediate owner review."
        if detector_count >= 2:
            return "Reproduce in an isolated environment and prepare a minimal repair experiment."
        return "Seek independent corroboration before proposing a repair."


def analyze_file(path: str) -> dict[str, Any]:
    payload = json.loads(open(path, encoding="utf-8").read())
    findings = payload.get("findings", payload)
    if not isinstance(findings, list):
        raise ValueError("Input must be a findings list or an object containing findings")
    return FleetTriage().analyze(findings)
