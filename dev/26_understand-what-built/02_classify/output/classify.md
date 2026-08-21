# Classify — compact map (propose only)

**When:** 2026-08-18  
**From:** `01_inventory/output/inventory.md` + live disk vs `docs/LAB-STATUS.md`  
**Operator Next (unchanged):** `mobile-planning-demo`  
**Not this file:** no `git mv`, no LAB-STATUS edit, no CURRENT rewrite.

Vocabulary stays the LAB-STATUS set. One extra **bucket** column for `dev/` only: `archive` (done diary) vs `live` (open factory or operator Next).

| Tag | Meaning (unchanged) |
|-----|---------------------|
| **SHIPPED** | v0.2 core surface; SPEC / PRODUCT |
| **SUPPORT** | Helpers on the same law; not the product definition alone |
| **LAB** | Experimental / incomplete; may vanish |
| **ARCHIVE** | Historical ICM receipts; Layer-4 only |
| **LOCAL** | Machine / tooling noise; often gitignored |
| **INSTANCE** | This checkout’s live state (CURRENT, events) — not a factory doc |

---

## 1. Root — path by path

### INSTANCE (this folder’s law and receipts)

| Path | Tag | Note |
|------|-----|------|
| `CURRENT.md` | **INSTANCE** | Sole live Next. Missing from LAB-STATUS table — add as INSTANCE, not SHIPPED factory text |
| `DECISIONS.md` | **INSTANCE** | Append-only human log |
| `decision-tree.md` | **INSTANCE** | Closed grill for this Next (phone demo) |
| `.aether/` | **INSTANCE** | events, preflight receipts, proposals, hooks |
| `.context.md` | **INSTANCE** | Descriptive; **stale** (2026-08-04 awareness-agent). Not law |

### SHIPPED (protocol identity)

| Path | Tag | Note |
|------|-----|------|
| `aether` | **SHIPPED** | POSIX CLI v0.2 (~2065 lines) |
| `SPEC-v0.2.md` | **SHIPPED** | Protocol contract |
| `PRODUCT.md` | **SHIPPED** | Core vs lab vs research |
| `CORE_PRINCIPLES.md` | **SHIPPED** | Filesystem truth |
| `AGENTS.md` | **SHIPPED** | CURRENT-first; models never approve |
| `NOT-IMPLEMENTED.md` | **SHIPPED** | Denials — **unlisted in LAB-STATUS**; DOC-AUTHORITY already NORMATIVE |
| `LICENSE` | **SHIPPED** | Apache-2.0 |

### SUPPORT (same law, not the definition)

| Path | Tag | Note |
|------|-----|------|
| `bin/aether` | **SUPPORT** | Symlink → `../aether` |
| `python/` (except pocket files) | **SUPPORT** | panel, shell, llm, garden, rival, fs, peer hook |
| `scripts/` (except pocket / A33 / edge) | **SUPPORT** | install, demo, CI, completion, codebase-review |
| `tests/` | **SUPPORT** | Includes pocket tests — tests of lab still support the repo |
| `docs/` | **SUPPORT** | Mixed NORMATIVE / NON-NORMATIVE — see DOC-AUTHORITY. A few files are LAB narrative (below) |
| `examples/alpha-demo/` | **SUPPORT** | Protocol demo |
| `examples/reel-control/` | **SUPPORT** | v0.2 stop-before-spiral |
| `examples/dev-task/` | **SUPPORT** | Non-reel authority sample |
| `examples/propose-current/` | **SUPPORT** | PROPOSE template + this-Next propose file |
| `examples/sidecars/` | **SUPPORT** | Sidecar sample |
| `README.md` | **SUPPORT** | Entry narrative (NON-NORMATIVE) |
| `START-HERE.md` | **SUPPORT** | Read-order routing |
| `ARCHITECTURE.md` | **SUPPORT** | Sketch (NON-NORMATIVE) |
| `AUTHORITY.md` | **SUPPORT** | Doctrine essay (NON-NORMATIVE) |
| `CHANGELOG.md` | **SUPPORT** | Narrative history |
| `SPEC-v0.1.md` | **SUPPORT** | Historical awareness spec |
| `.github/workflows/test.yml` | **SUPPORT** | CI |
| `skills/` | **SUPPORT** | `codebase-review`, `rival-editor` |
| `.grok/skills/meta-agent/` | **SUPPORT** | ICM factory for agents in this repo |
| `.grok/hooks/` | **SUPPORT** | Grok TUI aether brief hooks |
| `references/` | **SUPPORT** | Agent / swarm / personal-llm prompts — not authority |

