#!/bin/sh
# Build gomobile AAR for userspace tsnet. Not Yes. No secrets.
# Exit 2 until the AAR exists — JOIN must stay "invited" without it.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/android/tsnet/mechanicallts.aar"
if [ -f "$OUT" ]; then
  echo "tsnet AAR present: $OUT"
  exit 0
fi
if ! command -v gomobile >/dev/null 2>&1; then
  echo "named gap: gomobile not on PATH; JOIN cannot be connected" >&2
  exit 2
fi
echo "named gap: wrapper sources not bound this sit; JOIN cannot be connected" >&2
exit 2
