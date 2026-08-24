# DRAFT-RESEARCH — workshop vs protocol museum

**Not CURRENT. Not Yes. Not Confirm. Not A33.**  
Research eval for leftover `11_ux-polish` under live Next `sit-storm-factory`. Does not implement. Does not rewrite authority.

**Question:** Is Draft a document workshop (Google Docs Suggesting / Word Track Changes / Overleaf / HackMD), or a museum of the authority protocol?

**Verdict:** **Protocol museum with workshop verbs glued to the frame.**  
Engine hunk ICM is closer to FACE-SPEC than the glass. B4 can PASS while a sitter cannot work a proposal. That is not a workshop.

---

## What FACE-SPEC asked for

sit-join FACE-SPEC v1 (`dev/37_sit-join-workshop/01_research/output/FACE-SPEC.md`), still law in v2:

> **DRAFT — Suggesting on a proposal copy**  
> - Left/margin: live text (published). Inline: suggested inserts (purple), suggested deletes (strike).  
> - One hunk in focus (heading or selected span). Accept / Reject that hunk → **PROPOSE-CURRENT.md** only.  
> - Accept all remaining = all hunks into PROPOSE, still not Yes.  
> - Composer is **span-scoped instruction**, not a bubble log. SEND = desk inserts suggestions for the **focused hunk** …  
> - Last desk say is one line under the hunk, not a chat history.

v2 (`dev/38_sit-vst-headscale/01_research/output/FACE-SPEC.md`):

> DRAFT = Suggesting on `PROPOSE-CURRENT.md`. Hunk Accept/Reject. SEND = focused hunk. Last desk say one line.

Vendor map they actually selected (decision-tree S5b: document-workshop faces):

> Mode switch: Editing vs **Suggesting**. … Marks: new colour for inserts; strikethrough for deletes … Accept/Reject **one by one** … Mapping: **Plan** = published doc. **Draft** = Suggesting on a **copy**. (`VENDOR-NOTES.md`)

BEHAVIOURS:

| id | Need | Not |
|----|------|-----|
| B4 draft-is-workshop | Draft is a plan workshop: live vs proposed fields. Desk proposes. | Chat-app identity (composer+bubbles as the product) |
| B5 propose-not-current | Draft/Send writes PROPOSE only. CURRENT bytes unchanged until Yes | Model auto-write CURRENT |

B4’s *Not* is “don’t be ChatGPT.” FACE-SPEC’s *Do* is “be Suggesting.” Those are different tests. The scorer only runs the first.

---

## What glass actually is (08 `draft.png`)

Evidence: `/mnt/kingston-nixos-sync/opt/mechanicall-os/dev/39_sit-storm-factory/08_execute-nexts/output/draft.png` and `…/storm-0/uidump-draft.xml` (identical dump at `verify/uidump-draft.xml`). 10_demo-polish has no later Draft PNG.

**Above the fold of the score, Draft is an index of protocol headings, not a document.**

Uidump chip texts, in order (19 atoms):

`PREAMBLE` · `OBJECTIVE` · `PHASE` · `STATUS` · `BASELINE` · `NEXT` · `APPROVAL` · `KEEP` · `REJECT` · `LIMITS` · `NEXT ALLOWED ACTION` · `APPROVAL CONDITION` · `PROHIBITED` · `OBSERVATIONS` · `INFERENCES` · `UNKNOWNS` · `PROPOSED CURRENT CHANGE` · `CONFLICTS WITH EXISTING AUTHORITY` · `HUMAN DECISION REQUIRED`

Then a single card:

> `LIVE`  
> `**Objective:** Plan one afternoon of work I can say Yes to.`

Composer: `Suggest Objective` · `SEND`.

What is **missing from glass** vs FACE-SPEC:

| FACE-SPEC | 08 glass |
|-----------|----------|
| Cream paper with live text as the primary surface | Chip grid occupies ~5 of 6 visible score rows |
| Inline purple inserts / strikethrough deletes | Purple is **chip label colour** when `differs` |
| One hunk in focus *inside the document* | One field card below the museum; markdown source, not rendered paper |
| Accept / Reject on the focused change | **Not on this frame.** Focused OBJECTIVE is ink (does not differ). Accept exists in source only when `focused.differs` |
| Accept all remaining into PROPOSE | **Absent** in `ChatHome.kt` |
| Last desk say **one line under the hunk** | **Absent** from 08 uidump. Source later adds a 4-line history tail, still not under an inline mark |
| Composer = span-scoped instruction | Chat-shaped `OutlinedTextField` + SEND |
| Identity = paper workshop | Identity = labelled schema of CURRENT + proposal-doc template |

