from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_feedback", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_expands_scopes_and_tests() -> None:
    module = load_module(Path(__file__).parents[1] / "scripts" / "run_feedback.py")

    result = module.expand_args(
        ("--target", "{target}", "--scope", "{scope_each}", "{tests}"),
        Path("/tmp/project"),
        ["src", "lib"],
        ["tests/unit"],
    )

    assert result == [
        "--target",
        "/tmp/project",
        "--scope",
        "src",
        "--scope",
        "lib",
        "tests/unit",
    ]


def test_snapshot_detects_modified_file(tmp_path: Path) -> None:
    module = load_module(Path(__file__).parents[1] / "scripts" / "run_feedback.py")
    source = tmp_path / "src"
    source.mkdir()
    file_path = source / "example.py"
    file_path.write_text("VALUE = 1\n", encoding="utf-8")
    before = module.snapshot(tmp_path, ["src"])

    file_path.write_text("VALUE = 2\n", encoding="utf-8")
    changes = module.snapshot_changes(before, module.snapshot(tmp_path, ["src"]))

    assert changes == [{"path": "src/example.py", "change": "modified"}]


def test_loads_declared_tool_configuration() -> None:
    module = load_module(Path(__file__).parents[1] / "scripts" / "run_feedback.py")
    config = Path(__file__).parents[1] / "config" / "tools.toml"

    specs = module.load_specs(config, "review", set())

    assert {spec.tool_id for spec in specs} >= {
        "ruff-check",
        "mypy",
        "bandit",
        "architecture-cycles",
        "codex-security",
    }
    routes = {spec.tool_id: spec.reviewer_lanes for spec in specs}
    assert routes["mypy"] == ("types", "architecture", "async")
    assert routes["bandit"] == ("security", "errors")
    assert routes["codex-security"] == ("security",)


def test_normalized_records_include_adapter_owned_reviewer_routes(
    tmp_path: Path,
) -> None:
    module = load_module(Path(__file__).parents[1] / "scripts" / "run_feedback.py")
    spec = module.ToolSpec(
        tool_id="unavailable-example",
        tool_class="types",
        kind="unavailable",
        profiles=("review",),
        reviewer_lanes=("types",),
        timeout_seconds=1,
        rationale="No local capability.",
    )

    record = module.run_tool(
        spec,
        tmp_path,
        [],
        [],
        [],
        Path(sys.executable),
        {},
    )
    record["reviewer_lanes"] = list(spec.reviewer_lanes)

    assert record["reviewer_lanes"] == ["types"]
    assert record["result"] == "unavailable"


def test_output_cap_preserves_head_and_tail(monkeypatch) -> None:
    module = load_module(Path(__file__).parents[1] / "scripts" / "run_feedback.py")
    monkeypatch.setattr(module, "MAX_CAPTURE_CHARS", 100)

    value, truncated = module.cap_output("HEAD" + "x" * 200 + "TAIL")

    assert truncated is True
    assert value.startswith("HEAD")
    assert value.endswith("TAIL")
    assert "characters omitted" in value
