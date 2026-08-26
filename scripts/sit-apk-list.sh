#!/bin/sh
# List archived sit APKs. Newest last.
set -eu
ARCHIVE=${MECHANICALL_APK_ARCHIVE:-$HOME/.mechanicall/apk-archive}
[ -d "$ARCHIVE" ] || { echo "sit-apk-list: empty $ARCHIVE" >&2; exit 0; }
ls -1 "$ARCHIVE"/mechanicall-*-vc*.apk 2>/dev/null || true
if [ -L "$ARCHIVE/LAST.apk" ] || [ -f "$ARCHIVE/LAST.apk" ]; then
  echo "LAST -> $(readlink -f "$ARCHIVE/LAST.apk" 2>/dev/null || echo "$ARCHIVE/LAST.apk")"
fi
