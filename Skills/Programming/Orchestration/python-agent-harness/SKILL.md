---
name: python-agent-harness
description: Orchestrate a gated Python improvement run across every configured reviewer, explicit finding approval, bounded refactorers, read-only feedback tools, behavior verification, and final reporting. Use for complete Python Agent Harness runs, including authorized isolated demonstrations.
---

# Python Agent Harness

Read [references/protocol.md](references/protocol.md) and [references/artifact-contracts.md](references/artifact-contracts.md) before starting. Treat them as the run state machine and persistence contract.

## Intake

Freeze repository instructions, exact source/test scope, public behavior, target Python, tool availability, original/copy identities, and pre-existing working-tree state. Validate all skills with `Tools/Feedback Loop/scripts/validate_skills.py`.

## Review

Run the review Feedback Loop against the frozen scope first. Use adapter-declared `reviewer_lanes` to prepare normalized evidence inputs with provenance, scope, and limitations; do not copy execution commands into reviewer instructions. Then run `python-review` and every applicable individual reviewer under `Skills/Programming/Review`. Persist one validated artifact per reviewer, including explicit no-finding artifacts. Keep all findings `proposed`; external observations supply hypotheses, never domain conclusions or approval.

## Approval

Aggregate duplicate root causes without losing reviewer provenance. Classify every ID as approved, rejected, deferred, or needs revision. Require explicit user approval evidence. A direct user instruction authorizing safe refactors in an isolated demonstration is valid only for bounded, behavior-preserving, high-confidence items; defer uncertain, risky, external, or behavior-changing items.

## Refactoring

Build the approved plan with exact IDs, allowed paths, authorized change, preserved behavior, and checks. Invoke only relevant refactorers. Do not expose rejected/deferred items as implementation work. Stop on scope growth or baseline drift.

## Verification

Run the full Feedback Loop and public-interface tests supported by the target. Compare pre/post signals and source hashes. Record passed, failed, unavailable, and not-run independently. When a failure existed before refactoring and is unchanged afterward, classify it as pre-existing with both reports; never call it passed.

## Final report

Map every source diff to approved IDs and show every reviewer artifact, decision, refactorer result, tool outcome, test result, remaining recommendation, and original-project integrity proof. End in `final_review`; the user decides acceptance and any production application.

Validate review, approval, refactor, and verification JSON with `scripts/validate_artifact.py` before each transition.
