---
name: performance-review
description: Inspect scoped Python for demonstrated algorithmic, allocation, I/O, query, serialization, and event-loop performance risks without speculative optimization or edits. Use inside Python Agent Harness when evidence or a critical path justifies performance review.
---

# Performance Review

Optimize only demonstrated costs on relevant paths. This original skill uses mature complexity and profiler-style evidence without embedding third-party code.

## Inspect

- Identify asymptotic growth, repeated I/O/queries, avoidable full materialization, hot-loop work, serialization duplication, and blocking async calls.
- Check caches for invalidation, bounds, lifecycle, and correctness risk.
- Distinguish workload evidence from micro-optimization preferences.
- Avoid claims based solely on function length or cyclomatic complexity.

Require a realistic input size, critical path, benchmark/profile evidence, or mechanically clear complexity problem. Define the performance measure and behavior that must remain unchanged.

## Evidence boundary

Accept optional normalized complexity, profile, timing, or execution observations supplied by orchestration. Treat them as hypotheses with provenance, workload scope, and limitations; confirm the cost mechanism in source. Do not select, configure, or run analyzers or workloads here.

## Output and safety

Emit `lane: performance` findings with cost mechanism, expected benefit, and measurement plan. Do not run load against external systems or modify code; return `mutations_performed: false`.
