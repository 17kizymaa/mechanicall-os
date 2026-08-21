# 04_gate-client WALK — LIVE Decide (Cancel) → Receipt → Client

**Walker:** 04_gate-client + STORM publisher. Did not implement a redesign. Did not `aether approve` / `reject` / `next`. Did not tap Confirm. Two-tap Approve opened Why; **Cancel** only. Run on Client `current` is not Yes. Operator CURRENT.md untouched.

**When:** 2026-08-19 18:30–18:34 (device clock; capture live this session)  
**CURRENT:** SELECT / REJECTED / Next `people-app-phone-seat` (untouched).

## Live path

```
EDGE=anphuni@100.70.86.90
SERIAL=RZCW2038KHN
PKG=com.mechanicall.pocket.demo
OUT=dev/31_sequential-walk/04_gate-client/output
```

1. `ssh … "adb -s RZCW2038KHN get-state"` → **`device`**. SM-A336B. Live. No glass fallback.
2. `am force-stop` + `am start -n com.mechanicall.pocket.demo/.MainActivity` → `Starting: Intent { cmp=com.mechanicall.pocket.demo/.MainActivity }`
3. sleep 1.5s → dump Home. Decide **tile** clickable bounds `[40,1609][530,1734]` center **285,1671**.
4. `input tap 285 1671` → `decide.png` (1080×2400 PNG, 49725 bytes)
5. Approve clickable `[40,279][1040,418]` center **540,348**. One tap → `decide-armed.png` (*Tap again to approve*).
6. Second tap 540,348 → Why dialog `decide-dialog.png`. Cancel clickable `[502,2102][741,2221]`. Confirm `[761,2102][1020,2221]` **not tapped**.
7. `input tap 621 2161` **Cancel**. Auto-rotate flipped the A33 to landscape and Compose reset to Home (config change). LAST SAID still *You have not said yes yet.* Locked `user_rotation=0` for the rest of the walk; restored `accelerometer_rotation=1` after.
8. Hamburger `1016,168` → Rooms. Receipt `[40,801][1039,926]` → `receipt.png`.
9. Hamburger → Client `[40,1071][1039,1196]` → `client.png`. `current` already selected. Run `[40,727][1040,846]` tapped once (not Yes) → `client-run.png` in ~2.5s.

Glass from `dev/30_modular-seat/` was not used.

---

## What I saw (this session’s PNGs, read as images)

### Decide (`decide.png`, status 18:30 · LTE · 84%)

Title **Decide**. Hamburger top-right. Leftover rounded drawer edge on the far left.

Two pills, nothing else:

- Filled navy **Approve**
- Outlined **Reject**

No CURRENT fields. No folder. No model. No Why yet. No receipt. A gate with no work under it. Cream void to the nav bar.

### Armed (`decide-armed.png`, 18:30)

Same screen. Approve label flipped to **Tap again to approve**. Reject unchanged. Still no Why, no folder, no model.

### Why dialog (`decide-dialog.png`, 18:31)

Scrim over the armed gate. Sheet:

- *Are you sure you want to approve?*
- **Why?**
- Empty multiline box
- Outlined **Cancel** (left) · filled navy **Confirm** (right)

Why is mandatory chrome and empty. Confirm is the `yes()` path. **Cancel only.** Confirm not touched. Opening the dialog is not Yes.

### After Cancel

Dialog gone. LAST SAID on Home still *You have not said yes yet.* Pocket Next still `name-the-outcome`. Operator CURRENT still `people-app-phone-seat`. Rotation reset the activity to Home; that is a config-change, not a Yes.

### Receipt (`receipt.png`, 18:33)

Title **Receipt**. One cream card:

*No decision recorded yet. The machine did not pretend you agreed.*

Empty honesty. No YOU SAID. No timestamp. No folder. No model. Cancel held.

### Client (`client.png`, 18:34)

Title **Client**. Lecture: *This is not Yes.* / *Allowlisted verbs only. This room does not approve, reject, or next.*

Chips: **current** (lavender) · brief · validate · events · drift (verbs / help / status exist in code, clipped off the row). Filled navy **Run**. Empty cream below.

No composer. No people. No directory tree. A verb kiosk for the protocol.

### Run current (`client-run.png`, 18:34)

