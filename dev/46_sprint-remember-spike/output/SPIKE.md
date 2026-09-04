# SPIKE — last sprint vs Mechanicall’s three product claims

**Not Yes. Not a new Next.** Sitting: 2026-08-25–26 · `sit-mvp-rack` + pocket `sit-ui-sprint` · A33 `0.18.1-storage` · PR #8.  
**Claims under test** (from `PRODUCT.md`):

1. The **project remembers** (chat is ephemeral; CURRENT + events + artifacts are the trail).
2. The **human decides** (one written plan; yes only you can give; silence ≠ permission).
3. An AI-assisted project is **safe to put down and obvious to resume**.

**Method:** cold-start as of 2026-08-26 after compaction. Read what a stranger would read. Do not treat this chat as memory.

---

## Headline

| Claim | Score | One line |
|-------|-------|----------|
| Project remembers | **PARTIAL — authority FAIL, artifacts PASS** | Plates, FRAMEWORK, skins, APK, PR are on disk. **Live Next is not.** Operator `CURRENT.md` is a proposal sitting in the law slot (`aether current`: Next unset; `validate` FAIL). |
| Human decides | **PROTOCOL YES, GRIND NO** | Models did not `aether approve`. The human *did* steer (Go / kotlin / restore). CURRENT did not record those recants. Preflight allowed with `no_next_pin`. Approvals include `APPROVED` and “Didn’t really read.” |
| Safe to put down / obvious to resume | **FAIL as advertised** | Best resume file is the *other* folder’s handoff, and it is already stale vs the grill. Operator `.continue-here.md` still says `sit-distro-gate` and PR #7. Compaction was required because **chat was the working memory**. |

The last sprint **shipped a face** (SitRackView, millwork, lab archive). It **did not ship project-control**. That is the product.

---

## What the last sprint actually produced (honest inventory)

**On disk and usable**

- Native host: `SitRackView.kt` + `SitCRects.kt` + `LawPages.kt`; `MainActivity` no Compose `setContent` on the rack.
- Pack skins in `drawable-nodpi/sit_{splash,bind,plan,draft,skin}.png` (1080×2138).
- ICM: `dev/45_sit-mvp-rack/` plates / freeze / `02b_native-rack/output/FRAMEWORK.md`.
- Pocket: `/home/anphuni/sit-ui-sprint/` — U-series tree, `01_card-audit/output/CARD-AUDIT.md` (**FAIL, 0 extra-terminal buttons**), overlay layers, unapplied `PROPOSE-CURRENT.md`.
- Lab: `scripts/sit-apk-*`, `sit-look.sh`, `sit-wake.sh`; archive `~/.mechanicall/apk-archive/mechanicall-0.18.1-storage-vc24.apk`.
- Git: PR **https://github.com/17kizymaa/mechanicall-os/pull/8** (`feat/sit-rack-lab`).

**On the phone**

- `versionName=0.18.1-storage` `versionCode=24` (restored after a same-day overlay sideload).

**Not applied as law**

- Operator CURRENT recant (SitRackView host sentence) — still a proposal file **named** `CURRENT.md`.
- Pocket recant U10–U14 (CRT-only glyphs, painted buttons, MECHANICALL title, splash ≥2s) — `PROPOSE-CURRENT.md` Approval **PENDING**.
- Overlay host + splash 2s — assembled on “Go”, then **rolled back**.

---

## Claim 1 — Does the project remember?

PRODUCT: *“Durable project conversations mean: chat is ephemeral unless it lands as CURRENT updates + events + artifacts.”*  
CORE: *Filesystem is the single source of truth.*

### What a cold `aether current` remembers

```
root: mechanicall-os
Objective: (unset)
Next:      (unset)
Status:    APPROVED
Approval:  APPROVED
VALIDATE:  FAIL  (missing Objective, Phase, Next, Keep, Reject, Limits, Prohibited, Next allowed action)
```

Header has **no `**Next:**` field**. Body prose says “Live Next stays `sit-mvp-rack`.” Cold-start docs say: if header and body disagree, **stop**. Here the header is empty and the file *is* a proposal. That is not memory. That is a sticky note glued over the plan.

Last `next_selected` in events: `sit-conjure-desk → sit-mvp-rack` (2026-08-25T18:18Z). After that, the law file was replaced by a proposal and never merged. Events remember the *selection*. CURRENT does not present it as a pin.

### What events remember

830 lines. Counts: **preflight 561**, approve 115, note 58, next_selected 45, reject 24, artifact 24.

Tail is almost all `preflight sit-mvp-rack allowed` with `warn: no_next_pin`. That is a doorbell log, not a resume index. A stranger grepping events learns “we kept asking permission to do the same action after the pin fell off.” They do not learn: overlay recant, card-audit FAIL, rollback to 0.18.1.

