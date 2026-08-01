#!/bin/sh
# Control-layer CI gates — seats + authority (no cloud/K8s).
# Run: sh scripts/ci-control-layer-gates.sh
# Domain Next: ci-control-layer-gates
set -e
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
export AETHER_HOME="$ROOT"
export PATH="$ROOT:$PATH"
AETHER="$ROOT/aether"
PY="${PYTHON:-python3}"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'ok: %s\n' "$*"; }

cd "$ROOT"

# --- unit tests (pytest when available; else unittest-style modules) ---
if $PY -c "import pytest" 2>/dev/null; then
  $PY -m pytest -q \
    tests/test_aether_shell.py \
    tests/test_aether_shell_agent.py \
    tests/test_aether_panel.py \
    tests/test_aether_llm_personal.py \
    tests/test_aether_llm_presets.py \
    tests/test_aether_llm_grok_tui.py \
    || fail "pytest control-layer units"
  pass "pytest control-layer units"
else
  $PY tests/test_aether_llm_personal.py || fail "personal-llm units"
  $PY tests/test_aether_panel.py || fail "panel units"
  pass "unittest-style units (pytest not installed)"
fi

# --- desk must be gone ---
out=$("$AETHER" desk 2>&1) && fail "aether desk should not succeed" || true
printf '%s\n' "$out" | grep -qi 'removed\|unsacred\|shell\|panel' \
  || fail "desk should die with redirect to shell/panel"
pass "desk removed"

out=$("$AETHER" desk-serve 2>&1) && fail "desk-serve should not succeed" || true
printf '%s\n' "$out" | grep -qi 'removed\|unsacred\|shell\|panel' \
  || fail "desk-serve should die with redirect"
pass "desk-serve removed"

# --- tmp Domain: shell smoke + panel dump + preflight ---
TMP="${TMPDIR:-/tmp}/aether-cl-gates.$$"
mkdir -p "$TMP/domain"
trap 'rm -rf "$TMP"' EXIT INT HUP
cd "$TMP/domain"

"$AETHER" init . >/dev/null || fail "init"
"$AETHER" current init . >/dev/null || fail "current init"
cat > CURRENT.md <<'CUR'
# CURRENT

**Objective:** CI control-layer gates smoke Domain.
**Phase:** EXECUTE
**Status:** ACTIVE
**Baseline:** ci-control-layer-gates
**Next:** ci-smoke-step
**Approval:** PENDING

## Keep
- CURRENT sole authority

## Reject
- model self-approve

## Limits
- one Next

## Next allowed action
CI smoke only. Action id: `ci-smoke-step`.

## Approval condition
Human only.

## Prohibited
- automatic-approve
- commit-secrets
- deploy-production
CUR

# shell offline smoke
"$PY" "$ROOT/python/aether_shell.py" --smoke . >/dev/null \
  || fail "shell --smoke"
pass "shell --smoke"

# panel projection
dump=$("$AETHER" panel --dump . 2>&1) || fail "panel --dump"
printf '%s\n' "$dump" | grep -q 'ci-smoke-step' || fail "panel dump missing Next"
printf '%s\n' "$dump" | grep -qi 'NEXT\|Next\|ci-smoke' || fail "panel dump missing Next pin"
pass "panel --dump shows Next"

# preflight allow Next / refuse Prohibited
out=$("$AETHER" preflight ci-smoke-step . 2>&1) || fail "preflight Next should allow"
printf '%s\n' "$out" | grep -qi allow || fail "preflight allow message"
pass "preflight allows Next"

out=$("$AETHER" preflight deploy-production . 2>&1) && fail "deploy-production should refuse" || true
printf '%s\n' "$out" | grep -qi refuse || fail "preflight refuse message"
pass "preflight refuses Prohibited"

# agent profiles present in product tree
[ -f "$ROOT/references/aether-shell-agent-peer.md" ] || fail "missing peer agent profile"
[ -f "$ROOT/references/aether-shell-agent-grok.md" ] || fail "missing grok agent profile"
[ -f "$ROOT/python/aether_panel_tui.py" ] || fail "missing panel TUI module"
[ -f "$ROOT/python/aether_shell.py" ] || fail "missing shell"
pass "control-layer artifacts present"

# secrets hygiene: no raw ghp_/sk-or- in tracked product files (best-effort)
if command -v git >/dev/null && [ -d "$ROOT/.git" ]; then
  cd "$ROOT"
  if git grep -I -E 'ghp_[A-Za-z0-9]{20,}|sk-or-v1-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-]{20,}' \
    -- '*.py' '*.md' 'aether' 'tests' 'references' 'docs' 2>/dev/null \
    | grep -v 'TOKEN_PREFIX\|example\|placeholder\|ghp_\*' \
    | grep -q .; then
    fail "possible raw secrets in tracked product paths"
  fi
  pass "no obvious raw secrets in product paths"
fi

printf '\n== ci-control-layer-gates: ALL PASSED ==\n'
exit 0
