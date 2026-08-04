#!/bin/sh
# grok-aether-brief.sh — advisory Mechanicall context for Grok Build hooks.
# Non-blocking. Never edits CURRENT. Never exits non-zero for "drift".
#
# Usage:
#   SessionStart:    stdout may be ignored; we print brief to stderr + optional file.
#   UserPromptSubmit: print JSON additionalContext so the model sees live Next.
#
# Env:
#   AETHER_HOME     — mechanicall-os tree containing ./aether
#   MECHANICALL_PROJECT / cwd — Domain root with CURRENT.md
#   AETHER_BRIEF_MODE — session|prompt (default: auto from stdin hookEventName)

set -eu

resolve_aether() {
    if [ -n "${AETHER_BIN:-}" ] && [ -x "$AETHER_BIN" ]; then
        printf '%s\n' "$AETHER_BIN"
        return 0
    fi
    if [ -n "${AETHER_HOME:-}" ] && [ -x "$AETHER_HOME/aether" ]; then
        printf '%s\n' "$AETHER_HOME/aether"
        return 0
    fi
    # Script lives in mechanicall-os/scripts/
    here="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
    if [ -x "$here/aether" ]; then
        printf '%s\n' "$here/aether"
        return 0
    fi
    if command -v aether >/dev/null 2>&1; then
        command -v aether
        return 0
    fi
    return 1
}

# Domain project: prefer MECHANICALL_PROJECT, else cwd if CURRENT.md, else AETHER_HOME
resolve_project() {
    if [ -n "${MECHANICALL_PROJECT:-}" ] && [ -d "$MECHANICALL_PROJECT" ]; then
        printf '%s\n' "$MECHANICALL_PROJECT"
        return 0
    fi
    if [ -f "$(pwd)/CURRENT.md" ]; then
        pwd -P
        return 0
    fi
    if [ -n "${AETHER_HOME:-}" ] && [ -f "$AETHER_HOME/CURRENT.md" ]; then
        printf '%s\n' "$AETHER_HOME"
        return 0
    fi
    pwd -P
}

# Read hook stdin (JSON); may be empty
INPUT="$(cat 2>/dev/null || true)"
EVENT=""
if [ -n "$INPUT" ]; then
    EVENT="$(printf '%s' "$INPUT" | python3 -c '
import sys, json
try:
    d=json.load(sys.stdin)
    print(d.get("hookEventName") or d.get("hook_event_name") or "")
except Exception:
    print("")
' 2>/dev/null || true)"
fi

MODE="${AETHER_BRIEF_MODE:-}"
if [ -z "$MODE" ]; then
    case "$EVENT" in
        *prompt*|*Prompt*|*user_prompt*) MODE=prompt ;;
        *session*|*Session*|"") MODE=session ;;
        *) MODE=session ;;
    esac
fi

AETHER="$(resolve_aether 2>/dev/null || true)"
PROJ="$(resolve_project)"

if [ -z "$AETHER" ]; then
    MSG="[aether] not found — set AETHER_HOME or install aether on PATH. Protocol not auto-bound in this TUI."
    printf '%s\n' "$MSG" >&2
    if [ "$MODE" = "prompt" ]; then
        python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":sys.argv[1]}}))' "$MSG"
    fi
    exit 0
fi

export AETHER_HOME="${AETHER_HOME:-$(CDPATH= cd -- "$(dirname "$AETHER")" && pwd)}"
BRIEF="$("$AETHER" brief "$PROJ" 2>&1)" || BRIEF="[aether brief failed for $PROJ]"

# Always advisory on stderr (operator scrollback)
printf '%s\n' "$BRIEF" >&2

# Optional log (project-local, gitignored often via .aether)
logdir="$PROJ/.aether"
if mkdir -p "$logdir" 2>/dev/null; then
    printf '%s\n' "$BRIEF" > "$logdir/last-grok-brief.txt" 2>/dev/null || true
fi

if [ "$MODE" = "prompt" ]; then
    # Inject into model context (non-blocking)
    CTX=$(printf '%s\n\n%s\n' \
        "Mechanicall protocol (advisory — Grok does not auto-preflight; human is the gate)." \
        "$BRIEF")
    python3 -c '
import json, sys
ctx = sys.stdin.read()
# keep under a safe size
if len(ctx) > 6000:
    ctx = ctx[:6000] + "\n…[truncated]"
out = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": ctx,
    }
}
print(json.dumps(out))
' <<EOF
$CTX
EOF
fi

exit 0
