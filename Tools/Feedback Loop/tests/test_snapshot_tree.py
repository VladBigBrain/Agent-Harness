from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("snapshot_tree", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_manifest_changes_with_content(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    file_path = source / "example.py"
    file_path.write_text("VALUE = 1\n", encoding="utf-8")
    module = load_module(Path(__file__).parents[1] / "scripts" / "snapshot_tree.py")
    before = module.build_manifest(tmp_path, "src")

    file_path.write_text("VALUE = 2\n", encoding="utf-8")
    after = module.build_manifest(tmp_path, "src")

    assert before["file_count"] == 1
    assert before["aggregate_sha256"] != after["aggregate_sha256"]
