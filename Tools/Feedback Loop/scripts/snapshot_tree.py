"""Create a deterministic SHA-256 manifest for a complete directory tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def build_manifest(target: Path, scope: str) -> dict[str, object]:
    resolved_target = target.resolve(strict=True)
    root = (resolved_target / scope).resolve(strict=True)
    if not root.is_dir() or not root.is_relative_to(resolved_target):
        raise ValueError(f"Scope must be a directory inside target: {scope}")
    files: list[dict[str, object]] = []
    aggregate = hashlib.sha256()
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        relative = str(path.relative_to(resolved_target))
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        files.append({"path": relative, "size": len(content), "sha256": digest})
        aggregate.update(relative.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(str(len(content)).encode("ascii"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {
        "target": str(resolved_target),
        "scope": scope,
        "file_count": len(files),
        "aggregate_sha256": aggregate.hexdigest(),
        "files": files,
    }


def main() -> int:
    args = parse_args()
    manifest = build_manifest(args.target, args.scope)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(f"{json.dumps(manifest, indent=2, sort_keys=True)}\n", encoding="utf-8")
    sys.stdout.write(
        f"{manifest['file_count']} files {manifest['aggregate_sha256']} {args.output}\n"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        sys.stderr.write(f"snapshot error: {error}\n")
        raise SystemExit(2) from None
