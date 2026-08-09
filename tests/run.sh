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

# Snapshot source checkout so tests cannot silently rewrite live authority
# (GPT-5.6 10_ + second PR review: porcelain alone is insufficient).
SRC_PORCELAIN=""
src_authority_snap() {
  # prints hash lines for authority-relevant root files (tracked or not)
  for f in \
    "$ROOT/CURRENT.md" \
    "$ROOT/DECISIONS.md" \
    "$ROOT/.aether/events.jsonl" \
    "$ROOT/.aether/preflight-last" \
    "$ROOT/.aether/preflight.jsonl"
  do
    if [ -f "$f" ]; then
      cksum "$f" 2>/dev/null || true
    else
      printf 'MISSING %s\n' "$f"
    fi
  done
}
SRC_AUTH_SNAP=$(src_authority_snap)
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  SRC_PORCELAIN=$(git -C "$ROOT" status --porcelain 2>/dev/null || true)
fi

TMP="${TMPDIR:-/tmp}/aether-test.$$"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT INT HUP

# --- version + verb list (Opus next-09) ---
# Dispatch checks run only inside a disposable project — never against $ROOT.
ver_out=$("$AETHER" --version 2>&1) || fail "aether --version failed"
printf '%s\n' "$ver_out" | grep -qE '^aether [0-9]' || fail "version format: $ver_out"
ver2=$("$AETHER" version 2>&1) || fail "aether version failed"
[ "$ver_out" = "$ver2" ] || fail "version vs --version mismatch"
verbs=$("$AETHER" verbs 2>&1) || fail "aether verbs failed"
help_out=$("$AETHER" help 2>&1) || fail "help failed"
printf '%s\n' "$help_out" | grep -q 'AETHER_VERBS' || fail "help missing AETHER_VERBS line"
printf '%s\n' "$help_out" | grep -q 'preflight' || fail "help missing preflight"
# Each verb name must appear in help and must not be "unknown command" when
# invoked in a temp project. Never run approve/reject/deinit/next against the
# real checkout (those mutate CURRENT / events).
mkdir -p "$TMP/dispatch"
cd "$TMP/dispatch"
"$AETHER" init . >/dev/null || fail "dispatch sandbox init"
for v in $verbs; do
    printf '%s\n' "$help_out" | grep -qw "$v" \
        || fail "verb '$v' missing from help text"
    case "$v" in
        # Never invoke interactive / long-running / mutating verbs bare.
        # Help-only coverage is enough for dispatch (second PR review).
        approve|reject|next|preflight|probe|artifact|event|seed|rival|\
        shell|panel|watch|onboard|garden|try|demo|deinit|app)
            printf '%s\n' "$help_out" | grep -qw "$v" \
                || fail "verb '$v' missing from help (safe list)"
            ;;
        *)
            set +e
            out=$("$AETHER" "$v" 2>&1)
            ec=$?
            set -e
            printf '%s\n' "$out" | grep -qi 'unknown command' \
                && fail "verb '$v' reported unknown command" || true
            ;;
    esac
done
cd "$ROOT"
pass "version + verb list (next-09, sandboxed)"

# --- shellcheck (Opus next-07 / 🟠-4) — fatal when shellcheck is installed ---
# Install: nix-env -iA nixpkgs.shellcheck  |  apt install shellcheck
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck -s sh -S warning "$AETHER" || fail "shellcheck -s sh aether"
  pass "shellcheck aether (POSIX sh)"
else
  fail "shellcheck not found on PATH (required for next-07 gate). Install shellcheck and re-run."
fi

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

# --- preflight receipt (next-06 / Opus) ---
mkdir -p "$TMP/pfr"
cd "$TMP/pfr"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** receipt test
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** do-thing
**Approval:** PENDING

## Keep
- x

## Reject
- y

## Limits
- z

## Next allowed action
do-thing

## Approval condition
human

## Prohibited
- automatic-approve
CUR
# ABSENT before any preflight
out=$("$AETHER" approve "absent-check" . 2>&1) || fail "approve ABSENT path failed"
printf '%s\n' "$out" | grep -q 'preflight: ABSENT' || fail "want preflight: ABSENT: $out"
# reset fields for next approve
sed -i 's/\*\*Status:\*\*.*/**Status:** ACTIVE/' CURRENT.md 2>/dev/null || true
# portable reset via aether fields — use current_set through re-write
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** receipt test
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** do-thing
**Approval:** PENDING

## Keep
- x

## Reject
- y

## Limits
- z

## Next allowed action
do-thing

## Approval condition
human

## Prohibited
- automatic-approve
CUR
"$AETHER" preflight do-thing . >/dev/null || fail "preflight allow for receipt"
[ -f .aether/preflight-last ] || fail "preflight-last missing"
grep -q 'result=allowed' .aether/preflight-last || fail "receipt not allowed"
out=$("$AETHER" approve "pass-check" . 2>&1) || fail "approve PASS failed"
printf '%s\n' "$out" | grep -q 'preflight: PASS' || fail "want preflight: PASS: $out"
# STALE: change tree after preflight
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** receipt test
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** do-thing
**Approval:** PENDING

## Keep
- x

## Reject
- y

## Limits
- z

## Next allowed action
do-thing

## Approval condition
human

## Prohibited
- automatic-approve
CUR
"$AETHER" preflight do-thing . >/dev/null || fail "preflight before stale"
printf 'stale-touch\n' > extra-file.txt
out=$("$AETHER" approve "stale-check" . 2>&1) || fail "approve STALE path failed"
printf '%s\n' "$out" | grep -q 'preflight: STALE' || fail "want preflight: STALE: $out"
# approve must still succeed (non-blocking)
printf '%s\n' "$out" | grep -q 'APPROVED' || fail "STALE must not block approve"
pass "preflight receipt PASS/STALE/ABSENT"

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
[ "$ec" = "3" ] || fail "next before approve exit=$ec want 3"
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
[ "$ec" = "3" ] || fail "next unchanged exit=$ec want 3"
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
[ "$ec" = "3" ] || fail "probe refuse exit=$ec want 3"
"$AETHER" brief . >/dev/null || fail "brief"
pass "aether probe + brief"

