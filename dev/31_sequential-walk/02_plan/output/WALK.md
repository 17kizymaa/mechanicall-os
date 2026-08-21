# 02_plan WALK — LIVE Plan → Detailed plan → Bind

**Walker:** 02_plan only. Did not start 03/04. Did not implement. Did not `aether approve` / `reject` / `next`. Did not tap Confirm, Yes, Approve, or the Bind **button**. Opening/Bind is not Yes. CURRENT.md untouched.

**When:** 2026-08-19 18:03–18:11 (device clock; capture live this session)  
**CURRENT:** SELECT / REJECTED / Next `people-app-phone-seat` (untouched).

## Live path

```
EDGE=anphuni@100.70.86.90
SERIAL=RZCW2038KHN
PKG=com.mechanicall.pocket.demo
OUT=dev/31_sequential-walk/02_plan/output
```

1. `ssh … "adb -s RZCW2038KHN get-state"` → **`device`**. Live. No glass fallback.
2. App was **not** still on Rooms (01’s overlay had closed). On Home.
3. `am force-stop` + `am start -n com.mechanicall.pocket.demo/.MainActivity` → `Starting: Intent { cmp=com.mechanicall.pocket.demo/.MainActivity }`
4. sleep 1.5s → dump Home. Plan **tile** clickable bounds `[40,1454][530,1579]` center **285,1516**.
5. `input tap 285 1516` → `plan.png` (1080×2400 PNG, 110671 bytes)
6. dump Plan. **Detailed plan** clickable bounds `[40,1804][385,1923]` center **212,1863**.
7. `input tap 212 1863` → `plan-detailed.png` (144844 bytes). Swipe up → `plan-detailed-scroll.png` (190014 bytes).
8. Hamburger `1016,168` → Rooms dump. Bind text bounds `[40,936][1039,1061]` center **539,998**.
9. `input tap 539 998` → Bind screen. Dump folder field. `bind.png` (72081 bytes) = **default bind**, Bind button not tapped.
10. Typed a refuse-operator path into **Your folder** (DEL failed at first; appended). Photographed typing. Restored field to `/storage/emulated/0/mechanicall-pocket` by DEL then retype. **Did not tap Bind / Confirm.** Left on Bind with the demo path in the box.

Glass from `dev/30_modular-seat/` was not used.

---

## What I saw (this session’s PNGs, read as images)

### Plan (`plan.png`, status 18:03 · LTE · 84%)

Title **Plan**. Hamburger top-right. Leftover rounded drawer edge on the far left.

Six cream cards, labels CAPITALISED, bodies sized by length (short tokens huge; the long objective smaller):

| Label | Body |
|--------|------|
| OBJECTIVE | Plan one afternoon of work the client can say Yes to. |
| PHASE | SELECT |
| STATUS | REJECTED |
| BASELINE | demo-sitting |
| NEXT | name-the-outcome |
| APPROVAL | REJECTED |

Outlined chip **Detailed plan** at the bottom. No composer. No model. No folder tree. No files of work. CURRENT fields as a kiosk.

### Detailed plan (`plan-detailed.png` then `plan-detailed-scroll.png`, 18:03–18:04)

Chip flips to **Hide detailed plan**. Below it, a card of **unrendered** CURRENT.md source (`**Objective:**` still has asterisks; `## Keep` is literal hashes). Dump text:

```
# CURRENT

**Objective:** Plan one afternoon of work the client can say Yes to.
**Phase:** SELECT
**Status:** REJECTED
**Baseline:** demo-sitting
**Next:** name-the-outcome
**Approval:** REJECTED

## Keep
- their words on the page
- one Next

## Reject
- a chatbot with no plan
- model-as-authority

## Limits
- this folder is the only law for this sitting
- demo APK — not Mechanicall product

## Next allowed action
Name the outcome in a proposal, then human Yes.

## Approval condition
Human taps Yes on the phone (silence is never permission).

## Prohibited
- automatic-approve
- model-auto-approve
- commit-secrets
```

That is the “plan”: the pocket’s CURRENT.md, pretty-printed as cards then dumped as markdown. It **rejects a chatbot**. It does not query one.

### Bind default (`bind.png`, 18:05)

Title **Bind**. Lecture: *Opening and Bind are not Yes.*

Card:

- Outlined field **Your folder** = `/storage/emulated/0/mechanicall-pocket`
- Outlined button **Bind** (not tapped)
- Status: *This folder is bound. Opening is not a yes.*

No picker. No tree. No SAF. No Confirm. No Yes. Empty cream below. A path box plus a sermon.

### Bind refuse-path (`bind-refuse-typed.png` / `bind-select.png` / `bind-try-select.png`)

Typed `/storage/emulated/0/mechanicall-os` (operator-tree *name*; the tree is not on this phone). First type **appended** onto the demo path (`…/mechanicall-pocket/storage/emulated/0/mechanicall-os`) — a string field, not a directory chooser.

