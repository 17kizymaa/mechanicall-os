# 03_draft WALK — LIVE Draft Fields + Chat

**Walker:** 03_draft only. Did not start 04. Did not implement. Did not `aether approve` / `reject` / `next`. Did not tap Confirm, Yes, Approve, or **Save**. Opening is not Yes. CURRENT.md untouched.

**When:** 2026-08-19 18:19–18:25 (device clock; capture live this session)  
**CURRENT:** SELECT / REJECTED / Next `people-app-phone-seat` (untouched).

## Live path

```
EDGE=anphuni@100.70.86.90
SERIAL=RZCW2038KHN
PKG=com.mechanicall.pocket.demo
OUT=dev/31_sequential-walk/03_draft/output
```

1. `ssh … "adb -s RZCW2038KHN get-state"` → **`device`**. Live. SM-A336B. No glass fallback.
2. App was on Home after 02. `am force-stop` + `am start -n com.mechanicall.pocket.demo/.MainActivity` → `Starting: Intent { cmp=com.mechanicall.pocket.demo/.MainActivity }`
3. sleep 1.5s → dump Home. Draft **tile** clickable bounds `[550,1454][1040,1579]` center **795,1516**.
4. `input tap 795 1516` → `draft.png` (1080×2400 PNG, 133411 bytes)
5. Swipe up → `draft-chat.png` (126945 bytes). Host field **`http://100.90.85.68:11434`** (`Desk model (private network)`).
6. Confirmed Send cannot call `yes()`: `DraftModule` → `FaceBridge.draftChat` → `draft_chat()` writes **PROPOSE only**. `yes()` is a different bridge used by Decide. Tapped Message, typed `note only`, dismissed IME, `input tap 540 2151` **Send once**.
7. ~2s → `draft-send-wait.png`: *Waiting for a reply. This is not Yes.* Save and Send greyed. Still *No draft chat yet.*
8. >20s still waiting → `draft-send-hang.png`. **Stopped** per contract. No reply. No PROPOSE on glass. No `yes()`.
9. Scrolled to top. Tapped Fields chip (132,457) then Chat chip (326,457). `draft-fields-off.png` then `draft-empty.png` (*Show Fields or Chat.*).

Glass from `dev/30_modular-seat/` was not used.

---

## What I saw (this session’s PNGs, read as images)

### Draft (`draft.png`, status 18:19 · LTE · 84%)

Title **Draft**. Hamburger top-right. Leftover rounded drawer edge on the far left.

Lecture, not a session: *This is a proposal. Saving it does not change the plan. Save is not Yes.*

Two chips, both selected (lavender): **Fields** · **Chat**.

**FIELDS** card: *Locked schema. Edits go to a draft, not the plan.* Six outlined CURRENT boxes, same kiosk as Plan:

| Label | Body |
|--------|------|
| Objective | Plan one afternoon of work the client can say Yes to. |
| Phase | SELECT |
| Status | REJECTED |
| Baseline | demo-sitting |
| Next | name-the-outcome |
| Approval | REJECTED |

Filled navy **Save** (not tapped). Bottom of the frame peeks **CHAT** and *Draft on draft. Chat writes a proposal, not the plan.* — the closet under the form.

No bubbles. No threads. No people. No last-message preview. A CURRENT form that happens to have a Chat chip.

### Chat closet (`draft-chat.png`, 18:20)

Swipe did not leave Draft. The form tail is still on screen (Phase…Approval, Save). Then the **CHAT** card:

- *Draft on draft. Chat writes a proposal, not the plan.*
- **No draft chat yet.**
- Outlined **Desk model (private network)** = `http://100.90.85.68:11434` (hardcoded desk / tailnet Ollama, not a model picker, not a local-on-phone model).
- Empty **Message** box.
- Outlined **Send**.

That is the entire “chat app”: a URL field, a textarea, a Send. History is a sentence that says there is none. Roles in code would dump as `USER` / `ASSISTANT` labels plus raw text — a log, not bubbles. No thread list. No inbox. Chat sits *under* the schema form and can be toggled off.

### Send once (`draft-typed.png` → `draft-send-wait.png` → `draft-send-hang.png`, 18:21–18:24)

Typed **note only** (short; propose-shaped; not Yes). IME covered Send until BACK dismissed it. Message still held `note only`.

Tap Send:

- *Waiting for a reply. This is not Yes.*
- Save grey. Send grey.
- History still **No draft chat yet.**
- Host still `http://100.90.85.68:11434`.
- Composer did **not** clear (busy path; message stayed).

At 18:24 — more than 20s — still waiting. Screenshot `draft-send-hang.png` and **stopped**. No model reply. No structured-support payload. No PROPOSE text on glass. No Confirm. No Yes.

The desk host did not answer the phone in time. The “query local AI” path exists as a wait sermon. Live, it is a hang.

### Fields off (`draft-fields-off.png`, 18:25)

