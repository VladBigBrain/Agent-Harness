"""Run read-only Python feedback tools and normalize their evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib

MAX_CAPTURE_CHARS = 500_000
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}


@dataclass(frozen=True)
class ToolSpec:
    tool_id: str
    tool_class: str
    kind: str
    profiles: tuple[str, ...]
    reviewer_lanes: tuple[str, ...]
    timeout_seconds: int
    runtime: str | None = None
    module: str | None = None
    script: str | None = None
    args: tuple[str, ...] = ()
    requires_tests: bool = False
    rationale: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--scope", action="append", required=True)
    parser.add_argument("--tests", action="append", default=[])
    parser.add_argument("--test-option", action="append", default=[])
    parser.add_argument("--target-python", type=Path, required=True)
    parser.add_argument("--profile", choices=("review", "verification"), required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def feedback_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_specs(config_path: Path, profile: str, selected: set[str]) -> list[ToolSpec]:
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    if config.get("version") != 1:
        raise ValueError(
            f"Unsupported tool configuration version: {config.get('version')}"
        )
    specs: list[ToolSpec] = []
    for raw in config.get("tools", []):
        if profile not in raw.get("profiles", []):
            continue
        if selected and raw["id"] not in selected:
            continue
        specs.append(
            ToolSpec(
                tool_id=raw["id"],
                tool_class=raw["class"],
                kind=raw["kind"],
                profiles=tuple(raw.get("profiles", [])),
                reviewer_lanes=tuple(raw.get("reviewer_lanes", [])),
                timeout_seconds=int(raw.get("timeout_seconds", 300)),
                runtime=raw.get("runtime"),
                module=raw.get("module"),
                script=raw.get("script"),
                args=tuple(raw.get("args", [])),
                requires_tests=bool(raw.get("requires_tests", False)),
                rationale=raw.get("rationale"),
            )
        )
    return specs


def validate_relative_paths(target: Path, paths: list[str]) -> list[str]:
    resolved: list[str] = []
    for raw in paths:
        candidate = (target / raw).resolve()
        if not candidate.is_relative_to(target):
            raise ValueError(f"Path escapes target: {raw}")
        if not candidate.exists():
            raise ValueError(f"Path does not exist inside target: {raw}")
        resolved.append(raw)
    return resolved


def snapshot(target: Path, roots: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in roots:
        root = (target / raw).resolve()
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
                continue
            relative = str(path.relative_to(target))
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(result.items()))


def snapshot_changes(
    before: dict[str, str], after: dict[str, str]
) -> list[dict[str, str]]:
    changes: list[dict[str, str]] = []
    for path in sorted(before.keys() | after.keys()):
        if path not in before:
            changes.append({"path": path, "change": "created"})
        elif path not in after:
            changes.append({"path": path, "change": "deleted"})
        elif before[path] != after[path]:
            changes.append({"path": path, "change": "modified"})
    return changes


def expand_args(
    tokens: tuple[str, ...],
    target: Path,
    scopes: list[str],
    tests: list[str],
    test_options: list[str] | None = None,
) -> list[str]:
    expanded: list[str] = []
    for token in tokens:
        if token == "{scopes}":
            expanded.extend(scopes)
        elif token == "{tests}":
            expanded.extend(tests)
        elif token == "{test_options}":
            expanded.extend(test_options or [])
        elif token == "{target}":
            expanded.append(str(target))
        elif token == "{scope_each}":
            if expanded and expanded[-1] == "--scope":
                expanded.pop()
            for scope in scopes:
                expanded.extend(["--scope", scope])
        else:
            expanded.append(token)
    return expanded


def python_has_module(python: Path, module: str) -> bool:
    command = [
        str(python),
        "-c",
        "import importlib.util,sys;sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)",
        module,
    ]
    try:
        result = subprocess.run(
            command, check=False, capture_output=True, text=True, timeout=30
        )
    except subprocess.TimeoutExpired:
        return False
    return result.returncode == 0


def command_for(
    spec: ToolSpec,
    target: Path,
    scopes: list[str],
    tests: list[str],
    test_options: list[str],
    target_python: Path,
) -> tuple[list[str] | None, str | None]:
    if spec.kind in {"agent-capability", "unavailable"}:
        return None, spec.rationale
    if spec.requires_tests and not tests:
        return None, "No test paths were supplied."
    arguments = expand_args(spec.args, target, scopes, tests, test_options)
    if spec.kind == "script":
        if spec.script is None:
            return None, "Script path is missing from configuration."
        script_path = feedback_root() / spec.script
        if not script_path.is_file():
            return None, f"Configured script does not exist: {script_path}"
        return [sys.executable, str(script_path), *arguments], None
    if spec.kind == "python-module":
        if spec.module is None:
            return None, "Python module is missing from configuration."
        python = target_python if spec.runtime == "target" else Path(sys.executable)
        if not python.is_file():
            return None, f"Python runtime does not exist: {python}"
        if not python_has_module(python, spec.module):
            return None, f"Module {spec.module!r} is unavailable in {python}."
        return [str(python), "-m", spec.module, *arguments], None
    return None, f"Unsupported tool kind: {spec.kind}"


def cap_output(value: str) -> tuple[str, bool]:
    if len(value) <= MAX_CAPTURE_CHARS:
        return value, False
    omitted = len(value) - MAX_CAPTURE_CHARS
    marker = f"\n... [{omitted} characters omitted by Python Agent Harness] ...\n"
    remaining = MAX_CAPTURE_CHARS - len(marker)
    head_size = remaining // 2
    tail_size = remaining - head_size
    return f"{value[:head_size]}{marker}{value[-tail_size:]}", True


def output_text(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def run_tool(
    spec: ToolSpec,
    target: Path,
    scopes: list[str],
    tests: list[str],
    test_options: list[str],
    target_python: Path,
    environment: dict[str, str],
) -> dict[str, Any]:
    command, reason = command_for(
        spec, target, scopes, tests, test_options, target_python
    )
    if command is None:
        result = (
            "not_run"
            if spec.kind == "agent-capability" or spec.requires_tests
            else "unavailable"
        )
        return {
            "tool_id": spec.tool_id,
            "class": spec.tool_class,
            "result": result,
            "reason": reason,
            "command": None,
            "exit_code": None,
            "duration_seconds": 0.0,
            "stdout": "",
            "stderr": "",
            "output_truncated": False,
            "mutations_detected": [],
        }

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=target,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=spec.timeout_seconds,
        )
        stdout, stdout_truncated = cap_output(completed.stdout)
        stderr, stderr_truncated = cap_output(completed.stderr)
        return {
            "tool_id": spec.tool_id,
            "class": spec.tool_class,
            "result": "passed" if completed.returncode == 0 else "failed",
            "reason": None,
            "command": command,
            "exit_code": completed.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": stdout,
            "stderr": stderr,
            "output_truncated": stdout_truncated or stderr_truncated,
            "mutations_detected": [],
        }
    except subprocess.TimeoutExpired as error:
        stdout, stdout_truncated = cap_output(output_text(error.stdout))
        stderr, stderr_truncated = cap_output(output_text(error.stderr))
        return {
            "tool_id": spec.tool_id,
            "class": spec.tool_class,
            "result": "failed",
            "reason": f"Timed out after {spec.timeout_seconds} seconds.",
            "command": command,
            "exit_code": None,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": stdout,
            "stderr": stderr,
            "output_truncated": stdout_truncated or stderr_truncated,
            "mutations_detected": [],
        }


def main() -> int:
    args = parse_args()
    target = args.target.resolve(strict=True)
    if not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")
    scopes = validate_relative_paths(target, args.scope)
    tests = validate_relative_paths(target, args.tests)
    target_python = args.target_python.expanduser().absolute()
    if not target_python.is_file():
        raise ValueError(f"Target Python does not exist: {target_python}")
    config_path = (args.config or feedback_root() / "config" / "tools.toml").resolve(
        strict=True
    )
    selected = {item for value in args.only for item in value.split(",") if item}
    specs = load_specs(config_path, args.profile, selected)
    snapshot_roots = list(dict.fromkeys([*scopes, *tests]))
    baseline = snapshot(target, snapshot_roots)

    with tempfile.TemporaryDirectory(prefix="python-harness-") as temporary:
        environment = dict(os.environ)
        environment.update(
            {
                "MYPY_CACHE_DIR": str(Path(temporary) / "mypy"),
                "MYPYPATH": str(target / "src"),
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPYCACHEPREFIX": str(Path(temporary) / "pycache"),
                "RUFF_CACHE_DIR": str(Path(temporary) / "ruff"),
            }
        )
        records: list[dict[str, Any]] = []
        for spec in specs:
            record = run_tool(
                spec,
                target,
                scopes,
                tests,
                args.test_option,
                target_python,
                environment,
            )
            record["reviewer_lanes"] = list(spec.reviewer_lanes)
            changes = snapshot_changes(baseline, snapshot(target, snapshot_roots))
            record["mutations_detected"] = changes
            if changes:
                record["result"] = "failed"
                record["reason"] = "Tool changed the protected target scope."
            records.append(record)
            if changes:
                break

    final_snapshot = snapshot(target, snapshot_roots)
    report = {
        "schema_version": 1,
        "profile": args.profile,
        "target": str(target),
        "target_python": str(target_python),
        "scopes": scopes,
        "tests": tests,
        "test_options": args.test_option,
        "protected_files": len(baseline),
        "target_unchanged": baseline == final_snapshot,
        "tools": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        f"{json.dumps(report, indent=2, sort_keys=True)}\n", encoding="utf-8"
    )
    failed = any(record["result"] == "failed" for record in records)
    mutation = not report["target_unchanged"]
    if mutation or (args.strict and failed):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        sys.stderr.write(f"feedback runner error: {error}\n")
        raise SystemExit(2) from None
