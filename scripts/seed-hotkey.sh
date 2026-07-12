#!/bin/sh
# seed-hotkey.sh — RHIZOME layer 2: global capture popup.
# Pops an input line over whatever you're doing; pipes it to `aether seed`.
# Thought → file in under two seconds. Zero decisions at entry.
#
# Bind in XFCE: Settings → Keyboard → Application Shortcuts → add
#   /home/anphuni/mechanicall-os/scripts/seed-hotkey.sh
# or:
#   xfconf-query -c xfce4-keyboard-shortcuts \
#     -p "/commands/custom/<Super>s" -n -t string \
#     -s /home/anphuni/mechanicall-os/scripts/seed-hotkey.sh
#
# Uses rofi/dmenu/zenity when installed; otherwise falls back to a small
# floating xfce4-terminal prompt (no new dependencies).

AETHER="${AETHER_BIN:-aether}"
command -v "$AETHER" >/dev/null 2>&1 || AETHER="$(dirname "$0")/../aether"

if command -v rofi >/dev/null 2>&1; then
    text="$(rofi -dmenu -p 'seed' -l 0)"
elif command -v dmenu >/dev/null 2>&1; then
    text="$(printf '' | dmenu -p 'seed>')"
elif command -v zenity >/dev/null 2>&1; then
    text="$(zenity --entry --title=seed --text='seed>')"
elif command -v xfce4-terminal >/dev/null 2>&1; then
    # Fallback: tiny floating terminal running a read prompt.
    # The terminal process does the capture itself; nothing to collect here.
    exec xfce4-terminal --disable-server --title=seed --hide-menubar \
        --geometry=70x3 \
        -x sh -c "printf 'seed> '; IFS= read -r l; [ -n \"\$l\" ] && \"$AETHER\" seed \"\$l\""
else
    printf 'seed-hotkey: no popup tool (rofi/dmenu/zenity/xfce4-terminal)\n' >&2
    exit 1
fi

[ -n "$text" ] && exec "$AETHER" seed "$text"
exit 0
