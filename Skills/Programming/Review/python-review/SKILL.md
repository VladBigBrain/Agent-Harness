---
name: python-review
description: Coordinate all configured read-only Python reviewers and normalize evidence-backed findings across design, correctness, architecture, tests, style, security, dependencies, and APIs. Use during Python Agent Harness review before approval or refactoring.
---

# Python Review

Produce proposals, not edits.

## Required inputs

- repository root and explicit review scope;
- applicable repository instructions and Python/project conventions;
- known public interfaces and related tests;
- enabled reviewer lanes;
- optional normalized evidence inputs prepared by orchestration, each with provenance, scope, and limitations.

If the scope, repository instructions, or permission boundary is unclear, stop and report the missing input. Do not acquire or manufacture additional evidence to fill a gap.

## Read-only invariant

Do not modify source, tests, configuration, dependencies, generated artifacts, Git state, or external systems. Reviewer skills inspect the frozen scope and supplied evidence; orchestration owns all executable checks.

## Workflow

1. Read repository instructions and inventory only the requested scope.
2. Identify public behavior and the tests that currently observe it.
3. Run every configured reviewer lane for the frozen scope. Persist a no-finding artifact when a lane finds nothing. Separate technological findings from architectural findings.
4. Deduplicate overlapping findings and record disagreements instead of silently merging them.
5. Validate every finding against concrete source evidence; use supplied normalized observations only as supporting evidence.
6. Return the review artifact and a statement that no user code was changed.

Do not prescribe a pattern merely because it is idiomatic. Recommend OOP, functional, asynchronous, or architectural patterns only when they solve a demonstrated problem with proportionate complexity.

## Finding contract

Return findings as a list. Every item must contain:

```yaml
id: REV-001
lane: architecture | oop | functional | async | types | errors | tests | performance | style | simplification | security | dependencies | api-docs
title: concise problem statement
locations:
  - path: relative/path.py
    line: 1
evidence: concrete source observation, optionally supported by a normalized evidence reference
impact: behavior, risk, or maintenance cost
recommendation: smallest bounded change that addresses the evidence
behavior_surface: public interface or invariant that must remain stable
verification: tests or checks that would validate the recommendation
confidence: high | medium | low
status: proposed
```

IDs must be stable within the review artifact. `status` is always `proposed`; only the orchestration approval gate can produce an approved plan.

## Output

Return:

- scope and inputs actually inspected;
- technological and architectural findings in the contract above;
- normalized evidence inputs used or rejected, including provenance and limitations;
- rejected hypotheses worth documenting;
- open questions and review limitations;
- `mutations_performed: false`.
