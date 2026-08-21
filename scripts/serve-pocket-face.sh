#!/bin/sh
# Brake LAN/Tailscale face. GET is not Yes. Default http://192.168.0.51:8765/
# Phone adb sync is off unless POCKET_SYNC=1.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
export AETHER_HOME="$ROOT"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"
export POCKET_HOST_TWIN="${POCKET_HOST_TWIN:-$HOME/mechanicall-pocket}"
export POCKET_FACE_HOST="${POCKET_FACE_HOST:-192.168.0.51}"
export POCKET_FACE_PORT="${POCKET_FACE_PORT:-8765}"
export POCKET_SYNC="${POCKET_SYNC:-0}"
exec python3 "$ROOT/python/aether_pocket_serve.py"
