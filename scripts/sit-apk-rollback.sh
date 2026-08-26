#!/bin/sh
# Sideload an archived sit APK onto the A33 (downgrade allowed).
# Usage: sit-apk-rollback.sh [versionName|path|LAST]
# Opening the app is not Yes.
set -eu
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
ARCHIVE=${MECHANICALL_APK_ARCHIVE:-$HOME/.mechanicall/apk-archive}
want=${1:-LAST}
apk=
case "$want" in
  LAST|"")
    apk=$ARCHIVE/LAST.apk
    ;;
  /*|./*)
    apk=$want
    ;;
  *)
    apk=$(ls -1 "$ARCHIVE"/mechanicall-"$want"-vc*.apk 2>/dev/null | tail -1 || true)
    if [ -z "$apk" ]; then
      apk=$(ls -1 "$ARCHIVE"/mechanicall-*"$want"*.apk 2>/dev/null | tail -1 || true)
    fi
    ;;
esac
[ -n "$apk" ] && [ -f "$apk" ] || {
  echo "sit-apk-rollback: no archive match for '$want'" >&2
  echo "have:" >&2
  "$ROOT/scripts/sit-apk-list.sh" >&2 || true
  exit 1
}
# Resolve LAST symlink
apk=$(readlink -f "$apk" 2>/dev/null || echo "$apk")
echo "rollback $apk"
# sideload uses install -r; we need -d for versionCode down.
EDGE=${POCKET_EDGE:-${SIT_LOOK_HOST:-mbp-edge}}
SERIAL=${POCKET_SERIAL:-${SIT_LOOK_SERIAL:-RZCW2038KHN}}
PKG=${POCKET_APK_PKG:-com.mechanicall.pocket.demo}
ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" "mkdir -p /tmp/mechanicall-apk"
scp -o BatchMode=yes -q "$apk" "$EDGE:/tmp/mechanicall-apk/app-debug.apk"
ssh -o BatchMode=yes "$EDGE" \
  "set -e
   state=\$(adb -s $SERIAL get-state 2>/dev/null || true)
   if [ -z \"\$state\" ]; then
     state=\$(adb devices | awk -v s=$SERIAL '\$1==s {print \$2; exit}')
   fi
   [ \"\$state\" = device ] || {
     echo \"adb $SERIAL state=\${state:-missing}\" >&2
     exit 4
   }
   adb -s $SERIAL install -r -d /tmp/mechanicall-apk/app-debug.apk
   adb -s $SERIAL shell appops set $PKG MANAGE_EXTERNAL_STORAGE allow || true
   adb -s $SERIAL shell dumpsys package $PKG | grep -E 'versionName=|versionCode=' | head -4"
echo "rolled back $apk -> $EDGE adb:$SERIAL $PKG"
echo "opening the app is not Yes"