07 leftover **chose the museum**: wrap chips so NEXT/APPROVAL stop clipping (`07_chips/output/RECEIPT.md`: “the rest of the hunk ids wrap in full”). That is a protocol-index fix, not a Suggesting fix.

08 VISUAL then scored V3 PASS on “LIVE vs purple suggestion chips; not bubbles.” Non-chat is not yet a workshop.

---

## What ChatHome.kt is now (source, not 08 APK)

`/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/modules/ChatHome.kt`

Partial attempt to hide the museum:

```kotlin
val primary = setOf("Objective", "Next")
val shown = if (more) hunks else hunks.filter { it.id in primary || it.differs }
```

**This does not make a workshop.** `list_hunks` marks `differs` whenever PROPOSE has a non-empty hunk that is not byte-equal to live. `write_schema_draft` emits a full proposal-doc (`## Observations` … `## Human decision required`). Those headings exist only (or differently) on PROPOSE, so they **stay in `shown`**. MORE/LESS is a museum drawer, not a score.

Other source facts:

- SEND does pass `focus` into `FaceBridge.draftChat` — **this is the one FACE-SPEC clause that is wired.**
- Accept copy: `"Keep this suggestion on the proposal"` / `"Hunk kept on PROPOSE. Not Yes."` — protocol-correct, Word-incorrect.
- Reject copy: `"Restore live text into the proposal"` — the only hunk verb that does work.
- `lastSay` from `chatHistory` last non-user turn, `maxLines = 4` — FACE-SPEC said one line under the hunk.
- Composer label now `"Change $focus"` (08 glass still said `"Suggest Objective"`). Still a chat slot.
- No inline insert/delete; no span selection; no Accept-all; no paper body of CURRENT.

Naming collision a paper would flag: a chip **REJECT** (CURRENT heading) sits in the same grammar as **REJECT HUNK** (workshop verb). KEEP likewise. Protocol vocabulary ate the review chrome.

---

## Engine: hunk ICM is a workshop *backend*, not a face

`python/aether_pocket.py`

**`list_hunks`** — live vs proposed, never writes CURRENT:

```python
"differs": bool(pt) and pt != lt
```

Union of `markdown_hunks(CURRENT)` and `markdown_hunks(PROPOSE)`. Splitters are `##` headings **and** `AUTHORITY_FIELDS` (`Objective`…`Approval`). That is why a demo CURRENT plus a schema-draft PROPOSE becomes nineteen chips: six authority fields, Keep/Reject/Limits/… from live CURRENT, plus the proposal-doc template sections from `write_schema_draft`.

**`draft_chat(..., focus=)`** — FACE-SPEC SEND:

- If GATE busy: queue, not Yes.
- If `focus_id` and local stage would be `show-plan`: **promote to propose** (so a natural instruction still writes a hunk).
- Prompt is **this hunk only** + short schema names, not the whole file. Refuses `"refused: whole CURRENT in prompt"`.
- On propose + focus + hunk: `apply_hunk` → PROPOSE only.
- Model `parsed_stage == "propose"` **cannot** promote a question into a write.

**`accept_hunk`** — researchers will hate this honestly:

```python
def accept_hunk(...):
    """Keep the proposed hunk (already on PROPOSE). Not Yes."""
    ...
    text = prop.get(hid) or live.get(hid, "")
    return apply_hunk(root, hid, text)
```

Word Accept applies the mark to the live document and advances to the next change. Here Accept **re-writes the same proposed bytes onto PROPOSE**. Tests prove the only load-bearing claim: CURRENT is unchanged (`test_accept_hunk_is_not_yes`). The control is a protocol bumper sticker, not a review action.

**`reject_hunk`** restores live into PROPOSE. That is the real Suggesting Reject (on the copy).

B5 is the honest pass: Send/hunk/schema never touch CURRENT until Decide. B4 is the dishonest pass: see next section.

`_CHAT_SYS` still opens *“You are a Mechanicall peer on Chat.”* FACE-SPEC identity is paper. The prompt contract leaked the last product.

---

## Why B4 PASS is not evidence of a workshop

`python/app_verify.py`:

```python
has_chips = "AUTHORITY_FIELDS" in chat and (schemaDraft or readSchemaDraft)
has_hunks = "listHunks" in chat and "LIVE" in chat and "DRAFT" in chat
still_thread = "LazyColumn" in chat
b4 = (has_chips or has_hunks) and not still_thread
```

Need text: *“Draft is a plan workshop: live vs proposed fields.”*  
Scorer: *field chips exist and the page is not a message thread.*

08 VERIFICATION: `B4 PASS — DRAFT hunk chips + LIVE; not bubbles (stale 8/10 B4 obsolete)`.  
decision-tree already named the hole: *“B4 can PASS the scorer while you still hate the module.”*

