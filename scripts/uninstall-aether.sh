#!/bin/sh
# Remove the aether PATH symlink. Does not touch project files.
set -e
BIN_DIR="${AETHER_BIN_DIR:-$HOME/.local/bin}"
TARGET="$BIN_DIR/aether"

if [ -L "$TARGET" ] || [ -f "$TARGET" ]; then
    rm -f "$TARGET"
    printf 'removed: %s\n' "$TARGET"
else
    printf 'nothing to remove at %s\n' "$TARGET"
fi

printf '\nProject cleanup (optional, per project):\n'
printf '  aether deinit          # removes .aether/ only\n'
printf '  # or manually: rm -rf .aether\n'
printf '  # CURRENT.md, .context.md, .session.md are left for you to keep or delete\n'
printf '\nUnset if set: AETHER_HOME, AETHER_BIN\n'
