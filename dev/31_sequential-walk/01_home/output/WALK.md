# 01_home WALK — LIVE splash → home → hamburger

**Walker:** 01_home only. Did not start 02/03/04. Did not implement. Did not `aether approve` / `reject` / `next`. Did not tap Confirm, Yes, or Approve. Did not tap any tile. Menu left on Rooms list (not a Confirm path).

**When:** 2026-08-19 17:54 (device clock; capture live this session)  
**CURRENT:** SELECT / REJECTED / Next `people-app-phone-seat` (untouched).

## Live path

```
EDGE=anphuni@100.70.86.90
SERIAL=RZCW2038KHN
PKG=com.mechanicall.pocket.demo
OUT=dev/31_sequential-walk/01_home/output
```

1. `ssh … "adb -s RZCW2038KHN get-state"` → **`device`**. Live. No kill-server needed.
2. `am force-stop com.mechanicall.pocket.demo`
3. `am start -n com.mechanicall.pocket.demo/.MainActivity` → `Starting: Intent { cmp=com.mechanicall.pocket.demo/.MainActivity }`
4. sleep 0.35 → `exec-out screencap -p` → `splash.png` (1080×2400 PNG, 112376 bytes)
5. sleep 1.2 → `home.png` (1080×2400 PNG, 146871 bytes)
6. `input tap 1016 168` (hamburger, three lines top-right) → `menu.png` (1080×2400 PNG, 84301 bytes)
7. `uiautomator dump /sdcard/uidump.xml` while menu still open → `uidump.xml`

This overwrites the prior **BLOCKED-LIVE** receipt. Glass from `dev/30_modular-seat/` was not used.

---

## What I saw (this session’s PNGs, read as images)

### Splash (`splash.png`, status 17:54 · LTE · 84%)

Cream field. Centered navy chair-at-desk mark in a cream tile on a beige square. No wordmark, no “Mechanicall”, no folder, no composer, no model name, no “thinking”, no structured-support form. A leftover rounded edge peeks at the far left (drawer ghost). Opening is a logo. Opening is not Yes.

### Home (`home.png`, 17:54)

Title **Home**. Three-line hamburger top-right.

- Same chair mark, then wordmark **Mechanicall**.
- Lecture, not a session: *Opening this app is not a yes. Only Yes is.*
- **FOLDER** card: `/storage/emulated/0/mechanicall-pocket` — *This folder is bound. Opening is not a yes.* A printed bind claim. Not a directory picker. Not a tree. Not a selected working copy of *their* work.
- **NEXT** card: `name-the-outcome` (action-id, not a chat thread, not a local-model query).
- **LAST SAID** card: *You have not said yes yet.* Human Yes ledger. Not last model reply. Not structured support.
- Six tiles, two columns: **Plan · Draft · Decide · Receipt · Bind · Client**. Protocol sitemap. No composer. No bubbles. No conversation list. No “ask the local model”. No people.

### Hamburger / Rooms (`menu.png`, 17:54)

Tap 1016,168 opened a full-screen sheet titled **Rooms**. **Close** top-right (not tapped).

Nav (Home bold / selected): Home, Plan, Draft, Decide, Receipt, Bind, Client.

Then **PROJECT**: `CURRENT.md`, `PROPOSE-CURRENT.md`, `DECISIONS.md`, `.aether/events.jsonl`.

That is the bound “workspace” as shown: four protocol files. No source tree, no notes, no selected-directory listing of actual work. Rooms are not a defence. No Approve / Confirm / Yes on this sheet.

---

## uiautomator texts (live, menu open)

Package: `com.mechanicall.pocket.demo`. No content-desc. No Approve / Confirm / Yes.

Visible `text=`:

- Rooms
- Close
- Home
- Plan
- Draft
- Decide
- Receipt
- Bind
- Client
- PROJECT
- CURRENT.md
- PROPOSE-CURRENT.md
- DECISIONS.md
- .aether/events.jsonl

Clickable texts: Home, Plan, Draft, Decide, Receipt, Bind, Client, CURRENT.md, PROPOSE-CURRENT.md, DECISIONS.md, `.aether/events.jsonl`. Close is inside a clickable view (bounds ~899,90–1059,209). None of those were tapped.

Home-screen copy (Mechanicall, FOLDER path, NEXT, LAST SAID, the Yes lecture) is **not** in this dump because the dump was taken on the Rooms overlay.

---

## What failed (harsh, splash/home/menu only)

- Splash/home/menu never query a local model. No host, no Ollama, no “thinking”, no schema, no structured-support reply. LAST SAID is the human Yes ledger, not a model.
- Home does not open *on* a selected directory’s work. It opens on a bound-pocket **status board**. The path is the demo `mechanicall-pocket` on emulated storage. Bind is asserted in a card. There is no picker, no tree, no file of actual work.
- Hamburger is **Rooms** of protocol stages, then four authority filenames. Not threads. Not a workspace browser.
- No standard chat-app chrome on this path: no inbox, no last-message preview, no composer, no people, no send.
- Person-to-workspace bridge is inverted: the person is shown CURRENT fields and told they have not said Yes. The workspace is a museum of CURRENT.md. Opening the app is not Yes. Rooms are not a defence.

---

## Definition score (0–5, harsh)

Scored from live splash / home / hamburger only. Rooms are not a defence. Opening is not Yes.

| # | Claim | Score | Why |
|---|--------|------:|-----|
| 1 | Deploys and queries local AI for structured support | **0** | Zero model chrome on this path. No prompt, no reply, no local-AI status, no structured-support payload. LAST SAID is human Yes, not a model. Draft’s Chat tab is off this walker’s path and does not rescue Home. |
| 2 | Opens on a selected directory | **2** | A bound path is printed (`/storage/emulated/0/mechanicall-pocket`) and four protocol files appear under PROJECT. That is a pocket bind, not a selected working directory. No picker on Home, no tree, no files of actual work. Demo pocket, not “sit on *this* folder I chose.” |
| 3 | Standard chat-app framework | **0** | Splash = logo. Home = status cards + six protocol tiles. Menu = Rooms sitemap. No threads, no composer, no bubbles, no contacts. A kiosk with a hamburger. “Rooms” is Slack-wording, not a chat framework. |
| 4 | Bridge from person to workspace | **1** | Folder path + Next id are pointers. The person is parked in a lecture about Yes and a museum of CURRENT.md / DECISIONS.md. A bridge would put the person in conversation with the work in the folder. This puts the person in front of the protocol. |

**Totals:** 0 + 2 + 0 + 1 = **3 / 20**. Fail.

---

This is a protocol museum, not a chat bridge to a folder.