A paper cannot cite B4 as a workshop construct. It is a **negative test for chat identity**. The 08 glass is exactly what that test rewards: many CAPITALISED chips, a LIVE card, no `LazyColumn` bubbles.

Present `ChatHome.kt` may not even contain the substring `"DRAFT"` (it says `SUGGESTING`). `has_hunks` is a brittle contains. Either way, the scorer cannot see inline marks, hunk cursor, Accept-all, or “can a person change Next without reading HUMAN DECISION REQUIRED.”

---

## Mapping: FACE-SPEC clause → evidence → call

| Clause | Engine | Face source | 08 glass | Call |
|--------|--------|-------------|----------|------|
| Suggesting on PROPOSE copy | `apply_hunk` / `write_propose` | copy “on PROPOSE. Not Yes.” | banner “Suggesting on PROPOSE. Accept is not Yes.” | **Protocol OK** |
| Inline inserts / strike deletes | none (plain hunk text) | two stacked cards LIVE / SUGGESTING | LIVE only; purple chips | **Museum** |
| One hunk in focus | `focus` on `draft_chat` | chip selection | OBJECTIVE selected among 19 | **Index, not span** |
| Accept/Reject hunk → PROPOSE | `accept_hunk` no-op keep; `reject_hunk` restore | buttons if `differs` | **not visible** | **Verbs without review UI** |
| Accept all remaining → PROPOSE | none | none | none | **Missing** |
| SEND = focused hunk | `draft_chat(..., focus=)` + hunk prompt | `draftChat(..., focus)` | SEND next to Suggest Objective | **Wired** |
| Last desk say one line under hunk | JSON `say` | 4-line history well | absent | **Not a workshop line** |
| Not a bubble log | jsonl exists; face does not list it | no LazyColumn | no bubbles | **Negative pass** |
| Dump whole CURRENT into 7B | refuse | n/a | n/a | **Engine OK** |
| SEND is not Yes | B5 tests | notes | SEND stays SEND | **Protocol OK** |

**Summary:** authority constraints (B5, not-Yes, focus prompt) are implemented. Document-workshop *interaction* is not. The face visualises the **schema of the protocol** (headings of CURRENT + ICM proposal template) instead of the **score** (the text being suggested).

---

## Verdict (not Yes)

Draft today is a **protocol museum**:

1. **Atoms are headings, not edits.** Nineteen CAPITALISED chips on a demo CURRENT whose published body is six fields and a few sections (`examples/pocket-demo-client/CURRENT.md`). The extra chips (Observations, Inferences, Unknowns, Proposed CURRENT change, Conflicts with existing authority, Human decision required) are the **ICM proposal-doc template leaking onto the face**.
2. **Purple means “this heading exists on PROPOSE,” not “this span is a suggestion.”** FACE-SPEC stole Docs colour for inserts. Glass uses it as an index highlighter.
3. **The document is a caption.** LIVE shows raw `**Objective:** …`. There is no paper body, no strike, no next-change cursor.
4. **Accept does not accept.** It keeps bytes that are already on PROPOSE so that CURRENT stays sacred. That is a correct *authority* move and an incorrect *Suggesting* move. Sitters who know Word will think they published.
5. **07 doubled down on the museum** (wrap every hunk id). 11 CONTEXT already names the leftover: *“Draft = paper workshop (primary fields + diffs), not a chip museum.”* That is a proposal, not law — and it is the right diagnosis.

What *is* a workshop, and should not be thrown out: hunk-scoped SEND, PROPOSE-only writes, refuse-whole-file prompt, Reject-restores-live, GATE as thinking (not `…`). Those are the protocol. They are not the face.

---

## What additional evals a paper would demand

A CHI / CSCW / UIST paper on “local-first authority as document workshop” cannot stop at `app_verify` 10/10. The interesting claim is: **people can negotiate a plan with a model without the model becoming Yes, and without the UI becoming chat.** Current evidence only supports the second half of the second clause.

### 1. Construct validity of B4

- Independent coding of screenshots against FACE-SPEC clauses (table above) by raters who have not seen `app_verify.py`.
- Show that mechanical B4 PASS ≠ workshop code. 08 is the existence proof.
- Replace or supplement B4 with **task-visible** checks: inline mark present; focused hunk is a span in a document; Accept visible iff a mark exists; chip count ≤ k on a demo CURRENT.

### 2. Comparative usability vs the cited vendors (S5b)

Within-subjects, same CURRENT, three skins (not three products):

- **A. Chip museum** (today).
- **B. Dual-pane** live | PROPOSE wells (decision-tree S5 option 1, the rec they overrode).
- **C. Inline Suggesting** on cream paper (FACE-SPEC / S5b selection).

Tasks (must not include Confirm / `aether approve`):

