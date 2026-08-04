---
name: types-contracts-review
description: Inspect scoped Python typing, schemas, models, function signatures, and public contracts for evidence-backed ambiguity or unsoundness without edits. Use inside Python Agent Harness when annotations, validation models, protocols, structured data, or API contracts are relevant.
---

# Types and Contracts Review

Use the repository's minimum Python version and typing policy. This is an original reviewer.

## Inspect

- Check public parameters, returns, optional states, unions, generics, protocols, typed mappings, and model validation boundaries.
- Trace `Any`, casts, ignores, untyped decorators, serialization aliases, defaults, and required/optional fields to observable contracts.
- Distinguish an analysis limitation from a runtime contract defect.
- Reject annotation churn that adds no useful constraint.

Justify a finding with an unsafe reachable state, mismatched producer/consumer contract, runtime validation gap, or concrete diagnostic confirmed in source. Record compatible Python and library versions.

## Evidence boundary

Accept optional normalized contract observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the producer/consumer or runtime-validation mismatch in scoped source. Do not select, configure, or run analyzers here.

## Output and safety

Emit the shared contract with `lane: types`, the exact contract surface, and required verification. Do not add ignores, dependencies, or annotations during review; return `mutations_performed: false`.
