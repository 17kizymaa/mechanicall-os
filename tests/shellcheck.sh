#!/bin/sh
# Standalone shellcheck gate for aether (next-07).
# Run: sh tests/shellcheck.sh
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="$ROOT/aether"

if ! command -v shellcheck >/dev/null 2>&1; then
    printf 'FAIL: shellcheck not on PATH\n' >&2
    printf '  install: nix-env -iA nixpkgs.shellcheck\n' >&2
    printf '        or: apt install shellcheck\n' >&2
    exit 1
fi

shellcheck -s sh "$AETHER"
printf 'ok: shellcheck -s sh aether\n'
