#!/bin/sh
# aether bookmark: copy CURRENT.md. Never Yes. Never restore.
# Run: sh tests/bookmark.sh
set -e

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="${AETHER:-$ROOT/aether}"
export AETHER_HOME="${AETHER_HOME:-$ROOT}"
export PATH="$ROOT:$PATH"

fail() { printf 'FAIL bookmark: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

TMP="${TMPDIR:-/tmp}/aether-bookmark-test.$$"
rm -rf "$TMP"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT INT HUP

seed_project() {
    dir="$1"
    mkdir -p "$dir"
    (
        cd "$dir"
        "$AETHER" init . >/dev/null
        "$AETHER" current init . >/dev/null
    )
}

# --- restore is not this verb ---
seed_project "$TMP/rest"
set +e
out=$("$AETHER" bookmark restore "$TMP/rest" 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "restore exit=$ec want 2; out=$out"
printf '%s\n' "$out" | grep -q 'restore is not this verb' || fail "restore message: $out"
pass "restore is not this verb"

# --- unknown flag ---
set +e
out=$("$AETHER" bookmark --gpu-yes "$TMP/rest" 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "flag exit=$ec want 2"
printf '%s\n' "$out" | grep -q 'unknown flag' || fail "flag message: $out"
pass "unknown flag exits 2"

# --- invalid label ---
set +e
out=$("$AETHER" bookmark 'bad/label' "$TMP/rest" 2>&1)
ec=$?
set -e
[ "$ec" = "2" ] || fail "invalid label exit=$ec want 2; out=$out"
printf '%s\n' "$out" | grep -q 'invalid label' || fail "invalid label message: $out"
pass "invalid label exits 2"

# --- missing CURRENT.md ---
mkdir -p "$TMP/empty"
set +e
out=$("$AETHER" bookmark "$TMP/empty" 2>&1)
ec=$?
set -e
[ "$ec" = "1" ] || fail "missing CURRENT exit=$ec want 1; out=$out"
printf '%s\n' "$out" | grep -q 'no CURRENT.md' || fail "missing CURRENT message: $out"
pass "missing CURRENT.md exits 1"

# --- list empty ---
out=$("$AETHER" bookmark list "$TMP/rest")
printf '%s\n' "$out" | grep -q 'bookmark: none' || fail "empty list: $out"
pass "list none"

# --- snapshot copies; CURRENT unchanged ---
seed_project "$TMP/ok"
cp "$TMP/ok/CURRENT.md" "$TMP/ok/CURRENT.before"
out=$("$AETHER" bookmark this-current "$TMP/ok" </dev/null)
printf '%s\n' "$out" | grep -q 'BOOKMARK:' || fail "missing BOOKMARK: $out"
printf '%s\n' "$out" | grep -q 'Not a Yes' || fail "missing Not a Yes: $out"
cmp -s "$TMP/ok/CURRENT.md" "$TMP/ok/CURRENT.before" || fail "CURRENT.md changed"
snap=$(printf '%s\n' "$out" | awk '/^BOOKMARK:/{print $2}')
[ -n "$snap" ] && [ -f "$snap" ] || fail "snapshot missing: $out"
cmp -s "$TMP/ok/CURRENT.md" "$snap" || fail "snapshot bytes differ from CURRENT"
printf '%s\n' "$snap" | grep -q 'this-current.md' || fail "label missing from path: $snap"
csum=$(cksum "$snap" | awk '{print $1}')
grep -q '"kind":"bookmark"' "$TMP/ok/.aether/events.jsonl" || fail "event kind"
grep -q "$csum" "$TMP/ok/.aether/events.jsonl" || fail "event checksum $csum"
grep -q current-before "$TMP/ok/.aether/events.jsonl" && fail "bookmark wrote current-before event" || true
[ ! -d "$TMP/ok/.aether/current-before" ] || fail "bookmark created current-before/"
pass "snapshot copies; CURRENT unchanged; event cksum"

# --- list shows the new file ---
listed=$("$AETHER" bookmark list "$TMP/ok")
printf '%s\n' "$listed" | grep -q "$(basename "$snap")" || fail "list missing snap: $listed"
pass "list shows snapshot"

# --- duplicate labels allowed ---
sleep 1
out2=$("$AETHER" bookmark this-current "$TMP/ok" </dev/null)
snap2=$(printf '%s\n' "$out2" | awk '/^BOOKMARK:/{print $2}')
[ "$snap" != "$snap2" ] || fail "second snapshot reused path"
cmp -s "$TMP/ok/CURRENT.md" "$snap2" || fail "second snapshot mismatch"
pass "duplicate labels allowed"

# --- unlabeled snapshot ---
sleep 1
out3=$("$AETHER" bookmark "$TMP/ok" </dev/null)
snap3=$(printf '%s\n' "$out3" | awk '/^BOOKMARK:/{print $2}')
printf '%s\n' "$snap3" | grep -qE 'CURRENT-[0-9T]+Z\.md$' || fail "unlabeled path: $snap3"
pass "unlabeled snapshot"

# --- list newest first ---
listed2=$("$AETHER" bookmark list "$TMP/ok")
first=$(printf '%s\n' "$listed2" | head -1)
[ "$(basename "$first")" = "$(basename "$snap3")" ] || fail "newest first want $(basename "$snap3") got $(basename "$first")"
pass "list newest first"

# --- apply still uses current-before, not bookmarks ---
mkdir -p "$TMP/ok/.aether/proposals"
cat > "$TMP/ok/.aether/proposals/one.md" <<'EOF'
# CURRENT proposal — switch

## Proposed CURRENT.md

```markdown
# CURRENT

**Objective:** One halt.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** t
**Next:** pocket-playtester
**Approval:** DRAFT

## Keep
- one

## Reject
- two

## Limits
- three

## Next allowed action
**Action id:** `pocket-playtester`

Do the halt.

## Approval condition
Human runs aether approve.

## Prohibited
- automatic-approve
- model-auto-write-current
```
EOF
before_count=$(find "$TMP/ok/.aether/bookmarks" -name 'CURRENT-*.md' | wc -l | tr -d ' ')
"$AETHER" apply "$TMP/ok/.aether/proposals/one.md" "$TMP/ok" >/dev/null
after_count=$(find "$TMP/ok/.aether/bookmarks" -name 'CURRENT-*.md' | wc -l | tr -d ' ')
[ "$before_count" = "$after_count" ] || fail "apply wrote a bookmark"
[ -d "$TMP/ok/.aether/current-before" ] || fail "apply missed current-before"
pass "apply writes current-before, not bookmarks"

# --- proposal file snapshot; CURRENT and source unchanged ---
prop="$TMP/ok/.aether/proposals/one.md"
cp "$prop" "$TMP/ok/one.before"
cp "$TMP/ok/CURRENT.md" "$TMP/ok/CURRENT.before2"
outp=$("$AETHER" bookmark "$prop" note </dev/null)
printf '%s\n' "$outp" | grep -q 'BOOKMARK:' || fail "proposal missing BOOKMARK: $outp"
printf '%s\n' "$outp" | grep -q 'Not apply' || fail "proposal missing Not apply: $outp"
psnap=$(printf '%s\n' "$outp" | awk '/^BOOKMARK:/{print $2}')
[ -f "$psnap" ] || fail "proposal snapshot missing"
cmp -s "$prop" "$psnap" || fail "proposal snapshot bytes differ"
cmp -s "$prop" "$TMP/ok/one.before" || fail "proposal source changed"
cmp -s "$TMP/ok/CURRENT.md" "$TMP/ok/CURRENT.before2" || fail "CURRENT.md changed when bookmarking proposal"
printf '%s\n' "$psnap" | grep -q 'one-' || fail "proposal stem missing from path: $psnap"
grep -q 'one.md' "$TMP/ok/.aether/events.jsonl" || fail "event source not proposal"
listedp=$("$AETHER" bookmark list "$TMP/ok")
printf '%s\n' "$listedp" | grep -q "$(basename "$psnap")" || fail "list missing proposal snap"
pass "proposal snapshot; source and CURRENT unchanged"

# --- live verb list has bookmark, not restore ---
verbs=$("$AETHER" verbs)
printf '%s\n' "$verbs" | grep -qw bookmark || fail "bookmark missing from verbs"
printf '%s\n' "$verbs" | grep -qw restore && fail "restore in verbs" || true
printf '%s\n' "$verbs" | grep -qw preflight || fail "preflight missing from verbs"
printf '%s\n' "$verbs" | grep -qw current || fail "current missing from verbs"
printf '%s\n' "$verbs" | grep -qw approve || fail "approve missing from verbs"
printf '%s\n' "$verbs" | grep -qw apply || fail "apply missing from verbs"
for gone in garden rival spark graph session seed; do
    printf '%s\n' "$verbs" | grep -qw "$gone" && fail "$gone still in verbs" || true
done
pass "verbs has bookmark and gate; six rhizome verbs absent"

# --- non-TTY ignores stdin and does not hang ---
seed_project "$TMP/notty"
cp "$TMP/notty/CURRENT.md" "$TMP/notty/CURRENT.before"
out=$(printf 'ejected-verbs\n' | "$AETHER" bookmark "$TMP/notty")
printf '%s\n' "$out" | grep -q 'BOOKMARK:' || fail "non-tty missing BOOKMARK: $out"
snapnt=$(printf '%s\n' "$out" | awk '/^BOOKMARK:/{print $2}')
printf '%s\n' "$snapnt" | grep -qE 'CURRENT-[0-9T]+Z\.md$' || fail "non-tty renamed: $snapnt"
cmp -s "$TMP/notty/CURRENT.md" "$TMP/notty/CURRENT.before" || fail "non-tty changed CURRENT"
pass "non-tty keeps CURRENT stem and does not read stdin"

# pty_bookmark <line> <project> [args...]
# line empty means the user pressed enter. Exit status is aether's.
pty_bookmark() {
    _line="$1"
    _proj="$2"
    shift 2
    python3 - "$_line" "$AETHER" "$_proj" "$@" << 'PY'
import os, select, sys, time

line, aether, proj = sys.argv[1], sys.argv[2], sys.argv[3]
extra = sys.argv[4:]
cmd = [aether, "bookmark", *extra, proj]

try:
    import pty
except ImportError:
    sys.stderr.write("python pty missing\n")
    sys.exit(1)

master, slave = pty.openpty()
pid = os.fork()
if pid == 0:
    os.close(master)
    os.setsid()
    os.dup2(slave, 0)
    os.dup2(slave, 1)
    os.dup2(slave, 2)
    if slave > 2:
        os.close(slave)
    os.execv(cmd[0], cmd)

os.close(slave)
out = b""
sent = False
deadline = time.time() + 8
status = None
while time.time() < deadline:
    readable, _, _ = select.select([master], [], [], 0.2)
    if master in readable:
        try:
            chunk = os.read(master, 4096)
        except OSError:
            chunk = b""
        if chunk:
            out += chunk
            if not sent and b"Rename:" in out:
                payload = b"\n" if line == "" else (line.encode() + b"\n")
                os.write(master, payload)
                sent = True
    wpid, st = os.waitpid(pid, os.WNOHANG)
    if wpid:
        status = st
        while True:
            readable, _, _ = select.select([master], [], [], 0.05)
            if master not in readable:
                break
            try:
                chunk = os.read(master, 4096)
            except OSError:
                break
            if not chunk:
                break
            out += chunk
        break
else:
    try:
        os.kill(pid, 15)
        os.waitpid(pid, 0)
    except OSError:
        pass
    sys.stderr.write("timeout waiting for Rename prompt\n")
    os.close(master)
    sys.exit(1)

os.close(master)
if status is None:
    _, status = os.waitpid(pid, 0)
code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 1
sys.stdout.buffer.write(out.replace(b"\r", b""))
sys.exit(code)
PY
}

# --- TTY nickname ---
sleep 1
seed_project "$TMP/tty"
cp "$TMP/tty/CURRENT.md" "$TMP/tty/CURRENT.before"
set +e
out=$(pty_bookmark "ejected-verbs" "$TMP/tty")
ec=$?
set -e
[ "$ec" = "0" ] || fail "tty nickname exit=$ec out=$out"
printf '%s\n' "$out" | grep -q 'Rename:' || fail "missing Rename prompt: $out"
printf '%s\n' "$out" | grep -q 'BOOKMARK:' || fail "tty missing BOOKMARK: $out"
printf '%s\n' "$out" | grep -q 'Not a Yes' || fail "tty missing Not a Yes: $out"
snapt=$(printf '%s\n' "$out" | awk '/^BOOKMARK:/{print $2}')
printf '%s\n' "$snapt" | grep -q 'ejected-verbs-' || fail "stem not ejected-verbs: $snapt"
cmp -s "$TMP/tty/CURRENT.md" "$TMP/tty/CURRENT.before" || fail "tty nickname changed CURRENT"
cmp -s "$TMP/tty/CURRENT.md" "$snapt" || fail "tty snapshot bytes differ"
grep -q '"stem":"ejected-verbs"' "$TMP/tty/.aether/events.jsonl" || fail "event stem missing"
pass "tty nickname ejected-verbs; CURRENT unchanged"

# --- empty Rename keeps CURRENT ---
sleep 1
set +e
out=$(pty_bookmark "" "$TMP/tty")
ec=$?
set -e
[ "$ec" = "0" ] || fail "empty rename exit=$ec out=$out"
snape=$(printf '%s\n' "$out" | awk '/^BOOKMARK:/{print $2}')
printf '%s\n' "$snape" | grep -qE 'CURRENT-[0-9T]+Z\.md$' || fail "empty rename stem: $snape"
cmp -s "$TMP/tty/CURRENT.md" "$TMP/tty/CURRENT.before" || fail "empty rename changed CURRENT"
pass "empty Rename keeps CURRENT"

# --- reserved stems ---
for reserved in list restore; do
    set +e
    out=$(pty_bookmark "$reserved" "$TMP/tty")
    ec=$?
    set -e
    [ "$ec" = "2" ] || fail "reserved $reserved exit=$ec out=$out"
    printf '%s\n' "$out" | grep -q 'reserved stem' || fail "reserved message $reserved: $out"
done
pass "list and restore stems exit 2"

# --- invalid stem ---
set +e
out=$(pty_bookmark 'bad/stem' "$TMP/tty")
ec=$?
set -e
[ "$ec" = "2" ] || fail "invalid stem exit=$ec out=$out"
printf '%s\n' "$out" | grep -q 'invalid stem' || fail "invalid stem message: $out"
pass "invalid stem exits 2"

# --- live pin and version stay ---
pin_ck=$(cksum "$ROOT/.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md" | awk '{print $1}')
[ "$pin_ck" = "3532677481" ] || fail "pin cksum $pin_ck"
grep -q 'versionCode = 46' "$ROOT/android/app/build.gradle.kts" || fail "versionCode moved"
pass "pin cksum and versionCode 46"

pass "bookmark suite"
