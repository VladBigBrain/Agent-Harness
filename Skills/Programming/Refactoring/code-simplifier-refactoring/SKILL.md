---
name: code-simplifier-refactoring
description: Apply only explicitly approved Python simplification finding IDs within allowed paths, removing bounded duplication or complexity while preserving public behavior and tests. Use after Python Agent Harness approval for code simplification.
---

# Code Simplifier Refactoring

Consume the approved-plan contract from `python-refactoring`; never search for more simplifications.

## Preconditions

Require explicit approval evidence, finding IDs from the simplification lane, allowed paths, the exact behavior surface, authorized removals/restructure, baseline evidence, and required checks. Stop when any item is missing.

## Apply

1. Trace side effects, ordering, exceptions, logs, async behavior, and public imports named by the approved finding.
2. Map each deletion or control-flow rewrite to one approved ID.
3. Apply the smallest coherent simplification; preserve boundary adapters that serve distinct contracts.
4. Run focused public-interface tests, project static checks, and complexity comparison when requested.
5. Stop on behavior drift, baseline drift, or required path expansion.

Do not change requirements, add patterns, perform style cleanup outside the approved diff, or update expected outputs to hide regression.

## Output

Return the shared refactoring report, including removed branches/duplication, checks, behavior conclusion, and any not-applied item. A successful report has no unexpected paths or unapproved finding IDs.