When the box held `/storage/emulated/0/mechanicall-os`: *This folder is not on this phone yet. Bind a folder that exists.*

That is an **existence** check. It is **not** `refuse_if_operator` (“That folder is the operator tree…”). Operator refuse was not live-demonstrable: mechanicall-os is not on the A33. Bind button still not tapped. No Confirm.

### Bind restored (`bind-field-restored.png`, 18:11)

Field put back to `/storage/emulated/0/mechanicall-pocket`. Caption again *This folder is bound. Opening is not a yes.* Bind button not used as Yes.

---

## uiautomator texts (live)

Package: `com.mechanicall.pocket.demo`. No Approve / Confirm / Yes **controls** on Plan or Bind (the word “Yes” appears only inside the lecture copy).

**Plan:** OBJECTIVE, PHASE, STATUS, BASELINE, NEXT, APPROVAL, SELECT, REJECTED, demo-sitting, name-the-outcome, the objective sentence, Detailed plan / Hide detailed plan, Plan, plus the CURRENT.md dump above.

**Rooms (from Plan):** Rooms, Close, Home, Plan, Draft, Decide, Receipt, Bind, Client, PROJECT, CURRENT.md, PROPOSE-CURRENT.md, DECISIONS.md, `.aether/events.jsonl`. Same protocol sitemap as 01. Rooms are not a defence.

**Bind:** Opening and Bind are not Yes. / Your folder / `/storage/emulated/0/mechanicall-pocket` / Bind / This folder is bound. Opening is not a yes.  
After refuse-name type: `/storage/emulated/0/mechanicall-os` / This folder is not on this phone yet. Bind a folder that exists.

Clickable on Bind: the EditText, the Bind button (not tapped), the hamburger.

---

## What failed (harsh, Plan + Bind only)

- Plan never queries a local model. No host, no Ollama, no “thinking”, no structured-support **reply**. The structured thing is CURRENT.md parsed into six cards. The detailed thing is the same file, unrendered. The file itself **rejects** “a chatbot with no plan” and “model-as-authority”. This screen is the anti-chat.
- Size-by-length is a font trick, not intelligence.
- Plan does not open *on* a selected directory’s work. It opens on six protocol fields from a demo pocket. No tree, no file list, no editor of their notes.
- Bind is a string. You type a path. There is no picker, no browse, no preview of the folder. The default is `/storage/emulated/0/mechanicall-pocket` — a pre-bound demo, not “sit on *this* folder I chose.”
- Typing `mechanicall-os` did **not** hit operator-tree refuse. The phone said the folder is not here. Refuse-operator is code on the host; this seat could not show it.
- Hamburger is still Rooms of protocol stages + four authority filenames. Not threads. Not a workspace browser.
- No standard chat-app chrome on this path: no inbox, no composer, no bubbles, no people, no send. Plan is a form. Bind is a form. Detailed plan is a source dump of CURRENT.md.
- Person-to-workspace bridge is inverted: the person is shown CURRENT fields and told Bind is not Yes. The workspace is CURRENT.md again. A bridge would put them in the folder’s work. This puts them in front of the protocol.

Rooms are not a defence. Opening is not Yes. Bind is not Yes.

---

## Definition score (0–5, harsh)

Scored from live Plan / Detailed plan / Bind only. Rooms are not a defence. Opening/Bind is not Yes.

| # | Claim | Score | Why |
|---|--------|------:|-----|
| 1 | Deploys and queries local AI for structured support | **0** | Zero model chrome. Fields come from CURRENT.md. Detailed plan is the same markdown with asterisks showing. The copy **rejects** a chatbot. No prompt, no local-AI status, no structured-support payload. |
| 2 | Opens on a selected directory | **2** | Bind exposes an editable **Your folder** path; Plan reads CURRENT.md from the demo pocket. That is a bound path string, not a selected working directory. No picker, no tree, no files of actual work. Operator-named path → missing-folder, not operator refuse. Demo pocket, not “sit on *this* folder I chose.” |
| 3 | Standard chat-app framework | **0** | Plan = six protocol cards + a markdown dump. Bind = path field + Bind button. Menu = Rooms sitemap. No threads, no composer, no bubbles, no contacts. A kiosk that happens to have a hamburger. |
| 4 | Bridge from person to workspace | **1** | The path box and CURRENT dump are pointers. The person is parked in a lecture (Opening and Bind are not Yes) and a museum of CURRENT.md. A bridge would put the person in conversation with the work in the folder. This puts the person in front of the protocol. |

**Totals:** 0 + 2 + 0 + 1 = **3 / 20**. Fail.

---

Plan is CURRENT.md on cards; Bind is a path box that lectures you. Still not a chat bridge to a folder.
