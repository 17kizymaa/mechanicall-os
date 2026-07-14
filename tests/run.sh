#!/bin/sh
# Minimal integration tests for aether (P0 from GPT-5.6 review 2026-07-14)
# Run: sh tests/run.sh
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="$ROOT/aether"
export AETHER_HOME="$ROOT"
export PATH="$ROOT:$PATH"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

TMP="${TMPDIR:-/tmp}/aether-test.$$"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT INT HUP

# --- init ---
mkdir -p "$TMP/proj"
cd "$TMP/proj"
printf '# hello\n' > README.md
"$AETHER" init . >/dev/null || fail "init"
[ -f .context.md ] || fail "context after init"
[ -f .aether/trusted ] || fail "trusted after init"
[ -f .aether/.scope ] || fail "scope after init"
pass "init"

# --- idempotent init ---
"$AETHER" init . >/dev/null || fail "re-init"
pass "init idempotent"

# --- human context preserved ---
printf '# Context — proj\n\nKEEP_ME_HUMAN_NOTE\n\n' > .context.md
# force markers-less legacy then distill
"$AETHER" distill . --quiet --no-hooks || fail "distill"
grep -q 'KEEP_ME_HUMAN_NOTE' .context.md || fail "human note lost"
grep -q 'aether:generated:start' .context.md || fail "missing generated markers"
pass "human context preserved"

# edit human section only, distill again
# insert note before generated
awk '
  /aether:generated:start/ && !done { print "SECOND_HUMAN_LINE"; done=1 }
  { print }
' .context.md > .context.md.new && mv .context.md.new .context.md
"$AETHER" distill . --quiet --no-hooks || fail "distill2"
grep -q 'KEEP_ME_HUMAN_NOTE' .context.md || fail "human lost on 2nd distill"
grep -q 'SECOND_HUMAN_LINE' .context.md || fail "second human line lost"
pass "human survives repeated distill"

# --- hooks once ---
printf '#!/bin/sh\necho HOOK_FIRE >> "$PWD/.hookcount"\n' > .aether/hooks/on-distill
chmod +x .aether/hooks/on-distill
rm -f .hookcount
# trusted already from init
"$AETHER" distill . --quiet || fail "distill hooks"
count=$(wc -l < .hookcount | tr -d ' ')
[ "$count" = "1" ] || fail "hook ran $count times (want 1)"
pass "hooks run exactly once"

# --- --no-hooks ---
rm -f .hookcount
"$AETHER" distill . --quiet --no-hooks || fail "distill no-hooks"
[ ! -f .hookcount ] || fail "hooks ran despite --no-hooks"
pass "--no-hooks"

# --- untrusted skips hooks ---
rm -f .aether/trusted .hookcount
"$AETHER" distill . --quiet 2>"$TMP/warn.txt" || fail "distill untrusted"
[ ! -f .hookcount ] || fail "untrusted hooks ran"
grep -qi untrusted "$TMP/warn.txt" || grep -qi skip "$TMP/warn.txt" || fail "no untrusted warning"
pass "untrusted hooks skipped"

# --- trust ---
"$AETHER" trust . >/dev/null || fail "trust"
[ -f .aether/trusted ] || fail "trusted file"
pass "trust"

# --- path with spaces ---
mkdir -p "$TMP/space proj"
cd "$TMP/space proj"
printf 'x\n' > "my file.md"
"$AETHER" init . >/dev/null || fail "init spaces"
"$AETHER" distill . --quiet --no-hooks || fail "distill spaces"
[ -f .context.md ] || fail "context spaces"
pass "path with spaces (project dir)"

# --- empty project ---
mkdir -p "$TMP/empty"
cd "$TMP/empty"
"$AETHER" init . >/dev/null || fail "init empty"
"$AETHER" distill . --quiet --no-hooks || fail "distill empty"
pass "empty project"

printf '\nAll aether integration tests passed.\n'
