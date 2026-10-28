#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
python_bin="${HARNESS_PYTHON:-/opt/homebrew/bin/python3.12}"
codex_dir="${CODEX_HOME:-$HOME/.codex}"
source_dir="$root/upstream/token-optimizer"
version="$("$python_bin" -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$source_dir/plugins/token-optimizer/.codex-plugin/plugin.json")"
backup="$root/.local/backups/audit-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$backup"
for name in config.toml hooks.json AGENTS.md RTK.md; do
  if [ -f "$codex_dir/$name" ]; then cp -p "$codex_dir/$name" "$backup/$name"; fi
done
codex plugin marketplace add "$source_dir" --json
codex plugin add token-optimizer@alexgreensh-token-optimizer --json
engine="$codex_dir/plugins/cache/alexgreensh-token-optimizer/token-optimizer/$version/skills/token-optimizer/scripts/measure.py"
"$python_bin" "$engine" --runtime codex codex-install --profile balanced --no-subagent-hooks --json
"$python_bin" "$engine" --runtime codex codex-doctor --project "$root" --json > "$root/.local/token-optimizer-doctor.json"
printf 'Token Optimizer %s configured. Doctor: .local/token-optimizer-doctor.json\n' "$version"
printf 'Restart Codex, finish one turn, then check the Stop hook with codex-doctor.\n'
