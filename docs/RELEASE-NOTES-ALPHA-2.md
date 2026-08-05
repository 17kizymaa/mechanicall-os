# Mechanicall OS — v0.2.0-alpha.2 release notes (DRAFT)

**STATUS: DRAFT — do not tag until human says so after clean-machine checklist**  
**Target tag:** `v0.2.0-alpha.2` (new tag; do **not** move old tags)  
**Prerelease:** yes  
**Date drafted:** 2026-08-05  

## What this release *is*

**Mechanicall OS protocol alpha for technical users and supported design partners.**

Local-first **authority protocol**:

- one inspectable plan (`CURRENT.md`);
- one permitted **Next**;
- deterministic **cooperative** preflight when called;
- human-only approve / reject / next;
- events ledger;
- `aether demo` literacy path;
- Panel/shell helpers for operators.

**Canonical outcome:** real AI discussions with a **deterministic relationship to authority** — not deterministic prose.

## What this release is *not*

- A finished casual consumer app (single-app seat UX still incomplete)
- Multi-tenant open SaaS
- A sandbox that forces every external TUI to preflight
- Hosted Session as core product (capped lab ≤5; model provider may see traffic)
- “One document syncs the whole conversation”
- Firmware / UEFI packaging

## Systems

| Support | Note |
|---------|------|
| Linux | Primary |
| macOS | Best-effort |
| Windows | WSL only |

## Install (git)

```bash
git clone https://github.com/17kizymaa/mechanicall-os.git
cd mechanicall-os
git checkout v0.2.0-alpha.2   # after tag exists
chmod +x aether
./aether version
```

Optional: `sh scripts/install-aether.sh` / `sh scripts/uninstall-aether.sh`.

## Five-minute path

See **`docs/FIRST-PROJECT.md`**.

```bash
./aether demo          # DEMO OK
# then init a project, preflight refuse + allow, approve, return tomorrow via aether brief
```

## Core vs hosted lab

| Surface | Label |
|---------|--------|
| This repository / local `aether` | **Core** protocol product |
| anphuni.com Session | **Lab** — multi-seat hosted alpha, capped |
| Website static demo | Literacy only — real authority is on the user’s machine |

## Immortal pointer

Release must bind to an **immutable commit SHA** (tag).  
Editing release notes does not move the tag. Never retarget old tags.

## Human checklist before tag

- [ ] CI green on the commit to tag  
- [ ] `CURRENT.md` header Next == body Action id  
- [ ] `docs/FIRST-PROJECT.md` accurate  
- [ ] `./aether demo` DEMO OK  
- [ ] Clean machine: install → demo → project → refuse → uninstall  
- [ ] Human: `git tag -a v0.2.0-alpha.2 <sha>` + `gh release create … --prerelease`  

## Related

- GPT 06c peer · Opus NEXT-01..10 · `docs/RELEASE-NOTES-ALPHA.md` (earlier draft)  
- `PRODUCT.md` · `docs/ALPHA-LIMITATIONS.md` · `docs/LAB-STATUS.md`
