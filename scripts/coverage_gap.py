from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CoverageGap:
    def analyze(self, registry: Path, evidence: Path) -> dict[str, Any]:
        enhancements = json.loads(registry.read_text(encoding="utf-8")).get("enhancements", [])
        observed = json.loads(evidence.read_text(encoding="utf-8"))
        completed = set(observed.get("completed", []))
        active = set(observed.get("active", []))
        known = {item["id"] for item in enhancements}
        unknown = sorted((completed | active) - known)
        if unknown:
            raise ValueError(f"Unknown enhancement IDs: {', '.join(unknown)}")
        gaps = []
        for item in enhancements:
            status = "completed" if item["id"] in completed else "active" if item["id"] in active else "not_started"
            if status != "completed":
                gaps.append({
                    "id": item["id"], "name": item["name"], "phase": item["phase"],
                    "status": status, "required_evidence": item["evidence"], "gate": item["gate"],
                })
        return {
            "total": len(enhancements),
            "completed": len(completed),
            "active": len(active),
            "gaps": gaps,
            "coverage_percent": round(len(completed) / len(enhancements) * 100, 2) if enhancements else 0,
            "claim": "Coverage measures catalog adoption, not security effectiveness.",
        }
