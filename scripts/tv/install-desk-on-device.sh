#!/usr/bin/env bash
# Full device install path for House Desk demo (seed + index + open on TV).
# Requires: desk-serve already running with --lan on myarch, device on ADB.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DOMAIN="${1:-$ROOT/domains/house-tv-desk}"
IP="${EME640_IP:-192.168.1.235}"
PORT="${EME640_ADB_PORT:-5555}"
SERIAL="${EME640_SERIAL:-$IP:$PORT}"
HOST_IP="${AETHER_DESK_HOST:-192.168.1.241}"
DESK_URL="${AETHER_DESK_URL:-http://$HOST_IP:8788/}"
export EME640_IP="$IP" EME640_ADB_PORT="$PORT" AETHER_DESK_BRIDGE_URL="$DESK_URL"

echo "== connect $SERIAL =="
adb connect "$SERIAL" >/dev/null || true
adb -s "$SERIAL" get-state | grep -q device

echo "== movies index =="
python3 "$ROOT/scripts/tv/sync-movies-index.py" --root "$DOMAIN" --adb

echo "== push seed (no keys) =="
AETHER_DESK_BRIDGE_URL="$DESK_URL" "$ROOT/scripts/tv/push-mechanicall-seed.sh" "$DOMAIN"

echo "== on-device helpers =="
printf '%s\n' '#!/system/bin/sh' \
  "am start -a android.intent.action.VIEW -d ${DESK_URL} -n org.chromium.webview_shell/.WebViewBrowserActivity" \
  > /tmp/open-desk.sh
printf '%s\n' '#!/system/bin/sh' \
  'monkey -p org.xbmc.kodi -c android.intent.category.LAUNCHER 1' \
  > /tmp/open-kodi.sh
adb -s "$SERIAL" push /tmp/open-desk.sh /sdcard/Mechanicall/open-desk.sh >/dev/null
adb -s "$SERIAL" push /tmp/open-kodi.sh /sdcard/Mechanicall/open-kodi.sh >/dev/null
adb -s "$SERIAL" shell chmod 755 /sdcard/Mechanicall/open-desk.sh /sdcard/Mechanicall/open-kodi.sh

echo "== health from device =="
adb -s "$SERIAL" shell "wget -qO- ${DESK_URL}health" || true

echo "== open Desk on TV =="
adb -s "$SERIAL" shell am start -a android.intent.action.VIEW -d "$DESK_URL" \
  -n org.chromium.webview_shell/.WebViewBrowserActivity

echo
echo "Installed for demo:"
echo "  Desk URL:  $DESK_URL"
echo "  Home row:  ${DESK_URL}home"
echo "  Remote:    http://$HOST_IP:8787/"
echo "  Seed:      /sdcard/Mechanicall/"
echo "  Foreground should be WebViewBrowserActivity (Desk)"
