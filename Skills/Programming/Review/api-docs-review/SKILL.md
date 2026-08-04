---
name: api-docs-review
description: Compare scoped Python public APIs, schemas, command behavior, examples, and documentation for concrete contract drift without editing code or docs. Use inside Python Agent Harness when interfaces or documentation are part of the behavior surface.
---

# API and Documentation Review

Treat executable contracts and repository instructions as sources of truth in their declared order. This is an original reviewer.

## Inspect

- Inventory public functions/classes, routes, schemas, commands, configuration, error/status behavior, and supported examples.
- Compare names, signatures, defaults, optionality, payloads, side effects, deprecations, and version statements with docs and tests.
- Distinguish stale documentation from an implementation defect; do not choose silently between them.
- Ignore internal details not presented as public contract.

Justify a finding with a reproducible mismatch and identify affected consumers. State which source appears authoritative and any uncertainty requiring a decision.

## Evidence boundary

Accept optional normalized contract, example, or execution observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the mismatch against the declared authority order. Do not select, configure, or run analyzers, generators, or services here.

## Output and safety

Emit the shared contract with `lane: api-docs`, both sides of the mismatch, and verification. Do not edit code, docs, or generated schemas; return `mutations_performed: false`.
