# REAL-USE — bind → PLAN → DRAFT → SEND (Decide later)

**Not Yes. Not Confirm. Not `aether approve`. Not RZCW2038KHN.**  
Sitter, not engineer. I bound a folder. I want the desk to help change the plan. I will Decide later.

Glass walked: `dev/39_sit-storm-factory/08_execute-nexts/output/draft.png` (chip museum) plus PLAN on the same Next (`08_execute-nexts/output/plan.png`, `10_demo-polish/output/storm-0/home.png`).  
Source walked: `BindModule.kt`, `PlanModule.kt`, `ChatHome.kt`, `SeatNav.kt` `DeskStrip`, `SeatTheme.kt` `DeskStrip`.  
Contract: `BEHAVIOURS.md` B1–B6. Face: FACE-SPEC v2 PLAN/DRAFT (v1 paper still holds).

This file is a sit receipt, not a patch.

---

## Who I am

I am sitting one afternoon folder. I am not the operator tree. I do not have a Headscale key in my pocket. I do not know what `preauth` means. I can read a plan if Objective and Next are first. I can talk to a desk if the paper looks like a plan, not a museum of buttons.

Pitch I was sold: *You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.*

What I came to do: bind → read PLAN → ask the desk on DRAFT → SEND a change → leave DECIDE for later.

---

## Walk

### 1. Bind

Expectation: one folder. System picker. Binding is not Yes. No operator tree.

Source (`BindModule.kt`): FOLDER-only pad — **Choose your folder** (tree picker) and a support path field. Copy: *This sit holds one folder. Name it. Not the operator tree.* *Binding replaces the last project. Not Yes.* After bind, `SeatNav` lands on PLAN (`landingFrom` → `SeatRoute.Plan` unless walk is decide/receipt). Unbound chrome is FOLDER; DIR/FILES and DESK strip are after `projectOn`.

Glass after bind is already the rack (title `mechanicall-pocket`, DIR, FILES). I did not re-walk unbound glass this pass. I did not bind mechanicall-os.

**Stuck?** Typing `/sdcard/…` as “support” is still on the same page as the big pad. A non-engineer will tap **Choose your folder** and hope. That path is the sitting path. I did not treat bind as Yes.

### 2. PLAN — I came to read, then change

Expectation (B2 + FACE-SPEC): published plan. CAPITALISED live fields. **Objective and Next first.** Not a protocol dump as the only page. FACE-SPEC: PLAN is published `CURRENT.md`, read-only as law. B3: I can edit fields on PLAN without chat, and that write is a draft / PROPOSE, never live CURRENT.

Glass (`plan.png` / 10 `home.png` / uidump-plan): the paper is a cream card of raw markdown:

- `# CURRENT`
- `**Objective:**` … `**Next:** name-the-outcome` …
- `## Keep` / `## Reject` …

The dump fills the scroll. First lines I get are “The published plan.” and “Edit in Draft, or SAVE DRAFT here — not Yes.” I do not see SAVE DRAFT. I do not see an OBJECTIVE field. I do not see Next as a thing I can touch. Objective and Next are buried in stars. 08/10 uidump ScrollView children: three nodes — title, note, dump. No PlanField. No SAVE DRAFT.

Source (`PlanModule.kt`) *does* put `OBJECTIVE` / `NEXT` wells **under** that dump, then **SAVE DRAFT · not Yes**, then **Detailed plan**. So the APK I sat is dump-as-the-page. The tree I read still leads with the dump. If I never scroll past `# CURRENT`, I never find the editors. FACE-SPEC said Objective and Next first; the dump is still first.

**Stuck:** I cannot change the plan on PLAN on the glass. The note tells me to Edit in Draft. I go to DRAFT.

### 3. DRAFT — I wanted a workshop

Expectation (B4 + FACE-SPEC): paper workshop. Live vs proposed on the score. Desk proposes. One hunk in focus. Accept/Reject that hunk is not Yes. Last desk say one line. Composer is an instruction for the focused field, not a chat product. SEND = focused hunk.

Glass (`08_execute-nexts/output/draft.png` + uidump-draft): this is the chip museum.

Above the paper, the rack still eats the sit:

- JOIN NOT-ON-NET (grey, disabled)
- WAKE SLEEPING (**gold**, looks like the thing to press)
- SEND FOLDER · not Yes
- paste well: `preauth / login-server · not stored`
- JOIN and WAKE are not Yes.

