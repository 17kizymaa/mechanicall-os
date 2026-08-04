# Receipt — next-07-shellcheck

**Date:** 2026-08-04  
**Action:** `next-07-shellcheck` · APPROVED  
**Peer:** Opus 5 🟠-4 / NEXT-07  

## Deliverable

| Item | Detail |
|------|--------|
| Gate | `shellcheck -s sh aether` fatal in `tests/run.sh` if shellcheck present; **fail if missing** |
| Standalone | `tests/shellcheck.sh` |
| Findings | aether: **0** after small fixes |

## Fixes

| Issue | Resolution |
|-------|------------|
| SC2012 `ls` hooks | Portable `find` + sed |
| SC2016 backticks in template string | Rephrase without backticks |

## Install (this host)

```text
nix-env -iA nixpkgs.shellcheck   # → 0.11.0
```

## Tests

`ok: shellcheck aether (POSIX sh)` · full `tests/run.sh` green

## Human gate

```bash
aether next next-08-normative-docs
# or next-09-verb-list / park-protocol-alpha
```