### Split brain (two folders, two memories)

| Surface | Says | True of the sitting? |
|---------|------|----------------------|
| Operator CURRENT | Proposal; do not assemble until Go on FRAMEWORK | SitRackView **already implemented** and on the A33 |
| Operator `.continue-here.md` (2026-08-24) | Next `sit-distro-gate`; PR #7 | PR #7 **merged**; Next was re-SELECTED to `sit-mvp-rack` |
| `.context.md` | Root `/home/awareness-agent` | Wrong tree. Sidecar not refreshed |
| Pocket CURRENT | `discuss-sit-ui`; halt assemble; Plan as typeset CURRENT in LCD | Grill recanted typeset paper; U10–U14 **not in this file** |
| Pocket `PROPOSE-CURRENT.md` | CRT-only, MECHANICALL, buttons, splash ≥2s; Approval PENDING | Human stated these; never applied |
| Pocket `.continue-here.md` | Resume in sit-ui-sprint; don’t assemble; title TRANCEFORM still on chassis | Session continued in mechanicall-os anyway |
| Pocket `decision-tree.md` | U1–U25 decided, including U15 paper recant | Richest memory — **not** CURRENT |
| Chat compaction | 3 segments, ~1.5MB, ~1358 turns | Required because files were not the working memory |

**Artifacts remember.** `CARD-AUDIT.md`, `FRAMEWORK.md`, plates, skins, the APK archive, PR #8 — you can `cat` them tomorrow.

**Authority does not.** The one file cold-start *requires* is the one that was sacrificed to a proposal-in-place.

**Verdict:** the project remembers **work**. It does not remember **what to do next**. That is a fail on the product pitch, even though ICM folders did their job.

---

## Claim 2 — Does the human decide?

PRODUCT: *You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.*  
ALPHA-LIMITATIONS (already honest): preflight **cannot** stop an agent that never consults it, or that edits CURRENT.

### What held

- This sitting’s models did **not** run `aether approve` / `aether next`.
- Dual-Next was treated as Reject: UI work moved to a **client pocket** instead of a second operator Next.
- Card-audit halted for human Go. Imagine-as-spec stayed Reject. Camel PNG theft stayed Reject. USB ≠ LTE stayed Reject.
- Human lines that actually steered the face: grill U1–U25, “Go on layers”, “Go assemble”, “Just want kotlin now”, “restore the last apk”, “Pull request”, this spike.

Those are human decisions. They happened in **chat**, not as CURRENT apply.

### What leaked

1. **Yes was cheap.** Last operator approves: `APPROVED`, `...real reason...`, “Didn’t really read sh*t…”, then another `APPROVED`. The gate recorded a human, not a *reason*. SPEC wanted a real reason; the log has a byline.

2. **Preflight without a Next pin still allows.** After CURRENT became a proposal, `aether preflight sit-mvp-rack` → `allowed (no Next pin)`. The cooperative refuse did not fire. Assemble, overlay freeze, and rollback all happened under a warn.

3. **Go vs law.** Pocket CURRENT still prohibits `assemble-before-plate-go`. Card-audit: FAIL, do not freeze. Human then said assemble / kotlin. The agent treated chat Go as permission (correct for a human) and **did not** write that Go into CURRENT. Next agent will read “don’t assemble” and the phone will already have 0.18.1.

4. **Rollback was a human decision the protocol has no verb for.** There is `reject` and `next`. There is now `sit-apk-rollback.sh` (lab). There is no CURRENT event “we un-assembled the overlay.” Events.jsonl has no line for the restore.

5. **Proposal-in-CURRENT is a model-shaped failure the human didn’t clean.** Models are forbidden to overwrite CURRENT. So they left a proposal *as* CURRENT. The human never applied or rejected it. Law became Schrödinger: Status APPROVED, schema FAIL, Next unset.

**Verdict:** the human *can* decide, and did, repeatedly. Mechanicall did **not** make those decisions the plan. The pitch is “under a plan you can read.” By the end of the sprint the readable plan was the wrong document.

---

## Claim 3 — Safe to put down, obvious to resume?

Cold-start checklist (`docs/AGENT-AGNOSTIC-COLD-START.md`): read CURRENT → honour one Next → preflight → never invent a parallel plan.

### Stranger script (what I just did)

```text
cd mechanicall-os
cat CURRENT.md          → a proposal. No header Next. "Do not assemble until Go."
aether current          → Next unset, APPROVED
aether current validate → FAIL
cat .continue-here.md   → sit-distro-gate, PR #7, 2026-08-24
```

If the stranger stops there, they **miss**: SitRackView, pocket grill, card-audit FAIL, overlay rollback, PR #8, APK archive, U10–U14.