### LAB (real, not core)

| Path | Tag | Note |
|------|-----|------|
| `android/` | **LAB** | Sideload pocket APK chrome |
| `python/aether_pocket.py` | **LAB** | Pocket bind; execs real `aether` |
| `python/aether_pocket_serve.py` | **LAB** | LAN face; GET ≠ Yes |
| `scripts/aether-on-a33.sh` | **LAB** | Phone host |
| `scripts/agent-edit-a33.sh` | **LAB** | Phone editor |
| `scripts/pocket-refuse-root.sh` | **LAB** | Refuse operator tree |
| `scripts/push-aether-via-edge.sh` | **LAB** | USB via mbp-edge |
| `scripts/push-pocket-via-edge.sh` | **LAB** | Pocket copy via edge |
| `scripts/rehearse-pocket-spike.sh` | **LAB** | Week-7 host rehearsal |
| `scripts/serve-pocket-face.sh` | **LAB** | `:8765` face |
| `scripts/sync-pocket-engine.sh` | **LAB** | Engine sync |
| `examples/pocket-demo-client/` | **LAB** | Copy **off** this repo onto the phone |
| `docs/SINGLE-APP-DISTRIBUTION.md` | **LAB** | Incomplete casual packaging |
| `seat/` | **LAB** | README only — no Tauri `src/` in this checkout |
| `nix/` · `flake.nix` · `flake.lock` · `shell.nix` | **LAB** | Kingston / seat host tooling |
| `domains/` | **LAB** | README only — sample Domains not present |
| `research/` · `research/speculative/` | **LAB** | Not product claims |
| `docs/CASUAL-CORE-INTERFACE.md` | **LAB** (missing) | CURRENT says do not treat as shipped |

### ARCHIVE

| Path | Tag | Note |
|------|-----|------|
| `legacy/` | **ARCHIVE** | Old Python package; not the CLI |
| `dev/` (as a whole) | **ARCHIVE** / **LAB** | See §2 for per-folder bucket |
| `docs/DESK-REMOVED.md` | **ARCHIVE** | Points at ghost `dev/11_*` |

### LOCAL

| Path | Tag | Note |
|------|-----|------|
| `.planning/` | **LOCAL** | GSD forensics leftover; not a GSD product repo |
| `.memory/` | **LOCAL** | Optional recall fragment |
| `.envrc.example` | **LOCAL** | Direnv hint |
| `.gitignore` | **LOCAL** | Tooling |
| `__pycache__/` · `.pytest_cache/` | **LOCAL** | Build noise |
| `result` · `result-vm` · `*.qcow2` | **LOCAL** | Cited by LAB-STATUS; not in this listing |

---

## 2. `dev/` — every folder

`dev/README.md` already says: not SPEC, not the product, may be compacted. That stands.

