# Feedback tool adapter contract

Every configured tool must declare:

```yaml
tool_id: stable-name
version: exact version or unknown
class: lint | style | types | quality | architecture | tests | security | dependencies | quality-security
source: project_dependency | system | codex_capability | external_service
license: identifier | not_applicable | unknown
availability: available | unavailable | approval_required
mode: read_only | may_write
inputs:
  scope: []
  configuration: []
command_or_capability: ""
outputs:
  normalized_signal: finding | test_result | metric | report
reviewer_lanes: []
limitations: []
```

## Execution record

Each invocation returns:

```yaml
tool_id: stable-name
started_from_baseline: ""
scope: []
result: passed | failed | unavailable | not_run
exit_code: null
summary: ""
evidence_location: null
mutations_detected: []
limitations: []
```

Raw output is retained in the JSON run report, subject to the documented capture limit, and the harness normalizes status without rewriting the tool's meaning.

`reviewer_lanes` is an adapter-owned routing hint. It names review lanes that may receive a compact evidence input derived from the record. Routing does not assert that a finding exists and does not replace the reviewer's domain criteria. Orchestration passes references and limitations, not command ownership, to reviewers.

## Safety rules

- `may_write` tools are disabled during review.
- Installation into the harness-local `.venv` requires explicit approval; target environments remain untouched. Network access, service upload, or third-party code import always requires explicit scope.
- Do not treat absence of findings, an unavailable tool, or an incomplete scope as proof of correctness.
- Record configuration and version because results are not comparable without them.
- Tool findings remain evidence for a reviewer; they do not become approved refactoring items automatically.
- During verification, fail the run boundary if a tool unexpectedly changes files or operates outside its declared scope.
