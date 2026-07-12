#!/bin/sh
# Prefer headphone/headset ports when present; restore previous defaults after.
# Used by seed-voice.sh. PipeWire/Pulse via pactl.
#
# Usage:
#   audio-headset-toggle.sh prefer   # switch to headphones + headset/analog mic if available
#   audio-headset-toggle.sh restore  # restore saved defaults
#   audio-headset-toggle.sh status

set -e
STATE="${XDG_RUNTIME_DIR:-/tmp}/aether-audio-state"

save_state() {
    {
        echo "SINK=$(pactl get-default-sink 2>/dev/null || true)"
        echo "SOURCE=$(pactl get-default-source 2>/dev/null || true)"
        # card profiles
        pactl list short cards 2>/dev/null | while read -r idx name rest; do
            [ -n "$name" ] || continue
            prof=$(pactl list cards 2>/dev/null | awk -v n="$name" '
                $0 ~ "Name: "n {p=1}
                p && /Active Profile:/ {print $3; exit}
            ')
            echo "CARD|$name|$prof"
        done
    } > "$STATE"
}

restore_state() {
    [ -f "$STATE" ] || return 0
    while IFS= read -r line; do
        case "$line" in
            SINK=*)
                s="${line#SINK=}"
                [ -n "$s" ] && pactl set-default-sink "$s" 2>/dev/null || true
                ;;
            SOURCE=*)
                s="${line#SOURCE=}"
                [ -n "$s" ] && pactl set-default-source "$s" 2>/dev/null || true
                ;;
            CARD\|*)
                name=$(printf '%s' "$line" | cut -d'|' -f2)
                prof=$(printf '%s' "$line" | cut -d'|' -f3)
                [ -n "$name" ] && [ -n "$prof" ] && \
                    pactl set-card-profile "$name" "$prof" 2>/dev/null || true
                ;;
        esac
    done < "$STATE"
}

prefer_headset() {
    save_state
    # Onboard HDA only — force analog duplex so jack headphones + mic path exists
    # (port may show "not available" until physical plug; profile still arms it)
    for card in $(pactl list short cards 2>/dev/null | awk '{print $2}'); do
        case "$card" in
            *hdmi*|*GPU*|*nvidia*|*usb*) continue ;;
        esac
        # Duplex first; fall back to SPDIF out + analog in if analog out fails
        if ! pactl set-card-profile "$card" "output:analog-stereo+input:analog-stereo" 2>/dev/null; then
            pactl set-card-profile "$card" "output:iec958-stereo+input:analog-stereo" 2>/dev/null || true
        fi
    done
    sleep 0.3

    # Sink: never HDMI for voice capture sessions
    sink=$(pactl list short sinks 2>/dev/null | awk '
        tolower($2) ~ /analog/ && tolower($2) !~ /hdmi/ {print $2; exit}
    ')
    if [ -z "$sink" ]; then
        sink=$(pactl list short sinks 2>/dev/null | awk '
            tolower($2) !~ /hdmi/ {print $2; exit}
        ')
    fi
    [ -n "$sink" ] && pactl set-default-sink "$sink" 2>/dev/null || true

    # Source: analog mic / headset (never *.monitor)
    src=$(pactl list short sources 2>/dev/null | awk '
        tolower($2) ~ /analog/ && tolower($2) !~ /monitor/ {print $2; exit}
    ')
    if [ -z "$src" ]; then
        src=$(pactl list short sources 2>/dev/null | awk '
            tolower($2) !~ /monitor|hdmi/ {print $2; exit}
        ')
    fi
    [ -n "$src" ] && pactl set-default-source "$src" 2>/dev/null || true
    [ -n "$src" ] && pactl set-source-mute "$src" 0 2>/dev/null || true

    printf 'prefer: sink=%s source=%s (plug headset jack if silent)\n' \
        "$(pactl get-default-sink 2>/dev/null)" \
        "$(pactl get-default-source 2>/dev/null)"
}

status() {
    echo "default sink:   $(pactl get-default-sink 2>/dev/null)"
    echo "default source: $(pactl get-default-source 2>/dev/null)"
    pactl list cards 2>/dev/null | awk '
        /Name:/ {name=$2}
        /Active Profile:/ {print name, $0}
        /Headphones/ {print "  ", $0}
    ' | head -40
    if [ -f "$STATE" ]; then
        echo "saved state: $STATE"
    else
        echo "saved state: (none)"
    fi
}

cmd="${1:-status}"
case "$cmd" in
    prefer)  prefer_headset ;;
    restore) restore_state; echo "restored"; status ;;
    status)  status ;;
    *) echo "usage: $0 prefer|restore|status" >&2; exit 2 ;;
esac
