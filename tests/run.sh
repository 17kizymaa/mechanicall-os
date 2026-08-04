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

# --- control-layer unit tests ---
if python3 -c "import pytest" 2>/dev/null; then
  python3 -m pytest -q \
    "$ROOT/tests/test_aether_llm_personal.py" \
    "$ROOT/tests/test_aether_panel.py" \
    "$ROOT/tests/test_aether_shell.py" \
    "$ROOT/tests/test_aether_shell_agent.py" \
    "$ROOT/tests/test_aether_llm_presets.py" \
    "$ROOT/tests/test_aether_llm_grok_tui.py" \
    || fail "control-layer unit tests"
  pass "control-layer unit tests (pytest)"
else
  python3 "$ROOT/tests/test_aether_llm_personal.py" || fail "personal-llm unit tests"
  python3 "$ROOT/tests/test_aether_panel.py" || fail "panel unit tests"
  pass "unit tests (pytest missing; shell agent tests skipped — install pytest)"
fi

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
grep -qi refuse "$TMP/pf1.err" || true
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

# --- current validate + next (re-SELECT after APPROVED) ---------------
mkdir -p "$TMP/nextcycle"
cd "$TMP/nextcycle"
"$AETHER" init . >/dev/null || fail "init nextcycle"
"$AETHER" current init . >/dev/null || fail "current init nextcycle"
# good file after filling fields
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Cycle Next after approve.
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** wave0
**Next:** demo-one
**Approval:** PENDING

## Keep
- one next

## Reject
- dual next

## Limits
- sandbox only

## Next allowed action
Run demo-one.

## Approval condition
Human approve.

