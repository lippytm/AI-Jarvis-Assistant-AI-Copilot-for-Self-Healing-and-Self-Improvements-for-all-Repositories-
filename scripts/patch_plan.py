from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


class PatchPlan:
    """Create a bounded anti-bug patch plan; never edits a repository."""

    def build(self, path: Path) -> dict[str, Any]:
        issue = json.loads(path.read_text(encoding="utf-8"))
        required = ("repository", "finding_id", "summary", "reproducer", "suspected_files")
        missing = [key for key in required if not issue.get(key)]
        if missing:
            raise ValueError("Missing patch input: " + ", ".join(missing))
        if not isinstance(issue["suspected_files"], list):
            raise ValueError("suspected_files must be a list")
        if len(issue["suspected_files"]) > 20:
            raise ValueError("Circuit breaker: suspected file set exceeds 20")
        if issue.get("production_write_required"):
            raise ValueError("Patch planning cannot require a direct production write")
        identifier = self._id(issue)
        slug = re.sub(r"[^a-z0-9]+", "-", str(issue["finding_id"]).lower()).strip("-")[:40]
        return {
            "schema_version": "1.0",
            "patch_id": identifier,
            "repository": issue["repository"],
            "branch": f"repair/{slug}-{identifier[-8:]}",
            "mode": "draft_pull_request_only",
            "finding_id": issue["finding_id"],
            "summary": issue["summary"],
            "hypothesis": issue.get("hypothesis", "Root cause is not yet verified."),
            "suspected_files": sorted(set(issue["suspected_files"])),
            "steps": [
                "Capture the failing baseline and environment.",
                "Add or confirm a deterministic regression test.",
                "Change the smallest justified code surface.",
                "Run the original reproducer.",
                "Run affected and full configured test suites.",
                "Run security, dependency, and static checks.",
                "Generate resolution evidence and rollback instructions.",
                "Open a draft pull request for owner review.",
            ],
            "required_gates": [
                "reproducer_fails_before", "regression_test_exists", "reproducer_passes_after",
                "full_suite_passes", "security_checks_pass", "rollback_documented",
                "residual_risk_documented", "owner_approval",
            ],
            "prohibited": [
                "direct_default_branch_write", "automatic_merge", "automatic_deploy",
                "unrelated_refactor", "delete_failure_evidence", "weaken_test_to_make_it_pass",
            ],
            "rollback": issue.get("rollback", "Revert the dedicated repair commit."),
            "claim": "This is a repair plan, not evidence that the defect is fixed.",
        }

    @staticmethod
    def _id(issue: dict[str, Any]) -> str:
        encoded = json.dumps(issue, sort_keys=True, separators=(",", ":")).encode()
        return "patch-" + hashlib.sha256(encoded).hexdigest()[:16]
