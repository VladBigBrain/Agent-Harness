---
name: error-handling-review
description: Inspect scoped Python exception handling, cleanup, retries, timeouts, error translation, and observability for concrete failure risks without editing code. Use inside Python Agent Harness around I/O, integrations, resources, and error boundaries.
---

# Error Handling Review

Respect the repository's error contracts and prefer explicit, diagnosable failure behavior. This is an original reviewer informed by Python exception semantics.

## Inspect

- Trace raised, caught, translated, retried, logged, and suppressed failures across boundaries.
- Check exception specificity and chaining, resource cleanup, transaction ownership, retry idempotency/backoff, timeout composition, and partial side effects.
- Detect sensitive data in error messages or logs.
- Avoid recommending defensive catches that merely hide defects.

Require a reachable failure path, a lost contract, leaked resource, unsafe retry, or observability gap. Identify the expected public error/status/side-effect behavior.

## Evidence boundary

Accept optional normalized failure observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the reachable error path and boundary semantics in source; a broad catch is not automatically defective when it is an intentional translation boundary. Do not select, configure, or run analyzers here.

## Output and safety

Emit `lane: errors` findings with the failure path and verification scenario. Never trigger real failures against external systems or edit code; return `mutations_performed: false`.
