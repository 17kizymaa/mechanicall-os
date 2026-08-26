#!/bin/sh
# USB look pipe via mbp-edge adb. Not LTE. Not Funnel. Not NeuralBridge MCP.
# Wakes the panel, captures via a device file (stdout screencap leaks adb warnings),
# rejects non-PNG / tiny / near-black frames.
set -eu
out=${1:-/tmp/sit-look.png}
host=${SIT_LOOK_HOST:-${POCKET_EDGE:-mbp-edge}}
serial=${SIT_LOOK_SERIAL:-${POCKET_SERIAL:-RZCW2038KHN}}
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
if [ -x "$ROOT/scripts/sit-wake.sh" ]; then
  "$ROOT/scripts/sit-wake.sh" >/dev/null || true
fi
ssh -o BatchMode=yes -o ConnectTimeout=8 "$host" \
  "set -e
   adb -s $serial shell screencap -p /data/local/tmp/sit-look.png
   adb -s $serial pull /data/local/tmp/sit-look.png /tmp/sit-look-pull.png >/dev/null" \
  2>/tmp/sit-look.err || {
  echo "sit-look: ssh/adb failed" >&2
  cat /tmp/sit-look.err >&2 || true
  exit 1
}
scp -o BatchMode=yes -q "$host:/tmp/sit-look-pull.png" "$out" || {
  echo "sit-look: scp failed" >&2
  exit 1
}
python3 - "$out" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
raw = p.read_bytes()
if raw[:8] != b"\x89PNG\r\n\x1a\n":
    sys.stderr.write("sit-look: not a PNG (adb warning leaked into stdout?)\n")
    sys.exit(2)
if len(raw) < 80000:
    sys.stderr.write("sit-look: frame too small (%d bytes) — screen off?\n" % len(raw))
    sys.exit(3)
try:
    from PIL import Image
    im = Image.open(p).convert("RGB")
    # 1080x2400 near-black lock/doze compresses tiny; mean catches it.
    mean = sum(im.convert("L").resize((54, 120)).getdata()) / (54 * 120)
    if mean < 6:
        sys.stderr.write("sit-look: near-black (mean=%.1f) — wake the A33\n" % mean)
        sys.exit(4)
except ImportError:
    pass
PY
echo "$out"
