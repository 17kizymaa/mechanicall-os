# HANDOFF — Kotlin patches that strengthen the core loop

**Not Yes. Not CURRENT paste.** Execution agent: one patch at a time. Recycle SitRackView. Do not start a second chassis. Do not two-tap Yes. Do not bind mechanicall-os. Sync Chaquopy `android/app/src/main/python/aether_pocket.py` whenever you touch `python/aether_pocket.py`.

Active sit: **`0.19.20-inbox-net` vc 45**  
Archive: `~/.mechanicall/apk-archive/mechanicall-0.19.20-inbox-net-vc45.apk`  
Law: `python3 python/app_verify.py` must stay 15/15 (source). `mum_verify` M9 FLAG is iterate, not a fail of protocol.

CURRENT loop to strengthen:

`Goal (bound folder) → Draft NOT ACTIVE → Why → human Yes → quiet One Next → I did it → receipt ↔ send folder`

Keep: she stamps, he runs. Not yet keeps Next. Send ≠ Yes. Open / Bind / banks / GATE are not Decide.

---

## Live map (what the glass actually does)

| Loop beat | Hit | Code | Honest? |
|-----------|-----|------|---------|
| Bind | `BindPaper` / SAF | `startBind` / `bindPath` | Yes. Operator tree refused. Storm-0 SAF often misses — factory, not this patch list. |
| Plan ticket | `Field*` | `draftOrPeek` → `peekPage(n)` | Peek only. Does **not** edit. Does **not** open CRT. `pageIndex` changes for a dest that is never shown. |
| Plan phosphor | `SitHit.Lcd` | `peekPage(0)` | Truncated peek KEEP. `openTerminal()` exists and is **never called**. |
| Draft well | well → `SitHit.Lcd` | `openDraftWriter()` | KEEP from 15: bank stays on NOT ACTIVE plate; well tap opens writer. |
| Draft writer | `IsolatedMode.DRAFT` | `savePropose` on each change | PROPOSE only. KEEP. No extra “buttons” on the plate (cream pills recanted). |
| Why | `WhyStrip` / Decide `Lcd` | `editOnCrt("Why")` | Why lives in the phosphor EditText, not the millwork strip. |
| Yes | `DecidePaper` two-tap | `decideTap` → `FaceBridge.yes` | Correct two-tap + Why-required. After Yes: `labour=true`, stay PLAN. |
| Not yet (Decide) | `DecideNotYet` **or** `BankPlan`/`BankDraft` from Decide | `leaveDecideWithoutYes` → `FaceBridge.notYet` → **`pocket_reject`** | **BUG.** Navigation and product-No rewrite live CURRENT to REJECTED. |
| Labour | `DidIt` / `NotYetFeet` | `didIt` receipt-only; feet Not yet keeps Next | Correct — but UNSEEN until a human Yes. Do not fake Yes to see feet. |
| Receipt | `BankReceipt` | `receiptText` + `stripMd` | Leftover file from earlier sits. Template dumps markdown fields. Useless as “what happened this walk.” |
| Send | `Send` | overlay + `sendStatus` | Dest KEEP. Kotlin status (`none`/`idle`) collides with millwork “files only · not Yes”. |
| CRT dest | `openTerminal` | `IsolatedMode.CRT` on chassis (14) | Dead entry. FIT PARK as first-sit verb; dest is honest **if entered**. |
| JOIN/WAKE | lamps | `openNetworkPlate` | Leftover-lab / inbox. Not the commitment loop. Do not promote to Decide. |

---

## P0 — Not yet must not rewrite CURRENT

**This is the core-loop hole.** CURRENT Keep: “Not yet keeps Next.” “Draft is NOT ACTIVE; CURRENT unchanged until Yes.”

Today:

```631:641:python/aether_pocket.py
def not_yet(...):
    rejected = pocket_reject(pocket, reason)   # writes Status/Approval REJECTED, Phase SELECT
    rec = write_receipt(pocket, said="Not yet", reason=reason)
```

```598:605:MainActivity.kt
private fun leaveDecideWithoutYes() {
    if (rack.plate != SitPlate.DECIDE) return
    ...
    io.execute { FaceBridge.notYet(p, reason) }  // default reason "not yet"
}
```

