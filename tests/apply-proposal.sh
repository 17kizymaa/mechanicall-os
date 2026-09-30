#!/bin/sh
# aether apply: copy a proposal's fenced CURRENT body. Never the wrapper.
# Run: sh tests/apply-proposal.sh
set -e

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="${AETHER:-$ROOT/aether}"
export AETHER_HOME="${AETHER_HOME:-$ROOT}"
export PATH="$ROOT:$PATH"

fail() { printf 'FAIL apply: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

TMP="${TMPDIR:-/tmp}/aether-apply-test.$$"
rm -rf "$TMP"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT INT HUP

body_for() {
    next="$1"
    action="${2:-$1}"
    cat <<EOF
# CURRENT

**Objective:** One halt.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** t
**Next:** ${next}
**Approval:** DRAFT

## Keep
- one

## Reject
- two

## Limits
- three

## Next allowed action
**Action id:** \`${action}\`

Do the halt.

## Approval condition
Human runs aether approve.

## Prohibited
- automatic-approve
- model-auto-write-current
EOF
}

wrap_proposal() {
    # $1 dest file, $2 next, optional $3 action (default = next)
    dest="$1"
    next="$2"
    action="${3:-$2}"
    mkdir -p "$(dirname "$dest")"
    {
        printf '%s\n' '# CURRENT proposal — switch'
        printf '%s\n' ''
        printf '%s\n' '**APPLY: human must approve then merge — model must not overwrite CURRENT without human gate**'
        printf '%s\n' ''
        printf '%s\n' 'Preamble that must not become law.'
        printf '%s\n' ''
        printf '%s\n' '## Proposed CURRENT.md'
        printf '%s\n' ''
        printf '%s\n' '```markdown'
        body_for "$next" "$action"
        printf '%s\n' '```'
    } > "$dest"
}

seed_project() {
    dir="$1"
    mkdir -p "$dir/.aether/proposals"
    (
        cd "$dir"
        "$AETHER" init . >/dev/null
        "$AETHER" current init . >/dev/null
    )
}

