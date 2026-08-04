---
name: functional-review
description: Inspect scoped Python code for justified functional-programming opportunities and risks involving state, purity, composition, iteration, and data transformation without changing code. Use inside Python Agent Harness for transformation-heavy or stateful logic.
---

# Functional Review

Apply functional design selectively; do not reward abstraction for its own sake. This is an original skill informed by established Python functional patterns.

## Inspect

- Trace mutation, hidden shared state, order dependence, side effects, and non-determinism.
- Find repeated transformation pipelines, predicate logic, and state transitions that become clearer as small pure functions.
- Check iterator consumption, eager materialization, closures, partial application, and higher-order functions for readability and correctness.
- Prefer comprehensible loops when map/filter/reduce or clever composition would obscure control flow.

Justify a finding with a reproducible state interaction, duplicated transformation, testability problem, or measurable allocation cost. Preserve exception behavior, ordering, laziness, and side effects as public behavior where observable.

## Evidence boundary

Accept optional normalized observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the state interaction or transformation mechanism in source. Do not select, configure, or run analyzers here.

## Output and safety

Emit the shared finding contract with `lane: functional` and `status: proposed`. Include before/after semantic constraints and verification. Never edit files; report `mutations_performed: false`.
