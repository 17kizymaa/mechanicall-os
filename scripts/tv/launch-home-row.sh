#!/usr/bin/env bash
# Open parent home row (Kodi · Desk · Remote) on the TV browser.
set -euo pipefail
IP="${EME640_IP:-192.168.1.235}"
PORT="${EME640_ADB_PORT:-5555}"
SERIAL="${EME640_SERIAL:-$IP:$PORT}"
HOST_IP="${AETHER_DESK_HOST:-192.168.1.241}"
URL="${1:-http://$HOST_IP:8788/home}"

adb connect "$SERIAL" >/dev/null || true
adb -s "$SERIAL" shell am start -a android.intent.action.VIEW -d "$URL" \
  -n org.chromium.webview_shell/.WebViewBrowserActivity
echo "Home row: $URL"
