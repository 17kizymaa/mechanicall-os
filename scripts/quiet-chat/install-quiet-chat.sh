#!/bin/sh
# Install quiet chat on a RUNNING Alpine system (eMachine live or disk).
# Live USB: RAM root is wiped on reboot unless we also persist to ALPINECFG.
#
# Usage (as root):
#   sh install-quiet-chat.sh
#   # optional: KEY already in env, or pass path to env file:
#   CHAT_ENV=/path/to/chat.env sh install-quiet-chat.sh
#
# Persist to USB data partition (survives reboot of live media):
#   sh install-quiet-chat.sh --persist
set -e

PERSIST=0
for a in "$@"; do
  [ "$a" = "--persist" ] && PERSIST=1
done

CHAT_DIR=/opt/chat
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" 2>/dev/null && pwd)
[ -n "$SCRIPT_DIR" ] || SCRIPT_DIR=/opt/chat

echo "Installing quiet chat from $SCRIPT_DIR ..."

apk add python3 2>/dev/null || true

mkdir -p "$CHAT_DIR" /usr/local/bin /etc/profile.d /root
if [ -f "$SCRIPT_DIR/aether_desk.py" ]; then
  cp -f "$SCRIPT_DIR/aether_desk.py" "$SCRIPT_DIR/aether_llm.py" "$CHAT_DIR/"
else
  echo "Missing aether_desk.py next to this script" >&2
  exit 1
fi
chmod 755 "$CHAT_DIR/aether_desk.py"

# Keys: CHAT_ENV file, or /root/.chat.env, or create empty template
if [ -n "${CHAT_ENV:-}" ] && [ -f "$CHAT_ENV" ]; then
  install -m 600 "$CHAT_ENV" /root/.chat.env
elif [ -f /root/.chat.env ]; then
  :
elif [ -f /media/ALPINECFG/chat.env ]; then
  install -m 600 /media/ALPINECFG/chat.env /root/.chat.env
else
  echo "WARN: no chat.env — set OPENROUTER_API_KEY in /root/.chat.env" >&2
fi

# Hostname = free endpoint identity
echo openrouter > /etc/hostname
hostname openrouter 2>/dev/null || true
grep -q '[[:space:]]openrouter$' /etc/hosts 2>/dev/null || echo "127.0.0.1	openrouter" >> /etc/hosts

# Silence Alpine noise
: > /etc/motd
cat > /etc/issue <<'ISSUE'

  Welcome.

ISSUE

# Console launcher (NO login shell required — used by inittab)
cat > /usr/local/bin/chat-console <<'BIN'
#!/bin/sh
export HOME=/root
export TERM="${TERM:-linux}"
cd /root 2>/dev/null || cd /
if [ -f /root/.chat.env ]; then
  set -a
  # shellcheck disable=SC1091
  . /root/.chat.env
  set +a
fi
export AETHER_LLM_PROVIDER="${AETHER_LLM_PROVIDER:-openrouter}"
export AETHER_MODEL="${AETHER_MODEL:-openrouter/free}"
# brief wait for devices
sleep 1
clear 2>/dev/null || true
exec python3 /opt/chat/aether_desk.py /root
BIN
chmod 755 /usr/local/bin/chat-console

# Manual start
cat > /usr/local/bin/chat <<'BIN'
#!/bin/sh
export HOME=/root
[ -f /root/.chat.env ] && set -a && . /root/.chat.env && set +a
exec python3 /opt/chat/aether_desk.py "${1:-/root}"
BIN
chmod 755 /usr/local/bin/chat

# Login shells also go to chat (backup path)
cat > /etc/profile.d/zz-chat.sh <<'PROF'
case "$-" in *i*) ;; *) return 0 ;; esac
[ "${CHAT_SKIP:-}" = "1" ] && return 0
[ -n "$CHAT_STARTED" ] && return 0
export CHAT_STARTED=1
[ -f /root/.chat.env ] && set -a && . /root/.chat.env && set +a
cd /root 2>/dev/null || true
exec python3 /opt/chat/aether_desk.py /root
PROF
chmod 644 /etc/profile.d/zz-chat.sh

