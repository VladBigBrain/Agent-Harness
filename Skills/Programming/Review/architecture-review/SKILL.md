---
name: architecture-review
description: Inspect scoped Python modules for boundary violations, dependency direction, responsibility placement, import cycles, layering, and composition-root problems without edits. Use inside Python Agent Harness for architectural review distinct from implementation style.
---

# Architecture Review

Prioritize repository-declared boundaries over generic architecture preferences. This is an original reviewer.

## Inspect

- Read repository instructions and map declared layers, packages, entry points, and public boundaries.
- Compare actual imports and object construction with allowed dependency direction.
- Identify cycles, infrastructure leakage into domain code, misplaced orchestration, duplicated composition roots, and cross-layer data leakage.
- Separate a real boundary violation from a naming or directory preference.

A finding requires a concrete import/dependency path or responsibility conflict plus a realistic maintenance, testability, or runtime impact. Recommend the smallest boundary correction and state migration risk.

## Evidence boundary

Accept optional normalized dependency observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Reconstruct the relevant dependency path in source before reporting it. Do not select, configure, or run analyzers here.

## Output and safety

Emit `lane: architecture` findings using the shared contract. Include the dependency path as evidence and a verification rule or architecture test. Do not change packages or imports; return `mutations_performed: false`.