Callers: `BankPlan`, `BankDraft` (navigation), `DecideNotYet` (product No). Tapping **PLAN** after looking at Decide mutates the bound folder’s CURRENT without Yes.

`did_it` is the correct shape: receipt only, CURRENT bytes identical (`test_did_it_receipt_not_yes`).

`tests/test_aether_pocket.py::test_not_yet_select` **locks the bug** (asserts Status == REJECTED).

### Patch

1. `python/aether_pocket.py` `not_yet` → `return write_receipt(pocket, said="Not yet", reason=reason)` — never `pocket_reject`.
2. Copy the same function into `android/app/src/main/python/aether_pocket.py`.
3. Recant `test_not_yet_select`: CURRENT bytes unchanged; receipt contains “You said Not yet”; Next unchanged.
4. Add `test_leave_decide_without_yes_does_not_reject` (or equivalent) at the Python pocket layer.
5. Kotlin: keep `leaveDecideWithoutYes` calling `notYet` **after** (1), or skip the Python call on bank navigation and only write receipt on `DecideNotYet`. Prefer: **all** Not-yet paths go through the fixed `not_yet` so there is one door.

Do not rename `pocket_reject`. CLI `aether reject` may still exist for humans. The sit must not use it.

**Verify:** `pytest tests/test_aether_pocket.py tests/test_app_verify.py` · `app_verify` 15/15 · never Yes.

**Risk:** low. Aligns sit with `did_it`. Gauntlet G9 already only checks Next string + receipt line.

---

## P1 — Plan phosphor tap should open the CRT dest (or stop pretending)

`openTerminal()` is dead. Plan `Lcd` calls `peekPage(0)`, which sets `isolated = NONE` and only stores `pageIndex`.

`Field*` also `peekPage(n)` — TOC into a dest that never appears. Phosphor stays the ~120 peek. User “click the terminal on the Plan” currently no-ops as a reader.

FIT: CRT dest PARK as a **first-sit verb**. 14 already draws CRT **on the chassis** (`drawCrtDest` blits millwork + `sit_crt`, not IsolatedDark).

### Patch (pick one, do not do both)

**P1a (recommended for this sprint):** Plan `SitHit.Lcd` → `openTerminal()`. Well keys still `peekPage` **then** `openTerminal()` so the ticket TOC opens that heading in the tube. Title / `DismissZoom` returns to peek. Banks still select rooms.

**P1b:** Delete `openTerminal` if CRT stays PARK. Then Plan keys must change phosphor copy to that field’s clip (so peekPage is visible). Today changing `pageIndex` is invisible on the chassis peek because `lcdBody()` uses `idleLine`, not `pages[pageIndex]`.

P1a is the loop patch: Goal is a file you can actually read. P1b is honesty if CRT stays leftover-lab.

**Never:** LcdViewer. IsolatedDark flood. Whole CURRENT on the phosphor peek.

**Verify:** still of Plan → tap glass → CRT on chassis, caption OBJECTIVE/NEXT/…, title dismisses. `look_verify` L2. `app_verify` B11 stays source PASS.

---

## P2 — Send overlay: one line, not `none`

`drawSendOverlay` paints `$status\n$listing` on millwork that already says `files only · not Yes`. `offerStatus` often yields `none` → uidump `SEND overlay none`.

### Patch

- Kotlin: draw **listing only** (or `idle` never `none`). Status belongs in `sendNote` or GATE percent, not on the slip.
- `openSendOverlay`: `sendStatus = offer.status.ifBlank { "idle" }.let { if (it == "none") "idle" else it }`

F3 placement stays human-pinned. Accept ≠ Yes.

---

## P3 — Receipt is a strip of what they said, not a leftover markdown file

`write_receipt` emits a full `# Receipt` markdown page. The well dumps that file (stripMd still leaves a soup). Phosphor peeks 120 chars of the same soup. Leftover `gauntlet-seed` / “Not yet / REJECTED” from earlier storms is **honest for that pocket** and **useless as this walk’s outcome**.

### Patch (Kotlin + optional Python)

- Well: show **one** graphite line: `You said: …` or `(empty receipt)` if no `RECEIPT.md`.
- Phosphor: same one line via existing `clipPreview` + `stripMd`.
- Do not invent “You agreed.” Empty is empty.
- Optional later: `receipt_text` returns the **said** line, not the whole markdown page. That is Python. Do it after P0 so leftover REJECTED receipts stop being produced by navigation.

