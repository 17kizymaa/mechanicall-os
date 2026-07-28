#!/usr/bin/env bash
# Desk bridge smoke + optional live movie-suggest turn.
# Usage: ./scripts/tv/desk-smoke.sh [--live] [--lan]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DOMAIN="${DESK_DOMAIN:-$ROOT/domains/house-tv-desk}"
PORT="${AETHER_DESK_PORT:-18789}"
LIVE=0
LAN_ARGS=()
for a in "$@"; do
  case "$a" in
    --live) LIVE=1 ;;
    --lan) LAN_ARGS+=(--lan) ;;
  esac
done

export AETHER_HOME="$ROOT"
export PATH="$ROOT:$PATH"
cd "$ROOT"

echo "== unit tests =="
python3 tests/test_aether_desk.py
python3 tests/test_aether_desk_api.py

echo "== start desk-serve on :$PORT =="
python3 python/aether_desk_api.py "$DOMAIN" --port "$PORT" "${LAN_ARGS[@]}" &
PID=$!
cleanup() { kill "$PID" 2>/dev/null || true; wait "$PID" 2>/dev/null || true; }
trap cleanup EXIT
sleep 0.5

echo "== health =="
HEALTH=$(curl -sf "http://127.0.0.1:$PORT/health")
echo "$HEALTH"
echo "$HEALTH" | grep -q '"ok": true'

echo "== empty chat rejected =="
EMPTY=$(curl -s -X POST "http://127.0.0.1:$PORT/chat" \
  -H 'Content-Type: application/json' \
  -d '{"message":"  "}')
echo "$EMPTY"
echo "$EMPTY" | grep -q '"error": "empty"'

echo "== HTML has privacy =="
curl -sf "http://127.0.0.1:$PORT/" | grep -qi privacy

if [ "$LIVE" = "1" ]; then
  echo "== live movie-suggest turn =="
  REPLY=$(curl -s -X POST "http://127.0.0.1:$PORT/chat" \
    -H 'Content-Type: application/json' \
    -d '{"message":"Something funny under 2 hours we already have on disk. Suggest one title only."}')
  echo "$REPLY" | head -c 2000
  echo
  echo "$REPLY" | grep -q '"ok": true' || { echo "FAIL live chat"; exit 1; }
  # soft check for bunny in index
  echo "$REPLY" | grep -qi 'bunny\|movie\|watch\|film' || echo "WARN: reply may not mention catalog"
fi

echo "== ADB device (optional) =="
if adb devices 2>/dev/null | grep -qE 'device$'; then
  echo "device present"
  python3 scripts/tv/sync-movies-index.py --root "$DOMAIN" --adb || true
else
  echo "no device attached — skip index sync"
fi

echo "SMOKE OK"
