# Ghost-fix list (propose only — do not apply this stage)

Patches for labels that disagree with disk. Human applies later (stage 03+ or a dedicated edit).  
Operator Next unchanged.

---

## A. `docs/LAB-STATUS.md`

**Date line** still `2026-08-09 · polish-product-reciept-layer` (typo + stale). Bump when applied.

### Drop (path does not exist)

| Current row | Action |
|-------------|--------|
| `dev/19_product-receipt-layer/` ARCHIVE | **Delete row.** Note in `dev/18_opus5-protocol-completion/` or CHANGELOG that receipt-layer polish shipped as PR #5 |

### Add (exist; unlisted)

| Path | Tag | Note to add |
|------|-----|-------------|
| `CURRENT.md` | **INSTANCE** | Live Next / Approval; not a factory doc |
| `NOT-IMPLEMENTED.md` | **SHIPPED** | Normative denials (already in DOC-AUTHORITY) |
| `DECISIONS.md` | **INSTANCE** | Append-only log |
| `README.md` · `START-HERE.md` · `ARCHITECTURE.md` · `AUTHORITY.md` · `CHANGELOG.md` · `SPEC-v0.1.md` | **SUPPORT** | Narrative / historical |
| `decision-tree.md` | **INSTANCE** | Grill for current Next |
| `skills/` · `references/` · `.grok/` | **SUPPORT** | Agent factory + prompts |
| `.github/` | **SUPPORT** | CI |
| `python/aether_pocket.py` · `python/aether_pocket_serve.py` | **LAB** | Split out from blanket `python/` SUPPORT |
| `scripts/*pocket*` · `*a33*` · `*via-edge*` | **LAB** | Split out from blanket `scripts/` SUPPORT |
| `examples/pocket-demo-client/` | **LAB** | Bind-off-repo template |
| `dev/23_mobile-planning-demo/` | **LAB** (live) | Operator Next |
| `dev/24_repair-current-one-next/` | **ARCHIVE** | Repair applied |
| `dev/25_icm-people-app/` | **LAB** (live factory) | Not a second Next |
| `dev/26_understand-what-built/` | **LAB** (live factory) | Understand/classify |

### Correct in place

| Row | Fix |
|-----|-----|
| `domains/` “house-tv-desk, minimal-cli” | Samples **not present** — README only. Say so |
| `seat/` “Tauri/Vite seat shell” | **README only** in this checkout — no `src/` |
| `dev/` blanket ARCHIVE/LAB | Keep blanket; add live rows for 23 / 25 / 26 so agents do not archive the Next |

### Keep as-is (still true)

`aether` SHIPPED · SPECs/PRODUCT/PRINCIPLES/AGENTS/LICENSE · `tests/` SUPPORT · `docs/` SUPPORT · `bin/` SUPPORT · `research/` LAB · `android/` LAB · `nix`/`flake`/`shell.nix` LAB · `legacy/` ARCHIVE · `.planning/` LOCAL · `.aether/` INSTANCE · hosted Session LAB.

---

## B. `.context.md`

Stale generated block: `2026-08-04`, `file_count: 477`, still titled awareness-agent in the human README excerpt.

Footer lines to **drop or rewrite** when distilled:

```text
receipt-layer synthesis staged at dev/19_product-receipt-layer/01_analyze/output/
tree-org 2026-08-11: suite docs → dev/22_tree-org-2026-08-11/ (see MANIFEST.md)
```

Replacement (human notes, not generated):

```text
dev/19 and dev/22 are gone from disk. Lab diary index: see
dev/26_understand-what-built/02_classify/output/INDEX.md (draft)
until a human copies it to dev/INDEX.md.
```

Prefer `aether distill` for the generated inventory section rather than hand-editing the `aether:generated` block.

---

## C. Other stale cites (optional, later)

| File | Cite | Fix when convenient |
|------|------|---------------------|
| `docs/DESK-REMOVED.md` | `dev/11_aether-desk-android-tv/` | Keep as historical; mark **absent** |
| `NOT-IMPLEMENTED.md` | `dev/14_client-one-and-technique/...` | Mark **absent** or point at surviving research |
| `docs/SEAT-NIXOS-EFI-FOUNDATION.md` | `dev/14_.../KINGSTON-BOOT-NOW.md` | Same |
| `domains/README.md` | house-tv-desk, minimal-cli | Honest: samples not in tree |
| `seat/README.md` | npm / Tauri run | Honest: no source in this checkout |

Do not hunt every historical path this stage. A–B are the honesty gates.

---

## D. What this file is not

- Not a `git mv` list (that is `03_propose-tree`).
- Not permission to rewrite CURRENT.
- Not permission to archive `dev/23_*`.
