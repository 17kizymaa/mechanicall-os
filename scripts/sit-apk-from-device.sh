#!/bin/sh
# Pull the APK currently installed on the A33 into the local archive.
# Run this *before* overwriting. Not LTE.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
host=${SIT_LOOK_HOST:-${POCKET_EDGE:-mbp-edge}}
serial=${SIT_LOOK_SERIAL:-${POCKET_SERIAL:-RZCW2038KHN}}
pkg=${POCKET_APK_PKG:-com.mechanicall.pocket.demo}
tmp=$(mktemp /tmp/sit-device-apk.XXXXXX.apk)
trap 'rm -f "$tmp"' EXIT
remote=$(ssh -o BatchMode=yes -o ConnectTimeout=8 "$host" \
  "adb -s $serial shell pm path $pkg" | tr -d '\r' | sed -n 's/^package://p' | head -1)
[ -n "$remote" ] || { echo "sit-apk-from-device: $pkg not installed" >&2; exit 1; }
ssh -o BatchMode=yes "$host" "adb -s $serial pull '$remote' /tmp/sit-device.apk" >/dev/null
scp -o BatchMode=yes -q "$host:/tmp/sit-device.apk" "$tmp"
"$ROOT/scripts/sit-apk-archive.sh" "$tmp"
