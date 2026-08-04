# Python Agent Harness protocol

Version: `1.1`.

## State machine

```text
intake → baseline_tools → review → awaiting_approval → refactoring → verification → final_review
   ↘ stopped         ↘ stopped  ↘ stopped            ↘ stopped      ↘ stopped
```

Persist state transitions in the run report. Never infer success or approval from confidence, tool exit code, or absence of output.

## 1. Intake

1. Read all repository instructions affecting source and tests.
2. Freeze target identity, exact source/test paths, Python semantics, public contracts, and working-tree state.
3. For an isolated copy, hash the complete source tree before copying, copy current working-tree content, and verify the copy hash matches.
4. Discover tools without installing into the target. Record tool version/configuration and unavailable prerequisites.
5. Validate skill structure and orchestration contracts.

Stop if the scope escapes the target, the original cannot be protected, or repository instructions conflict with the requested operation.

## 2. Baseline Feedback Loop

Run every relevant configured tool in read-only mode before refactoring. Hash protected source/tests before and after every command. Persist raw normalized evidence. Non-zero findings are `failed` signals, not runner failure unless mutation occurs. Agent-only and unavailable tools retain distinct statuses.

The Feedback Loop configuration owns concrete commands and the `reviewer_lanes` routing map. Orchestration converts routed records into reviewer-facing evidence inputs containing only a stable reference, concise observation, provenance, scope, and limitations. Reviewers do not select tools, interpret process status, or receive execution responsibility.

Run supported public-interface tests before refactoring so later failures can be classified as introduced or pre-existing.

## 3. Review

Run every reviewer against the complete frozen source scope:

1. OOP/SOLID;
2. functional;
3. async;
4. architecture;
5. types/contracts;
6. error handling;
7. tests;
8. performance;
9. style;
10. simplification;
11. security;
12. dependencies;
13. API/docs.

Persist one review artifact per reviewer, even with zero findings. Each finding must cite source evidence and may cite a normalized evidence-input reference. It must also state realistic impact, a bounded recommendation, behavior surface, verification, and confidence. Reviewers never edit or execute analyzers.

## 4. Aggregation and approval

Deduplicate only shared mechanisms; retain contributing reviewer IDs. Present every finding in an approval bundle. Valid decisions are approved, rejected, deferred, and needs revision.

Convert an approved finding into a plan item only when approval evidence, allowed paths, exact authorized change, preserved public behavior, and required checks are present. In a user-authorized isolated demo, approve only high-confidence local changes that are reversible and demonstrably behavior-preserving. Defer behavior changes, external integrations, uncertain security fixes, broad renames, dependency changes, and fixes needing unavailable checks.

## 5. Refactoring

Invoke `python-refactoring` for the common gate, `style-refactoring` for approved style IDs, and `code-simplifier-refactoring` for approved simplification IDs. A relevant refactorer may return a no-op artifact when the plan contains no items in its lane.

Map every edit to one approved ID. Do not widen files or improve adjacent code. Stop on unexpected paths, baseline drift, behavior uncertainty, or test changes that merely hide a regression.

## 6. Verification

1. Re-run Ruff lint and format check, Mypy, Radon, Bandit, architecture cycles, project architecture tests, and supported Pytest scope.
2. Run Codex Security final review when available.
3. Compare pre/post tool outcomes and public-interface tests.
4. Confirm every source change maps to an approved ID.
5. Confirm tools caused no unexpected mutation.
6. Recompute the original-project status and source hash; require an exact match with intake.

A refactor is behavior-preserving only when required public-interface tests pass or when an unchanged pre-existing failure is documented and unrelated to the change with evidence. Unavailable mandatory checks keep the result unverified.

## 7. Final review

Produce a readable report containing run scope, before/after source summary, every reviewer result, approval decisions, each refactorer result, raw tool-report links, tests, pre-existing failures, security/dependency limitations, original integrity proof, and remaining recommendations. Keep the isolated copy when the user requested inspection. Do not apply copy changes back to the source project automatically.
