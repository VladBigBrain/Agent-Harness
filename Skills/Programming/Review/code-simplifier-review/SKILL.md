---
name: code-simplifier-review
description: Inspect scoped Python for duplicated logic, dead or redundant code, unnecessary abstraction, deep branching, and needless exception wrappers without edits. Use inside Python Agent Harness when simpler code can preserve the same public behavior.
---

# Code Simplifier Review

Prefer the least complex code that expresses the required behavior. This is an original reviewer.

## Inspect

- Find repeated business rules, redundant branches, dead paths, pass-through layers, single-use abstractions, needless temporaries, and exception wrappers that add no contract.
- Distinguish intentional boundary duplication and readability helpers from accidental complexity.
- Trace side effects, ordering, exception types, logging, async behavior, and public imports before proposing removal.
- Never merge code merely because text looks similar.

Require a behavior-preserving simplification with a bounded diff, named invariant, and verification surface. Estimate deletion/branch reduction without treating line count as the goal.

## Evidence boundary

Accept optional normalized duplication, complexity, reachability, or execution observations supplied by orchestration. Treat them as hypotheses with provenance and limitations; confirm every proposed simplification against source behavior. Do not select, configure, or run analyzers here.

## Output and safety

Emit `lane: simplification` findings with preserved behavior and rollback boundary. Do not delete or rewrite code during review; return `mutations_performed: false`.