FIT elevate: “Forward later; not this hole” — still true as millwork. The **loop** patch is the one-line reader, not a new plate.

---

## P4 — Why belongs on the Why strip, not as a second phosphor editor

Decide `Lcd` and `WhyStrip` both `editOnCrt("Why")`, which puts an EditText in the **STATUS tube**. The millwork Why strip is then a dead label.

### Patch

- `WhyStrip` → `editOnCrt` with dest = well strip (new `PackRect` or reuse `fieldObjective` band), **or** keep phosphor Why **only** when the strip is tapped and clip the IME to `isolatedEdit` **inside the well**, not the tube.
- Decide `Lcd` should peek the Why line (`idleLine`), not steal the tube for typing.

Smaller Kotlin than P0/P1. Do after P1 so CRT and Why do not fight the same glass.

---

## P5 — Plan keys are a TOC, not a form (do not “fix” into an editor)

Already written: `17_network_inbox/output/PLAN-VS-DRAFT.md`. Do **not** make `Field*` open the Draft writer. That mixes live law with suggestion.

If millwork still looks like five software buttons, that is a **paint** FLAG (printed headings). Hits stay peeks (and P1a may open CRT at that page).

---

## P6 — Draft plate has no extra buttons (keep it)

15 recanted cream LIVE/PROPOSED pills. Well is one NOT ACTIVE plate; tap opens the whole-file writer. Auto-save `onDraftTextChanged` → `savePropose`. Do **not** add SAVE DRAFT / ALPHA keys. “Appropriate buttons” = **none**; the plate is the door.

If the execution agent is asked for buttons, refuse unless the human stamps a recant of P3/FIT draft well.

---

## P7 — `peekPage` vs `idleLine` (invisible TOC)

Even without P1, Plan field taps are a no-op on glass: `lcdBody()` ignores `pages`. Minimal patch if P1a waits: on PLAN, `idleLine` = clip of `pages[pageIndex].title + body` (still ≤120). Ticket TOC becomes visible on the tube without opening CRT.

Do this **or** P1a, not a third reader.

---

## P8 — Bank leave Decide is inconsistent

`BankPlan` / `BankDraft` call `leaveDecideWithoutYes`. `BankReceipt` does not. After P0 that inconsistency is only “does this navigation write a Not-yet receipt?”

Recommend: **only** `DecideNotYet` writes Not-yet receipt. Bank taps are room changes. Silence is not Not yet. Matches CURRENT: Open/banks are not Decide.

```kotlin
SitHit.BankPlan -> if (face.bound) {
    rack.dismissEdit()
    goBank(SitPlate.PLAN)  // no notYet
}
```

`DecideNotYet` keeps `leaveDecideWithoutYes` (receipt-only after P0) then `goBank(PLAN)`.

---

## Execution order for the agent

1. **P0** (Python `not_yet` + tests + Chaquopy sync). Halt. Human can sit Decide → Plan without nuking CURRENT.
2. **P8** (Kotlin bank leave). Same APK bump is fine if stacked on P0.
3. **P1a or P7** (Plan actually readable). Pick from the sit still of “click the terminal.”
4. **P2** (send `none`).
5. **P3** (receipt one line).
6. **P4** after P1 (Why vs tube).
7. Never P5-as-editor. Never P6 pills. Never Yes. Never L4 nodpi. Never farm-paint `sit_chassis.png`.

Version: bump from `0.19.20-inbox-net` vc 45. One name per halt, e.g. `0.19.21-not-yet-keeps`.

---

## Sit hazards (until P0 lands)

On `0.19.20`, **do not** tap PLAN or DRAFT or Not yet while plate is DECIDE. That path `pocket_reject`s the bound seed. Leave Decide via **RECEIPT bank** or title dismiss (`DismissZoom` does not call `notYet`).

Do not two-tap YES to see labour feet. FLAG UNSEEN.

---

## Out of scope (do not steal this halt)

JOIN/WAKE inbox millwork plate, GATE percent polish, Markwon, SAF bind on storm-0, mum-as-simple-mode, website, Generate, Play, operator-tree bind.