Run returned in ~2.5s. Card of **unrendered** pocket CURRENT.md (`**Objective:**` still has asterisks; `## Keep` is literal hashes):

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
…
```

Same file Plan already showed as cards and as “detailed plan.” Same file Draft already showed as six boxes. Run is `cat CURRENT.md`. It is **not** a local-model query. It is **not** Yes. Dump text also carries Limits (*demo APK — not Mechanicall product*), Next allowed action (*Name the outcome in a proposal, then human Yes.*), Approval condition (*Human taps Yes on the phone*), Prohibited (`automatic-approve`, `model-auto-approve`, `commit-secrets`).

Swipe on the card did not reveal more (same pixels).

---

## uiautomator texts (live)

Package: `com.mechanicall.pocket.demo`. Confirm existed on the Why dialog and was **not** tapped.

**Decide:** Approve / Tap again to approve / Reject / Decide.

**Dialog:** Are you sure you want to approve? / Why? / Cancel / Confirm. Clickable: Why field, Cancel `[502,2102][741,2221]`, Confirm `[761,2102][1020,2221]`.

**Receipt:** No decision recorded yet. The machine did not pretend you agreed. / Receipt. Only clickable: hamburger.

**Rooms (from Receipt / Client):** Rooms, Close, Home, Plan, Draft, Decide, Receipt, Bind, Client, PROJECT, CURRENT.md, PROPOSE-CURRENT.md, DECISIONS.md, `.aether/events.jsonl`. Same protocol sitemap as 01–03. Rooms are not a defence.

**Client:** Aether client / This is not Yes. / Allowlisted verbs only. This room does not approve, reject, or next. / current brief validate events drift / Run / then the CURRENT.md dump.

---

## What failed (harsh, Decide + Receipt + Client only)

- Decide never queries a local model. Two buttons and a Why box. The structured thing Confirm would write is a human Yes into the pocket, not a model payload. Cancel left nothing.
- Receipt is a single empty sentence. A receipt of a chat app would show the last turn, the files touched, the folder. This shows that the machine did not pretend. Honest. Not a workspace.
- Client Run is the closest thing this walker has to “query.” It printed CURRENT.md. That is `aether current` chrome, not Ollama, not structured support, not on-device AI. The copy on the same screen **rejects a chatbot**.
- None of these rooms open *on* a selected directory’s work. The pocket path is implied (Client reads it). No picker, no tree, no notes, no files of actual work. PROJECT in Rooms is still four protocol filenames.
- No standard chat-app chrome on this path: no inbox, no composer, no bubbles, no people, no send. Decide is a two-tap gate. Receipt is a card. Client is verb chips + Run + a markdown dump.
- Person-to-workspace bridge is inverted again: the person is offered Approve/Reject on nothing they can see, then a sermon that no decision was recorded, then a `cat` of the same CURRENT.md. A bridge would put them in the folder. This puts them in front of the protocol’s lock.

Rooms are not a defence. Opening is not Yes. Cancel is not Yes. Run is not Yes.

---

## Definition score (0–5, harsh)

Scored from live Decide / Receipt / Client + one Run. Rooms are not a defence. Opening is not Yes.

| # | Claim | Score | Why |
|---|--------|------:|-----|
| 1 | Deploys and queries local AI for structured support | **0** | Zero model chrome. Decide is a gate. Receipt is empty. Client Run dumps CURRENT.md from the pocket. No host, no Ollama, no “thinking”, no structured-support payload. |
| 2 | Opens on a selected directory | **2** | Client `current` reads the demo pocket. Same `/storage/emulated/0/mechanicall-pocket` implied since Home. No picker, no tree, no files of actual work. Four protocol names in Rooms. |
| 3 | Standard chat-app framework | **0** | Approve / Reject / Why / empty receipt / verb chips. No threads, no composer, no bubbles, no contacts. A kiosk that happens to have a hamburger. |
| 4 | Bridge from person to workspace | **1** | Cancel proved the gate can refuse. Run proved the pocket file can be printed. The person is still parked in protocol (Yes lecture, CURRENT dump). A bridge would put them in conversation with the work in the folder. |

**Totals:** 0 + 2 + 0 + 1 = **3 / 20**. Fail.

---

Decide is a two-tap lock on an empty room; Receipt is an empty honesty card; Client is `cat CURRENT.md`. Still not a chat bridge to a folder.

Whole-app verdict: `STORM.md`.
