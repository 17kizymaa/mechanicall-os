# Inventory — what Mechanicall OS has built

**When:** 2026-08-18  
**Operator Next (unchanged):** `mobile-planning-demo`  
**This file:** understand-only. No moves. No CURRENT rewrite.

---

## 1. The product in one breath

**You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.**

Shipped core (PRODUCT + SPEC-v0.2 + LAB-STATUS):

```text
CURRENT.md          live law (one Next)
aether              POSIX CLI v0.2 (~2065 lines, repo-root; bin/aether → ../aether)
aether preflight    allow (0) / refuse (3)
human approve       only actualisation
.aether/events.jsonl  append-only receipts
```

It is **not** a sandbox, not Play Store, not Session-as-core, not Hyprland rice, not a finished casual single-app.

Honest alpha claim (README): inspectable authority contract + deterministic preflight **when consulted**. Cooperative, not a jail.

---

## 2. What is actually shipped vs what sits beside it

### SHIPPED — protocol identity

| Path | What it is |
|------|------------|
| `aether` | One-true CLI. Verbs: init, onboard, try, panel, shell, app, deinit, status, distill, watch, repair, poke, trust, current, preflight, approve, reject, next, demo, brief, drift, probe, event, artifact, seed, spark, session, graph, garden, rival, help, version, verbs |
| `SPEC-v0.2.md` | Authority contract (winner over SPEC-v0.1) |
| `PRODUCT.md` | Core vs lab vs research boundary |
| `CORE_PRINCIPLES.md` | Filesystem truth, cooperative authority |
| `AGENTS.md` | CURRENT-first; models never approve |
| `NOT-IMPLEMENTED.md` | Explicit denials |
| `LICENSE` | Apache-2.0 |

### SUPPORT — helpers on the same law

| Path | What it is |
|------|------------|
| `python/` | 11 modules. Panel TUI, Domain shell, LLM plumbing, garden/rival, **pocket demo bridge** |
| `scripts/` | 23 behaviours (install, demo, CI, pocket push/serve/rehearse) |
| `tests/` | `run.sh` + `negative.sh` + `shellcheck.sh` + 8 pytest files (panel/shell/llm/pocket) |
| `docs/` | 37 files — mixed NORMATIVE / NON-NORMATIVE; map is `docs/DOC-AUTHORITY.md` |
| `examples/` | alpha-demo, reel-control, dev-task, propose-current, pocket-demo-client, sidecars |
| `bin/aether` | Symlink to `../aether` |

### LAB — real files, not core claims

| Path | What it is | Honest state |
|------|------------|--------------|
| `android/` | Compose + Chaquopy pocket APK | Demo only; SDK not in this Nix shell by default |
| `python/aether_pocket.py` + `_serve.py` | Pocket bind + LAN face `:8765` | Week 8 face up; GET ≠ Yes; sitting cancelled |
| `seat/` | Tauri/Vite desktop experiment | **README only** on disk — no `src/` here |
| `nix/` + `flake.nix` | Kingston / seat host modules | Host tooling |
| `domains/` | Sample Domain folders | **README only** — samples not present |
| `research/speculative/` | Club-cortex / dashboard sketches | Not product |
| `dev/` | ICM stages + receipts | 163 files; archive/lab |

### ARCHIVE / gone / stale pointers

| Claimed path | Disk now |
|--------------|----------|
| `legacy/aether/` | Old Python package (not the CLI) |
| `dev/19_product-receipt-layer/` | Cited in LAB-STATUS + `.context.md` — **absent** |
| `dev/22_tree-org-2026-08-11/` | Cited in `.context.md` — **absent** |
| `dev/11_aether-desk-android-tv/` | Cited in `docs/DESK-REMOVED.md` — **absent** |
| `dev/14_client-one-and-technique/` | Cited in NOT-IMPLEMENTED / SEAT-NIXOS — **absent** |
| `docs/CASUAL-CORE-INTERFACE.md` | CURRENT says **missing** (do not treat as shipped) |
| `seat/` source tree | README describes Tauri app; **no source in this checkout** |

`.context.md` is stale (last distill 2026-08-04, file_count 477, still talks about awareness-agent). It is descriptive, not law.

---

## 3. The protocol you can run today

