#!/bin/sh
# A33 127.0.0.1:11434 -> edge python hop -> myarch Tailscale Ollama.
# ssh -R is refused on mbp-edge; hop on the edge instead. Not Decide.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
DEST="${DESK_TS_HOST:-100.90.85.68}"

scp -o BatchMode=yes -q "$ROOT/scripts/desk-hop-proxy.py" "$EDGE:/tmp/desk-hop-proxy.py"
ssh -o BatchMode=yes "$EDGE" "pkill -f /tmp/desk-hop-proxy.py >/dev/null 2>&1 || true"
sleep 0.3
ssh -o BatchMode=yes "$EDGE" "nohup python3 /tmp/desk-hop-proxy.py 11434 $DEST >/tmp/desk-hop-proxy.log 2>&1 </dev/null &
sleep 0.4
adb -s $SERIAL reverse --remove tcp:11434 >/dev/null 2>&1 || true
adb -s $SERIAL reverse tcp:11434 tcp:11434
curl -sS -m 2 http://127.0.0.1:11434/api/tags | head -c 80
echo"
echo "desk-through is not Decide"
