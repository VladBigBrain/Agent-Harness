from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_artifact", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validator_path() -> Path:
    return (
        Path(__file__).parents[3]
        / "Skills"
        / "Programming"
        / "Orchestration"
        / "python-agent-harness"
        / "scripts"
        / "validate_artifact.py"
    )


def test_review_accepts_traceable_no_findings() -> None:
    module = load_module(validator_path())
    document = {
        "run_id": "HARNESS-TEST",
        "reviewer": "style-review",
        "scope": ["src"],
        "findings": [],
        "evidence_inputs": [
            {
                "ref": "feedback-run:style-observation-1",
                "summary": "A configured convention differs at one source location.",
                "provenance": "feedback-loop",
                "scope": ["src/example.py"],
                "limitations": [
                    "The observation does not establish readability impact."
                ],
                "disposition": "used",
            }
        ],
        "mutations_performed": False,
    }

    module.validate_review(document)


def test_review_rejects_execution_details_in_evidence_input() -> None:
    module = load_module(validator_path())
    document = {
        "run_id": "HARNESS-TEST",
        "reviewer": "types-contracts-review",
        "scope": ["src"],
        "findings": [],
        "evidence_inputs": [
            {
                "ref": "feedback-run:types-observation-1",
                "summary": "A producer and consumer disagree.",
                "provenance": "feedback-loop",
                "scope": ["src/example.py"],
                "limitations": [],
                "disposition": "used",
                "command": ["concrete-analyzer", "src"],
            }
        ],
        "mutations_performed": False,
    }

    with pytest.raises(ValueError, match="must not embed execution details"):
        module.validate_review(document)


def test_review_accepts_legacy_tool_signals_for_retained_artifacts() -> None:
    module = load_module(validator_path())
    document = {
        "run_id": "HARNESS-TEST",
        "reviewer": "style-review",
        "scope": ["src"],
        "findings": [],
        "tool_signals": ["legacy retained signal"],
        "mutations_performed": False,
    }

    module.validate_review(document)


def test_approval_rejects_plan_id_leakage() -> None:
    module = load_module(validator_path())
    document = {
        "run_id": "HARNESS-TEST",
        "decisions": [
            {
                "finding_id": "REV-STYLE-001",
                "decision": "deferred",
                "rationale": "Risky.",
            }
        ],
        "approved_plan": {
            "plan_id": "PLAN-TEST",
            "approval_evidence": "Explicit user instruction.",
            "items": [
                {
                    "finding_id": "REV-STYLE-001",
                    "allowed_paths": ["src/example.py"],
                    "authorized_change": "Rename a local.",
                    "preserved_behavior": "Public output.",
                    "required_checks": ["pytest"],
                }
            ],
        },
    }

    with pytest.raises(ValueError, match="exactly match"):
        module.validate_approval(document)