| Folder | Tag | Bucket | One line |
|--------|-----|--------|----------|
| `01_research-grok-heavy-reviews` | **ARCHIVE** | archive | Grok Heavy review research |
| `02_test-code-review-command` | **ARCHIVE** | archive | `/code-review` design |
| `03_mechanical-codebase-review` | **ARCHIVE** | archive | Landed `scripts/codebase_review.py` |
| `04_codebase-review-swarm-mimic` | **ARCHIVE** | archive | Thin; no CONTEXT |
| `05_grok-usb-bootstrap` | **ARCHIVE** | archive | Portable USB pipeline |
| `06_nixos-install` | **ARCHIVE** | archive | **PARKED** after analyze |
| `08_v0.2-control-layer` | **ARCHIVE** | archive | Where v0.2 was born — keep findable |
| `09_distribute-alpha` | **ARCHIVE** | archive | Alpha packaging receipts |
| `15_mbp-seat-gop-chat` | **ARCHIVE** | archive | MBP GOP notes; no CONTEXT |
| `15_project-control-layer` | **ARCHIVE** | archive | Duplicate number 15; one PROPOSE |
| `17_client-one-session-three` | **ARCHIVE** | archive | Peer-review fragment |
| `18_opus5-protocol-completion` | **ARCHIVE** | archive | Opus NEXT-01…10 receipts |
| `18_protocol-first` | **ARCHIVE** | archive | Duplicate number 18; one RECEIPT |
| `23_mobile-planning-demo` | **LAB** | **live** | **Operator Next.** Do not archive this Next |
| `24_repair-current-one-next` | **ARCHIVE** | archive | Repair applied; factory closed |
| `25_icm-people-app` | **LAB** | **live** | Factory; waiting proceed-to-03 *there* |
| `26_understand-what-built` | **LAB** | **live** | This factory. Compact later with the diary |

### Ghosts (cited, not on disk)

| Cited path | Cited by | Classify as |
|------------|----------|-------------|
| `dev/07_*` | numbering gap only | never on disk here — do not invent |
| `dev/10_*` … `dev/13_*` | numbering gap | same |
| `dev/11_aether-desk-android-tv/` | `docs/DESK-REMOVED.md` | **GHOST** — keep the DESK-REMOVED note; drop live path claims |
| `dev/14_client-one-and-technique/` | NOT-IMPLEMENTED, SEAT-NIXOS | **GHOST** — cite as historical if needed |
| `dev/16_*` | numbering gap | never on disk |
| `dev/19_product-receipt-layer/` | LAB-STATUS, `.context.md` | **GHOST** — work landed as PR #5; folder gone |
| `dev/20_*` · `dev/21_*` | numbering gap | never on disk |
| `dev/22_tree-org-2026-08-11/` | `.context.md` | **GHOST** — prior compact attempt; MANIFEST gone |

Do **not** recreate ghosts. Fix the pointers (see `ghost-fix.md`).

---

## 3. Mixed directories (do not move yet)

These stay where they are until `03_propose-tree` writes a manifest. Classification only:

| Directory | Rule |
|-----------|------|
| `python/` | Keep one folder. Tag pocket modules LAB in LAB-STATUS; do not split the package this Next |
| `scripts/` | Keep one folder. Tag `*pocket*`, `*a33*`, `*via-edge*` as LAB |
| `examples/` | Keep one folder. Tag `pocket-demo-client` LAB |
| `docs/` | Keep one folder. DOC-AUTHORITY already splits NORMATIVE vs narrative |
| `tests/` | Keep one folder. Pocket tests stay SUPPORT (they guard the lab contract) |
| `dev/` | Keep one folder. INDEX (this stage’s `INDEX.md`) is the compact map, not a rename |

**Do not do identity C** (re-root the product as `01_bind/` …). Core stays at repo root.

---

## 4. What a later move list may touch (preview, not a manifest)

`03_propose-tree` should consider **only**:

1. Write `dev/INDEX.md` (copy of this stage’s `INDEX.md` after you edit it).
2. Patch `docs/LAB-STATUS.md` from `ghost-fix.md` (drop `19`, add missing INSTANCE/SHIPPED/unlisted, split pocket files).
3. Optionally append a one-line distill note to `.context.md` (or run `aether distill`) so it stops citing `19` / `22`.
4. Optionally rename the duplicate `15_*` / `18_*` **in place** to unique numbers — only if you want numbers unique. Not required for honesty. INDEX is enough.
5. Do **not** move `23`, `25`, or `26` this cycle.
6. Do **not** move `aether`, `python/`, `docs/`, or `CURRENT.md`.

---

## 5. Checkpoint

Edit any row that is wrong. Then:

- **proceed to 03** — write a propose-only `MANIFEST.md` / `PROPOSE.md` (still no moves until you apply)
- **stop** — keep this map; do not propose moves
- **proceed to 03** on `dev/25_*` — different factory (people-app scaffold)
- **resume** / **reject** `mobile-planning-demo` — operator Next; you, not the model

Silence is not Yes. No directories were moved this turn.
