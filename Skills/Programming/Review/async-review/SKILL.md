---
name: async-review
description: Inspect scoped Python async code for blocking work, missing awaits, unsafe task lifecycles, cancellation loss, races, cleanup, timeouts, and backpressure without edits. Use inside Python Agent Harness for asyncio, async frameworks, or concurrent workflows.
---

# Async Review

Use Python's documented async semantics and the target framework's contracts. This is an original reviewer.

## Inspect

- Trace every coroutine, await, task creation, queue, lock, timeout, and async context manager.
- Detect blocking I/O or CPU work on the event loop, fire-and-forget tasks without ownership, swallowed cancellation, unbounded concurrency, and missing cleanup.
- Check timeout/retry interaction, race windows, shared mutable state, ordering guarantees, and resource closure on error.
- Distinguish real concurrency requirements from unnecessary async wrappers.

Require a concrete execution path and realistic failure mode. Specify whether cancellation, timing, ordering, side effects, or error mapping is part of preserved public behavior.

## Evidence boundary

Accept optional normalized observations supplied by orchestration, but treat them as hypotheses with provenance and limitations. Confirm the execution path against async semantics and record uncertainty that cannot be resolved from scoped source. Do not select, configure, or run analyzers here.

## Output and safety

Emit the shared finding contract with `lane: async` and `status: proposed`; include a focused async verification scenario. Do not start services, contact networks, or modify code. Return `mutations_performed: false`.
