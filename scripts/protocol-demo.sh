#!/bin/sh
# protocol-demo.sh — one-command refuse → allow → approve → re-SELECT → ledger
# Never mutates the caller's live CURRENT; uses AETHER_DEMO_ROOT or mktemp.
# Usage: sh scripts/protocol-demo.sh [--quiet]
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="${AETHER:-$ROOT/aether}"
export AETHER_HOME="$ROOT"
QUIET=0
for a in "$@"; do
    case "$a" in
        --quiet|-q) QUIET=1 ;;
    esac
done

log() {
    if [ "$QUIET" = "0" ]; then
        printf '%s\n' "$*"
    fi
}

die() {
    printf 'DEMO FAIL: %s\n' "$*" >&2
    exit 1
}

WORK="${AETHER_DEMO_ROOT:-}"
CLEANUP=0
if [ -z "$WORK" ]; then
    WORK="$(mktemp -d "${TMPDIR:-/tmp}/aether-protocol-demo.XXXXXX")"
    CLEANUP=1
fi
if [ "$CLEANUP" = "1" ]; then
    trap 'rm -rf "$WORK"' EXIT INT HUP
fi

mkdir -p "$WORK"
cd "$WORK"

log "STEP 0/6 seed sandbox at $WORK"
"$AETHER" init . >/dev/null 2>&1 || true
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Protocol demo sandbox — refuse then allow then approve then re-SELECT.
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** protocol-demo
**Next:** demo-one
**Approval:** PENDING

## Keep
- one next

## Reject
- dual next

## Limits
- temp root only

## Next allowed action
demo-one only.

## Approval condition
Human approve in demo script.

## Prohibited
- automatic-approve
- demo-forbidden
CUR

log "STEP 1/6 REFUSE — preflight outside Next"
set +e
out1="$("$AETHER" preflight demo-forbidden . 2>&1)"
ec1=$?
set -e
log "$out1"
[ "$ec1" -ne 0 ] || die "expected refuse for demo-forbidden"
printf '%s\n' "$out1" | grep -qi refuse || die "no REFUSE text"
log "STEP 1/6 REFUSE ok"

log "STEP 2/6 ALLOW — preflight Next"
set +e
out2="$("$AETHER" preflight demo-one . 2>&1)"
ec2=$?
set -e
log "$out2"
[ "$ec2" -eq 0 ] || die "expected allow for demo-one"
printf '%s\n' "$out2" | grep -qi allow || die "no ALLOW text"
log "STEP 2/6 ALLOW ok"

log "STEP 3/6 NO SILENT PASS — model-as-approver is prohibited (do not run approve without human)"
# Protocol literacy: we do not invoke approve until step 4 with explicit human-labelled reason.
# A silent no-op would be wrong; we assert Approval still PENDING.
grep -qi 'PENDING' CURRENT.md || die "Approval not PENDING before human approve"
log "STEP 3/6 NO SILENT PASS ok (Approval still PENDING)"

log "STEP 4/6 APPROVE — human-labelled"
set +e
out4="$("$AETHER" approve "DEMO-HUMAN-YES" . 2>&1)"
ec4=$?
set -e
log "$out4"
[ "$ec4" -eq 0 ] || die "approve failed"
grep -qi 'APPROVED' CURRENT.md || die "APPROVED not set"
log "STEP 4/6 APPROVED ok"

log "STEP 5/6 RE-SELECT — aether next"
set +e
out5="$("$AETHER" next demo-two . 2>&1)"
ec5=$?
set -e
log "$out5"
[ "$ec5" -eq 0 ] || die "next failed"
grep -q 'demo-two' CURRENT.md || die "Next not demo-two"
printf '%s\n' "$out5" | grep -q 'NEXT_SELECTED' || die "no NEXT_SELECTED"
log "STEP 5/6 RE-SELECT ok"

log "STEP 6/6 LEDGER"
if [ -f .aether/events.jsonl ]; then
    log "--- events tail ---"
    if [ "$QUIET" = "0" ]; then
        tail -n 8 .aether/events.jsonl
    fi
    grep -q '"kind":"preflight"' .aether/events.jsonl || die "missing preflight events"
    grep -q '"kind":"approve"' .aether/events.jsonl || die "missing approve event"
    grep -q '"kind":"next_selected"' .aether/events.jsonl || die "missing next_selected event"
else
    die "events.jsonl missing"
fi
log "STEP 6/6 LEDGER ok"

printf 'DEMO OK\n'
exit 0
