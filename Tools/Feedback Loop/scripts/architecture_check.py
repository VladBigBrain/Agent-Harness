"""Detect Python import cycles inside explicitly scoped source roots."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModuleFile:
    name: str
    path: Path
    is_package: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--scope", action="append", required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def module_name(path: Path, scope_root: Path) -> tuple[str, bool]:
    relative = path.relative_to(scope_root)
    parts = list(relative.with_suffix("").parts)
    is_package = parts[-1] == "__init__"
    if is_package:
        parts = parts[:-1]
    return ".".join(parts), is_package


def discover_modules(target: Path, scopes: Iterable[str]) -> dict[str, ModuleFile]:
    modules: dict[str, ModuleFile] = {}
    for scope in scopes:
        scope_root = (target / scope).resolve()
        if not scope_root.is_dir():
            continue
        for path in sorted(scope_root.rglob("*.py")):
            name, is_package = module_name(path, scope_root)
            if name:
                modules[name] = ModuleFile(name=name, path=path, is_package=is_package)
    return modules


def resolve_relative(module: ModuleFile, imported: str | None, level: int) -> str:
    package_parts = module.name.split(".") if module.is_package else module.name.split(".")[:-1]
    keep = max(0, len(package_parts) - level + 1)
    base = package_parts[:keep]
    if imported:
        base.extend(imported.split("."))
    return ".".join(base)


def closest_module(name: str, known: set[str]) -> str | None:
    candidate = name
    while candidate:
        if candidate in known:
            return candidate
        candidate = candidate.rpartition(".")[0]
    return None


def imported_modules(module: ModuleFile, tree: ast.AST, known: set[str]) -> set[str]:
    imports: set[str] = set()
    for node in ast.walk(tree):
        candidates: list[str] = []
        if isinstance(node, ast.Import):
            candidates.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = (
                resolve_relative(module, node.module, node.level)
                if node.level > 0
                else (node.module or "")
            )
            if base:
                candidates.append(base)
                candidates.extend(f"{base}.{alias.name}" for alias in node.names if alias.name != "*")
        for candidate in candidates:
            resolved = closest_module(candidate, known)
            if resolved and resolved != module.name:
                imports.add(resolved)
    return imports


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: set[tuple[str, ...]] = set()
    visiting: list[str] = []
    active: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            start = visiting.index(node)
            cycle = visiting[start:]
            rotations = [tuple(cycle[index:] + cycle[:index]) for index in range(len(cycle))]
            cycles.add(min(rotations))
            return
        if node in visited:
            return
        active.add(node)
        visiting.append(node)
        for dependency in sorted(graph.get(node, set())):
            visit(dependency)
        visiting.pop()
        active.remove(node)
        visited.add(node)

    for module in sorted(graph):
        visit(module)
    return [list(cycle) for cycle in sorted(cycles)]


def analyze(target: Path, scopes: list[str]) -> dict[str, object]:
    resolved_target = target.resolve(strict=True)
    modules = discover_modules(resolved_target, scopes)
    known = set(modules)
    graph: dict[str, set[str]] = {name: set() for name in modules}
    parse_errors: list[dict[str, object]] = []
    for name, module in modules.items():
        try:
            tree = ast.parse(module.path.read_text(encoding="utf-8"), filename=str(module.path))
        except (OSError, SyntaxError, UnicodeError) as error:
            parse_errors.append({"module": name, "path": str(module.path), "error": str(error)})
            continue
        graph[name] = imported_modules(module, tree, known)
    edges = [
        {"from": source, "to": target_name}
        for source in sorted(graph)
        for target_name in sorted(graph[source])
    ]
    return {
        "tool_id": "architecture-cycles",
        "target": str(resolved_target),
        "scopes": scopes,
        "files": len(modules),
        "edges": edges,
        "cycles": find_cycles(graph),
        "parse_errors": parse_errors,
    }


def main() -> int:
    args = parse_args()
    result = analyze(args.target, args.scope)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{rendered}\n", encoding="utf-8")
    else:
        sys.stdout.write(f"{rendered}\n")
    return 1 if result["cycles"] or result["parse_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
