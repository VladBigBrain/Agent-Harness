---
name: python-refactoring
description: Apply only user-approved Python refactoring items within explicit file and behavior boundaries, then verify observable behavior. Use after Python Agent Harness has converted proposed review findings into an approved plan.
---

# Python Refactoring

Implement the approved plan without reopening review.

## Required inputs

```yaml
plan_id: PLAN-001
approved_finding_ids: [REV-001]
items:
  - finding_id: REV-001
    allowed_paths: [src/package/module.py]
    authorized_change: bounded description
    preserved_behavior: public interface or invariant
    required_checks: [named test or command]
excluded_paths: []
approval_evidence: explicit user decision from the current orchestration run
```

Also require the repository instructions, the baseline review artifact, and the exact working-copy state used for the plan. If approval evidence or a boundary is absent, stop without editing.

## Authorization invariant

- Change only listed items and allowed paths.
- Do not add improvements discovered while editing.
- Do not reinterpret a rejected, deferred, or proposed finding as approved.
- Do not install packages, import third-party code, change external systems, or weaken tests.
- If an approved change requires a wider edit than authorized, report the mismatch and pause.

## Workflow

1. Re-read repository instructions and confirm the working-copy baseline.
2. Map each edit to one approved finding ID before applying it.
3. Apply the smallest coherent change that satisfies the authorized description.
4. Run the required public-interface tests and configured feedback checks.
5. If behavior changes or a required check fails, revert only the refactorer's own recoverable edit or stop with an exact failure report; never hide the failure by changing expectations.
6. Return a change and verification report for final user review.

## Output contract

```yaml
run_id: HARNESS-YYYYMMDD-NNN
plan_id: PLAN-001
refactorer: python-refactoring
applied:
  - finding_id: REV-001
    changed_paths: []
    summary: ""
not_applied: []
unexpected_changes: []
checks:
  - command: ""
    result: passed | failed | not_run
    evidence: ""
behavior_preserved: true | false | unverified
remaining_risks: []
```

`unexpected_changes` must be empty for a successful run. Do not declare completion when required checks are missing or the behavior surface is unverified.
