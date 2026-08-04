---
name: security-review
description: Inspect scoped Python for validated security risks involving trust boundaries, injection, authentication, authorization, secrets, unsafe parsing, logging, and resource abuse without exploitation or edits. Use inside Python Agent Harness when security boundaries or attacker-controlled data are in scope.
---

# Security Review

Use repository threat context and evidence-backed security reasoning. This is an original reviewer.

## Inspect

- Map untrusted input, identities, authorization decisions, secrets, deserialization, filesystem/shell access, outbound calls, logs, and resource limits.
- Confirm a reachable source-to-sink path and existing controls.
- Separate vulnerability, defense-in-depth opportunity, dependency advisory, and unknown.
- Do not access secrets, exploit systems, contact services, or create harmful payloads.

A finding requires a realistic attacker capability, reachable mechanism, security impact, evidence, and confidence. Prefer safe static validation; record assumptions and sanitization/control evidence.

## Evidence boundary

Accept optional normalized security observations supplied by orchestration, but treat them as hypotheses with provenance, scope, and limitations. Validate the source-to-sink path, controls, attacker capability, and impact independently. Do not select, configure, or run security analyzers here.

## Output and safety

Emit the shared contract with `lane: security`, threat preconditions, affected asset, control gap, and safe verification. Keep review read-only and return `mutations_performed: false`.
