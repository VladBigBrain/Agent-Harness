#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rtk="$root/.local/bin/rtk"
[ -x "$rtk" ] || { echo 'Run npm run setup:core first.' >&2; exit 69; }
codex_dir="${CODEX_HOME:-$HOME/.codex}"
backup="$root/.local/backups/codex-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$backup"
for name in AGENTS.md RTK.md hooks.json config.toml; do
  if [ -f "$codex_dir/$name" ]; then
    cp -p "$codex_dir/$name" "$backup/$name"
  else
    : > "$backup/$name.was-absent"
  fi
done
printf '%s\n' "$backup" > "$root/.local/last-codex-backup"
"$rtk" init -g --codex
node - "$codex_dir/hooks.json" "$rtk" <<'NODE'
const fs = require('node:fs');
const [file, binary] = process.argv.slice(2);
const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
const quoted = "'" + binary.replaceAll("'", "'\\''") + "'";
for (const group of doc.hooks?.PreToolUse ?? []) {
  for (const hook of group.hooks ?? []) {
    if (hook.command === 'rtk hook codex') hook.command = quoted + ' hook codex';
  }
}
fs.writeFileSync(file, JSON.stringify(doc, null, 2) + '\n');
NODE
printf 'Backup: %s\n' "$backup"
printf 'Open a new Codex chat or restart the client; review/trust the new hook if prompted.\n'
