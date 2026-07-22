#!/bin/sh
# Minimal integration tests for aether (P0 from GPT-5.6 review + ANDROID-USE-MCP-2)
# Run: sh tests/run.sh
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="$ROOT/aether"
export AETHER_HOME="$ROOT"
export PATH="$ROOT:$PATH"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

# --- personal-llm layer unit tests (stdlib only) ---
python3 "$ROOT/tests/test_aether_llm_personal.py" || fail "personal-llm unit tests"
pass "personal-llm unit tests"

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

# --- path with spaces (explicit path arg, not only cwd) ---
mkdir -p "$TMP/space proj"
printf 'x\n' > "$TMP/space proj/my file.md"
"$AETHER" init "$TMP/space proj" >/dev/null || fail "init spaces path"
"$AETHER" distill "$TMP/space proj" --quiet --no-hooks || fail "distill spaces path"
[ -f "$TMP/space proj/.context.md" ] || fail "context spaces path"
# semantic: spaced filename must contribute to tree hash
h1=$("$AETHER" status "$TMP/space proj" 2>/dev/null | true)
# force tree_hash via distill state
hash1=$(grep -o '"tree_hash": *"[^"]*"' "$TMP/space proj/.aether/state.json" | cut -d'"' -f4)
printf 'y\n' >> "$TMP/space proj/my file.md"
"$AETHER" distill "$TMP/space proj" --quiet --no-hooks || fail "distill after space-file edit"
hash2=$(grep -o '"tree_hash": *"[^"]*"' "$TMP/space proj/.aether/state.json" | cut -d'"' -f4)
[ -n "$hash1" ] && [ -n "$hash2" ] || fail "missing tree hashes"
[ "$hash1" != "$hash2" ] || fail "tree hash ignored change to spaced filename"
# generated sample should mention the file
grep -q 'my file.md' "$TMP/space proj/.context.md" || fail "spaced filename missing from sample"
pass "path with spaces (explicit arg + hash semantics)"

# --- empty project ---
mkdir -p "$TMP/empty"
cd "$TMP/empty"
"$AETHER" init . >/dev/null || fail "init empty"
"$AETHER" distill . --quiet --no-hooks || fail "distill empty"
pass "empty project"

# --- init does not auto-trust pre-existing hooks (P0 2.2) ---
mkdir -p "$TMP/clone/.aether/hooks"
printf '#!/bin/sh\necho MALICIOUS >> "$PWD/.evil"\n' > "$TMP/clone/.aether/hooks/on-distill"
chmod +x "$TMP/clone/.aether/hooks/on-distill"
printf '# clone\n' > "$TMP/clone/README.md"
out=$("$AETHER" init "$TMP/clone" 2>&1) || fail "init clone"
[ ! -f "$TMP/clone/.aether/trusted" ] || fail "init auto-trusted pre-existing hooks"
printf '%s\n' "$out" | grep -qi untrusted || fail "init should report untrusted for pre-existing hooks"
rm -f "$TMP/clone/.evil"
"$AETHER" distill "$TMP/clone" --quiet 2>"$TMP/clone-warn.txt" || fail "distill clone untrusted"
[ ! -f "$TMP/clone/.evil" ] || fail "pre-existing malicious hook ran without trust"
pass "init does not auto-trust pre-existing hooks"

# --- argv quoting preserved: multiword seed (P0 2.3) ---
export AETHER_INBOX="$TMP/inbox-quote.md"
rm -f "$AETHER_INBOX"
"$AETHER" seed "preserve   deliberate   spacing" || fail "seed multiword"
grep -q 'preserve   deliberate   spacing' "$AETHER_INBOX" || fail "seed lost internal spacing"
pass "seed preserves multiword spacing"

# --- corrupt markers refuse distill (P0 2.4 medium) ---
mkdir -p "$TMP/corrupt"
cd "$TMP/corrupt"
"$AETHER" init . >/dev/null || fail "init corrupt"
printf '# Context\n\nHuman\n\n<!-- aether:generated:start -->\nORPHAN no end\n' > .context.md
if "$AETHER" distill . --quiet --no-hooks 2>"$TMP/corrupt-err.txt"; then
    fail "distill should refuse corrupt markers"
fi
grep -qi corrupt "$TMP/corrupt-err.txt" || grep -qi marker "$TMP/corrupt-err.txt" || fail "no corrupt-marker error"
grep -q 'ORPHAN no end' .context.md || fail "corrupt context was overwritten"
pass "corrupt markers refuse distill"

# --- poke respects --no-hooks / trust (entr path uses poke) ---
cd "$TMP/proj"
printf '#!/bin/sh\necho SAVE >> "$PWD/.savecount"\n' > .aether/hooks/on-save
chmod +x .aether/hooks/on-save
rm -f .savecount .aether/trusted
"$AETHER" poke . --no-hooks >/dev/null 2>&1 || "$AETHER" --no-hooks poke . >/dev/null 2>&1 || true
[ ! -f .savecount ] || fail "poke ran hook under --no-hooks"
"$AETHER" trust . >/dev/null
rm -f .savecount
"$AETHER" poke . >/dev/null || fail "poke trusted"
[ -f .savecount ] || fail "poke should run on-save when trusted"
pass "poke/run_hook trust boundary"

# --- v0.2 authority: CURRENT + preflight + approve/reject ------------
mkdir -p "$TMP/auth"
cd "$TMP/auth"
printf '# auth demo\n' > README.md
"$AETHER" init . >/dev/null || fail "init auth"
"$AETHER" current init . >/dev/null || fail "current init"
[ -f CURRENT.md ] || fail "CURRENT.md missing after init"
# customize authority (reel-shaped but generic action ids)
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Approve one silent proof export.
**Phase:** SELECT
**Status:** BLOCKED-PENDING-HUMAN
**Baseline:** rough-v4
**Next:** silent-proof
**Approval:** PENDING