# --- usage ---
set +e
out=$("$AETHER" apply 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "no-args exit=$ec want 2"
printf '%s\n' "$out" | grep -q 'usage:' || fail "no-args missing usage"
pass "apply with no file exits 2"

# --- wrapper without a CURRENT fence is refused; live file stays ---
seed_project "$TMP/wrap"
cp "$TMP/wrap/CURRENT.md" "$TMP/wrap/CURRENT.before"
cat > "$TMP/wrap/bare.md" <<'EOF'
# CURRENT proposal — bare
**APPLY: human must approve then merge — model must not overwrite CURRENT without human gate**
No fence in here.
EOF
set +e
out=$("$AETHER" apply "$TMP/wrap/bare.md" "$TMP/wrap" 2>&1)
ec=$?
set -e
[ "$ec" = "3" ] || fail "bare wrapper exit=$ec want 3; out=$out"
printf '%s\n' "$out" | grep -q 'will not copy the wrapper' || fail "bare wrapper message: $out"
cmp -s "$TMP/wrap/CURRENT.md" "$TMP/wrap/CURRENT.before" || fail "bare wrapper wrote CURRENT"
pass "wrapper without a CURRENT fence is refused"

# --- fenced body lands; preamble does not; approve is not implied ---
seed_project "$TMP/ok"
wrap_proposal "$TMP/ok/.aether/proposals/one.md" "pocket-playtester"
set +e
out=$("$AETHER" apply --dry-run "$TMP/ok/.aether/proposals/one.md" 2>&1)
ec=$?
set -e
[ "$ec" = "0" ] || fail "dry-run exit=$ec; out=$out"
printf '%s\n' "$out" | grep -q 'DRY-RUN' || fail "dry-run missing DRY-RUN: $out"
grep -q 'one sentence' "$TMP/ok/CURRENT.md" || fail "dry-run wrote CURRENT"
grep -q proposal_applied "$TMP/ok/.aether/events.jsonl" && fail "dry-run wrote proposal_applied" || true

out=$("$AETHER" apply "$TMP/ok/.aether/proposals/one.md")
printf '%s\n' "$out" | grep -q 'APPLIED:' || fail "missing APPLIED: $out"
printf '%s\n' "$out" | grep -q 'Not an approval' || fail "missing not-an-approval: $out"
printf '%s\n' "$out" | grep -q 'refuses while Next is already' || fail "missing next-refuse hint: $out"
grep -q '^# CURRENT$' "$TMP/ok/CURRENT.md" || fail "title missing"
grep -q 'CURRENT proposal' "$TMP/ok/CURRENT.md" && fail "wrapper title landed in CURRENT" || true
grep -q '^APPLY:' "$TMP/ok/CURRENT.md" && fail "APPLY banner landed in CURRENT" || true
grep -q 'Preamble that must not' "$TMP/ok/CURRENT.md" && fail "preamble landed in CURRENT" || true
grep -q '^\*\*Next:\*\* pocket-playtester$' "$TMP/ok/CURRENT.md" || fail "Next not copied"
grep -q proposal_applied "$TMP/ok/.aether/events.jsonl" || fail "no proposal_applied event"
grep -q '"kind":"approve"' "$TMP/ok/.aether/events.jsonl" && fail "apply wrote an approve event" || true
[ -d "$TMP/ok/.aether/current-before" ] || fail "no backup dir"
ls "$TMP/ok/.aether/current-before"/CURRENT-*.md >/dev/null || fail "no backup file"
# backup is the previous template, not the new body
grep -q 'one sentence' "$TMP/ok/.aether/current-before"/CURRENT-*.md || fail "backup is not the previous CURRENT"

n1=$(find "$TMP/ok/.aether/current-before" -type f -name 'CURRENT-*.md' | wc -l | tr -d ' ')
out=$("$AETHER" apply "$TMP/ok/.aether/proposals/one.md")
printf '%s\n' "$out" | grep -q 'already applied' || fail "second apply: $out"
n2=$(find "$TMP/ok/.aether/current-before" -type f -name 'CURRENT-*.md' | wc -l | tr -d ' ')
[ "$n1" = "$n2" ] || fail "second apply wrote another backup ($n1 -> $n2)"
pass "fenced body applied once; preamble stayed out; no approve"

# --- header Next must match Action id ---
seed_project "$TMP/pin"
wrap_proposal "$TMP/pin/.aether/proposals/bad.md" "pocket-playtester" "other-client"
cp "$TMP/pin/CURRENT.md" "$TMP/pin/CURRENT.before"
set +e
out=$("$AETHER" apply "$TMP/pin/.aether/proposals/bad.md" 2>&1)
ec=$?
set -e
[ "$ec" = "3" ] || fail "pin mismatch exit=$ec; out=$out"
printf '%s\n' "$out" | grep -q 'does not match Action id' || fail "pin message: $out"
cmp -s "$TMP/pin/CURRENT.md" "$TMP/pin/CURRENT.before" || fail "pin mismatch wrote CURRENT"
pass "Next / Action id split is refused"

# --- Next that Prohibited would refuse does not land ---
seed_project "$TMP/ban"
wrap_proposal "$TMP/ban/.aether/proposals/ban.md" "automatic-approve"
cp "$TMP/ban/CURRENT.md" "$TMP/ban/CURRENT.before"
set +e
out=$("$AETHER" apply "$TMP/ban/.aether/proposals/ban.md" 2>&1)
ec=$?
set -e
[ "$ec" = "3" ] || fail "prohibited Next exit=$ec; out=$out"
printf '%s\n' "$out" | grep -q 'prohibited' || fail "prohibited message: $out"
cmp -s "$TMP/ban/CURRENT.md" "$TMP/ban/CURRENT.before" || fail "prohibited Next wrote CURRENT"
pass "prohibited Next is refused before write"

# --- an earlier fence is not the body; the one after Proposed CURRENT is ---
seed_project "$TMP/earlier"
{
    printf '%s\n' '# CURRENT proposal — example first'
    printf '%s\n' ''
    printf '%s\n' '```markdown'
    body_for "wrong-one"
    printf '%s\n' '```'
    printf '%s\n' ''
    printf '%s\n' '## Proposed CURRENT.md'
    printf '%s\n' ''
    printf '%s\n' '```markdown'
    body_for "right-one"
    printf '%s\n' '```'
} > "$TMP/earlier/.aether/proposals/two.md"
"$AETHER" apply "$TMP/earlier/.aether/proposals/two.md" >/dev/null
grep -q '^\*\*Next:\*\* right-one$' "$TMP/earlier/CURRENT.md" || fail "took the earlier fence"
grep -q 'wrong-one' "$TMP/earlier/CURRENT.md" && fail "earlier fence leaked" || true
pass "body is the fence after Proposed CURRENT"

# --- a file that is already a CURRENT body copies straight across ---
seed_project "$TMP/raw"
body_for "already-body" > "$TMP/raw/ready.md"
"$AETHER" apply "$TMP/raw/ready.md" "$TMP/raw" >/dev/null
grep -q '^\*\*Next:\*\* already-body$' "$TMP/raw/CURRENT.md" || fail "raw CURRENT body not applied"
pass "ready # CURRENT file copies as itself"

# --- proposal under project A must not land on cwd project B ---
seed_project "$TMP/A"
seed_project "$TMP/B"
wrap_proposal "$TMP/A/.aether/proposals/from-a.md" "from-a"
printf '\nB-MARKER\n' >> "$TMP/B/CURRENT.md"
(
    cd "$TMP/B"
    "$AETHER" apply "$TMP/A/.aether/proposals/from-a.md" >/dev/null
)
grep -q 'B-MARKER' "$TMP/B/CURRENT.md" || fail "cwd project B was replaced"
grep -q '^\*\*Next:\*\* from-a$' "$TMP/A/CURRENT.md" || fail "home project A was not replaced"
pass "proposal home wins over the current directory"

# --- explicit project path can target somewhere else, and says so ---
seed_project "$TMP/C"
wrap_proposal "$TMP/C/.aether/proposals/from-c.md" "from-c"
cp "$TMP/C/CURRENT.md" "$TMP/C/CURRENT.before"
set +e
out=$("$AETHER" apply "$TMP/C/.aether/proposals/from-c.md" "$TMP/B" 2>&1)
ec=$?
set -e
[ "$ec" = "0" ] || fail "explicit onto exit=$ec; out=$out"
printf '%s\n' "$out" | grep -q 'note: this proposal belongs to' || fail "missing cross-tree note: $out"
grep -q '^\*\*Next:\*\* from-c$' "$TMP/B/CURRENT.md" || fail "explicit target was not written"
cmp -s "$TMP/C/CURRENT.md" "$TMP/C/CURRENT.before" || fail "explicit target also wrote the home"
pass "explicit project path is honoured and noted"

# --- today's anphuni-project proposal shape, on a copy, not the live file ---
REAL="$HOME/anphuni-project/.aether/proposals/CURRENT-proposal-20260930-1724.md"
if [ -f "$REAL" ]; then
    live_cur="$HOME/anphuni-project/CURRENT.md"
    live_ev="$HOME/anphuni-project/.aether/events.jsonl"
    c1=$(cksum "$live_cur")
    e1=$(cksum "$live_ev")
    seed_project "$TMP/real"
    cp "$REAL" "$TMP/real/.aether/proposals/CURRENT-proposal-20260930-1724.md"
    "$AETHER" apply "$TMP/real/.aether/proposals/CURRENT-proposal-20260930-1724.md" >/dev/null
    grep -q '^\*\*Next:\*\* pocket-playtester$' "$TMP/real/CURRENT.md" || fail "real proposal Next"
    grep -q 'CURRENT proposal' "$TMP/real/CURRENT.md" && fail "real proposal wrapper landed" || true
    grep -q '^APPLY:' "$TMP/real/CURRENT.md" && fail "real proposal APPLY line landed" || true
    grep -q 'Draft the pocket-playtester session' "$TMP/real/CURRENT.md" || fail "real proposal objective missing"
    c2=$(cksum "$live_cur")
    e2=$(cksum "$live_ev")
    [ "$c1" = "$c2" ] || fail "live anphuni CURRENT.md changed"
    [ "$e1" = "$e2" ] || fail "live anphuni events.jsonl changed"
    pass "20260930-1724 body extracts; live anphuni-project untouched"
else
    pass "skip live 1724 fixture (file not on this machine)"
fi

pass "apply-proposal suite"
