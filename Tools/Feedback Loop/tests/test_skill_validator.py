from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_skills", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_validates_minimal_skill(tmp_path: Path) -> None:
    skill = tmp_path / "sample-skill"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: sample-skill\ndescription: Inspect a sample safely. Use for validation tests.\n---\n\n# Sample\n",
        encoding="utf-8",
    )
    (skill / "agents" / "openai.yaml").write_text(
        'interface:\n  display_name: "Sample"\n  short_description: "Validate a minimal sample skill"\n'
        '  default_prompt: "Use $sample-skill for this sample."\n',
        encoding="utf-8",
    )

    module = load_module(Path(__file__).parents[1] / "scripts" / "validate_skills.py")

    assert module.validate_skill(skill / "SKILL.md")["valid"] is True
