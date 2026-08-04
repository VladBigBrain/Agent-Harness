---
name: style-refactoring
description: Apply only explicitly approved Python style finding IDs inside allowed paths while preserving public names and behavior, then run required checks. Use after Python Agent Harness approval for naming, imports, formatting, or readability changes.
---

# Style Refactoring

Consume the approved-plan contract from `python-refactoring`; do not perform review.

## Preconditions

Require `plan_id`, explicit approval evidence, approved style finding IDs, allowed paths, authorized edits, preserved behavior, and required checks. Stop if a rename affects an unapproved public import/API or if formatter output exceeds allowed paths.

## Apply

1. Confirm the working baseline and repository style configuration.
2. Map every edit to one approved ID.
3. Apply the smallest naming, import, formatting, or readability change specified.
4. Never run an auto-fixer across a wider scope; preview deterministic changes first when possible.
5. Run the affected public-interface tests and exact verification checks named by the approved plan.

Do not add unrelated cleanup, change semantics, weaken tests, or acquire additional tooling. If a required wider compatibility change appears, stop and return it as unapproved scope growth.

## Output

Return the shared refactoring report with changed paths per approved ID, exact checks, behavior conclusion, residual risks, and `unexpected_changes: []`. Missing required checks mean `behavior_preserved: unverified`, not success.
