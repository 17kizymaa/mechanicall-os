#!/bin/sh
# RHIZOME layer 3 — voice capture → aether seed
# Hold-free: record SECS seconds (default 8), transcribe, plant seed.
# Prefers: whisper.cpp (whisper-cli / main) → openai-whisper → speech-recognition fail soft.
#
# Bind e.g. Super+V in XFCE Application Shortcuts.
# Env: AETHER_VOICE_SECS, AETHER_VOICE_MODEL, AETHER_BIN

set -e
SECS="${AETHER_VOICE_SECS:-8}"
AETHER="${AETHER_BIN:-aether}"
command -v "$AETHER" >/dev/null 2>&1 || AETHER="$(dirname "$0")/../aether"
TMPDIR="${TMPDIR:-/tmp}"
WAV="$TMPDIR/aether-seed-$$.wav"
trap 'rm -f "$WAV" "$TMPDIR/aether-seed-$$.txt"' EXIT

notify() {
    if command -v notify-send >/dev/null 2>&1; then
        notify-send -t 2000 "aether seed" "$1" 2>/dev/null || true
    fi
    printf '%s\n' "$1" >&2
}

# record
if command -v arecord >/dev/null 2>&1; then
    notify "listening ${SECS}s…"
    arecord -q -f S16_LE -r 16000 -c 1 -d "$SECS" "$WAV" || {
        notify "mic record failed"; exit 1
    }
elif command -v ffmpeg >/dev/null 2>&1; then
    notify "listening ${SECS}s (ffmpeg)…"
    ffmpeg -hide_banner -loglevel error -f pulse -i default -t "$SECS" -ac 1 -ar 16000 "$WAV" || {
        notify "mic record failed"; exit 1
    }
else
    notify "need arecord or ffmpeg for mic capture"
    exit 1
fi

text=""
# whisper.cpp family
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

# openai-whisper CLI
if [ -z "$text" ] && command -v whisper >/dev/null 2>&1; then
    text="$(whisper "$WAV" --model tiny.en --language en --output_format txt --output_dir "$TMPDIR" 2>/dev/null \
        | tail -1 || true)"
    base="$(basename "$WAV" .wav)"
    [ -f "$TMPDIR/$base.txt" ] && text="$(tr '\n' ' ' < "$TMPDIR/$base.txt")"
    rm -f "$TMPDIR/$base.txt"
fi

# trim
text="$(printf '%s' "$text" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
if [ -z "$text" ]; then
    notify "no transcript (install whisper.cpp or whisper; seed path still ready)"
    exit 2
fi

"$AETHER" seed "$text"
notify "planted: $text"
