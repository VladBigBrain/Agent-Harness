---
name: dependency-review
description: Inspect scoped Python dependency declarations, locks, imports, version constraints, duplication, maintenance, licensing, and available vulnerability signals without installation or changes. Use inside Python Agent Harness when dependency risk or necessity is in scope.
---

# Dependency Review

Evaluate the target project's declared environment, not the harness environment. This is an original reviewer.

## Inspect

- Map manifests, lock files, configured indexes, direct imports, runtime/dev groups, pins, and duplicate capabilities.
- Check whether a dependency is used, appropriately scoped, reproducibly constrained, and compatible with the project Python version.
- Report license or maintenance uncertainty rather than guessing.
- Never contact private indexes, reveal index URLs with credentials, or resolve/install packages during review unless separately authorized.

Justify a finding with a declared/import mismatch, unsafe constraint, validated advisory, abandoned critical package evidence, or licensing incompatibility. Preserve raw advisory identifiers and affected version range.

## Evidence boundary

Accept optional normalized dependency or advisory observations supplied by orchestration, but treat them as evidence with provenance, affected versions, and limitations. Confirm them against declared manifests and locks. Do not select, configure, run, resolve, or install dependency analyzers here; missing advisory evidence is not a pass.

## Output and safety

Emit `lane: dependencies` findings with manifest location, package/version evidence, consumer, and remediation boundary. Do not change locks or environments; return `mutations_performed: false`.