If they are lucky they find `/home/anphuni/sit-ui-sprint` — **not in this repo**, not linked from operator CURRENT. That pocket’s CURRENT still says typeset Plan + halt assemble. The handoff says resume *there*. This workspace stayed *here*. Dual-Next Reject produced dual-home.

### Put-down failures this sitting actually hit

| Moment | What should have been enough | What was required |
|--------|------------------------------|-------------------|
| Context compact (~1358 turns) | CURRENT + stage `output/` | Compaction summaries + this chat |
| “Restore the last APK” | `scripts/sit-apk-rollback.sh LAST` | Reconstruct SitRackView from the **conversation** (archive was invented *after* the need) |
| Title MECHANICALL / splash 2s / CRT-only | Pocket CURRENT after apply | Handoff + PROPOSE + decision-tree, none of which `aether current` shows |
| PR | one branch = the sitting | PR #8 is clean; working tree still holds leftover Compose, overlay PNGs, storm dumps, broken CURRENT |

**Safe to put down** would mean: close the TUI, tomorrow `aether current` names the Next and the halt file.  
**Obvious to resume** would mean: one folder, one CURRENT, one “not yet” (e.g. apply PROPOSE or Go imagine-buttons).

Today: two folders, three CURRENT-shaped files (operator proposal, pocket CURRENT, pocket PROPOSE), a stale continue-here, a rich decision-tree nobody’s Next points at, and a phone that is ahead of the law.

**Verdict:** putting it down is safe in the sense that **files don’t vanish**. Resuming is **not obvious**. You have to already know the sitting.

---

## What *did* work (don’t throw the factory)

These pieces matched the pitch and should be kept:

- **ICM stage `output/` halt** — FRAMEWORK.md, CARD-AUDIT.md, plates/layers PREVIEW — a human *can* inspect without the model.
- **Propose file vs CURRENT** — when used as a *sibling* (`.aether/proposals/`, pocket `PROPOSE-CURRENT.md`), the gate is real. The bug was parking a proposal **at** `CURRENT.md`.
- **Client pocket** — correct instinct against dual-Next. Incomplete: operator CURRENT was not parked to a *valid* pin (“Next unset / mesh later”).
- **Sit-lab (end of grind)** — archive + rollback + look that rejects black frames. That is resume-for-binaries. It is not resume-for-law.
- **ALPHA-LIMITATIONS** — already says we don’t sandbox. The sprint proved that document, not the README pitch.

---

## Scores as a stranger would file them

Use these if you want a receipt, not a vibe.

| ID | Question | PASS/FAIL | Evidence |
|----|----------|-----------|----------|
| S1 | One Next on disk | **FAIL** | Operator header Next absent; validate FAIL; preflight `no_next_pin` |
| S2 | CURRENT matches the phone | **FAIL** | Law says don’t assemble; A33 has 0.18.1 SitRackView |
| S3 | Artifacts survive chat death | **PASS** | `dev/45`, pocket plates, PR #8, apk-archive |
| S4 | Events explain the last human recant | **FAIL** | No event for overlay assemble or APK restore; 561 duplicate preflights |
| S5 | Models withheld approve/next | **PASS** | events `by=human` on approve; no model next_selected this sitting |
| S6 | Human Yes is a reason | **FAIL** | `APPROVED` / “Didn’t really read” in the log |
| S7 | Cold start lands the next agent in the right folder | **FAIL** | `.continue-here.md` vs pocket handoff vs this workspace |
| S8 | Unapplied recants are obviously unapplied | **PARTIAL** | PROPOSE says PENDING; operator CURRENT *looks* like law (Status APPROVED) |

**Sprint face:** useful. **Sprint as Mechanicall:** the control layer blinked.

---

## What to do about it (not this spike)

Human picks. Silence is not Go.

1. **Park a real operator CURRENT** — restore a valid schema with header `**Next:** sit-mvp-rack` *or* a parked Next (“none — UI sprint lives in sit-ui-sprint”). Do not leave a proposal in the law slot. Apply or reject `.aether/proposals/CURRENT-proposal-20260825-2114.md`.
2. **Apply or reject pocket `PROPOSE-CURRENT.md`** — U10–U14 are either law or they aren’t. `aether approve` with a real reason, or leave PENDING and stop treating handoff as law.
3. **One resume file** — rewrite operator `.continue-here.md` to: PR #8, A33 `0.18.1-storage`, pocket path, card-audit FAIL, overlay not frozen, “do not assemble until Go imagine-buttons.” Delete or date-stamp the distro-gate compact.
4. **Preflight refuse when Next is unset** — today’s `allowed + warn` is how the grind escaped the plan.
5. **Event the binary** — `sit-apk-archive` / rollback should append `.aether/events.jsonl` (`kind: artifact` or `note`) so restore is greppable.

Not mesh. Not Funnel. Not Imagine-as-spec. Not model-auto-write-current.