- Change **Next** to a named id.
- Reject a bad Objective suggestion.
- Find whether Approval is live or proposed.

Measures: time, errors, NASA-TLX, System Usability Scale, **and** a mental-model probe: “Did you publish the plan?” after Accept and after SEND. Hypothesis: Accept on today’s face inflates false-Yes.

### 3. Authority comprehension (the actual product)

Forced-choice after a 3-minute sit:

- Which file is law? (`CURRENT.md` vs `PROPOSE-CURRENT.md`)
- Which control publishes? (SEND / ACCEPT HUNK / JOIN / Confirm+Why)
- Does purple mean insert, differs, or “protocol heading”?

If sitters cannot answer, the museum taught the *vocabulary* of the protocol and not the *brake*.

### 4. Scale / information scent

Demo pocket already 19 chips. Operator CURRENT (`CURRENT.md` in this tree) has more `##` sections. Eval: chip count vs heading count on n real pockets; working-memory test (can they still see Objective after wrap?). FACE-SPEC PLAN said CAPITALISED fields are **anchors, not the only atoms**. Draft inverted that: atoms *are* the headings.

Collision test: KEEP / REJECT as **both** document sections and review verbs. Error rates on “reject the suggestion” vs “open the Reject heading.”

### 5. Accessibility (pair with the sibling a11y eval)

TalkBack walk of 19 unlabeled-as-document buttons vs a single WebView/paper with suggestion roles. Focus order: JOIN well and GATE strip currently sit *above* the score; a sitter using a keyboard/IME to SEND never sees Accept. 08 uidump: SEND at y≈2097; LIVE card already clipped; Accept not in hierarchy.

### 6. Prompt / model eval (engine, still needed)

Paper-grade, not vibes:

- Log `draft_chat` prompts on SEND with focus. Assert: no full CURRENT, hunk ≤ `HUNK_MAX_CHARS` (2048), `focus` id matches the chip.
- Instruction fidelity: “shorten Objective” must not rewrite Next (hunk isolation).
- Keyword `chat_stage` vs natural language without focus (focus path currently forces propose — good; unfocused path is still a bag of trigger words: `"draft"`, `"rewrite"`).
- `_CHAT_SYS` “peer on Chat” vs `_CHAT_SYS_HUNK` “one hunk patch” — ablation on identity drift.

### 7. Accept/Reject as interaction, not as file IO

Instrument:

- After SEND, is Accept visible? (today: only if parser wrote a differing hunk)
- Does Accept change any byte a sitter can see besides a toast? (today: no, if PROPOSE already had that hunk)
- Does Reject restore the LIVE card? (yes, if they can find the control)
- Word’s “Accept and move to next” — time-to-next-diff. Today: no next-diff cursor; sitters hunt purple chips.

### 8. Ecological sitting (not emulator-only)

storm-0 1080×2340 at 08 is one viewport. Paper workshop claims fail if IME covers SEND, or if DESK strip + JOIN well steal the first 600 px (uidump JOIN well `[45,498]–[1035,630]`, tabs start y=650, score starts y=760). A workshop eval must measure **score viewport height** after chrome, with IME up.

Never A33. Lab USB/emulator is allowed; do not treat storm-0 PASS as a people-app field study.

### 9. Longitudinal / teaching

Does the museum *onboard* the protocol (maybe useful) or block the first successful propose? First-run: bind → Draft → change Next → see it on PROPOSE → open Decide (do not Confirm in the study). If they never leave the chip grid, the product is a glossary.

### 10. What not to eval as success

- `app_verify` 10/10, `tests/test_aether_pocket.py` hunk cases, 08 VISUAL V3 PASS — these are **non-chat** and **non-Yes**. Cite them as safety, not as workshop validation.
- Imagine mocks. FACE-SPEC: “Imagine-mocks as the spec” is Never.

---

## Recommendation to the leftover (not an implementation, not law)

11 CONTEXT already states the leftover: paper workshop, primary fields + diffs. That matches FACE-SPEC better than 07’s wrap-all-ids.

If a later Next is applied by a human (`examples/propose-current/CURRENT-sit-ux-draft.md` is **proposal, not CURRENT**):

- Stop rendering `markdown_hunks` as the primary surface. Paper first; chips as **jump anchors** for Objective/Next + differing hunks, not for `HUMAN DECISION REQUIRED`.
- Do not emit proposal-doc headings onto the Draft index; or do not `list_hunks` them as chips.
- Put Accept/Reject on the **mark**, always visible when `differs`, with copy that cannot be heard as publish.
- Keep SEND → `draft_chat(focus=)` and B5. Those are the protocol.

Until then: **Draft is a protocol museum that can SEND a focused field.** Researchers would not call that Suggesting.

Silence is never permission. This file is not Yes.
