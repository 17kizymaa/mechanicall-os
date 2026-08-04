# Commit hygiene plan — commit-hygiene

**Date:** 2026-08-04  
**Branch:** `feat/domain-shell-panel-tui`  
**Authority:** Next=`commit-hygiene` · APPROVED  
**Preflight:** ALLOW  
**Status:** TRIAGED — **no commits applied** (await human batch approval)

## Summary

| Metric | Value |
|--------|------:|
| Dirty paths (pre-ignore tweak) | ~103 |
| Tracked modified | 21 |
| Untracked (many dirs) | ~82 |
| Secret scan (live `sk-or-…` tokens) | **none found** (docs only mention prefix) |
| Largest never-commit | `mechanicall-portable-vm.qcow2` (~22 MB) |

## Never commit (ignore / leave local)

Applied to `.gitignore` this turn (or already covered):

| Path / pattern | Why |
|----------------|-----|
| `*.qcow2` | VM disk image |
| `/result`, `/result-vm` | Nix store symlinks |
| `*.bak`, `python/*.bak*` | Editor backups (`aether_panel.py.bak-pre-v0`) |
| `.aether/last-grok-brief.txt` | Regenerable brief cache |
| `seat/node_modules/`, `seat/dist/`, `seat/src-tauri/target/` | Already ignored |

**Review before any commit of `.aether/`:**

| Path | Recommendation |
|------|----------------|
| `.aether/events.jsonl` | Optional inspectability — **include** if you want protocol ledger in git; scrub if personal |
| `.aether/chat.jsonl`, `shell.jsonl` | Prefer **omit** (local session noise) unless you want them |
| `.aether/panel.html`, `PANEL.md` | Optional product samples — your call |
| `.aether/REPO-MOVE-*.md` | Optional history note |

**Oddball:** root `os` is a PostScript document — almost certainly accidental; **do not commit** until you identify it.

**`.planning/tmp`:** treat as local GSD noise unless you want planning artifacts.

---

## Proposed commit batches (human picks which to apply)

### Batch A — Protocol product core (highest value)

**Intent:** Ship the authority protocol alpha that smoke-verify proved.

```
aether
tests/run.sh
scripts/protocol-demo.sh
scripts/grok-aether-brief.sh
.grok/hooks/README.md
.grok/hooks/aether-session-start.json
.grok/hooks/aether-prompt-context.json
docs/PROTOCOL-TEST-SURFACE.md
docs/GROK-SEAT.md
docs/PROTOCOL-LAB.md
docs/RELEASE-NOTES-ALPHA.md
docs/OUTLOOK-RESEARCH-BOUNDARY.md
docs/PERSONAL-LLM-DEFINITION.md
PRODUCT.md
START-HERE.md
AUTHORITY.md
DECISIONS.md
AGENTS.md
ARCHITECTURE.md
CORE_PRINCIPLES.md
NOT-IMPLEMENTED.md
README.md
.gitignore
CURRENT.md          # live authority — include only if you want this tree’s CURRENT in git
dev/18_opus5-protocol-completion/
dev/18_protocol-first/
```

**Suggested message:**
```
feat(protocol): demo, brief/drift/probe, Grok seat hooks, product boundary docs

Ship aether next/demo/brief/drift/probe, protocol demo script, Grok observability
hooks, and PRODUCT/AGENTS peer-absorb wording. Session remains lab, not core.
```

### Batch B — Panel / TUI / LLM seat code

```
python/aether_panel.py
python/aether_panel_tui.py
python/aether_llm.py
python/peer_translate_hook.py
docs/PANEL-GROK-SPLIT.md
docs/DEVELOPMENT.md
shell.nix
```

**Message sketch:** `feat(panel): Grok-split TUI and LLM panel updates`

### Batch C — Nix / Kingston portable seat

```
flake.nix
nix/hosts/portable-kingston.nix
nix/modules/seat-kiosk.nix
docs/nixos-transition.md
scripts/rebuild-portable-kingston.sh
scripts/seat-kiosk-session.sh
scripts/seat-menu.sh
scripts/seat-verify-kingston.sh
scripts/sync-to-kingston.sh
scripts/install-grok-on-kingston.sh
scripts/fix-android-default-boot.sh
scripts/fix-grub-android-hardcoded.sh
scripts/try.sh
```

