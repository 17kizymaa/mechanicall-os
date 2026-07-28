#!/usr/bin/env bash
# Open Desk URL on House TV via ADB VIEW intent (no APK required).
set -euo pipefail
IP="${EME640_IP:-192.168.1.235}"
PORT="${EME640_ADB_PORT:-5555}"
SERIAL="${EME640_SERIAL:-$IP:$PORT}"
URL="${AETHER_DESK_URL:-${1:-http://192.168.1.241:8788/}}"
# chat-only desk (strip accidental /home)
URL="${URL%%/home}"
URL="${URL%%/home/}"
case "$URL" in */) ;; *) URL="$URL/" ;; esac

echo "adb connect $SERIAL"
adb connect "$SERIAL" >/dev/null || true
echo "Opening $URL on device..."
adb -s "$SERIAL" shell am start -a android.intent.action.VIEW -d "$URL"
echo "Done. Ensure desk-serve is running with --lan on myarch."
