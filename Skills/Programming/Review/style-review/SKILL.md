---
name: style-review
description: Inspect scoped Python readability, naming, imports, formatting, and repository-specific conventions without mixing style with structural redesign or editing files. Use inside Python Agent Harness for evidence-backed style review.
---

# Style Review

Apply repository rules first, then established Python conventions. This is an original reviewer informed by established readability principles.

## Inspect

- Read project configuration before checking names, imports, formatting, line length, comments, and local consistency.
- Identify ambiguous names, misleading abstractions, inconsistent terminology, unreadable expressions, and imports that obscure ownership.
- Separate deterministic convention violations from human readability findings.
- Suppress personal preferences and churn when the project permits the current form.

Justify a finding by citing a project rule, a misleading semantic signal, repeated comprehension cost, or a reproducible convention violation. Preserve public names unless approval explicitly covers compatibility.

## Evidence boundary

Accept optional normalized convention observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the applicable repository rule and exact source location. Do not select, configure, run, or fix through analyzers here.

## Output and safety

Emit `lane: style` findings with the applicable rule and smallest change. Do not perform formatting, import sorting, or renaming; return `mutations_performed: false`.
