#!/bin/sh
# Five-minute alpha demo: authority → refuse → allow → artifact → human approve.
# Does not mention LoRA, Club-cortex, or personal journals.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
AETHER="${AETHER_BIN:-$ROOT/aether}"
export AETHER_HOME="$ROOT"

DEMO="${1:-${TMPDIR:-/tmp}/mechanicall-alpha-demo.$$}"
mkdir -p "$DEMO"
cd "$DEMO"

printf '=== Scene 1 — Authority ===\n'
"$AETHER" init .
"$AETHER" current init .
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** Prove one allowed action and one refused action.
**Phase:** EXECUTE
**Status:** READY-FOR-REVIEW
**Baseline:** alpha-demo
**Next:** write-tests
**Approval:** PENDING

## Keep
- plain-file authority

## Reject
- sandbox-claims

## Limits
- no production deploy

## Next allowed action
Write a tiny test note.

## Approval condition
Human runs: `aether approve "demo ok"`.

## Prohibited
- deploy-production
- add-postgres
CUR
"$AETHER" current .

printf '\n=== Scene 2 — Refusal ===\n'
set +e
"$AETHER" preflight deploy-production .
rc=$?
set -e
[ "$rc" -ne 0 ] || { printf 'FAIL: deploy-production should refuse\n' >&2; exit 1; }

printf '\n=== Scene 3 — Allowed action ===\n'
"$AETHER" preflight write-tests .

printf '\n=== Scene 4 — Evidence ===\n'
mkdir -p artifacts
printf 'alpha demo test report\n' > artifacts/test-report.txt
"$AETHER" artifact artifacts/test-report.txt --action write-tests --status produced

printf '\n=== Scene 5 — Human decision ===\n'
"$AETHER" approve "demo ok"

printf '\n=== Scene 6 — Inspectability ===\n'
printf '%s\n' '--- CURRENT.md ---'
cat CURRENT.md
printf '\n%s\n' '--- events (tail) ---'
tail -n 5 .aether/events.jsonl

printf '\nDemo complete in %s\n' "$DEMO"
printf 'Inspect: cat CURRENT.md && cat .aether/events.jsonl\n'
printf 'Daily surface: cd %s && aether panel\n' "$DEMO"
# refresh panel projections for the demo project
if [ -f "$ROOT/python/aether_panel.py" ]; then
    python3 "$ROOT/python/aether_panel.py" "$DEMO" --write >/dev/null 2>&1 || true
    printf 'Also wrote .aether/PANEL.md + panel.html\n'
fi
