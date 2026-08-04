"""Capture read-only Git identity and working-tree status as JSON evidence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def git(target: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(target), *arguments],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout


def capture(target: Path) -> dict[str, object]:
    resolved_target = target.resolve(strict=True)
    status = git(
        resolved_target,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ).splitlines()
    return {
        "target": str(resolved_target),
        "head": git(resolved_target, "rev-parse", "HEAD").strip(),
        "branch": git(resolved_target, "branch", "--show-current").strip(),
        "status_porcelain_v1": status,
    }


def main() -> int:
    args = parse_args()
    state = capture(args.target)
    status = state["status_porcelain_v1"]
    if not isinstance(status, list):
        raise TypeError("Captured Git status must be a list")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(f"{json.dumps(state, indent=2, sort_keys=True)}\n", encoding="utf-8")
    sys.stdout.write(f"{state['head']} {len(status)} status entries\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, TypeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        sys.stderr.write(f"git state error: {error}\n")
        raise SystemExit(2) from None
