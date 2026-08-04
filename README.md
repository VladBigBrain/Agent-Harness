# Python Agent Harness

Status: **implemented and locally demonstrated — ready for user review**.

Python Agent Harness coordinates evidence-only reviewers, explicit approval, path-bounded refactoring, and read-only verification tools to improve Python code without silently changing public behavior.

## Workflow

1. `python-review` runs all reviewer lanes and emits traceable proposed findings without editing user code.
2. `python-agent-harness` aggregates and deduplicates findings, then stops at an explicit approval artifact.
3. `python-refactoring` dispatches only approved finding IDs and allowed paths to the specialized refactorers.
4. The Feedback Loop repeats lint, formatting, types, architecture, security, complexity, and tests; unavailable signals remain unavailable rather than being reported as passed.
5. Final review compares the verified result with the approved plan and records deferred work.

## Skills

`Skills/Programming/Review` contains the review coordinator plus 13 focused reviewers:

- object-oriented design and SOLID;
- functional design;
- async/concurrency;
- architecture;
- types and contracts;
- error handling;
- tests;
- performance;
- style;
- code simplification;
- security;
- dependencies;
- API and documentation.

`Skills/Programming/Refactoring` contains the approval-enforcing coordinator, style refactorer, and code-simplifier refactorer. `Skills/Programming/Orchestration/python-agent-harness` owns the protocol, artifact contracts, and executable JSON validator.

Every skill has valid Codex frontmatter and `agents/openai.yaml`. Reviewers declare a no-change contract; refactorers require approved finding IDs, exact allowed paths, preserved behavior, and verification gates.

Reviewer skills are tool-independent: they contain domain principles, review questions, evidence criteria, and the shared finding contract, but no analyzer names or execution instructions. `Tools/Feedback Loop/config/tools.toml` owns concrete adapters and `reviewer_lanes` routing; orchestration converts their output into bounded evidence inputs that reviewers must independently confirm in source.

## Feedback Loop

`Tools/Feedback Loop` includes executable adapters and tests:

- target-native Ruff lint and format checks;
- target-native Mypy and Pytest;
- local Bandit and Radon signals;
- a deterministic stdlib AST import-cycle check;
- complete-tree SHA-256 and Git-state integrity capture;
- orchestration artifact and skill validation;
- Codex Security routing;
- explicit unavailable records for pip-audit and Sonar when safe prerequisites are absent.

The project-local `.venv` contains only harness development tooling. Exact tested versions are recorded in `Tools/Feedback Loop/requirements-dev.lock`; no global installation is required.

## Run a read-only review

```bash
.venv/bin/python "Tools/Feedback Loop/scripts/run_feedback.py" \
  --target /isolated/project-copy \
  --scope src \
  --tests tests \
  --target-python /path/to/project/python \
  --profile review \
  --output /safe/report/review-tools.json
```

Validate an orchestration artifact:

```bash
.venv/bin/python \
  "Skills/Programming/Orchestration/python-agent-harness/scripts/validate_artifact.py" \
  --kind approval \
  --file /safe/report/approval-bundle.json
```

## Demonstration status

The harness was tested end-to-end on an isolated copy of the complete current `src/` tree from the Project Agent repository. The demonstration ran every reviewer, all relevant local tools, approval aggregation, every refactorer, focused interface tests, full comparable tests, final review, and source-integrity checks. Two safe approved changes were applied only in the copy; all risky or uncertain findings were deferred. The original repository's HEAD, working-tree status, file manifest, and source digest remained identical before and after.

The retained demonstration report and copy live outside this repository in the user-facing Codex task outputs. The native Codex Security scan completed over all 279 copied `src/` objects and retained its sealed report, findings, coverage, manifest, and SARIF evidence with risky changes deferred. An unavailable external integration (for example Sonar or network-backed advisory resolution) is never treated as a passed check.

Existing placeholders under `Skills/{Java,Other,Python}` and `Tools/{Java,Other,Python}` remain untouched.
