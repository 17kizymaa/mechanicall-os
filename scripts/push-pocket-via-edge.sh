#!/bin/sh
# Push the pocket *template* to the Samsung A33 via mbp-edge USB adb.
# Never pushes mechanicall-os. Demo only.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
REMOTE_SD="${POCKET_PHONE_PATH:-/sdcard/mechanicall-pocket}"
SRC="$ROOT/examples/pocket-demo-client"

[ -f "$SRC/CURRENT.md" ] || { echo "missing $SRC/CURRENT.md" >&2; exit 1; }

STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/mechanicall-pocket"
cp "$SRC/CURRENT.md" "$SRC/PROPOSE-CURRENT.md" "$SRC/README.md" \
  "$STAGE/mechanicall-pocket/"
if [ -f "$STAGE/mechanicall-pocket/SITTING.md" ] || true; then
  cat > "$STAGE/mechanicall-pocket/SITTING.md" <<EOF
# Demo sitting
Pocket Domain on the phone. Not mechanicall-os.
Bind: $REMOTE_SD
USB host: mbp-edge ($EDGE)
Serial: $SERIAL
Ollama: myarch Tailscale 100.90.85.68:11434 (demo: whole folder).
EOF
fi

ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" "mkdir -p /tmp/mechanicall-pocket-pack"
scp -o BatchMode=yes -q -r "$STAGE/mechanicall-pocket" \
  "$EDGE:/tmp/mechanicall-pocket-pack/"
ssh -o BatchMode=yes "$EDGE" \
  "adb -s $SERIAL push /tmp/mechanicall-pocket-pack/mechanicall-pocket $REMOTE_SD"
echo "pushed $SRC -> $EDGE adb:$SERIAL:$REMOTE_SD"
