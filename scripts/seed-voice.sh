#!/bin/sh
# RHIZOME layer 3 — voice capture → aether seed
# On start: prefer headphone/headset ports (when plugged). After: restore audio.
#
# Bind Super+V. Env: AETHER_VOICE_SECS, AETHER_VOICE_MODEL, AETHER_BIN
# AETHER_VOICE_NO_TOGGLE=1 skips headset switch.

set -e
SECS="${AETHER_VOICE_SECS:-8}"
AETHER="${AETHER_BIN:-aether}"
command -v "$AETHER" >/dev/null 2>&1 || AETHER="$(dirname "$0")/../aether"
TOGGLE="$(dirname "$0")/audio-headset-toggle.sh"
TMPDIR="${TMPDIR:-/tmp}"
WAV="$TMPDIR/aether-seed-$$.wav"

cleanup() {
    rm -f "$WAV" "$TMPDIR/aether-seed-$$.txt"
    if [ "${AETHER_VOICE_NO_TOGGLE:-0}" != "1" ] && [ -x "$TOGGLE" ]; then
        "$TOGGLE" restore >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

notify() {
    if command -v notify-send >/dev/null 2>&1; then
        notify-send -t 2000 "aether seed" "$1" 2>/dev/null || true
    fi
    printf '%s\n' "$1" >&2
}

# Prefer headphones + headset mic when the jack/BT set is present
if [ "${AETHER_VOICE_NO_TOGGLE:-0}" != "1" ] && [ -x "$TOGGLE" ]; then
    "$TOGGLE" prefer >/dev/null 2>&1 || true
fi

# record from Pulse/PipeWire default source (post-toggle)
if command -v ffmpeg >/dev/null 2>&1; then
    notify "listening ${SECS}s (headset if plugged)…"
    ffmpeg -hide_banner -loglevel error -f pulse -i default -t "$SECS" -ac 1 -ar 16000 "$WAV" || {
        notify "mic record failed — plug headset or check: $TOGGLE status"
        exit 1
    }
elif command -v arecord >/dev/null 2>&1; then
    notify "listening ${SECS}s…"
    arecord -q -f S16_LE -r 16000 -c 1 -d "$SECS" "$WAV" || {
        notify "mic record failed"; exit 1
    }
else
    notify "need ffmpeg or arecord for mic capture"
    exit 1
fi

text=""
for bin in whisper-cli whisper main whisper-cpp; do
    if command -v "$bin" >/dev/null 2>&1; then
        MODEL="${AETHER_VOICE_MODEL:-$HOME/models/ggml-base.en.bin}"
        if [ -f "$MODEL" ]; then
            out="$TMPDIR/aether-seed-$$"
            "$bin" -m "$MODEL" -f "$WAV" -otxt -of "$out" 2>/dev/null || true
            [ -f "$out.txt" ] && text="$(tr '\n' ' ' < "$out.txt")"
            rm -f "$out.txt"
        fi
        break
    fi
done

if [ -z "$text" ] && command -v whisper >/dev/null 2>&1; then
    base="$(basename "$WAV" .wav)"
    whisper "$WAV" --model tiny.en --language en --output_format txt --output_dir "$TMPDIR" >/dev/null 2>&1 || true
    [ -f "$TMPDIR/$base.txt" ] && text="$(tr '\n' ' ' < "$TMPDIR/$base.txt")"
    rm -f "$TMPDIR/$base.txt"
fi

text="$(printf '%s' "$text" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
if [ -z "$text" ]; then
    notify "no transcript (whisper ready; mic may be silent until headset plugged)"
    exit 2
fi

"$AETHER" seed "$text"
notify "planted: $text"
