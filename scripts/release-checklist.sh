#!/bin/sh
# Pre-tag checklist for Mechanicall OS alpha. Exit 0 only if all gates pass.
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0
ok() { printf 'ok: %s\n' "$1"; }
bad() { printf 'FAIL: %s\n' "$1" >&2; fail=1; }

[ -f LICENSE ] && grep -qi 'Apache License' LICENSE && ok "LICENSE Apache-2.0" || bad "LICENSE"
[ -f docs/ALPHA-LIMITATIONS.md ] && ok "ALPHA-LIMITATIONS.md" || bad "ALPHA-LIMITATIONS.md"
[ -f docs/INTEGRATION-AGENTS.md ] && ok "INTEGRATION-AGENTS.md" || bad "INTEGRATION-AGENTS.md"
[ -f .github/workflows/test.yml ] && ok "CI workflow" || bad "CI workflow"
[ -f python/aether_panel.py ] && ok "aether_panel.py" || bad "panel"
[ -x aether ] || [ -f aether ] && ok "aether CLI" || bad "aether"
grep -q 'panel)' aether && ok "aether panel wired" || bad "aether panel not in CLI"
grep -qi 'preflight' README.md && ok "README preflight language" || bad "README claims"
grep -qi 'block unapproved execution' README.md && bad "README still overclaims block execution" || ok "README no overclaim"

printf '\nRunning tests…\n'
if sh tests/run.sh; then
    ok "tests/run.sh"
else
    bad "tests/run.sh"
fi

printf '\nSmoke: alpha-demo + panel dump…\n'
DEMO="${TMPDIR:-/tmp}/mechanicall-checklist-demo.$$"
if sh scripts/alpha-demo.sh "$DEMO" >/dev/null \
    && AETHER_HOME="$ROOT" ./aether panel "$DEMO" --dump | grep -q Next; then
    ok "alpha-demo + panel --dump"
else
    bad "alpha-demo / panel smoke"
fi
rm -rf "$DEMO" 2>/dev/null || true

if [ "$fail" -ne 0 ]; then
    printf '\nChecklist FAILED\n' >&2
    exit 1
fi
printf '\nChecklist PASSED — ready for human review, then tag v0.2.0-alpha.1\n'
printf 'Do not push/tag without operator confirmation.\n'
exit 0