**Message sketch:** `feat(nix): portable Kingston host + seat kiosk scripts`

### Batch D — Tauri seat app (source only; builds ignored)

```
seat/   # without node_modules/dist/target (gitignore)
```

**Message sketch:** `feat(seat): Tauri/Vite seat shell scaffold`

### Batch E — Dev stage archives (ICM workspaces)

Split or one mega-commit by taste:

| Dir | Theme |
|-----|--------|
| `dev/15_mbp-seat-gop-chat/` (+ modified tracked files) | MBP seat / GOP chat |
| `dev/15_project-control-layer/` | Control layer stages |
| `dev/16_anphuni-pipeline-redo/` | Pipeline redo |
| `dev/17_client-one-session-three/` | Client One session three |
| `dev/10_*`, `dev/13_*`, `dev/14_*`, `dev/07_*`, `dev/09_…` | Older archives |
| `dev/CURRENT.md-REWIRING/` | CURRENT rewiring experiment |

**Risk:** large narrative/export dumps under `dev/15_mbp-seat-gop-chat/exports/` — skim before commit.

### Batch F — Research / domains (optional)

```
research/personal-llm-proposals/
research/speculative/*
domains/
docs/MECHANICALL-ALPHA-DIRECTION.md
docs/NAMING.md
docs/INTERNAL-TOOLS.md
docs/SINGLE-APP-DISTRIBUTION.md
docs/THREE-WEEK-REALITY-SPRINT.md
```

**Message sketch:** `docs(research): speculative notes and domain sketches`  
Mark speculative as non-authority.

### Batch G — Park / never for now

- `mechanicall-portable-vm.qcow2` (ignored)
- `result`, `result-vm` (ignored)
- `python/aether_panel.py.bak-pre-v0` (ignored)
- root `os` (unknown PS)
- `.planning/` unless you use GSD in-repo
- Local-only `.aether/*.jsonl` if you prefer clean Domain state per machine

---

## Recommended order

1. Confirm **Batch A** only first (protocol alpha) — smallest product-truth slice.  
2. Then **B** if panel is in-scope for this branch.  
3. **C/D** only if this branch is meant to carry seat/nix.  
4. **E/F** last or separate PR(s) so history stays reviewable.

## Commands (after you pick batches)

```bash
# example: Batch A only
git add aether tests/run.sh scripts/protocol-demo.sh scripts/grok-aether-brief.sh \
  .grok/hooks/ .gitignore \
  docs/PROTOCOL-TEST-SURFACE.md docs/GROK-SEAT.md docs/PROTOCOL-LAB.md \
  docs/RELEASE-NOTES-ALPHA.md docs/OUTLOOK-RESEARCH-BOUNDARY.md \
  docs/PERSONAL-LLM-DEFINITION.md \
  PRODUCT.md START-HERE.md AUTHORITY.md DECISIONS.md \
  AGENTS.md ARCHITECTURE.md CORE_PRINCIPLES.md NOT-IMPLEMENTED.md README.md \
  CURRENT.md dev/18_opus5-protocol-completion/ dev/18_protocol-first/

git status   # review
git commit -m "$(cat <<'EOF'
feat(protocol): demo, brief/drift/probe, Grok seat hooks, product boundary docs

Ship protocol CLI surface and docs. No publish/tag. Session remains lab.
EOF
)"
```

**Do not** `git push` unless human asks.  
**Do not** commit secrets / `.env` / qcow2 / nix `result*`.

## Open human choices

1. Which batches this session: **A only** / **A+B** / **all product** / **everything except G**?  
2. Include live **`CURRENT.md`** in Batch A, or leave Domain-local?  
3. Commit **`.aether/events.jsonl`** for inspectability, or ignore as machine-local?  
4. Keep **`os`** / investigate?

## Verdict this turn

- Triage complete  
- `.gitignore` hardened for VM/Nix/bak/brief  
- **Zero commits** until you name batch IDs (e.g. “commit A then B”)