```bash
aether current              # parsed Objective / Next / Approval
aether current validate     # schema — VALIDATE: OK on this tree
aether preflight <id>       # Next pin
aether probe <id>           # dry would-preflight
aether approve / reject     # human only
aether next <id>            # after APPROVED, re-SELECT
aether demo                 # temp-root loop, never live CURRENT
aether brief / drift        # paste + git dirty
aether panel / shell        # optional cooperative seats
aether seed / garden        # capture; never overrides CURRENT
```

Exit codes: 0 ok/allow · 1 error (or drift dirty) · 2 usage · 3 protocol refuse.

49 git commits on `master`. Protocol alpha waves (unknown-cmd through lab-status, PRs #2–#6) are the last merged identity work. Pocket + ICM people-app + CURRENT repair live as **uncommitted / untracked** working-tree work.

---

## 4. Python surfaces (what they actually do)

| Module | Role | Size |
|--------|------|------|
| `aether_panel.py` | Grok-left / CURRENT-right Project Panel | ~1597 loc |
| `aether_panel_tui.py` | Seat TUI pages (PANEL / SHELL) | ~1622 loc |
| `aether_llm.py` | Shared LLM (Grok TUI, OpenRouter, Groq, Anthropic, Ollama) | ~1395 loc |
| `aether_shell.py` | Domain-bound operator REPL | ~784 loc |
| `aether_shell_agent.py` | Tool loop for `aether shell` | ~577 loc |
| `aether_garden.py` | Propose seed destinations | ~368 loc |
| `aether_pocket.py` | Demo APK / pocket bind; execs real `aether` | ~388 loc |
| `peer_translate_hook.py` | PEER middleman for Grok TUI | ~359 loc |
| `aether_pocket_serve.py` | LAN mum-face; Yes is POST not GET | ~214 loc |
| `aether_rival.py` | Rival Editor v0 | ~139 loc |
| `aether_fs.py` | Shared FS helpers (desk removed) | ~69 loc |

None of these are a second authority store. Panel/shell/pocket **project** CURRENT; they must not replace it.

---

## 5. ICM `dev/` catalog (the built history)

Numbered folders are the agent architecture. They are **not** the product. `dev/README.md` says so.

### Present (16 folders)

| Folder | What was built | State |
|--------|----------------|-------|
| `01_research-grok-heavy-reviews` | Research for `/review-codebase` via Grok Heavy / API | Done receipts |
| `02_test-code-review-command` | `/code-review` design + SuperGrok-rate verification | Done receipts |
| `03_mechanical-codebase-review` | Mechanical codebase-review skill/script | Landed `scripts/codebase_review.py` + `skills/codebase-review/` |
| `04_codebase-review-swarm-mimic` | Swarm-mimic notes | Thin; **no CONTEXT.md** |
| `05_grok-usb-bootstrap` | Full 01–05 ICM pipeline; portable USB | Implement ran; verify/review empty-ish |
| `06_nixos-install` | NixOS install analysis | **PARKED** after 01_analyze |
| `08_v0.2-control-layer` | **This is where v0.2 was born** — truth-reset, CURRENT, preflight ledger, e2e | Done (the product) |
| `09_distribute-alpha` | License, install/CI, onboard, release-notes draft | Done (alpha packaging) |
| `15_mbp-seat-gop-chat` | MBP Alpine seat GOP chat notes | Lab notes; **no CONTEXT** |
| `15_project-control-layer` | PROPOSE for control-layer seats | Thin propose file; **duplicate number 15** |
| `17_client-one-session-three` | Client-one / Session peer reviews | Fragment (`05_review` only) |
| `18_opus5-protocol-completion` | Opus 5 lead + execute; 26 receipts; NEXT-01…10 | Archive of protocol polish |
| `18_protocol-first` | Protocol-first sprint receipt | **Duplicate number 18** |
| `23_mobile-planning-demo` | **Live Next.** Spike weeks 1–8 host; LAN face; sitting cancelled | Resumed-then-parked sitting |
| `24_repair-current-one-next` | Forensics split: human applied CURRENT-A | Done (one Next restored) |
| `25_icm-people-app` | People-app **factory**: discovery + stage map done | Waiting **proceed to 03** |

### Missing numbers (cited elsewhere, not on disk)

`07`, `10`, `11`, `12`, `13`, `14`, `16`, `19`, `20`, `21`, `22`

Known ghosts from docs:

- `11` — aether-desk / Android TV (desk **removed**; see `docs/DESK-REMOVED.md`)
- `14` — client-one + technique / sovereign TUI research
- `19` — product-receipt-layer (PR #5 polish; LAB-STATUS still lists it)
- `22` — tree-org 2026-08-11 (`.context.md` last line)

### Numbering bugs

- Two `15_*` folders.
- Two `18_*` folders.
- Jump 09 → 15 → 17 → 18 → 23 (history compacted or never checked in).
- `23` has weeks `02, 03, 05–08` (no `01` or `04` stage folders).
- `25` has `03–05` CONTEXT files but empty `output/` (not run).

This is why a directory refactor is tempting. The tree **already is** ICM; it is just an uncompacted lab diary.

---

## 6. Live work right now (do not confuse these)

Three things exist at once. Only one is operator Next.

| Thing | Folder | Is it Next? | Status |
|-------|--------|-------------|--------|
| Phone planning demo | `dev/23_mobile-planning-demo/` | **YES** — `CURRENT.md` | Spike host-done through week 8 face; sitting 2026-08-16 cancelled; human must **resume remaining weeks** or **reject** this Next |
| CURRENT split repair | `dev/24_repair-current-one-next/` | No (finished factory) | Human applied option A; probe ALLOW `mobile-planning-demo` |
| People-app factory | `dev/25_icm-people-app/` | No (factory) | 01 discovery + 02 map done. Product of factory = copyable workspace `01_bind → 06_receipt`. Scaffolding not written |
| This understand pass | `dev/26_understand-what-built/` | No (factory) | This file |

CURRENT Limits: if the sitting stays cancelled, human `aether reject` and re-SELECT — do not leave this Next as decoration.

---

## 7. What “refactor the directories ICM” can mean

Three different jobs. Do not mix them.

### A. Compact the lab diary (`dev/`)

Leave shipped paths alone. Relabel / archive / merge numbered stages. Fix LAB-STATUS ghosts. Dedup 15 and 18. Write a one-page `dev/INDEX.md`.

Risk: low if it is propose-then-move with a manifest. Does **not** require changing operator Next if it stays a factory. Still needs a human Yes before any `git mv`.

### B. Continue the people-app factory (`25`)

Already mapped. Next stage there is `03_scaffolding` — empty copyable workspace, not this repo’s layout.

That is **not** “refactor mechanicall-os directories.” It is emit a new tree for a person-with-a-folder.

### C. Re-root the product tree as ICM stages

Make the **repo itself** look like `01_bind/ 02_show-plan/ …`. That would fight PRODUCT: core is `aether` + CURRENT at **project root**, not a numbered pipeline. ICM is how *we develop*; it is not the product layout.

Recommendation from this inventory: **A** if you want a cleaner mechanicall-os; **B** if you want Jake’s people app; **do not do C** as identity.

A fourth thing you did **not** ask this turn, but CURRENT still requires: decide resume vs close `mobile-planning-demo`.

---

## 8. Suggested compact map (propose only — not applied)

If later stage `02_classify` runs, a useful first cut is:

```text
SHIPPED   aether, SPEC-v0.2, PRODUCT, CORE_PRINCIPLES, AGENTS, NOT-IMPLEMENTED, LICENSE
SUPPORT   python/ (except pocket), scripts/ (except A33/pocket), tests/, docs/, examples/, bin/
LAB       android/, python/aether_pocket*.py, scripts/*pocket* *a33*, seat/, nix/, domains/, research/
ARCHIVE   dev/01–09, 15, 17, 18, 24   (receipts)
LIVE LAB  dev/23 (operator Next), dev/25 (factory), this 26 (factory)
LOCAL     .planning/, .aether/, __pycache__
```

Do **not** treat this table as a move list until a later stage writes a path-by-path manifest and you say proceed.

---

## 9. Checkpoint

Edit this file if any row is wrong. Then say one of:

- **proceed to 02** (classify / compact map for *this* factory)
- **proceed to 03** on `dev/25_icm-people-app` (scaffold people-app workspace)
- **resume** `mobile-planning-demo` (operator Next — remaining spike)
- **reject** `mobile-planning-demo` (human `aether reject` — you, not the model)

Silence is not Yes. No directories were moved this turn.
