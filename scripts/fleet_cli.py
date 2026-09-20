from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.coverage_gap import CoverageGap
from scripts.fleet_triage import analyze_file
from scripts.patch_plan import PatchPlan
from scripts.readiness import assess
from scripts.resolution_evidence import build_files
from scripts.validate_catalog import validate


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(prog="jarvis-fleet")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    commands.add_parser("readiness")
    triage = commands.add_parser("triage")
    triage.add_argument("findings")
    patch = commands.add_parser("plan-patch")
    patch.add_argument("issue")
    evidence = commands.add_parser("prove-resolution")
    evidence.add_argument("record")
    evidence.add_argument("--output", default="artifacts/resolution")
    coverage = commands.add_parser("coverage")
    coverage.add_argument("evidence")
    args = parser.parse_args()

    if args.command == "validate":
        emit(validate())
    elif args.command == "readiness":
        emit(assess())
    elif args.command == "triage":
        emit(analyze_file(args.findings))
    elif args.command == "plan-patch":
        emit(PatchPlan().build(Path(args.issue)))
    elif args.command == "prove-resolution":
        emit(build_files(Path(args.record), Path(args.output)))
    elif args.command == "coverage":
        emit(CoverageGap().analyze(Path("catalog/rnd-enhancements.json"), Path(args.evidence)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
