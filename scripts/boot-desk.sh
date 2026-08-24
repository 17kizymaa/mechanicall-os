#!/bin/sh
# Boot myarch local model (anyone can run this). Private binds only. Not Decide.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
MODEL="${DESK_MODEL:-personal-llm-sft-v4:latest}"
LAN="${DESK_LAN:-http://192.168.0.51:11434}"
TS="${DESK_TS:-http://100.90.85.68:11434}"

probe() {
  curl -sS -m 2 "$1/api/tags" >/dev/null 2>&1
}

if ! probe "http://127.0.0.1:11434"; then
  if command -v systemctl >/dev/null 2>&1; then
    systemctl start ollama 2>/dev/null || systemctl --user start ollama 2>/dev/null || true
  fi
  if ! probe "http://127.0.0.1:11434"; then
    ollama serve >/tmp/mechanicall-ollama.log 2>&1 &
    sleep 2
  fi
fi

if ! probe "http://127.0.0.1:11434"; then
  echo "desk quiet: ollama not on 127.0.0.1:11434" >&2
  exit 4
fi

tags=$(curl -sS -m 4 http://127.0.0.1:11434/api/tags || true)
printf '%s\n' "$tags" | grep -q "$MODEL" || printf '%s\n' "$tags" | grep -q "personal-llm-sft-v4" || {
  echo "desk quiet: model $MODEL not listed" >&2
  echo "$tags" | head -c 200 >&2
  exit 5
}

echo "DESK idle"
echo "local  http://127.0.0.1:11434  model=$MODEL"
echo "lan    $LAN"
echo "tail   $TS"
echo "public 0.0.0.0 refused"
if [ -x "$ROOT/scripts/desk-through-a33.sh" ]; then
  sh "$ROOT/scripts/desk-through-a33.sh" || echo "usb reverse skipped"
fi
echo "boot-desk is not Decide"
