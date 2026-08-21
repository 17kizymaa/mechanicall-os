#!/bin/sh
# Copy python/aether_pocket.py into the Chaquopy tree (one source).
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/android/app/src/main/python"
for name in aether_pocket.py aether_client.py aether_inbox.py; do
  src="$ROOT/python/$name"
  dst="$ROOT/android/app/src/main/python/$name"
  if [ -f "$src" ]; then
    cp "$src" "$dst"
    echo "copied $src -> $dst"
  fi
done
