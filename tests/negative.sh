#!/bin/sh
# Negative-path tests for aether (Opus peer NEXT-02 / next-02-negative-tests).
# Asserts unknown verbs and authority near-misses do not look like success.
# Run: sh tests/negative.sh
# Or via: sh tests/run.sh
set -e

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="${AETHER:-$ROOT/aether}"
export AETHER_HOME="${AETHER_HOME:-$ROOT}"
export PATH="$ROOT:$PATH"

fail() { printf 'FAIL negative: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

assert_unknown() {
    verb="$1"
    set +e
    out=$("$AETHER" "$verb" 2>&1)
    ec=$?
    set -e
    [ "$ec" = "2" ] || fail "verb '$verb' exit=$ec want 2"
    printf '%s\n' "$out" | grep -qi 'unknown command' \
        || fail "verb '$verb' missing 'unknown command' message"
    # Must not look like a successful authority/status report
    printf '%s\n' "$out" | grep -qiE 'CURRENT\.md \(authority\)|Phase:|preflight\(' \
        && fail "verb '$verb' printed status/authority-shaped success output" || true
    printf '%s\n' "$out" | grep -qi 'Allowed:' \
        && fail "verb '$verb' printed Allowed: (must not look like preflight)" || true
}

# --- garbage verbs ---
for bad in nexr xyzzy notacommand ''; do
    # empty first arg is awkward; skip empty
    [ -n "$bad" ] || continue
    assert_unknown "$bad"
done
pass "garbage verbs exit 2"

# --- single-char mutations of authority verbs (Opus NEXT-02) ---
# Each should be unknown (exit 2), not silently status.
auth_verbs="preflight approve reject next current probe demo brief drift"
for v in $auth_verbs; do
    # drop first char
    mut=$(printf '%s' "$v" | cut -c2-)
    [ -n "$mut" ] && [ "$mut" != "$v" ] && assert_unknown "$mut"
    # swap first two letters when length >= 2
    a=$(printf '%s' "$v" | cut -c1)
    b=$(printf '%s' "$v" | cut -c2)
    rest=$(printf '%s' "$v" | cut -c3-)
    if [ -n "$b" ]; then
        assert_unknown "${b}${a}${rest}"
    fi
done
# explicit near-misses from peer review / next-01
for bad in preflght aprove distil nexxt preflghtt; do
    assert_unknown "$bad"
done
pass "authority near-miss verbs exit 2"

# --- missing required args (die → exit 1) ---
assert_usage() {
    label="$1"
    shift
    set +e
    out=$("$@" 2>&1)
    ec=$?
    set -e
    [ "$ec" = "2" ] || fail "$label exit=$ec want 2 (usage)"
    # should not print Allowed: as if preflight succeeded
    printf '%s\n' "$out" | grep -qi '^Allowed:' \
        && fail "$label printed Allowed:" || true
}

assert_usage "preflight no-args" "$AETHER" preflight
assert_usage "next no-args" "$AETHER" next
assert_usage "probe no-args" "$AETHER" probe
assert_usage "event no-args" "$AETHER" event
pass "missing required args exit 2 (usage)"

# --- project with no CURRENT: consequential preflight refuses ---
TMPN="${TMPDIR:-/tmp}/aether-negative.$$"
mkdir -p "$TMPN/empty"
trap 'rm -rf "$TMPN"' EXIT INT HUP
cd "$TMPN/empty"
# no init / no CURRENT
set +e
out=$("$AETHER" preflight anything . 2>&1)
ec=$?
set -e
[ "$ec" = "3" ] || fail "preflight without CURRENT exit=$ec want 3"
printf '%s\n' "$out" | grep -qi refuse \
    || fail "preflight without CURRENT missing refuse message"
pass "preflight without CURRENT refuses (exit 3)"

# --- path-as-cmd still works (regression for next-01) ---
mkdir -p "$TMPN/pathcmd"
set +e
out=$("$AETHER" "$TMPN/pathcmd" 2>&1)
ec=$?
set -e
[ "$ec" = "0" ] || fail "path-as-cmd exit=$ec"
printf '%s\n' "$out" | grep -q 'root:' || fail "path-as-cmd missing root line"
pass "path-as-cmd status still works"

# --- known verbs still dispatch (not falsely unknown) ---
set +e
out=$("$AETHER" help 2>&1)
ec=$?
set -e
[ "$ec" = "0" ] || fail "help exit=$ec"
printf '%s\n' "$out" | grep -qi 'aether' || fail "help missing aether banner"
pass "help still works"

printf 'ok: negative path suite (next-02)\n'
