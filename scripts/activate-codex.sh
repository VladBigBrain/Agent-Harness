#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rtk="$root/.local/bin/rtk"
[ -x "$rtk" ] || { echo 'Run npm run setup:core first.' >&2; exit 69; }
codex_dir="${CODEX_HOME:-$HOME/.codex}"
backup="$root/.local/backups/codex-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$backup"
for name in AGENTS.md hooks.json config.toml; do
  if [ -f "$codex_dir/$name" ]; then
    cp -p "$codex_dir/$name" "$backup/$name"
  else
    : > "$backup/$name.was-absent"
  fi
done
printf '%s\n' "$backup" > "$root/.local/last-codex-backup"
"$rtk" init -g --codex
printf 'Backup: %s\n' "$backup"
printf 'Open a new Codex chat or restart the client; review/trust the new hook if prompted.\n'