# --- negative paths (Opus NEXT-02 / next-02-negative-tests) ---
# Dedicated suite: unknown verbs, authority near-misses, missing args, no CURRENT.
sh "$ROOT/tests/negative.sh" || fail "tests/negative.sh"
pass "negative path suite (tests/negative.sh)"

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

# --- probe/brief are non-mutating (GPT-5.6 10_ review) ---
mkdir -p "$TMP/probe-dry"
cd "$TMP/probe-dry"
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** probe dry
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** write-tests
**Approval:** PENDING

## Prohibited
- deploy-production
CUR
: > .aether/events.jsonl
rm -f .aether/preflight-last .aether/preflight.jsonl
"$AETHER" probe write-tests . >/dev/null || fail "probe allow"
"$AETHER" probe deploy-production . >/dev/null 2>&1 || true
# expect refuse exit 3
set +e
"$AETHER" probe deploy-production .
pec=$?
set -e
[ "$pec" = "3" ] || fail "probe refuse exit want 3 got $pec"
[ ! -s .aether/events.jsonl ] || fail "probe wrote events"
[ ! -f .aether/preflight-last ] || fail "probe wrote preflight-last"
"$AETHER" brief . >/dev/null || fail "brief"
[ ! -s .aether/events.jsonl ] || fail "brief wrote events"
[ ! -f .aether/preflight-last ] || fail "brief wrote preflight-last"
# real preflight still writes
"$AETHER" preflight write-tests . >/dev/null || fail "preflight allow"
[ -s .aether/events.jsonl ] || fail "preflight should write events"
pass "probe/brief non-mutating; preflight still records"

# --- artifact --project DIR from other cwd (second PR review bug #1) ---
mkdir -p "$TMP/art-proj" "$TMP/art-cwd"
cd "$TMP/art-proj"
"$AETHER" init . >/dev/null
printf 'blob\n' > proof.txt
cd "$TMP/art-cwd"
"$AETHER" artifact "$TMP/art-proj/proof.txt" --project "$TMP/art-proj" --action proof --status produced \
  >/dev/null || fail "artifact --project from other cwd"
ls "$TMP/art-proj/.aether/artifacts/"*.json >/dev/null 2>&1 \
  || fail "artifact meta not under --project root"
[ ! -d "$TMP/art-cwd/.aether" ] || fail "artifact leaked into cwd project"
pass "artifact --project DIR from foreign cwd"

# --- git dirty STALE: further edits while dirty must change fp (second PR review bug #2) ---
mkdir -p "$TMP/git-stale"
cd "$TMP/git-stale"
git init -q
git config user.email "test@example.com"
git config user.name "test"
printf '# t\n' > README.md
git add README.md
git commit -q -m init
"$AETHER" init . >/dev/null
"$AETHER" current init . >/dev/null
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** stale git
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** t
**Next:** write-tests
**Approval:** PENDING

## Prohibited
- deploy-production
CUR
printf 'x\n' >> README.md
"$AETHER" preflight write-tests . >/dev/null || fail "preflight dirty1"
fp1=$(grep '^ts=' .aether/preflight-last | sed 's/.*|fp=//')
printf 'y\n' >> README.md
"$AETHER" preflight write-tests . >/dev/null || fail "preflight dirty2"
fp2=$(grep '^ts=' .aether/preflight-last | sed 's/.*|fp=//')
[ -n "$fp1" ] && [ -n "$fp2" ] || fail "missing fps"
[ "$fp1" != "$fp2" ] || fail "authority_fp unchanged after further dirty edit ($fp1)"
# receipt status should not stay PASS after mutate-without-new-preflight wait:
# print_preflight_receipt_status compares live fp to last — force re-read via approve trace
printf 'z\n' >> README.md
out=$("$AETHER" approve "check-stale" . 2>&1) || true
printf '%s\n' "$out" | grep -qi 'STALE\|preflight:' || true
# stronger: call internal path via second preflight would update; check print by comparing
# live fp vs stored without re-preflight — use probe/approve output
printf '%s\n' "$out" | grep -qi STALE || fail "expected STALE after dirty edit without new preflight: $out"
pass "git dirty authority_fp content-sensitive + STALE"

# --- source checkout unchanged by the suite (porcelain + authority hashes) ---
AFTER_AUTH_SNAP=$(src_authority_snap)
if [ "$SRC_AUTH_SNAP" != "$AFTER_AUTH_SNAP" ]; then
  printf 'FAIL: tests mutated root authority files (second PR review)\n' >&2
  printf 'before:\n%s\n--- after:\n%s\n' "$SRC_AUTH_SNAP" "$AFTER_AUTH_SNAP" >&2
  exit 1
fi
pass "source authority file hashes unchanged"
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  AFTER_PORCELAIN=$(git -C "$ROOT" status --porcelain 2>/dev/null || true)
  if [ "$SRC_PORCELAIN" != "$AFTER_PORCELAIN" ]; then
    printf 'FAIL: tests dirtied source checkout (GPT-5.6 10_ safety)\n' >&2
    printf 'before:\n%s\n--- after:\n%s\n' "$SRC_PORCELAIN" "$AFTER_PORCELAIN" >&2
    exit 1
  fi
  pass "source checkout porcelain unchanged"
fi

printf '\nAll aether integration tests passed.\n'
