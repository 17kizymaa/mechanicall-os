# Receipt — next-05-loc-decision

**Date:** 2026-08-04  
**Action:** `next-05-loc-decision` · APPROVED  
**Peer:** Opus 5 🟠-1 / NEXT-05  

## Decision (chosen)

**Option (a) — retire the myth; keep single file.**  
Not option (b) — split the CLI (deferred).

| Retire | Keep |
|--------|------|
| ≤220 lines | One POSIX `aether` at repo root |
| “One screen of `cat aether`” | No build step; `cat`/`grep` still work |
| | Verb-section readability; soft growth budget |

## Files touched

| File | Change |
|------|--------|
| `SPEC-v0.2.md` | **CLI size doctrine** section (normative) |
| `SPEC-v0.1.md` | LOC budget → HISTORICAL; stripped `===edit marker===` residue |
| `CORE_PRINCIPLES.md` | Clarify inspectability ≠ one-screen CLI |
| `CHANGELOG.md` | New (decision + same-day protocol waves) |

## Measured

`wc -l aether` ≈ **1899** (host, post next-04)

## Not done

- Physical split of `aether`  
- Hard CI max-line gate  

## Human gate

```bash
aether next next-06-preflight-receipt
# or next-07-shellcheck / park-protocol-alpha
```
