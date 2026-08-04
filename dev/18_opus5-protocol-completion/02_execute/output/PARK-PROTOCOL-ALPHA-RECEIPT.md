# Park — protocol alpha (Opus peer wave complete)

**Date:** 2026-08-04  
**Action:** `park-protocol-alpha` · APPROVED  
**Branch:** `feat/domain-shell-panel-tui` (ahead of last push only with uncommitted work)  
**Host tip (committed):** `33abafa` panel · `6a1a014` protocol (merged to `master` via PR **#3** as `5dd2c9f`)  
**Authority:** Next=`park-protocol-alpha` · APPROVE/APPROVED/APPROVED  

## Park meaning

Stop opening new Opus NEXT waves unless human re-SELECTs.  
Protocol alpha follow-ups **NEXT-01 … NEXT-10** are **done on the working tree** (not all committed/pushed).

## Smoke at park

| Check | Result |
|-------|--------|
| `aether preflight park-protocol-alpha` | ALLOW |
| `aether current validate` | OK (warn: all APPROVE(D) — lifecycle wants a later Next) |
| `sh tests/run.sh` | **ALL PASSED** |
| Dirty paths | ~**110** (large uncommitted delta after PR #3) |

## What this cycle delivered

### Already on `master` (PR #3)

- Protocol: `next` / `demo` / `brief` / `drift` / `probe` / hooks / PRODUCT boundary docs  
- Panel: Grok-split TUI, llm, peer_translate  

### Working tree (Opus peer absorb + NEXT-01…10) — **uncommitted**

| Next | Deliverable |
|------|-------------|
| 01 | Unknown command → exit 2 |
| 02 | `tests/negative.sh` |
| 03 | Apache-2.0 discoverability (LICENSE already present) |
| 04 | Exit codes 0/1/2/3 |
| 05 | LOC doctrine retire ≤220 / one-screen |
| 06 | Preflight receipt PASS/STALE/ABSENT |
| 07 | shellcheck gate |
| 08 | `docs/DOC-AUTHORITY.md` NORMATIVE map |
| 09 | `AETHER_VERBS` / `AETHER_VERSION` / completion |
| 10 | `docs/LAB-STATUS.md` lab vs shipped |

Receipts: `dev/18_opus5-protocol-completion/02_execute/output/NEXT-*.md`  
Peer chain: `…/PEER-REVIEW-OPUS5-2026-08-04.md` + index  

## Explicitly parked / not done

- Commit + push of NEXT-01…10 (human batch / PR)  
- Publish/tag release  
- Blocking Grok hooks  
- Full dirty-tree cleanup (nix, seat, older `dev/*`)  
- Live site privacy re-verify  
- Shellcheck on all scripts (only `aether` gated)  

## Suggested human moves (after park)

1. **Commit waves** — e.g. one PR: protocol peer fixes (aether + tests + docs NEXT-01…10)  
2. **Or** leave uncommitted until next session: `aether brief` rehydrates  
3. **Re-SELECT** when ready:  
   `aether next commit-peer-waves` or `aether next idle`  

## Resume commands

```bash
cd /mnt/kingston-nixos-sync/opt/mechanicall-os
./aether brief
./aether current
sh tests/run.sh
cat dev/18_opus5-protocol-completion/02_execute/output/PARK-PROTOCOL-ALPHA-RECEIPT.md
```

## Product lock (unchanged)

Local authority protocol = CURRENT + preflight + human yes.  
Session = capped lab only. Grok does not auto-preflight. Silence ≠ permission.

---

**PARKED.** Models do not approve the next wave without human `aether next` + `approve`.
