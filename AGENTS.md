# Agent Harness

- Prefer the pinned upstream tools. This repository composes them; do not build another agent framework.
- Keep work in the root task. Spawn subagents only when explicitly requested.
- Treat upstream/ as third-party source: do not edit it or remove its licenses.
- Keep credentials, local usage reports, machine paths and config backups under ignored .local/.
- Validate exit codes, exact evidence and total task usage; output compression alone does not prove savings.
- Preserve existing Codex permissions, checks and unrelated hooks when configuring tools.
