#!/bin/sh
# Copy slim aether CLI to the A33 (not the operator tree).
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
DEST="${POCKET_AETHER_HOME:-/sdcard/mechanicall-aether}"
ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" "mkdir -p /tmp/mechanicall-aether-phone"
scp -o BatchMode=yes -q "$ROOT/aether" "$EDGE:/tmp/mechanicall-aether-phone/aether"
ssh -o BatchMode=yes "$EDGE" "adb -s $SERIAL shell mkdir -p $DEST
adb -s $SERIAL push /tmp/mechanicall-aether-phone/aether $DEST/aether"
echo "pushed aether -> $EDGE adb:$SERIAL:$DEST"