Then banks: PLAN / **DRAFT** / DECIDE / RECEIPT.

Then the “score” is not paper. It is a FlowRow of heading chips, all at once:

PREAMBLE · OBJECTIVE · PHASE · STATUS · BASELINE  
NEXT · APPROVAL · KEEP · REJECT · LIMITS  
NEXT ALLOWED ACTION · APPROVAL CONDITION · PROHIBITED  
OBSERVATIONS · INFERENCES · UNKNOWNS  
PROPOSED CURRENT CHANGE  
CONFLICTS WITH EXISTING AUTHORITY  
HUMAN DECISION REQUIRED

Purple chips look “on.” Ink chips look dead. OBJECTIVE is boxed purple because it is focused — I only know that because I already knew the code. KEEP and REJECT sit in the same row as NEXT. Those are plan *sections*, not hunk Accept/Reject. FACE-SPEC’s Accept/Reject hunk controls are not on this glass at all.

LIVE is still markdown: `**Objective:** Plan one afternoon of work I can say Yes to.`  
Last desk say is not on this frame (scrolled off or empty). Composer: **Suggest Objective** + **SEND**.

Source (`ChatHome.kt`) still *is* that museum, with a filter: show Objective, Next, and anything that `differs`, else **MORE $hidden**. Glass 08 has no MORE/LESS — every markdown heading from `list_hunks` is a chip. `list_hunks` splits the whole CURRENT by heading, so KEEP/REJECT/LIMITS become buttons. Filter in source would hide some ink chips until MORE; it would still paint PREAMBLE and every purple differs-chip as the face. It is not live-vs-proposed paper. It is a heading picker plus one LIVE card.

**Stuck:** I came to change the plan. I get a museum of the plan’s table of contents. I tap OBJECTIVE because that word matches what I care about. I still cannot see the proposed line next to the live line unless a hunk already differs. On this glass, LIVE is the live Objective with markdown punctuation. No SUGGESTING block. No ACCEPT HUNK.

### 4. JOIN paste well

I wanted the desk. The strip puts a secret box in my face first.

FACE-SPEC v2 still specifies the well (“paste preauth”). 11_ux-polish leftover says the well should be **gone**; provision is backend. Glass still has the well. JOIN is **disabled** until the well is non-blank (08 uidump: JOIN `enabled="false"`; WAKE `enabled="true"`).

What I actually do, as a sitter:

1. I do not have `preauth / login-server`.
2. I will not paste a key I do not understand into a box labelled “not stored.”
3. JOIN stays NOT-ON-NET. I cannot JOIN.
4. WAKE is gold anyway (lab desk probe / USB-LAN). It looks awake. FACE-SPEC: WAKE disabled until connected **or** lab USB/LAN — lab makes the gold lie for a phone sitter. I almost tap WAKE because it is the only lit verb.
5. SEND FOLDER sits next to WAKE. I almost tap that too, because I bound a folder and I want to send it to the desk. Copy says not Yes. Still a SEND.

Source now: `SeatNav` passes `paste = ""`, `onPaste = {}`, `joinAccept(pocket, "")`, `joinEnabled = join.status != "connected"`. The well is being cut. `DeskStrip` still *takes* `paste` / `onPaste`. Glass I sat still *shows* the well. Mid-cut is not a sitting APK.

**Stuck hard here.** The desk I wanted is gated by a paste I cannot perform. The gold WAKE is the trap. JOIN is not Yes — I did not treat it as Yes — but it also is not a path I can walk.

### 5. SEND — talk to the desk, still not Yes

Expectation: type a change to the focused field. SEND asks the desk. GATE strip shows LOAD then STREAM. SEND stays labelled SEND. Writes PROPOSE only. CURRENT does not move. Not Yes.

Glass: composer at the bottom, SEND grey plate. I can type “make the afternoon about naming the outcome” with OBJECTIVE focused and tap SEND.

What I fear from this face:

- Two SENDs: strip **SEND FOLDER · not Yes** vs paper **SEND**. Wrong tap stages an upload, not a suggestion.
- If the desk is not actually up, note becomes “Desk quiet.” GATE stays IDLE lamps. I already stared at gold WAKE.
- LIVE still shows `**Objective:**` so I think I am editing markdown, not a field.
- 28s timeout in source (`SEND_TIMEOUT_MS`). Sitting in silence with no STREAM looks like a dead chat.

