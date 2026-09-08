#!/bin/sh
# Smoke Send-folder dest. Stages. Not Yes. Not FILES. USB ≠ LTE. Not Play.
# Source probe always. Device look only if mbp-edge A33 is up.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
NAV="$ROOT/android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt"
RACK="$ROOT/android/app/src/main/java/com/mechanicall/pocket/demo/SitRackView.kt"
CRECTS="$ROOT/android/app/src/main/java/com/mechanicall/pocket/demo/SitCRects.kt"

grep -q "openSendOverlay" "$NAV"
grep -q "stageSendFolder" "$NAV"
grep -q "sendFolder" "$NAV"
grep -q "SitHit.Send" "$NAV"
grep -q "sendOverlay" "$RACK"
grep -q "tap outside to dismiss" "$RACK"
grep -q "SitHit.Files" "$NAV"
grep -q "folderSend" "$CRECTS"
grep -q "folderOem" "$CRECTS"
echo "sit-send-smoke: source PASS (dest, FOLDER plaque stages, not Yes, FILES other hit)"

EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
OUT="${1:-$ROOT/dev/57_first-sit-look/10_send_folder/output/send-overlay.png}"
if ssh -o BatchMode=yes -o ConnectTimeout=5 "$EDGE" "adb -s $SERIAL get-state" 2>/dev/null | grep -q device; then
  mkdir -p "$(dirname "$OUT")"
  SIT_LOOK_HOST="$EDGE" POCKET_SERIAL="$SERIAL" "$ROOT/scripts/sit-look.sh" "$OUT" || \
    echo "sit-send-smoke: look failed (panel?)" >&2
  echo "sit-send-smoke: USB look -> $OUT (not LTE, not Yes)"
else
  echo "sit-send-smoke: A33 not on USB; source-only (not a testers receipt)"
fi
