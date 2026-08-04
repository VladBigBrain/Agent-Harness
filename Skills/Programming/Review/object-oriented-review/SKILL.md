---
name: object-oriented-review
description: Inspect scoped Python code for evidence-backed object-oriented design and SOLID issues without editing files. Use inside Python Agent Harness when classes, inheritance, composition, protocols, responsibilities, or dependency inversion are relevant.
---

# Object-Oriented Review

Adapt mature OOP/SOLID reasoning to the repository's actual architecture. This skill is original; it copies no third-party implementation.

## Inspect

- Identify classes with multiple unrelated reasons to change, leaky abstractions, invalid substitutability, broad interfaces, and concrete dependency coupling.
- Compare inheritance with composition only when the current hierarchy causes duplication, unsafe overrides, or state coupling.
- Check domain ownership, lifecycle, and invariants before proposing a pattern.
- Reject pattern-driven redesign when a function or simple data structure is clearer.

Treat a recommendation as justified only when a concrete dependency, invariant violation, repeated change pattern, or testability problem demonstrates impact. Name the affected public behavior and the smallest design change.

## Evidence boundary

Accept optional normalized observations supplied by orchestration, but treat each as a hypothesis with provenance and limitations. Confirm or reject it against the object model and the criteria above. Do not select, configure, or run analyzers here; an observation or metric threshold alone is not an OOP finding.

## Output and safety

Emit the Python Review finding contract with `lane: oop`, precise locations, evidence, impact, bounded recommendation, preserved behavior, verification, confidence, and `status: proposed`. Do not modify code, tests, configuration, dependencies, Git state, or external systems. End with `mutations_performed: false`.
