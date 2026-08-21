#!/bin/sh
# One STORM walker, one emulator serial, one pocket. Never Confirm. Never the A33.
set -eu
SERIAL="${1:?emulator-NNNN}"
OUT="${2:?/tmp/storm-env/<id>/out}"
PKG=com.mechanicall.pocket.demo
mkdir -p "$OUT"

adb() { command adb -s "$SERIAL" "$@"; }

case "$(adb get-serialno 2>/dev/null || true)" in
  RZCW2038KHN) echo "refused: live A33" >&2; exit 3 ;;
esac

dump() {
  name="$1"
  adb shell uiautomator dump /sdcard/uidump.xml >/dev/null
  adb pull /sdcard/uidump.xml "$OUT/uidump-${name}.xml" >/dev/null
  adb exec-out screencap -p > "$OUT/${name}.png"
}

adb shell am force-stop "$PKG"
adb shell am start -n "$PKG/.MainActivity"
sleep 3
dump home
echo "opening is not Decide; Confirm was not tapped"
