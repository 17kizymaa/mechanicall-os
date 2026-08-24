#!/bin/sh
# Sideload the demo Brake APK to the A33 via mbp-edge USB adb.
# Does not write CURRENT. Opening the app is not Yes.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
APK="${1:-$ROOT/android/app/build/outputs/apk/debug/app-debug.apk}"
PKG="${POCKET_APK_PKG:-com.mechanicall.pocket.demo}"

[ -f "$APK" ] || { echo "missing APK: $APK" >&2; exit 1; }

ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" "mkdir -p /tmp/mechanicall-apk"
scp -o BatchMode=yes -q "$APK" "$EDGE:/tmp/mechanicall-apk/app-debug.apk"
# Remote must fail if install fails (unauthorized used to print success anyway).
ssh -o BatchMode=yes "$EDGE" \
  "set -e
   state=\$(adb -s $SERIAL get-state 2>/dev/null || true)
   if [ -z \"\$state\" ]; then
     state=\$(adb devices | awk -v s=$SERIAL '\$1==s {print \$2; exit}')
   fi
   [ \"\$state\" = device ] || {
     echo \"adb $SERIAL state=\${state:-missing} (Allow USB debugging on the A33, then retry)\" >&2
     adb devices -l >&2 || true
     exit 4
   }
   adb -s $SERIAL install -r /tmp/mechanicall-apk/app-debug.apk
   adb -s $SERIAL shell appops set $PKG MANAGE_EXTERNAL_STORAGE allow || true
   adb -s $SERIAL shell cmd appops set $PKG MANAGE_EXTERNAL_STORAGE allow || true
   adb -s $SERIAL shell dumpsys package $PKG | grep -E 'versionName=|versionCode=' | head -4"
echo "sideloaded $APK -> $EDGE adb:$SERIAL $PKG"
echo "opening the app is not Yes"
