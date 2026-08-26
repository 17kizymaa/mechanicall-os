#!/bin/sh
# Copy an APK into ~/.mechanicall/apk-archive named by versionName + versionCode.
# Not git. Not Yes. Sideload still required to land it on the A33.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
APK=${1:-$ROOT/android/app/build/outputs/apk/debug/app-debug.apk}
ARCHIVE=${MECHANICALL_APK_ARCHIVE:-$HOME/.mechanicall/apk-archive}
AAPT=${AAPT:-}
[ -f "$APK" ] || { echo "sit-apk-archive: missing $APK" >&2; exit 1; }
if [ -z "$AAPT" ]; then
  AAPT=$(ls "$HOME/.android-sdk-mechanicall/build-tools/"*/aapt 2>/dev/null | tail -1 || true)
fi
[ -n "$AAPT" ] && [ -x "$AAPT" ] || { echo "sit-apk-archive: aapt not found" >&2; exit 1; }
badging=$("$AAPT" dump badging "$APK")
vc=$(printf '%s\n' "$badging" | sed -n "s/.*versionCode='\\([^']*\\)'.*/\\1/p" | head -1)
vn=$(printf '%s\n' "$badging" | sed -n "s/.*versionName='\\([^']*\\)'.*/\\1/p" | head -1)
[ -n "$vc" ] && [ -n "$vn" ] || { echo "sit-apk-archive: no version in $APK" >&2; exit 1; }
safe=$(printf '%s' "$vn" | tr '/ :' '---')
mkdir -p "$ARCHIVE"
dest="$ARCHIVE/mechanicall-${safe}-vc${vc}.apk"
cp -f "$APK" "$dest"
# pointer to last archived (rollback default)
ln -sfn "$dest" "$ARCHIVE/LAST.apk"
printf '%s\n' "$dest"
