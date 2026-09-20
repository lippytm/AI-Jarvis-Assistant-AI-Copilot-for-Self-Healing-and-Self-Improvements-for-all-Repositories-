from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED = (
    "repository", "commit_before", "commit_after", "finding_id", "reproducer_before",
    "reproducer_after", "tests", "rollback", "monitoring", "owner_approval",
)


class ResolutionEvidence:
    """Build a tamper-evident manifest without claiming universal bug elimination."""

    def build(self, path: Path) -> dict[str, Any]:
        record = json.loads(path.read_text(encoding="utf-8"))
        missing = [key for key in REQUIRED if key not in record]
        if missing:
            raise ValueError("Missing resolution evidence: " + ", ".join(missing))
        tests = record["tests"]
        if not isinstance(tests, list) or not tests:
            raise ValueError("tests must contain at least one result")
        failed = [item for item in tests if item.get("status") != "passed"]
        gates = {
            "original_reproducer_failed_before": record["reproducer_before"].get("status") == "failed",
            "original_reproducer_passed_after": record["reproducer_after"].get("status") == "passed",
            "all_tests_passed": not failed,
            "rollback_documented": bool(str(record["rollback"]).strip()),
            "monitoring_documented": bool(str(record["monitoring"]).strip()),
            "owner_approved": record["owner_approval"] is True,
            "distinct_commits": record["commit_before"] != record["commit_after"],
        }
        status = "verified_candidate" if all(gates.values()) else "not_verified"
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        return {
            "schema_version": "1.0",
            "status": status,
            "gates": gates,
            "failed_tests": failed,
            "evidence_sha256": hashlib.sha256(canonical).hexdigest(),
            "record": record,
            "residual_risk": record.get("residual_risk", ["Unknown defects may remain."]),
            "claim": (
                "The documented defect passed the defined verification gates."
                if status == "verified_candidate"
                else "The documented defect has not passed every verification gate."
            ),
            "non_claim": "This manifest does not prove the repository is free of all errors or vulnerabilities.",
        }

    def markdown(self, manifest: dict[str, Any]) -> str:
        record = manifest["record"]
        gate_lines = "\n".join(
            f"- [{'x' if passed else ' '}] {name.replace('_', ' ')}"
            for name, passed in manifest["gates"].items()
        )
        residual = "\n".join(f"- {item}" for item in manifest["residual_risk"])
        return (
            f"# Resolution Evidence — {record['finding_id']}\n\n"
            f"- Repository: {record['repository']}\n"
            f"- Before: {record['commit_before']}\n"
            f"- After: {record['commit_after']}\n"
            f"- Status: **{manifest['status']}**\n"
            f"- Evidence SHA-256: `{manifest['evidence_sha256']}`\n\n"
            f"## Verification gates\n\n{gate_lines}\n\n"
            f"## Residual risk\n\n{residual}\n\n"
            f"## Scope statement\n\n{manifest['non_claim']}\n"
        )


def build_files(source: Path, output_dir: Path) -> dict[str, str]:
    engine = ResolutionEvidence()
    manifest = engine.build(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "resolution-evidence.json"
    md_path = output_dir / "resolution-evidence.md"
    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(engine.markdown(manifest), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "status": manifest["status"]}
