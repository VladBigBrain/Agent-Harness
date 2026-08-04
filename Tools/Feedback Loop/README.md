# Feedback Loop tools

This branch provides executable, read-only adapters for Python Agent Harness. The runner normalizes local tool output, isolates caches in a temporary directory, hashes protected source/test paths before and after each command, and fails on unexpected mutation.

## Included components

- `config/tools.toml` — declarative profiles and unavailable-tool rationale;
- `scripts/run_feedback.py` — orchestrates tools and writes one traceable JSON report;
- `scripts/architecture_check.py` — stdlib AST import-cycle detector;
- `scripts/validate_skills.py` — dependency-free skill/frontmatter/link validator;
- `scripts/snapshot_tree.py` — deterministic complete-tree integrity manifest;
- `scripts/capture_git_state.py` — read-only Git HEAD/branch/status evidence;
- `tests/` — runner, architecture, skill, and artifact-contract tests;
- `requirements-dev.txt` — project-local development tools only;
- `requirements-dev.lock` — exact tested environment resolved on 2026-08-04;
- `tool-inventory.md` — selection, source, maturity, license, consumers, and limitations;
- `contract.md` — normalized adapter contract.

## Run

```bash
.venv/bin/python "Tools/Feedback Loop/scripts/run_feedback.py" \
  --target /isolated/project-copy \
  --scope src \
  --tests tests \
  --target-python /path/to/project/python \
  --profile review \
  --output /safe/report/review-tools.json
```

Repeat `--test-option` for safe Pytest selection flags such as `--ignore=tests/path.py` when a baseline collection failure is separately preserved as evidence.

Use `--strict` only when any available-tool finding must fail the command. Review runs normally persist all failures as evidence and continue. Never use Ruff/Bandit/Pytest auto-fix or update modes. `codex-security` is an agent capability invoked by orchestration and routed to the security lane; Sonar and network-backed dependency advisories remain explicitly unavailable unless their prerequisites receive separate authorization.

Concrete tool-to-reviewer routing is declared as `reviewer_lanes` in `config/tools.toml` and copied into normalized run records. Reviewer skills never name or launch these tools; orchestration presents only bounded evidence inputs with provenance and limitations.
