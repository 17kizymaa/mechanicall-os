#!/bin/sh
# Print a sendable sitting URL, then serve the brake face.
# GET is not Yes. Default twin is ~/mechanicall-pocket (not this repo).
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
export AETHER_HOME="$ROOT"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"
export POCKET_HOST_TWIN="${POCKET_HOST_TWIN:-$HOME/mechanicall-pocket}"
export POCKET_FACE_HOST="${POCKET_FACE_HOST:-192.168.0.51}"
export POCKET_FACE_PORT="${POCKET_FACE_PORT:-8765}"
export POCKET_SYNC="${POCKET_SYNC:-0}"

python3 - "$ROOT" "$POCKET_HOST_TWIN" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "python"))
from aether_pocket import PocketError, refuse_if_operator

try:
    root = refuse_if_operator(sys.argv[2])
except PocketError as exc:
    print(exc, file=sys.stderr)
    sys.exit(3)
print("twin", root)
PY

echo "Send this URL: http://${POCKET_FACE_HOST}:${POCKET_FACE_PORT}/"
echo "GET is not Yes. They tap Yes or Not yet."
echo "Receipt will land in: $POCKET_HOST_TWIN/RECEIPT.md"
echo "POCKET_SYNC=$POCKET_SYNC (1 = also pull/push phone)"
exec sh "$ROOT/scripts/serve-pocket-face.sh"
