from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("architecture_check", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_reports_import_cycle(tmp_path: Path) -> None:
    source = tmp_path / "src" / "package"
    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "a.py").write_text("from package import b\n", encoding="utf-8")
    (source / "b.py").write_text("from package import a\n", encoding="utf-8")

    module = load_module(Path(__file__).parents[1] / "scripts" / "architecture_check.py")
    result = module.analyze(tmp_path, ["src"])

    assert result["parse_errors"] == []
    assert result["cycles"] == [["package.a", "package.b"]]


def test_accepts_acyclic_imports(tmp_path: Path) -> None:
    source = tmp_path / "src" / "package"
    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (source / "a.py").write_text("from package import b\n", encoding="utf-8")
    (source / "b.py").write_text("VALUE = 1\n", encoding="utf-8")

    module = load_module(Path(__file__).parents[1] / "scripts" / "architecture_check.py")
    result = module.analyze(tmp_path, ["src"])

    assert result["cycles"] == []
    assert result["files"] == 3