## Prohibited
- automatic-approve
CUR
"$AETHER" current validate . >/dev/null || fail "validate good CURRENT"
# missing Next fails validate
cp CURRENT.md CURRENT.bak
sed -i '/^\*\*Next:\*\*/d' CURRENT.md
if "$AETHER" current validate . >/dev/null 2>&1; then fail "validate should fail missing Next"; fi
mv CURRENT.bak CURRENT.md
# next before approve must refuse (exit 2)
set +e
out=$("$AETHER" next demo-two . 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "next before approve exit=$ec want 2"
printf '%s\n' "$out" | grep -qi 'not approved' || fail "next before approve wrong message"
grep -q 'demo-one' CURRENT.md || fail "next mutated CURRENT before approve"
# approve then next
"$AETHER" approve "wave0" . >/dev/null || fail "approve for next"
"$AETHER" next demo-two . >/dev/null || fail "next after approve"
grep -q 'demo-two' CURRENT.md || fail "next did not set demo-two"
grep -qi 'PENDING' CURRENT.md || fail "next should reset Approval PENDING"
grep -qi 'SELECT' CURRENT.md || fail "next should set Phase SELECT"
grep -q '"kind":"next_selected"' .aether/events.jsonl || fail "next_selected event missing"
# unchanged next refuses
set +e
out=$("$AETHER" next demo-two . 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "next unchanged exit=$ec want 2"
printf '%s\n' "$out" | grep -qi 'unchanged' || fail "next unchanged wrong message"
"$AETHER" current validate . >/dev/null || fail "validate after next"
pass "v0.2 current validate + next re-SELECT"

# --- protocol demo + probe + brief + drift ----------------------------
cd "$ROOT"
out=$("$AETHER" demo --quiet 2>&1) || fail "aether demo failed: $out"
printf '%s\n' "$out" | grep -q 'DEMO OK' || fail "demo missing DEMO OK"
pass "aether demo"

mkdir -p "$TMP/probe"
cd "$TMP/probe"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** probe test
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** write-tests
**Approval:** PENDING

## Keep
- x

## Reject
- y

## Limits
- z

## Next allowed action
write-tests

## Approval condition
human

## Prohibited
- automatic-approve
CUR
set +e
"$AETHER" probe write-tests . >/dev/null 2>&1
ec=$?
set -e
[ "$ec" = "0" ] || fail "probe allow exit=$ec"
set +e
"$AETHER" probe automatic-approve . >/dev/null 2>&1
ec=$?
set -e
[ "$ec" = "2" ] || fail "probe refuse exit=$ec want 2"
"$AETHER" brief . >/dev/null || fail "brief"
pass "aether probe + brief"

# drift: only if git available in temp (may not be a repo)
cd "$ROOT"
set +e
"$AETHER" drift . >/dev/null 2>&1
dec=$?
set -e
# exit 0 or 1 both ok (clean or dirty working tree)
[ "$dec" = "0" ] || [ "$dec" = "1" ] || fail "drift exit=$dec"
pass "aether drift (exit 0|1)"

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

# --- first-run onboard + app register + deinit (alpha distribution) ---
mkdir -p "$TMP/onboard"
cd "$TMP/onboard"
printf '# onboard demo\n' > README.md
"$AETHER" onboard --yes . >/dev/null || fail "onboard --yes"
[ -f CURRENT.md ] || fail "onboard missing CURRENT.md"
[ -f .aether/COMMANDS.md ] || fail "onboard missing COMMANDS.md"
[ -f .aether/PANEL.md ] || fail "onboard should write PANEL.md"
[ -f .aether/panel.html ] || fail "onboard should write panel.html"
[ -f .aether/events.jsonl ] || fail "onboard missing events"
grep -q '"kind":"onboard_complete"' .aether/events.jsonl || fail "onboard_complete event missing"
grep -q 'aether panel' .aether/COMMANDS.md || fail "cheatsheet should prefer panel"
out=$("$AETHER" preflight deploy-production . 2>&1) && fail "onboard deploy-production should refuse" || true
printf '%s\n' "$out" | grep -qi refuse || fail "onboard refuse message missing"
out=$("$AETHER" preflight write-tests . 2>&1) || fail "onboard write-tests should allow"
printf '%s\n' "$out" | grep -qi allow || fail "onboard allow message missing"
pass "onboard --yes"

mkdir -p "$TMP/appreg"
cd "$TMP/appreg"
printf '# app\n' > README.md
"$AETHER" app register my-dev-app . >/dev/null || fail "app register"
[ -f .aether/app.json ] || fail "app.json missing"
grep -q 'my-dev-app' .aether/app.json || fail "app name missing"
[ -f CURRENT.md ] || fail "app register should create CURRENT when missing"
[ -f .aether/COMMANDS.md ] || fail "app register cheatsheet"
grep -q deploy-production CURRENT.md || fail "dev CURRENT missing prohibited deploy"
out=$("$AETHER" app status . 2>&1) || fail "app status"
printf '%s\n' "$out" | grep -q 'my-dev-app' || fail "app status content"
pass "app register + status"

mkdir -p "$TMP/deinit"
cd "$TMP/deinit"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
"$AETHER" deinit --yes . >/dev/null || fail "deinit"
[ ! -d .aether ] || fail "deinit left .aether"
[ -f CURRENT.md ] || fail "deinit should keep CURRENT.md by default"
"$AETHER" init . >/dev/null
"$AETHER" deinit --yes --with-current . >/dev/null || fail "deinit with-current"
[ ! -f CURRENT.md ] || fail "deinit --with-current left CURRENT.md"
pass "deinit"

# alpha demo script smoke
sh "$ROOT/scripts/alpha-demo.sh" "$TMP/alpha-demo" >/dev/null || fail "alpha-demo.sh"
[ -f "$TMP/alpha-demo/CURRENT.md" ] || fail "alpha-demo CURRENT"
grep -q '"kind":"approve"' "$TMP/alpha-demo/.aether/events.jsonl" || fail "alpha-demo approve event"
pass "alpha-demo.sh"

# --- project panel projection (non-interactive) ---
mkdir -p "$TMP/panel"
cd "$TMP/panel"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Panel test
**Phase:** EXECUTE
**Status:** READY
**Baseline:** t
**Next:** write-tests
**Approval:** PENDING

## Prohibited
- deploy-production
CUR
out=$("$AETHER" panel . --dump 2>&1) || fail "panel --dump"
printf '%s\n' "$out" | grep -q 'write-tests' || fail "panel dump missing Next"
printf '%s\n' "$out" | grep -qi 'prohibited\|deploy-production' || fail "panel dump missing prohibited"
"$AETHER" panel . --write >/dev/null || fail "panel --write"
[ -f .aether/PANEL.md ] || fail "PANEL.md missing"
[ -f .aether/panel.html ] || fail "panel.html missing"
grep -q 'write-tests' .aether/PANEL.md || fail "PANEL.md content"
# non-TTY interactive should fail closed with dump-like exit
set +e
"$AETHER" panel . </dev/null >/dev/null 2>"$TMP/panel-err.txt"
prc=$?
set -e
[ "$prc" -ne 0 ] || fail "panel interactive on non-TTY should fail"
pass "panel dump + write + non-TTY guard"

# --- control-layer seats gates (also run in CI job alone) ---
sh "$ROOT/scripts/ci-control-layer-gates.sh" || fail "ci-control-layer-gates"
pass "ci-control-layer-gates"

printf '\nAll aether integration tests passed.\n'