Source SEND: `FaceBridge.draftChat(…, focus)` — focused hunk. Busy note: “Desk thinking. GATE is the strip.” Good. I never watched STREAM on this glass (IDLE). I did not open DECIDE. I did not tap Confirm.

### 6. Decide later

DECIDE is a bank on the same row. I can see it. I do not tap it. Two-tap + Why is later. Bind / Send / JOIN / WAKE / DIR / FILES are not Yes. I leave.

---

## Expectation vs APK

| I expected | Glass / APK I sat | Source now (not glass) |
|------------|-------------------|-------------------------|
| FOLDER only until bind | After bind: full rack. Bind overlay via DIR. | Matches B1 after `projectOn` |
| PLAN = Objective + Next first, readable | Markdown dump is the page. Stars, `# CURRENT`, Keep/Reject. | Dump **then** Objective/Next wells + SAVE DRAFT — still dump-first |
| Edit plan on PLAN without chat (B3) | No editors on 08/10 uidump | Editors exist below the dump; write schema draft, not CURRENT |
| DRAFT = paper, live vs proposed | Chip museum of every heading | Same chips; MORE/LESS hides some; still not paper diffs |
| Desk proposes on the focused hunk | Suggest Objective + SEND. No hunk Accept on this frame | Accept/Reject hunk only when `focused.differs` |
| JOIN without me owning a key | Paste well + JOIN disabled empty | Well unwired; JOIN with empty paste; unused `invitePaste` leftover |
| WAKE after the desk is on the net | Gold SLEEPING while JOIN NOT-ON-NET | Still `wakeEnabled = connected \|\| deskOn` — lab probe lights gold |
| One SEND that means “ask the desk” | SEND FOLDER on the strip + SEND on the composer | Same two verbs |
| Decide later | DECIDE visible, not required | Same |

FACE-SPEC “compact rack around the document”: on DRAFT the document never starts. Chips start. The well and three strip verbs sit on every bank.

---

## B1–B6 as I lived them (not a cert)

| id | Sit | Not a Yes |
|----|-----|-----------|
| B1 bind-first | Source: unbound is FOLDER. I bound a folder, not this repo. Unbound glass not re-dumped here. | Not certified |
| B2 plan-readable | **Fail on glass.** Dump is the only page. Objective/Next are markdown inside the dump, not CAPITALISED fields first. | Fail closed for this sit |
| B3 plan-manual-edit | **Fail on glass.** No PLAN fields. Source has wells under the dump — I would still miss them. | Fail on APK I sat |
| B4 draft-is-workshop | **Fail on glass.** Chip museum. Chat-shaped composer+SEND. FACE-SPEC paper diffs absent. | Fail |
| B5 propose-not-current | I did not inspect bytes. SEND is supposed to write PROPOSE. I did not publish. | Unverified this sit |
| B6 decide-only-yes | I did not tap Confirm. I did not treat Bind/Send/JOIN/WAKE/DIR/FILES as Yes. DECIDE left for later. | Not a pass — I just did not Yes |

Walkers never tap Confirm. This walker did not.

---

## Where I get stuck (ordered)

1. **JOIN paste well.** I cannot JOIN. I do not know what to paste. JOIN is dead until I do. The leftover pass wants this well gone; the glass still is the well.
2. **Chip museum.** DRAFT is every CURRENT heading as a button, including KEEP, REJECT, HUMAN DECISION REQUIRED. I lose Objective/Next in the wrap. 07 already “fixed” wrap (FlowRow). Wrap made the museum *taller*, not calmer.
3. **PLAN dump.** I cannot read the plan as fields. I cannot edit it on PLAN on the APK. The note points me to Draft, which is the museum.
4. **Gold WAKE + SEND FOLDER.** Brightest verbs are not “ask the desk about Objective.” I will tap the wrong gold thing when SEND sits quiet.
5. **LIVE still markdown.** `**Objective:**` is not a field. FACE-SPEC wanted live text vs purple suggestion on paper.
6. **Two SENDs.** Folder vs hunk. Both say SEND. Only one is the desk.

---

## Verdict

The sit I wanted: bind a folder, read a plan, ask the desk to suggest a change, leave Yes for later.

The sit I got: bind works as “one folder, not Yes,” then a rack whose DESK strip is a JOIN puzzle, PLAN is a CURRENT dump, DRAFT is a heading-chip museum, and SEND is a chat box under the museum.

**Not Yes.** Do not implement from this file. Do not treat PASS elsewhere as this sit. Paper workshop is still the hole.
