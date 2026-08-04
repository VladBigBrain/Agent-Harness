# Programming skills

This hierarchy separates analysis, authorized transformation, and orchestration. A concrete skill lives in its own directory with a `SKILL.md`; branch-level README files describe composition and future components.

- `Review/` owns read-only findings.
- `Refactoring/` owns changes authorized by an approved plan.
- `Orchestration/` owns state transitions, approval gates, and final reporting.

Shared rule: a downstream component may consume an upstream artifact, but it may not silently reinterpret or widen it.