# *** IMPORTANT: tty1 starts chat directly (what you see after reboot) ***
if [ -f /etc/inittab ]; then
  cp -a /etc/inittab /etc/inittab.bak.quietchat 2>/dev/null || true
  # comment default getty on tty1 if present; add chat-console
  if grep -q 'chat-console' /etc/inittab 2>/dev/null; then
    :
  else
    # disable common getty lines for tty1
    sed -i 's/^\(tty1::respawn:.*getty.*\)/#\1/' /etc/inittab
    sed -i 's/^\(tty1::respawn:.*agetty.*\)/#\1/' /etc/inittab
    printf '\n# quiet chat (mechanicall)\ntty1::respawn:/usr/local/bin/chat-console\n' >> /etc/inittab
  fi
  # apply without full reboot if possible
  kill -HUP 1 2>/dev/null || true
fi

# Minimal CURRENT (silent context only)
[ -f /root/CURRENT.md ] || cat > /root/CURRENT.md <<'CUR'
# CURRENT

**Objective:** Private conversation.
**Next:** talk
**Phase:** EXECUTE
**Status:** READY
**Approval:** PENDING

## Keep
- Quiet chat

## Reject
- Technical noise on screen

## Next allowed action
Talk.

## Prohibited
- model-approve
CUR

echo "Installed. hostname=$(cat /etc/hostname 2>/dev/null)"
echo "Test now:  chat"
echo "Or reboot — tty1 should open chat (if this install is still on disk)."

# Persist onto ALPINECFG when asked / available
persist_to_cfg() {
  CFG=""
  for d in /media/ALPINECFG /media/*/ALPINECFG /mnt/ALPINECFG; do
    [ -d "$d" ] && CFG=$d && break
  done
  if [ -z "$CFG" ]; then
    # try label mount
    mkdir -p /media/ALPINECFG
    if command -v findfs >/dev/null 2>&1; then
      DEV=$(findfs LABEL=ALPINECFG 2>/dev/null || true)
      [ -n "$DEV" ] && mount -t vfat "$DEV" /media/ALPINECFG 2>/dev/null && CFG=/media/ALPINECFG
    fi
  fi
  if [ -z "$CFG" ] || [ ! -d "$CFG" ]; then
    echo "No ALPINECFG mount — skip USB persist."
    echo "After reboot on LIVE USB you must re-run this install (RAM root)."
    return 0
  fi
  echo "Persisting to $CFG ..."
  mkdir -p "$CFG/quiet-chat" "$CFG/auto"
  cp -f /opt/chat/aether_desk.py /opt/chat/aether_llm.py "$CFG/quiet-chat/"
  cp -f "$SCRIPT_DIR/install-quiet-chat.sh" "$CFG/quiet-chat/" 2>/dev/null || \
    cp -f /opt/chat/../quiet-chat/install-quiet-chat.sh "$CFG/quiet-chat/" 2>/dev/null || true
  # copy this installer into CFG if we are the copy
  cp -f "$0" "$CFG/quiet-chat/install-quiet-chat.sh" 2>/dev/null || true
  [ -f /root/.chat.env ] && install -m 600 /root/.chat.env "$CFG/chat.env"
  # one command rehydrate after every live boot
  cat > "$CFG/auto/start" <<'START'
#!/bin/sh
# Run once after live boot:  sh /media/ALPINECFG/auto/start
set -e
DIR=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
export CHAT_ENV="$DIR/chat.env"
sh "$DIR/quiet-chat/install-quiet-chat.sh"
echo "Reboot or run: chat"
START
  chmod +x "$CFG/auto/start" 2>/dev/null || true
  cat > "$CFG/README-AFTER-REBOOT.txt" <<'R'
LIVE Alpine forgets /opt and /etc on reboot (RAM).

After each boot, as root:
  1) mount -t vfat the ALPINECFG partition to /media/ALPINECFG
  2) sh /media/ALPINECFG/auto/start
  3) reboot   (or: chat)

Or install Alpine to internal disk so changes stick permanently.
R
  echo "Wrote $CFG/auto/start and chat files."
}

if [ "$PERSIST" = "1" ]; then
  persist_to_cfg
else
  # auto-persist if partition already mounted
  [ -d /media/ALPINECFG ] && PERSIST=1 && persist_to_cfg || true
fi

echo DONE
