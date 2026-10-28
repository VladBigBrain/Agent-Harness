#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
.local/bin/rtk --version
node_modules/.bin/ccusage --version
printf '\nPinned upstream checkouts:\n'
git submodule status
printf '\nCompression accounting (not subscription savings):\n'
.local/bin/rtk gain