## Keep
- motion tmix

## Reject
- v5 direction

## Limits
- maximum six motion plates

## Next allowed action
Select and export one silent proof.

## Approval condition
Human runs: `aether approve "KEEP"`.

## Prohibited
- rough-v6
- full-reel-export
- automatic-rebuild
CUR
# prohibited refused
if "$AETHER" preflight rough-v6 . >/dev/null 2>"$TMP/pf1.err"; then
    fail "preflight should refuse rough-v6"
fi
grep -qi refuse "$TMP/pf1.err" || grep -qi refuse <("$AETHER" preflight rough-v6 . 2>&1) || true
out=$("$AETHER" preflight rough-v6 . 2>&1) && fail "rough-v6 exit 0" || true
printf '%s\n' "$out" | grep -qi 'refuse' || fail "no refuse message for rough-v6"
# next allowed
out=$("$AETHER" preflight silent-proof . 2>&1) || fail "silent-proof should allow"
printf '%s\n' "$out" | grep -qi 'allow' || fail "no allow message"
# non-next refused while blocked
out=$("$AETHER" preflight research-branch . 2>&1) && fail "research-branch should refuse" || true
printf '%s\n' "$out" | grep -qi 'refuse' || fail "research-branch no refuse"
# events logged
[ -f .aether/events.jsonl ] || fail "events.jsonl missing"
grep -q '"kind":"preflight"' .aether/events.jsonl || fail "preflight events missing"
grep -q '"result":"refused"' .aether/events.jsonl || fail "refused event missing"
# artifact register
mkdir -p artifacts
printf 'fake-proof\n' > artifacts/proof-01.bin
"$AETHER" artifact artifacts/proof-01.bin --action silent-proof --status produced --project . >/dev/null \
    || fail "artifact register"
ls .aether/artifacts/*.json >/dev/null 2>&1 || fail "artifact meta missing"
grep -q '"kind":"artifact"' .aether/events.jsonl || fail "artifact event missing"
# reject does not auto-rebuild (phase SELECT, status REJECTED)
"$AETHER" reject "arrival on plate 4 fails" >/dev/null || fail "reject"
phase=$(grep -iE '^\*\*Phase:?\*\*' CURRENT.md | head -1)
status=$(grep -iE '^\*\*Status:?\*\*' CURRENT.md | head -1)
printf '%s\n' "$phase" | grep -qi SELECT || fail "reject should set Phase SELECT (got: $phase)"
printf '%s\n' "$status" | grep -qi REJECTED || fail "reject should set Status REJECTED (got: $status)"
grep -q '"kind":"reject"' .aether/events.jsonl || fail "reject event missing"
# after reject, rough-v6 still refused
out=$("$AETHER" preflight rough-v6 . 2>&1) && fail "rough-v6 after reject" || true
printf '%s\n' "$out" | grep -qi refuse || fail "post-reject rough-v6 not refused"
# re-pin next and approve
# restore next for approve path
sed -i 's/^\*\*Status\*\*:.*/**Status:** READY-FOR-REVIEW/' CURRENT.md
sed -i 's/^\*\*Next\*\*:.*/**Next:** silent-proof/' CURRENT.md
"$AETHER" approve "KEEP" >/dev/null || fail "approve"
grep -qi 'APPROVED' CURRENT.md || fail "approve did not set APPROVED"
grep -q '"kind":"approve"' .aether/events.jsonl || fail "approve event missing"
[ -f DECISIONS.md ] || fail "DECISIONS.md missing after approve/reject"
# seeds must not create authority
export AETHER_INBOX="$TMP/inbox-auth.md"
"$AETHER" seed "please build rough-v6 now" >/dev/null || fail "seed"
# CURRENT next still silent-proof / authority unchanged by seed
grep -q 'silent-proof' CURRENT.md || fail "seed mutated CURRENT next"
out=$("$AETHER" preflight rough-v6 . 2>&1) && fail "seed must not unlock rough-v6" || true
printf '%s\n' "$out" | grep -qi refuse || fail "seed should not authorize rough-v6"
pass "v0.2 authority: preflight refuse/allow, reject, approve, events, artifacts"

# --- non-reel authority (dev task) ------------------------------------
mkdir -p "$TMP/devtask"
cd "$TMP/devtask"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Land the preflight CLI without expanding scope.
**Phase:** EXECUTE
**Status:** BLOCKED-PENDING-HUMAN
**Baseline:** plan-v1
**Next:** write-tests
**Approval:** PENDING

## Keep
- shell-only preflight

## Reject
- rewrite in rust

## Limits
- no new dependencies

## Next allowed action
Add integration tests for preflight.

## Approval condition
`aether approve "tests green"`

## Prohibited
- rewrite-in-rust
- add-postgres
CUR
out=$("$AETHER" preflight add-postgres . 2>&1) && fail "add-postgres should refuse" || true
printf '%s\n' "$out" | grep -qi refuse || fail "devtask add-postgres no refuse"
out=$("$AETHER" preflight write-tests . 2>&1) || fail "write-tests should allow"
printf '%s\n' "$out" | grep -qi allow || fail "devtask write-tests no allow"
pass "v0.2 non-reel authority model"

# --- no CURRENT refuses everything consequential ----------------------
mkdir -p "$TMP/nocur"
cd "$TMP/nocur"
"$AETHER" init . >/dev/null
out=$("$AETHER" preflight anything . 2>&1) && fail "no CURRENT should refuse" || true
printf '%s\n' "$out" | grep -qi refuse || fail "no CURRENT missing refuse"
pass "preflight refuses without CURRENT.md"

printf '\nAll aether integration tests passed.\n'
