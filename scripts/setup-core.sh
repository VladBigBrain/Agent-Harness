#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
case "$(uname -s)/$(uname -m)" in
  Darwin/arm64) ;;
  *) echo 'This bootstrap pins the macOS Apple Silicon RTK-OSS asset.' >&2; exit 64 ;;
esac
bin_dir="${HARNESS_BIN_DIR:-$HOME/.local/bin}"
mkdir -p "$bin_dir" .local/bin .local/downloads
for name in rtk ccusage; do
  target="$root/.local/bin/$name"
  if [ "$name" = ccusage ]; then target="$root/node_modules/.bin/ccusage"; fi
  if [ -e "$bin_dir/$name" ] || [ -L "$bin_dir/$name" ]; then
    if [ ! -L "$bin_dir/$name" ] || [ "$(readlink "$bin_dir/$name")" != "$target" ]; then
      echo "Refusing to replace existing $bin_dir/$name" >&2; exit 73
    fi
  fi
done
archive="$root/.local/downloads/rtk-oss-1.1.0-aarch64-apple-darwin.tar.gz"
if [ ! -f "$archive" ]; then
  curl --fail --location --proto '=https' --tlsv1.2 \
    'https://github.com/rtk-ai/rtk/releases/download/v1.1.0/rtk-oss-aarch64-apple-darwin.tar.gz' \
    --output "$archive"
fi
printf '%s  %s\n' '1623590dd8d65374f61589c599c764c08ba9ce993ebe6b601312a89a3c874558' "$archive" | shasum -a 256 -c -
scratch="$(mktemp -d "$root/.local/rtk-extract.XXXXXX")"
trap 'rm -rf "$scratch"' EXIT
tar -xzf "$archive" -C "$scratch" rtk
install -m 755 "$scratch/rtk" .local/bin/rtk
npm ci --ignore-scripts --no-audit --no-fund
[ -L "$bin_dir/rtk" ] || ln -s "$root/.local/bin/rtk" "$bin_dir/rtk"
[ -L "$bin_dir/ccusage" ] || ln -s "$root/node_modules/.bin/ccusage" "$bin_dir/ccusage"
.local/bin/rtk --version
node_modules/.bin/ccusage --version
printf 'RTK-OSS v1.1.0 and ccusage 20.0.45 installed. Run npm run activate:codex next.\n'
