#!/bin/sh
# Install aether onto PATH via symlink. Reversible: scripts/uninstall-aether.sh
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
BIN_DIR="${AETHER_BIN_DIR:-$HOME/.local/bin}"
TARGET="$BIN_DIR/aether"

mkdir -p "$BIN_DIR"
ln -sfn "$ROOT/aether" "$TARGET"
chmod +x "$ROOT/aether" 2>/dev/null || true

printf 'installed: %s -> %s\n' "$TARGET" "$ROOT/aether"
printf '\nAdd to your shell profile if needed:\n'
printf '  export PATH="%s:$PATH"\n' "$BIN_DIR"
printf '  export AETHER_HOME="%s"\n' "$ROOT"
printf '\nFirst project:\n'
printf '  See: %s/docs/FIRST-PROJECT.md\n' "$ROOT"
printf '  cd /path/to/project && aether onboard --yes\n'
printf '  aether demo           # sandbox literacy (never your live CURRENT)\n'
printf '  aether panel          # optional daily surface\n'
printf '\nRemove CLI: %s/scripts/uninstall-aether.sh\n' "$ROOT"
