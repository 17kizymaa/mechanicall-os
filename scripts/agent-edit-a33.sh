#!/bin/sh
# Pull A33 pocket → Ollama (propose only) → push PROPOSE-CURRENT.md back.
# Never writes CURRENT.md. Never approve.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
EDGE="${POCKET_EDGE:-anphuni@100.70.86.90}"
SERIAL="${POCKET_SERIAL:-RZCW2038KHN}"
PHONE="${POCKET_PHONE_PATH:-/sdcard/mechanicall-pocket}"
HOST_TWIN="${POCKET_HOST_TWIN:-$HOME/mechanicall-pocket}"
OLLAMA="${POCKET_OLLAMA:-http://127.0.0.1:11434}"
MODEL="${POCKET_MODEL:-personal-llm-sft-v4:latest}"
INSTR="${1:-Draft a mum-class proposal for this sitting. Keep one Next. Do not approve.}"

mkdir -p "$HOST_TWIN"
ssh -o BatchMode=yes -o ConnectTimeout=8 "$EDGE" \
  "adb -s $SERIAL pull $PHONE/CURRENT.md /tmp/a33-CURRENT.md
   adb -s $SERIAL pull $PHONE/PROPOSE-CURRENT.md /tmp/a33-PROPOSE.md"
scp -o BatchMode=yes -q "$EDGE:/tmp/a33-CURRENT.md" "$HOST_TWIN/CURRENT.md"
scp -o BatchMode=yes -q "$EDGE:/tmp/a33-PROPOSE.md" "$HOST_TWIN/PROPOSE-CURRENT.md"

export AETHER_HOME="$ROOT"
export PYTHONPATH="$ROOT/python${PYTHONPATH:+:$PYTHONPATH}"
python3 - "$HOST_TWIN" "$OLLAMA" "$MODEL" "$INSTR" <<'PY'
import hashlib, sys
from pathlib import Path
from aether_pocket import agent_edit_propose, refuse_if_operator

pocket, host, model, instr = sys.argv[1:5]
root = refuse_if_operator(pocket)
cf = root / "CURRENT.md"
before = hashlib.sha256(cf.read_bytes()).hexdigest()
r = agent_edit_propose(root, ollama_host=host, model=model, instruction=instr, timeout=300)
print(r.text)
after = hashlib.sha256(cf.read_bytes()).hexdigest()
if before != after:
    raise SystemExit("REFUSED: CURRENT.md changed — aborting push")
print("CURRENT.md unchanged", before[:12])
PY

scp -o BatchMode=yes -q "$HOST_TWIN/PROPOSE-CURRENT.md" "$EDGE:/tmp/a33-PROPOSE.md"
ssh -o BatchMode=yes "$EDGE" \
  "adb -s $SERIAL push /tmp/a33-PROPOSE.md $PHONE/PROPOSE-CURRENT.md"
echo "pushed PROPOSE-CURRENT.md only → $PHONE"
