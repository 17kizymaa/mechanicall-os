#!/usr/bin/env bash
# Push House Desk seed tree to Android TV /sdcard/Mechanicall/
# Keys are NOT pushed (stay on myarch).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DOMAIN="${1:-$ROOT/domains/house-tv-desk}"
IP="${EME640_IP:-192.168.1.235}"
PORT="${EME640_ADB_PORT:-5555}"
SERIAL="${EME640_SERIAL:-$IP:$PORT}"
REMOTE="${MECHANICALL_REMOTE:-/sdcard/Mechanicall}"

echo "Connecting adb $SERIAL ..."
adb connect "$SERIAL" >/dev/null || true

echo "Pushing seed from $DOMAIN → $REMOTE"
adb -s "$SERIAL" shell "mkdir -p $REMOTE/library $REMOTE/.aether"

adb -s "$SERIAL" push "$DOMAIN/CURRENT.md" "$REMOTE/CURRENT.md"
adb -s "$SERIAL" push "$DOMAIN/README.md" "$REMOTE/README.md" 2>/dev/null || true
if [ -f "$DOMAIN/library/movies-index.md" ]; then
  adb -s "$SERIAL" push "$DOMAIN/library/movies-index.md" "$REMOTE/library/movies-index.md"
fi
if [ -f "$DOMAIN/library/navigate-help.md" ]; then
  adb -s "$SERIAL" push "$DOMAIN/library/navigate-help.md" "$REMOTE/library/navigate-help.md"
fi

# Bridge URL hint for a future WebView APK (plain text, no secrets)
BRIDGE_URL="${AETHER_DESK_BRIDGE_URL:-http://192.168.1.241:8788/}"
echo "$BRIDGE_URL" | adb -s "$SERIAL" shell "cat > $REMOTE/bridge.url"

echo "Done. Device seed:"
adb -s "$SERIAL" shell "ls -la $REMOTE; echo '---'; cat $REMOTE/bridge.url"
echo
echo "Desk still runs on myarch:  aether desk-serve --lan --port 8788 $DOMAIN"
echo "No API keys were pushed."
