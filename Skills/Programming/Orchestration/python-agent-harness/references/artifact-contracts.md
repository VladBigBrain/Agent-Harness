# Artifact contracts

Use JSON for persisted run artifacts. Validate each file with `scripts/validate_artifact.py` before a state transition.

## Review

Required fields: `run_id`, `reviewer`, `scope`, `findings`, `evidence_inputs`, and `mutations_performed: false`. Every evidence input contains a stable `ref`, concise `summary`, `provenance`, inspected `scope`, `limitations`, and whether the reviewer used or rejected it. It must not embed execution commands or make the domain decision on the reviewer's behalf.

Every finding uses a stable `REV-*` ID, one supported lane, concrete locations/evidence/impact/recommendation, preserved behavior, verification, confidence, and `status: proposed`. An empty `findings` list is a traceable successful no-finding result. The validator accepts legacy `tool_signals` artifacts only for already-retained demonstration compatibility; new runs emit `evidence_inputs`.

## Approval

Record one decision per finding: `approved`, `rejected`, `deferred`, or `needs_revision`, always with rationale. `approved_plan.items` must exactly match approved IDs and must include allowed paths, authorized change, preserved behavior, and required checks. Store the explicit user instruction in `approval_evidence`; never infer it from reviewer confidence.

## Refactoring

Record `run_id`, `plan_id`, `refactorer`, applied and not-applied IDs, checks, behavior conclusion, and `unexpected_changes`. A successful result requires `unexpected_changes: []`.

## Verification

Record every check as passed, failed, unavailable, or not run. Include changed paths, whether tools mutated the copy unexpectedly, whether the original project stayed unchanged, and whether public behavior is preserved. Unavailable signals never count as passed.
