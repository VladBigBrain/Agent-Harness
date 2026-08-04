"""Validate Agent-Harness skill structure without third-party YAML packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("missing closing frontmatter delimiter") from error
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if not separator or not value.strip():
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, content


def validate_skill(skill_file: Path) -> dict[str, object]:
    errors: list[str] = []
    try:
        metadata, content = parse_frontmatter(skill_file)
    except (OSError, UnicodeError, ValueError) as error:
        return {"path": str(skill_file), "name": None, "valid": False, "errors": [str(error)]}

    unexpected = set(metadata) - {"name", "description"}
    name = metadata.get("name")
    description = metadata.get("description")
    if unexpected:
        errors.append(f"unexpected frontmatter keys: {sorted(unexpected)}")
    if not name or not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append("name must be hyphen-case and at most 64 characters")
    if name and skill_file.parent.name != name:
        errors.append("skill folder must match frontmatter name")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        errors.append("description is missing or invalid")
    if "TODO" in content or "[TODO" in content:
        errors.append("placeholder TODO remains")

    agent_file = skill_file.parent / "agents" / "openai.yaml"
    if not agent_file.is_file():
        errors.append("agents/openai.yaml is missing")
    else:
        agent_content = agent_file.read_text(encoding="utf-8")
        if name and f"${name}" not in agent_content:
            errors.append("default prompt does not reference the skill name")
        if "display_name:" not in agent_content or "short_description:" not in agent_content:
            errors.append("required UI metadata is missing")

    for raw_link in LINK_PATTERN.findall(content):
        link = raw_link.split("#", 1)[0]
        if not link or "://" in link:
            continue
        if not (skill_file.parent / link).resolve().exists():
            errors.append(f"broken relative link: {raw_link}")

    return {"path": str(skill_file), "name": name, "valid": not errors, "errors": errors}


def main() -> int:
    args = parse_args()
    root = args.root.resolve(strict=True)
    skills = [validate_skill(path) for path in sorted(root.rglob("SKILL.md"))]
    report = {
        "root": str(root),
        "skills": skills,
        "count": len(skills),
        "valid": bool(skills) and all(skill["valid"] for skill in skills),
    }
    rendered = f"{json.dumps(report, indent=2, sort_keys=True)}\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        sys.stderr.write(f"skill validation error: {error}\n")
        raise SystemExit(2) from None
