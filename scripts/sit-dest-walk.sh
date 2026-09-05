#!/bin/sh
# Dest stills on an emulator. Never Confirm. Never A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/dev/57_first-sit-look/02_still/output}"
exec python3 "$ROOT/python/sit_dest_walk.py" --out "$OUT"