Fields chip outlined (off). Chat still lavender. Form gone. Only the CHAT card remains: same host, same `note only`, Send still grey, still *Waiting for a reply. This is not Yes.* Chat without the form is still a host+textarea closet, not a chat app.

### Empty (`draft-empty.png`, 18:25)

Both chips off (outlined). Cream void. Lecture remains. Prompt: **Show Fields or Chat.**

That is the product with both closets shut: a title, a sermon, two toggles, and empty space. A standard chat app cannot be turned off until the screen says “show chat.” Chat is optional chrome on a CURRENT form.

---

## uiautomator texts (live)

Package: `com.mechanicall.pocket.demo`. No Approve / Confirm / Yes **controls** on Draft (the word “Yes” appears only inside lecture copy: *Save is not Yes*, *Waiting for a reply. This is not Yes.*, *the client can say Yes to.*). Save was not tapped. Send was tapped once.

**Draft (top):** This is a proposal. Saving it does not change the plan. Save is not Yes. / Fields / Chat / FIELDS / Locked schema. Edits go to a draft, not the plan. / Objective, Phase, Status, Baseline, Next, Approval / the six CURRENT values / Save / CHAT / Draft on draft. Chat writes a proposal, not the plan.

**Chat (scrolled):** No draft chat yet. / Desk model (private network) / `http://100.90.85.68:11434` / Message / Send.

**After Send:** Waiting for a reply. This is not Yes. History still *No draft chat yet.* Message still `note only`.

**Empty:** Fields / Chat / Show Fields or Chat.

Clickable on Draft: the six schema EditTexts, Save (not tapped), host EditText, Message EditText, Send (tapped once), hamburger. FilterChips are tappable even when dump marks the labels `clickable=false`.

---

## What failed (harsh, Draft only)

- This is a **CURRENT form with a chat closet**, not a standard chat app. Fields is six protocol boxes + Save. Chat is a card you scroll to, then can hide. Empty state is “show the form or the closet.” Rooms are not a defence. Opening is not Yes.
- “Queries the local AI for structured support” is a wait line. Send hung >20s on `http://100.90.85.68:11434`. No reply. No proposal text. History still empty. The structured thing on screen is CURRENT.md in text fields, same as Plan, not a model payload.
- Host is a **desk IP typed into a form**, default `100.90.85.68:11434`. Not on-device. Not a model roster. Not “the product is the local model.” The model is a private-network URL you can edit. The product is the schema.
- Composer exists. That is the only chat-app chrome. No inbox, no threads, no bubbles, no people, no last-message list, no pinned composer-as-home. History, if it ever filled, is `role.uppercase()` plus body — a log dump.
- Chat **must write PROPOSE only**. Code path is `draft_chat` → `write_propose`. Live, it wrote nothing visible: hang, then stop. We did not get a PROPOSE on glass. We also did not get a Yes. Send is not Yes. Waiting is not Yes.
- Draft does not open *on* a selected directory’s work. It opens on the same six pocket fields Plan already showed. No tree. No notes. No files of actual work. The bound path is implied, not shown as a workspace.
- Person-to-workspace bridge is inverted again: the person is lectured (*Save is not Yes* / *Chat writes a proposal, not the plan* / *Waiting for a reply. This is not Yes.*) and parked in CURRENT fields. A bridge would put them in conversation with the folder. This puts them in front of the protocol, with a closet that times out to the desk.

Rooms are not a defence. Opening is not Yes. Send is not Yes.

---

## Definition score (0–5, harsh)

Scored from live Draft Fields + Chat + one Send + empty toggle. Rooms are not a defence. Opening is not Yes.

| # | Claim | Score | Why |
|---|--------|------:|-----|
| 1 | Deploys and queries local AI for structured support | **1** | Host + Send exist and did enter *Waiting for a reply.* That is more chrome than Plan. Live query **hung >20s**. No reply. No structured-support payload. The structure on screen is CURRENT.md in six boxes. Desk Ollama did not answer. |
| 2 | Opens on a selected directory | **2** | Same as 02: demo pocket implied. Schema is CURRENT from `/storage/emulated/0/mechanicall-pocket`. No picker, no tree, no files of work. Host is a URL, not a folder. |
| 3 | Standard chat-app framework | **1** | Composer + Send exist. Everything else is missing: no threads, no bubbles, no inbox, no people, no pinned chat-as-home. Chat is a **FilterChip closet** under a CURRENT form and can be switched off until the screen is empty. A form with a chat closet is not a chat app. |
| 4 | Bridge from person to workspace | **1** | Copy claims chat writes a proposal, not the plan. Live Send never delivered a proposal. The person is lectured and left in schema fields. The workspace is still CURRENT/PROPOSE protocol, not the folder’s work. |

**Totals:** 1 + 2 + 1 + 1 = **5 / 20**. Fail.

---

Draft is CURRENT.md in editable boxes; Chat is a host+textarea closet that hung. Still not a chat bridge to a folder.
