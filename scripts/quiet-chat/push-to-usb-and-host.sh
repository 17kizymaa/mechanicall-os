#!/bin/sh
# From operator (myarch): push quiet-chat + OpenRouter key to eMachine and/or ALPINECFG.
# Usage:
#   sh scripts/quiet-chat/push-to-usb-and-host.sh [EMACHINE_IP]
set -e
ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
QC="$ROOT/scripts/quiet-chat"
IP=${1:-192.168.1.235}
ENV_FILE=${CHAT_ENV_SRC:-$HOME/Desktop/.env}

KEY=""
if [ -f "$ENV_FILE" ]; then
  KEY=$(awk '/^sk-or-/{print; exit}' "$ENV_FILE")
fi
if [ -z "$KEY" ]; then
  echo "No sk-or- key in $ENV_FILE" >&2
  exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp "$QC/aether_desk.py" "$QC/aether_llm.py" "$QC/install-quiet-chat.sh" "$TMP/"
printf '%s\n' "OPENROUTER_API_KEY=$KEY" "AETHER_LLM_PROVIDER=openrouter" "AETHER_MODEL=openrouter/free" > "$TMP/chat.env"
chmod 600 "$TMP/chat.env"

SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=8"
SCP="scp -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=8"

if $SSH "root@$IP" "true" 2>/dev/null; then
  echo "Pushing to root@$IP ..."
  $SSH "root@$IP" "mkdir -p /tmp/quiet-chat"
  $SCP "$TMP/aether_desk.py" "$TMP/aether_llm.py" "$TMP/install-quiet-chat.sh" "$TMP/chat.env" "root@$IP:/tmp/quiet-chat/"
  $SSH "root@$IP" "CHAT_ENV=/tmp/quiet-chat/chat.env sh /tmp/quiet-chat/install-quiet-chat.sh --persist"
  echo "Remote install done. Reboot the eMachine and watch tty1."
else
  echo "Cannot SSH root@$IP — machine offline or no sshd."
  echo "Plug ALPINECFG USB into this PC and re-run with stick mounted, or bring eMachine online."
fi

# If ALPINECFG is on MBP as root mount
if ssh -o BatchMode=yes -o ConnectTimeout=4 mbp-root "blkid -L ALPINECFG" 2>/dev/null | grep -q .; then
  echo "Also writing ALPINECFG on mbp-edge..."
  ssh -o BatchMode=yes mbp-root "mkdir -p /media/ALPINECFG && umount /media/ALPINECFG 2>/dev/null; mount -t vfat \$(blkid -L ALPINECFG) /media/ALPINECFG"
  scp -o BatchMode=yes mbp-root:/dev/null /dev/null 2>/dev/null || true
fi
