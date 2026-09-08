# Elevation — basic and solid, per room

**Not Yes. Not millwork. Not a new host.**  
P=1 peek contract: `PEEK.md` (still unstamped). Walk: `04_walk_hits`. Inspo already stolen: `19_PRUNE` (till + mum gate + quiet Start). This file **thickens** that with product grammar + libraries that fit **SitRackView**.

**Constraint:** leftover Compose / LcdViewer **returning as the host** is Reject. Libraries may live **inside a room** (TextView, EditText, Intent). They must not replace the recycled chassis.

**One add that earns its keep:** [Markwon](https://noties.io/Markwon/) `io.noties.markwon:core` (+ optional `:editor`) — CommonMark → native Spannable. No WebView. No HTML hop. Fits paper Plan / Draft / Receipt. Compose markdown renderers (Twain, multiplatform-markdown-renderer) stay off unless a human recants F1.

Deps on disk today: `activity-ktx`, `lifecycle-runtime-ktx`, Chaquopy. Elevation prefers **platform first**, then **one paper library**.

---

## How to read a row

| Column | Means |
|--------|--------|
| Steal | Interaction grammar from a real product |
| Don’t | Chrome / metaphor that fights You Decide |
| Solid | Kotlin / Android that is boring and correct |
| Peek | What millwork must show (does not recant `PEEK.md`) |
| Elevate | The one basic move that makes the room feel finished |

---

## Door — Bind

**Steal:** Android **Files** / **Gander**: you name *this* folder, the OS remembers the grant. Obsidian “open vault” — one house, not a search of the phone.  
**Don’t:** file-explorer museum; SimpleStorage if it drags `WRITE_EXTERNAL_STORAGE`; auto-bind this operator tree.

**Solid (already / tiny):**
- `ActivityResultContracts.OpenDocumentTree()` (in use)
- `takePersistableUriPermission`
- `androidx.documentfile:documentfile` if tree listing must stop using raw `File` on SAF trees
- `DocumentsContract` child query — **not** `DocumentFile.listFiles()` on big folders

**Peek:** folder **display name**, or “Name a folder.”  
**Elevate:** one huge name. Last bound folder as a single “this house” chip — not a recents carousel. OEM picker is the product; we don’t restyle it.

---

## Goal — Plan

**Steal:** **iA Writer** / a till **ticket**: the published bill, cream paper, graphite, headings you can skim. GitHub **README on a PR** — file, not chat.  
**Don’t:** chat bubbles; CRT tube; WebView markdown; whole CURRENT on glass.

**Solid:**
- Markwon `setMarkdown(textView, currentMd)` on a **paper dest later**
- Chassis stays `clipPreview` ~120 of Objective + Next (PEEK)
- `StaticLayout` we already have is enough for the peek

**Peek:** “This is the plan.” Truncated Objective + Next.  
**Elevate:** peek is a **ticket header** (Next id as the SKU, Objective as the line). Full CURRENT is paper, Markwon, later — not IsolatedDark CRT.

---

## Draft — NOT ACTIVE

**Steal:** GitHub **Suggesting** / HITL “propose → review”: editable, labeled **not merged**. iA Writer focus mode — one file, no chrome.  
**Don’t:** rich-text WYSIWYG bars; Compose editor as the sit; ALPHA/BETA/GAMMA.

**Solid:**
- Keep `EditText` + `savePropose` (law B3/B13)
- Optional: `io.noties.markwon:editor` — highlight markdown **in the same EditText** (MarkwonEditorTextWatcher). Not a second widget.
- IME: already `IME_FLAG_NO_ENTER_ACTION`

**Peek:** **NOT ACTIVE** louder than “draft.” Short proposed Next vs live.  
**Elevate:** violet accent on suggestion vs graphite live (19 prune). Writer is the dest. No toolbar of toys.  
**LLM (parked, scaffold):** prose → `personal-llm-sft-v4` → merge schema into PROPOSE. See `DRAFT-LLM.md`. Generate is a **Draft dest chore**, not chassis GATE.

---

## Stamp — Decide

**Steal:** **Monzo / Wise send sheet**: restates amount + destination, reason required, then a fat Yes. **BIG Launcher**: one meaning per tap, thumb-sized, accident-resistant. Android **Protected Confirmation** *idea* (see the statement, then agree) — not the TEE API this halt.  
**Don’t:** BiometricPrompt as Yes (that’s a lock, not a Why). Confirm. Publish. First-tap. Swipe-without-Why. Protected Confirmation API skipping Why.

**Solid:**
- Platform only. Two-tap we have (`decideArmed`). Why EditText we have.
- Optional: `View.performHapticFeedback(CONFIRM)` on the second tap — then quiet.
- Do **not** add `ConfirmationPrompt` / Keystore attestation this sprint.

**Peek:** Why; armed = “Yes? tap again.” “You have not said yes yet.”  
**Elevate:** restated card on the well: **Next** (the thing) + **Why** (hers) + **Yes** / **Not yet**. Millwork = till charge plate, not a plugin knob.

---

## Quiet home — Your One Next

**Steal:** **Duolingo Start** / gym **GO**: after commitment, home is one action. **Things 3 Today**: one line, two feet. 19 busyboard.  
**Don’t:** streak shame; dashboard of lamps; JOIN/WAKE; Lottie pets.

**Solid:**
- Platform. `SitPlate.NEXT` already.
- Optional **one** motion: `ViewPropertyAnimator` or `MotionLayout` stamp/GO **once**, ≤400ms, then still. Don’t loop.
- No WorkManager as the face (that’s waiting / Generate following).

**Peek:** one line Next id. Feet: I did it / Not yet.  
**Elevate:** type so large the Next *is* the room. Feet are till buttons, not banks.

---

## I did it

**Steal:** Things 3 check; till **“paid.”** Labour, then the strip prints.  
**Don’t:** confetti; XP; treating the tap as a second Yes.

**Solid:**
- `did_it()` / `write_receipt` (in). Never `yes()`.
- Optional haptic `CONTEXT_CLICK`.
- Share later via receipt FileProvider — not this tap.

**Peek:** same home.  
**Elevate:** the foot is as big as Yes was, but **quieter colour** (graphite, not the Yes accent). Copy: “I did it” not “Complete” not “Done ✓”.

---

## Not yet (home)

**Steal:** leaving the till without charging. The ticket stays on the spike.  
**Don’t:** `notYet` after Yes (would un-stamp). Sulk copy.

**Solid:** idleLine only. CURRENT bytes unchanged (already).  
**Peek:** “Not yet. The Next stays.”  
**Elevate:** grey foot. No receipt rewrite.

---

## What happened — Receipt

**Steal:** thermal **till strip**; a letter you can forward tomorrow. Print that survives the chat.  
**Don’t:** CRT page; fake agree; printer millwork as the *only* receipt (parked as visual, not as the file).

**Solid:**
- File `RECEIPT.md` (law). Peek empty = “(empty receipt)”.
- Markwon on the well for the md strip.
- Forward: `FileProvider` + `Intent.ACTION_SEND` `text/plain` / `text/markdown`. Not Yes.
- `PrintHelper` / `PrintManager` **following** (receipt-printer parked).

**Peek:** truncated what happened, or empty.  
**Elevate:** monospace strip, when / You said / Next / one trail. Looks like a stub, not a terminal.

---

## Bag — Send folder

**Steal:** Android **Share sheet** (send *out*); **zip2share** (folder → one bag); bank “files only, not the live plan.” Quick Share **PIN** is Accept ≠ Yes if we ever Nearby — not this sprint.  
**Don’t:** Send as Yes; Nearby as product identity; Bada/GMS as a second app.

**Solid (platform, already close):**
- Overlay listing we have + `stageSendFolder`
- Elevate the *out* path: `FileProvider` + `Intent.createChooser` for a zip of the bound folder (`java.util.zip`) when she wants OEM share — **still not Yes**
- `documentfile` for SAF-safe listing
- Headscale later

**Peek:** lamp + “files only, not the live plan, not Yes.”  
**Elevate:** bag is a **packing slip** (file names), not a settings cream panel. F3 still open (recommend 1: near Draft/Plan).

---

## Waiting — GATE

**Steal:** Play Store / DownloadManager **progress** — honest wait, not a door.  
**Don’t:** typing dots; GATE opens CRT; Generate this halt.

**Solid:**
- Keep LOAD/STREAM/ETA copy (B7 law)
- `ProgressBar` / draw on millwork, not a second widget kit
- `WorkManager` only if Generate returns (`sit-bound-draft` following)

**Peek:** clipped ETA.  
**Elevate:** a bar that is clearly **wait**, visually quieter than Yes.

---

## Leftover-lab (do not elevate as first sit)

JOIN / WAKE / IsolatedMode.CRT — archive. Millwork must not light them as peers of Yes. Headscale / WOLs stay chores behind a mode (F1=2).

---

## Library board (honest)

| Add? | Artifact | Rooms | Verdict |
|------|----------|-------|---------|
| maybe | `io.noties.markwon:core:4.6.2` | Plan dest, Receipt well, Draft highlight | **One** paper library. Native Spannable. |
| maybe | `io.noties.markwon:editor:4.6.2` | Draft EditText | Same family. No new widget. |
| maybe | `androidx.documentfile:documentfile:1.1.0` | Bind listing, Send bag | If SAF tree, not raw File |
| later | FileProvider + share chooser | Receipt forward, Send zip | Platform. Not a lib. |
| no | Compose markdown / Twain / MarkRead | — | New host. Reject this halt. |
| no | Lottie / confetti | Next / I did it | Mascot. |
| no | BiometricPrompt / ConfirmationPrompt | Decide | Skips Why or fakes a second Yes. |
| no | SimpleStorage | Bind | Extra permission stories. SAF is enough. |
| no | Nearby / Bada | Send | Following, not identity. |

---

## Colour (from 19, still)

Cream paper + graphite ink. **Violet = NOT ACTIVE.** **Amber/green = active Next / Yes.** One accent, not a rainbow. Neo-brutalist Yes: thick border, thumb-sized, press-shadow — **painted on recycled millwork**, not a Compose Button.

---

## What this is not

- A stamp on `PEEK.md` (still yours)
- A license to replace SitRackView
- Millwork this sitting (that’s `06` after PEEK stamp)
- Website

## Halt

Steal grammar into millwork **after** PEEK is stamped. If a library is to land, name it on `06` (Markwon is the only likely yes). Confirm not tapped.
