#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APK="${1:-$ROOT/android/house-desk/app/build/outputs/apk/debug/app-debug.apk}"
IP="${EME640_IP:-192.168.1.235}"
PORT="${EME640_ADB_PORT:-5555}"
SERIAL="${EME640_SERIAL:-$IP:$PORT}"

if [ ! -f "$APK" ]; then
  echo "Missing APK: $APK"
  echo "Build first: scripts/tv/build-house-desk-apk.sh"
  echo "Or open without APK: scripts/tv/open-desk-on-tv.sh"
  exit 1
fi

adb connect "$SERIAL" >/dev/null || true
"$ROOT/scripts/tv/push-mechanicall-seed.sh" || true
adb -s "$SERIAL" install -r "$APK"
echo "Installed. Launch Desk from Leanback home, or:"
adb -s "$SERIAL" shell monkey -p os.mechanicall.housedesk.debug -c android.intent.category.LEANBACK_LAUNCHER 1 \
  || adb -s "$SERIAL" shell monkey -p os.mechanicall.housedesk -c android.intent.category.LAUNCHER 1 \
  || true
