---
name: tests-review
description: Inspect scoped Python tests and public behavior for missing scenarios, fragile assertions, nondeterminism, untested failure paths, and interface gaps without changing tests. Use inside Python Agent Harness to assess verification confidence.
---

# Tests Review

Review tests as behavioral evidence, not as implementation authority. This is an original reviewer informed by mature testing practice.

## Inspect

- Map changed or risky behavior to public-interface, contract, unit, integration, and async tests.
- Check success, boundary, failure, cancellation/timeout, cleanup, serialization, and concurrency scenarios where relevant.
- Detect assertions coupled only to internals, uncontrolled time/randomness, shared state, order dependence, and external-service reliance.
- Do not demand coverage for unreachable or trivial implementation details.

Justify a finding with an important behavior that can regress unnoticed or a reproducible source of test instability. Propose the smallest focused scenario and stable assertion surface.

## Evidence boundary

Accept optional normalized execution or coverage observations supplied by orchestration, but treat them as bounded evidence with provenance, scope, and limitations. A passing observation proves only the executed cases. Do not select, configure, or run test frameworks here.

## Output and safety

Emit the shared contract with `lane: tests`, named test location, missing behavior, and execution constraints. Do not edit tests or update snapshots during review; return `mutations_performed: false`.
