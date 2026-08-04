"""Validate Python Agent Harness JSON artifacts and approval boundaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FINDING_ID = re.compile(r"^REV-[A-Z0-9-]+$")
DECISIONS = {"approved", "rejected", "deferred", "needs_revision"}
CONFIDENCE = {"high", "medium", "low"}
EVIDENCE_DISPOSITIONS = {"used", "rejected"}
EXECUTION_DETAIL_FIELDS = {"command", "exit_code", "stdout", "stderr"}
LANES = {
    "api-docs",
    "architecture",
    "async",
    "dependencies",
    "errors",
    "functional",
    "oop",
    "performance",
    "security",
    "simplification",
    "style",
    "tests",
    "types",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kind",
        choices=("review", "approval", "refactor", "verification"),
        required=True,
    )
    parser.add_argument("--file", type=Path, required=True)
    return parser.parse_args()


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def require_text(mapping: dict[str, Any], key: str, label: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}.{key} must be non-empty text")
    return value


def validate_finding(raw: Any, seen: set[str]) -> str:
    finding = require_mapping(raw, "finding")
    finding_id = require_text(finding, "id", "finding")
    if not FINDING_ID.fullmatch(finding_id) or finding_id in seen:
        raise ValueError(f"invalid or duplicate finding id: {finding_id}")
    seen.add(finding_id)
    if finding.get("lane") not in LANES:
        raise ValueError(f"invalid lane for {finding_id}")
    for field in (
        "title",
        "evidence",
        "impact",
        "recommendation",
        "behavior_surface",
        "verification",
    ):
        require_text(finding, field, finding_id)
    locations = require_list(finding.get("locations"), f"{finding_id}.locations")
    if not locations:
        raise ValueError(f"{finding_id}.locations must not be empty")
    if finding.get("confidence") not in CONFIDENCE:
        raise ValueError(f"invalid confidence for {finding_id}")
    if finding.get("status") != "proposed":
        raise ValueError(f"review finding {finding_id} must remain proposed")
    return finding_id


def validate_evidence_input(raw: Any) -> None:
    evidence = require_mapping(raw, "review evidence input")
    for field in ("ref", "summary", "provenance"):
        require_text(evidence, field, "review evidence input")
    require_list(evidence.get("scope"), "review evidence input.scope")
    require_list(evidence.get("limitations"), "review evidence input.limitations")
    if evidence.get("disposition") not in EVIDENCE_DISPOSITIONS:
        raise ValueError("review evidence input.disposition must be used or rejected")
    leaked = sorted(EXECUTION_DETAIL_FIELDS & evidence.keys())
    if leaked:
        raise ValueError(
            f"review evidence input must not embed execution details: {leaked}"
        )


def validate_review(document: dict[str, Any]) -> None:
    require_text(document, "run_id", "review")
    require_text(document, "reviewer", "review")
    require_list(document.get("scope"), "review.scope")
    has_evidence_inputs = "evidence_inputs" in document
    has_legacy_tool_signals = "tool_signals" in document
    if has_evidence_inputs and has_legacy_tool_signals:
        raise ValueError(
            "review must use evidence_inputs or legacy tool_signals, not both"
        )
    if has_evidence_inputs:
        for raw in require_list(
            document.get("evidence_inputs"), "review.evidence_inputs"
        ):
            validate_evidence_input(raw)
    elif has_legacy_tool_signals:
        require_list(document.get("tool_signals"), "review.tool_signals")
    else:
        raise ValueError("review.evidence_inputs is required")
    if document.get("mutations_performed") is not False:
        raise ValueError("review.mutations_performed must be false")
    seen: set[str] = set()
    for finding in require_list(document.get("findings"), "review.findings"):
        validate_finding(finding, seen)


def validate_approval(document: dict[str, Any]) -> None:
    require_text(document, "run_id", "approval")
    decisions = require_list(document.get("decisions"), "approval.decisions")
    seen: set[str] = set()
    approved: set[str] = set()
    for raw in decisions:
        decision = require_mapping(raw, "decision")
        finding_id = require_text(decision, "finding_id", "decision")
        if finding_id in seen:
            raise ValueError(f"duplicate decision for {finding_id}")
        seen.add(finding_id)
        if decision.get("decision") not in DECISIONS:
            raise ValueError(f"invalid decision for {finding_id}")
        require_text(decision, "rationale", finding_id)
        if decision["decision"] == "approved":
            approved.add(finding_id)
    plan = require_mapping(document.get("approved_plan"), "approval.approved_plan")
    require_text(plan, "plan_id", "approved_plan")
    require_text(plan, "approval_evidence", "approved_plan")
    plan_ids: set[str] = set()
    for raw in require_list(plan.get("items"), "approved_plan.items"):
        item = require_mapping(raw, "approved plan item")
        finding_id = require_text(item, "finding_id", "approved plan item")
        if finding_id in plan_ids:
            raise ValueError(f"duplicate approved plan item: {finding_id}")
        plan_ids.add(finding_id)
        if not require_list(item.get("allowed_paths"), f"{finding_id}.allowed_paths"):
            raise ValueError(f"{finding_id}.allowed_paths must not be empty")
        require_text(item, "authorized_change", finding_id)
        require_text(item, "preserved_behavior", finding_id)
        if not require_list(
            item.get("required_checks"), f"{finding_id}.required_checks"
        ):
            raise ValueError(f"{finding_id}.required_checks must not be empty")
    if plan_ids != approved:
        raise ValueError("approved plan IDs must exactly match approved decisions")


def validate_refactor(document: dict[str, Any]) -> None:
    require_text(document, "run_id", "refactor")
    require_text(document, "plan_id", "refactor")
    require_text(document, "refactorer", "refactor")
    require_list(document.get("applied"), "refactor.applied")
    require_list(document.get("not_applied"), "refactor.not_applied")
    unexpected = require_list(
        document.get("unexpected_changes"), "refactor.unexpected_changes"
    )
    if unexpected:
        raise ValueError("refactor.unexpected_changes must be empty")
    require_list(document.get("checks"), "refactor.checks")
    if document.get("behavior_preserved") not in {True, False, "unverified"}:
        raise ValueError("invalid refactor.behavior_preserved")


def validate_verification(document: dict[str, Any]) -> None:
    require_text(document, "run_id", "verification")
    require_list(document.get("checks"), "verification.checks")
    require_list(document.get("changed_paths"), "verification.changed_paths")
    if not isinstance(document.get("copy_unchanged_by_tools"), bool):
        raise TypeError("verification.copy_unchanged_by_tools must be boolean")
    if not isinstance(document.get("original_project_unchanged"), bool):
        raise TypeError("verification.original_project_unchanged must be boolean")
    if document.get("behavior_preserved") not in {True, False, "unverified"}:
        raise ValueError("invalid verification.behavior_preserved")


VALIDATORS = {
    "review": validate_review,
    "approval": validate_approval,
    "refactor": validate_refactor,
    "verification": validate_verification,
}


def main() -> int:
    args = parse_args()
    document = require_mapping(
        json.loads(args.file.read_text(encoding="utf-8")), "document"
    )
    VALIDATORS[args.kind](document)
    sys.stdout.write(
        json.dumps({"file": str(args.file), "kind": args.kind, "valid": True}) + "\n"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        sys.stderr.write(f"artifact validation error: {error}\n")
        raise SystemExit(1) from None
