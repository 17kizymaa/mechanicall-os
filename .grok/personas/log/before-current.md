----- CURRENT-20261007T092323Z-1709225.md -----
# CURRENT

**Objective:** Mechanicall is my Yes. This cut the tool ships one standard kit so every named anphuni alias gets the same room, the same opener, the same folder — and I can hand out URLs.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-09-18 · isolation-millwork done 09-16 (apex) · operator-auth e99af1c · roster closed 2026-09-18 session
**Next:** legal-assimilation-report
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

Share URLs. Not another framework.
 
Every alias in `~/anphuni-project/projects/` gets the **same three things**, produced by this tool:

1. **Room face** — the You Decide room as it is today: chat-only, Send is hello. Paper stays on `happy-birthday` only. Steal-paint (Telegram grammar) is **parked** until real people sit it and FLAG.
2. **Opener** — one `propose.md` per alias that seeds the thread (`lib/you-decide.mjs` `seedFromPropose`). Hello grammar. Does not provoke technical ideas. Asks what they keep the say on — that is them disposing of authority without hearing the word aether:
   - When this is done, what's true that isn't true now?
   - Anything I should **never** do without asking you first? (post it publicly · delete anything · spend money · message anyone as you · change the name or look · use your photos/videos)
   - What are you afraid of me breaking?
   - Who else has to be happy with it?
   - How often do you want to hear from me?
   - Drop files here if it helps. Replying is hello. Nothing is decided until you say so.
3. **Folder standard** — `projects/<alias>/` = `POINTER.md` · `INTAKE.md` (their answers, verbatim) · `MATERIAL/` · `PROPOSALS/` · `DELIVERED/` · `RECEIPTS/` · `NOTES.md`. No client `CURRENT.md`. Pointers, not their Yes.

The primary user is me. They need not learn aether.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. Chat is hello. Their opener answers become that project's **Limits** — I write them, they never stamp.
- **This Next:** `share-urls-kit` — the kit (scaffold + opener template + links list), inspectable shell/Python, in this repo. Applying it to the roster is the **operator** instance's Next (`share-urls-wave-1`), not this one.
- **Not this halt:** Telegram/TradingView paint, GTK desk, APK loop, mint, deploy, sharing, renaming/deleting operator folders, any nested CURRENT.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `share-urls-kit` | scaffold, opener template, links script, site face |
| Operator | `~/anphuni-project/CURRENT.md` | `share-urls-wave-1` | alias roster, mint, INTAKE, LINKS, sharing |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions

## Relax
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- Kit is generic: no alias names hard-coded except the paper allow-list
- Kit writes only under `mechanicall-os/` (`scripts/`, `templates/`) and, if asked, `~/sites/anphuni.com-repo` on disk — **no deploy**
- No emails, names, or secrets in git; opener is generic, INTAKE stays in the operator tree
- Local `:8788` is the sit; apex only after human deploy
- No `aether approve` / `aether next` by the model
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there

## Parked (following — not this Next)
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — `pocket-playtester` alias runs an authority-disposal APK-servicing loop; MVP not up to standard; steal more interaction grammar first; multi-agent when it comes
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product

## Next allowed action
**Action id:** share-urls-kit

Build the kit in this repo. Inspectable shell/Python. No mint, no deploy, no share, no folder rename/delete.

1. `scripts/alias-scaffold.sh <alias> [--root DIR]` — creates `projects/<alias>/{POINTER.md,INTAKE.md,NOTES.md,MATERIAL,PROPOSALS,DELIVERED,RECEIPTS}` from `templates/alias/`. Idempotent; never overwrites an existing file; never writes `CURRENT.md`.
2. `templates/alias/OPENER.md` — the hello-grammar opener above, alias name substituted, nothing else. `INTAKE.md` template mirrors the opener questions with blank answers + "**never without asking**" list that maps to `agent-publish-delete-spend-message-deploy`.
3. `scripts/alias-links.py --root ~/anphuni-project` — read-only; emits `LINKS.md` (alias · room URL · status · has-opener · has-intake) from `projects/*/POINTER.md`. Rooms without an id print `unminted`.
4. Site face check on disk (`~/sites/anphuni.com-repo`): chat-only default holds; `propose.md` seeds the thread; Paper dock only for the birthday id. FLAGS if not. Do not deploy.
5. Receipt `dev/70_share-urls-kit/output/RECEIPT.md`. Halt. Human then applies the kit under the operator Next.

## Evidence sought
1. Did one kit remove per-alias improvisation?
2. Did the opener get real answers about what they keep the say on — without a form and without technical talk?
3. Did INTAKE → Limits make a later Next safer, or was it ceremony?
4. Did two instances stay clean, or did I keep reaching across?
5. Which aliases got a reply at all?

## Approval condition
Human `aether approve` with a real reason after pasting this body. Then `aether next share-urls-kit`. Ordinary personal edits without ceremony. Destructive or external actions still need an explicit Yes. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261007T093541Z-2158598.md -----
# CURRENT

**Objective:** Mechanicall is my Yes. This cut makes the prototype APK a CI assemble check in this repo. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-07 · header was legal-assimilation-report (receipt 2026-09-19) · body Action id was still share-urls-kit · APK 0.19.21-loop-from-20 versionCode 46
**Next:** apk-ci-prototype
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

The prototype APK becomes a CI test. One assemble check, in this repo, on the binary already named in `android/app/build.gradle.kts`.

The primary user is me. They need not learn aether. Chat is hello. Their opener answers become that project's Limits — I write them, they never stamp. That is them disposing of authority without hearing the word aether.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. Chat is hello. Their opener answers become that project's **Limits** — I write them, they never stamp.
- **This Next:** `apk-ci-prototype` — one CI job that assembles the debug APK. Inspectable. No upload, no sideload, no store signing, no protocol lesson.
- **Not this halt:** sharing the protocol, teaching aether, another person stamping Yes, opening or editing the trading CURRENT, sideload, Play or other publish, apex deploy, mint, renaming or deleting operator folders, Telegram/TradingView paint, GTK desk.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `apk-ci-prototype` | CI assemble of the prototype APK |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS, sharing |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- The APK in this cut is a prototype; CI assembles it and does not publish it

## Relax
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next writes only under `mechanicall-os/` (the CI workflow and `dev/75_apk-ci-prototype/`). It does not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` is the sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- CI may run `assembleDebug`. CI may not upload, sideload, store-sign, or message anyone
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there

## Parked (following — not this Next)
- **legal-assimilation-report** — receipt 2026-09-19; header was left on that id
- **share-urls-kit** — previous body Action id; kit work is not this halt
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — `pocket-playtester` alias runs an authority-disposal APK-servicing loop; MVP not up to standard; steal more interaction grammar first; multi-agent when it comes
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here

## Next allowed action
**Action id:** apk-ci-prototype

Make the prototype APK a CI assemble check. No publish, no share, no other CURRENT.

1. Add a job to `.github/workflows/test.yml` that checks out the repo and runs `./gradlew :app:assembleDebug` with working directory `android/`. The app under test is `versionName` `0.19.21-loop-from-20`, `versionCode` 46.
2. The job is a pass/fail assemble. It does not upload the APK, sign it for a store, sideload it, or send it to anyone.
3. If the runner JDK cannot assemble, write that fact in the receipt and halt. Do not swap in a different APK or a different Next.
4. Receipt `dev/75_apk-ci-prototype/output/RECEIPT.md` with the job name and the assemble result. Halt.

## Evidence sought
1. Did CI assemble this prototype debug APK?
2. Did the job stay inside the repo, with no upload and no sideload?
3. Did this file stay the only CURRENT touched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Ordinary personal edits without ceremony. Destructive or external actions still need an explicit Yes. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261007T101450Z-3587161.md -----
# CURRENT

**Objective:** Mechanicall is my Yes. Give the client a downloadable APK, with a stable layer I use to develop the tester's version live. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-07 · replaces apk-ci-prototype · prototype com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · closed-tester sit, not production
**Next:** tester-apk-live
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

The client can download the tester APK. The stable layer is the pin I develop that version on, live, after this halt. The pin is the prototype already in the tree. This halt does not move the pin.

The primary user is me. They need not learn aether. Chat is hello. Their opener answers become that project's Limits — I write them, they never stamp.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `tester-apk-live` — pin the stable layer, assemble the closed-tester debug APK, leave that file as the download. Then I develop the tester version live from the pin.
- **Not this halt:** teaching aether, a client CURRENT, the trading CURRENT, Play production, apex deploy, mint, renaming or deleting operator folders, Telegram/TradingView paint, GTK desk, the whole pocket-playtest loop.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `tester-apk-live` | stable pin and the downloadable tester APK |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS, sharing |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it

## Relax
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next writes only under `mechanicall-os/` (`dev/75_tester-apk-live/` and the debug APK it copies). It does not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` is the sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- This halt may assemble the closed-tester debug APK and leave it as a file. It may not pick a recipient address, a website, or a store. Play upload, apex deploy, spend, delete, and messaging a person stay off
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there

## Parked (following — not this Next)
- **apk-ci-prototype** — assemble-only Next; replaced by this objective
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — earlier body Action id
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here

## Next allowed action
**Action id:** tester-apk-live

Pin the stable layer and produce the client's downloadable tester APK. Live development of later tester builds starts from that pin after this halt.

1. Write `dev/75_tester-apk-live/output/STABLE-LAYER.md`. The pin is `applicationId` `com.mechanicall.pocket.demo`, `versionName` `0.19.21-loop-from-20`, `versionCode` 46, plus `git rev-parse HEAD` and whether the worktree is dirty. Do not bump the version in this halt.
2. From `android/`, run `./gradlew :app:assembleDebug`. Copy the debug APK to `dev/75_tester-apk-live/output/`. Record path, byte size, and sha256.
3. If the JDK cannot assemble, write that fact in the receipt and halt. Do not substitute another binary.
4. Receipt `dev/75_tester-apk-live/output/RECEIPT.md`. The APK file is the client download. No Play upload, no apex deploy, no invented recipient. Halt.

## Evidence sought
1. Is the stable layer pinned to this prototype, version unchanged?
2. Is there one debug APK on disk with a sha256, ready for the client to download?
3. Did this file stay the only CURRENT touched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Ordinary personal edits without ceremony. Destructive or external actions still need an explicit Yes. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261012T113628Z-1739220.md -----
# CURRENT

**Objective:** Mechanicall is my Yes. Give the client a downloadable APK, with a stable layer I use to develop the tester's version live. I still dispose.
**Phase:** SELECT
**Status:** REJECTED
**Baseline:** 2026-10-07 · share starts here · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · closed-tester sit, not production · remote CI not considered
**Next:** session-memory
**Approval:** REJECTED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

The share of the pinned tester APK is where this starts. The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. The share dies 24 hours after it starts.

The primary user is me. They need not learn aether. Chat is hello. Their opener answers become that project's Limits — I write them, they never stamp.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `apk-share-24h` — one loopback share of the pinned debug APK. It expires 24 hours after start. Then halt.
- **Not this halt:** a remote CI layer, a CI vendor, a GitHub Android job, Play, apex deploy, messaging a person, teaching aether, a client CURRENT, the trading CURRENT, mint, renaming or deleting operator folders, the whole pocket-playtest loop.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `apk-share-24h` | the 24-hour loopback share of the pinned tester APK |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS, who the share is handed to |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it
- A share of this APK has a deadline

## Relax
- The operator is not bound by this file's limits on handing the tester APK onward. Recipient, website, and store limits here do not bind the operator. The operator still disposes and still does not stamp a client CURRENT. This line does not edit or merge the operator CURRENT.
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next writes only under `mechanicall-os/` (`dev/76_apk-share-24h/` and the loopback share of the existing APK). It does not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy. This share does not replace that sit and does not go on apex
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, or deploy apex. The operator may hand the share on
- The share binds `127.0.0.1` only and stops accepting downloads 24 hours after the receipt time
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt. Do not add a workflow and do not pick a vendor

## Parked (following — not this Next)
- **remote CI layer** — not considered. `test.yml` is Python only. No Android job. No artifact upload
- **tester-apk-live** — pin and debug APK already on disk
- **apk-ci-prototype** — assemble-only Next; the miss before the pin
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — alias links, not this APK
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- **session-memory** — .memory/ sidecar: append-only ledger + topics; stage 77
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here

## Next allowed action
**Action id:** apk-share-24h

Share the pinned tester APK on loopback. The share expires 24 hours after it starts. Remote CI stays unconsidered.

1. Use the existing file `dev/75_tester-apk-live/output/mechanicall-pocket-0.19.21-loop-from-20-vc46-debug.apk`. Confirm sha256 `44900cc0adc6b823a99bdca6a2992868e4017202d540b003dc31d31d66ac4d8f` and 62526130 bytes. If either differs, halt. Do not rebuild and do not bump the version.
2. Serve that file on `127.0.0.1` only, on a free port, one path. Do not bind a public address. Do not use the room clip. Do not deploy apex.
3. Write `dev/76_apk-share-24h/output/SHARE.md` with the URL, port, pid, byte size, sha256, started-at, and expires-at. expires-at is started-at plus 24 hours. The process exits at expires-at. This halt does not wait out the day.
4. Receipt `dev/76_apk-share-24h/output/RECEIPT.md`. No recipient name, email, or inbox. The operator hands the share on. Halt.

## Evidence sought
1. Is the loopback share serving the pinned APK, same sha256?
2. Does the receipt name a deadline 24 hours after start?
3. Did `test.yml`, the operator CURRENT, and the version pin stay untouched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Ordinary personal edits without ceremony. Destructive or external actions still need an explicit Yes. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261012T130749Z-755859.md -----
# CURRENT

**Objective:** Mechanicall: You Decide is prototype-quality for one sit. The agent's smarts stay files and folders. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-12 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · the ordered Yes sentence is already in the dirty demo · the plan heading tap still clears the section · closed-tester, not production
**Next:** glass-prototype
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

This week is the app. One slice. A plan heading stays on the glass until the sitter leaves the plan. The agent stays files and folders. The app does not grow a model.

The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. This halt does not install and does not upload.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `glass-prototype` — one plan-heading slice on the demo glass. Then halt.
- **Not this halt:** a version bump, a phone install, Play, a store pack, storm, a Confirm tap, a Yes tap, a model inside the APK, rooms, remint, video, the operator CURRENT, the 24-hour share, the session-memory sidecar.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `glass-prototype` | the plan-heading slice on the demo glass |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it
- A share of this APK has a deadline
- The agent's smarts stay files and folders
- The archive pin stays versionCode 46 until a later Next

## Relax
- The operator is not bound by this file's limits on handing the tester APK onward. Recipient, website, and store limits here do not bind the operator. The operator still disposes and still does not stamp a client CURRENT. This line does not edit or merge the operator CURRENT.
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next may edit the plan LCD hit in `android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt` so a heading peek survives that tap
- This Next may edit the send-slip strings in that demo only where aether, OEM FILES, or action-id are still drawn. "files only · not Yes" and "not the plan" stay
- Do not restyle `decideCopy` or `receiptStrip` when they already say Yes writes the plan and Not yet leaves it
- Do not repaint the five heading strips
- Do not bump versionCode. Do not assemble a store APK. Do not install. Do not boot storm. Do not tap Confirm. Do not tap Yes
- Do not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, or deploy apex
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt. Do not add a workflow and do not pick a vendor

## Parked (following — not this Next)
- **apk-share-24h** — the loopback share of the pinned APK. Not this week
- **session-memory** — .memory/ sidecar receipt is stage 77. The Next was rejected. Not reopened here
- **remote CI layer** — not considered. `test.yml` is Python only. No Android job. No artifact upload
- **tester-apk-live** — pin and debug APK already on disk
- **apk-ci-prototype** — assemble-only Next; the miss before the pin
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — alias links, not this APK
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here

## Next allowed action
**Action id:** glass-prototype

Make one plan heading stay visible. The agent's smarts stay files and folders. Then halt.

1. In `MainActivity.onHit`, a PLAN LCD tap sets `planToc = false` and peeks page 0. A heading tap (`FieldObjective`, `FieldNext`, `FieldKeep`, `FieldReject`, `FieldLimits`) must keep that section up until the sitter leaves the plan bank.
2. Leave `decideCopy` and `receiptStrip` as they are when they already say Yes writes the plan and Not yet leaves it.
3. On the send slip, drop aether, OEM FILES, and action-id if those strings are still drawn. Keep "files only · not Yes" and "not the plan".
4. Do not bump versionCode. Do not install. Do not upload. Do not boot storm. Do not tap Confirm. Do not tap Yes. Halt.

## Evidence sought
1. Does a heading tap still show that section after the plan LCD is tapped?
2. Did versionCode stay 46, and did the archive APK stay the pin?
3. Did the operator CURRENT, Play, and storm stay untouched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Millwork stays closed while Approval is DRAFT. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261012T140939Z-2971578.md -----
# CURRENT

**Objective:** Mechanicall: You Decide is prototype-quality for one sit. Share and Desk work at a basic level. The gate lamp shows the desk. The agent's smarts stay files and folders. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-12 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · heading peek stays through a plan LCD tap in the dirty demo · send slip no longer draws aether, OEM FILES, or action-id · Wake and Join hits do nothing · gate percent is stored and not drawn · closed-tester, not production
**Next:** share-desk
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

One operations slice. Share is the Send stage. Desk is a probe of the private desk. The gate lamp draws the loading bar and the desk words already in the demo. The draft keeps "not the plan" and shows a proposed line only when that line is already in the draft. The app does not grow a model.

The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. This halt does not install on the phone and does not upload.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `share-desk` — basic Share, basic Desk, and the gate lamp. Then halt.
- **Not this halt:** a version bump, a phone install, Play, a store pack, a second storm, a Confirm tap, a Yes tap, a model inside the APK, a draft_chat or Ollama call, an Onyx call, Join, wol-pi wake, rooms, remint, video, the operator CURRENT, the 24-hour share, the session-memory sidecar.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `share-desk` | basic Share, Desk, and the gate lamp |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it
- A share of this APK has a deadline
- The agent's smarts stay files and folders
- The archive pin stays versionCode 46 until a later Next
- "files only · not Yes" and "not the plan" stay on the glass

## Relax
- The operator is not bound by this file's limits on handing the tester APK onward. Recipient, website, and store limits here do not bind the operator. The operator still disposes and still does not stamp a client CURRENT. This line does not edit or merge the operator CURRENT.
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next may edit `MainActivity.kt` so the Wake lamp calls `desk_probe` on the bound folder. Quiet or idle is the result. Join stays a no-op. Do not call `wake_desk`.
- This Next may edit `SitRackView.kt` so the existing gate draws a loading bar when `gatePercent` is above 0, and draws LOAD, STREAM, QUEUE, WARM, or QUIET when the gate state is one of those. Percent 0 and idle keep the painted WAIT plate.
- On the draft plate, show the existing `proposed` line under "not the plan" when that line is already non-empty. Do not invent the line. Do not call `draft_chat`.
- Send stays the folder stage. A stage may show its up-percent on that same gate bar. The slip keeps "files only · not Yes". Do not start the 24-hour share.
- Do not restyle `decideCopy` or `receiptStrip`. Do not repaint the five heading strips. Do not repaint nodpi plates.
- Do not bump versionCode. Do not assemble a store APK. Do not install on the phone. Do not boot a second storm. A look on the already-running storm-0, emulator only, is allowed after the edit. Do not tap Confirm. Do not tap Yes.
- Do not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, deploy apex, or spend an Onyx call
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt. Do not add a workflow and do not pick a vendor

## Parked (following — not this Next)
- **glass-prototype** — heading peek and the send-slip string drop are in the dirty demo. Not recommitted here. Not reopened.
- **desk-model-turn** — a local desk or Onyx reading that writes the inline suggestion. Complex. Not this halt. No spend until a later Next asks.
- **apk-share-24h** — the loopback share of the pinned APK. Not this week
- **session-memory** — .memory/ sidecar receipt is stage 77. The Next was rejected. Not reopened here
- **remote CI layer** — not considered. `test.yml` is Python only. No Android job. No artifact upload
- **tester-apk-live** — pin and debug APK already on disk
- **apk-ci-prototype** — assemble-only Next; the miss before the pin
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — alias links, not this APK
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here
- Join and wol-pi wake — lamps may stay visible; the hits stay closed

## Next allowed action
**Action id:** share-desk

Make Share, Desk, and the gate lamp work at a basic level. The agent's smarts stay files and folders. Then halt.

1. Wake calls `desk_probe` for the bound folder. The gate shows QUIET or IDLE. Do not wake wol-pi. Do not join a net.
2. Draw the loading bar on the existing gate when a transfer percent is above 0. Draw LOAD, STREAM, QUEUE, WARM, or QUIET on that lamp when the gate state says so. Idle and zero percent keep WAIT.
3. On Draft, keep "not the plan". Show the existing proposed line when the draft already has one. Do not call a model to write it.
4. Send stays files only, not Yes. A local stage may move the same bar, then the lamp returns to WAIT if the drop is quiet.
5. Do not bump versionCode. Do not install on the phone. Do not upload. Do not boot a second storm. Do not tap Confirm. Do not tap Yes. Halt.

## Evidence sought
1. Does Wake show QUIET or IDLE, and does Join still do nothing?
2. Does the gate draw a bar only when percent is above 0, and WAIT when it is idle?
3. Did versionCode stay 46, and did the phone, the archive pin, and the operator CURRENT stay untouched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Millwork stays closed while Approval is DRAFT. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261012T150736Z-857553.md -----
# CURRENT

**Objective:** Mechanicall: You Decide is prototype-quality for one sit. Plan, Draft, Decide, and Receipt are one tray. The gate stays the painted plate. The agent's smarts stay files and folders. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-12 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · heading peek stays · send slip keeps "files only · not Yes" · Wake calls desk_probe and the glass drew IDLE over WAIT · a transfer bar was drawn · closed-tester, not production
**Next:** page-chrome
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

One chrome slice. The chassis already matches. The four wells do not. Plan is the reference tray: cream strips, one word, an amber pip. Draft, Decide, and Receipt use that tray. The sentences stay. The painted gate stays WAIT. No second desk word. No loading bar on the glass.

The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. This halt does not install on the phone and does not upload.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `page-chrome` — one tray for the four wells. Then halt.
- **Not this halt:** a version bump, a phone install, Play, a store pack, a second storm, a Confirm tap, a Yes tap, a model inside the APK, a draft_chat or Ollama call, an Onyx call, Join, wol-pi wake, more desk words on the gate, rooms, remint, video, the operator CURRENT, the 24-hour share, the session-memory sidecar.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `page-chrome` | one tray across the four wells |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it
- A share of this APK has a deadline
- The agent's smarts stay files and folders
- The archive pin stays versionCode 46 until a later Next
- "files only · not Yes" and "not the plan" stay on the glass
- The plan tray is the chrome reference: cream strip, one word, amber pip

## Relax
- The operator is not bound by this file's limits on handing the tester APK onward. Recipient, website, and store limits here do not bind the operator. The operator still disposes and still does not stamp a client CURRENT. This line does not edit or merge the operator CURRENT.
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next may edit `sit_well_draft.png`, `sit_well_decide.png`, and `sit_well_receipt.png` so those wells use the plan tray. Draft loses the flat grey card. Decide's WHY is one strip, and Not yet is a strip. YES stays the metal stamp. Receipt's inner sheet is the same ruled paper as the send slip.
- This Next may edit `SitRackView.kt` so the gate draws no second word and no bar. Painted WAIT stays. The send list sits on the ruled lines, and the plan strip does not show through the folder.
- Wake may keep calling `desk_probe`. Do not draw QUIET, IDLE, LOAD, STREAM, QUEUE, or WARM on the gate. Join stays a no-op. Do not call `wake_desk`.
- Do not restyle `decideCopy` or `receiptStrip`. Do not change "not the plan", "NOT ACTIVE", or "files only · not Yes". Do not repaint the five plan heading strips. Do not repaint the chassis, the title plaque, the three lamps, or the four bank keys.
- Do not bump versionCode. Do not assemble a store APK. Do not install on the phone. Do not boot a second storm. A look on the already-running storm-0, emulator only, is allowed after the edit. Do not tap Confirm. Do not tap Yes.
- Do not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, deploy apex, or spend an Onyx call
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt. Do not add a workflow and do not pick a vendor

## Parked (following — not this Next)
- **share-desk** — Wake already calls `desk_probe` in the dirty demo. The extra gate word and the bar are recanted by this Next. Not recommitted here.
- **desk-model-turn** — a local desk or Onyx reading that writes the inline suggestion. Not this halt. No spend until a later Next asks.
- **glass-prototype** — heading peek and the send-slip string drop are in the dirty demo. Not reopened.
- **apk-share-24h** — the loopback share of the pinned APK. Not this week
- **session-memory** — .memory/ sidecar receipt is stage 77. The Next was rejected. Not reopened here
- **remote CI layer** — not considered. `test.yml` is Python only. No Android job. No artifact upload
- **tester-apk-live** — pin and debug APK already on disk
- **apk-ci-prototype** — assemble-only Next; the miss before the pin
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — alias links, not this APK
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here
- Join and wol-pi wake — lamps may stay visible; the hits stay closed

## Next allowed action
**Action id:** page-chrome

Make Plan, Draft, Decide, and Receipt one tray. Leave the sentences. Leave the painted gate. Then halt.

1. Stop drawing a second word on the gate. Stop drawing the bar. Painted WAIT stays, including after Wake. Do not remove the `desk_probe` call.
2. Draft uses the plan tray. The grey card goes. NOT ACTIVE and "not the plan" stay.
3. Decide's WHY is one strip. Not yet is a strip. YES stays the metal stamp.
4. Receipt's inner sheet is the send slip's ruled paper, in the same tray. The receipt sentence stays.
5. The send list sits on those rules. The plan strip does not show through the folder. "files only · not Yes" stays.
6. Do not bump versionCode. Do not install on the phone. Do not upload. Do not boot a second storm. Do not tap Confirm. Do not tap Yes. Halt.

## Evidence sought
1. Do Draft, Decide, and Receipt use the plan's tray, with the same sentences still readable?
2. Does the gate stay the painted WAIT, with no IDLE, QUIET, LOAD, STREAM, QUEUE, or WARM drawn over it?
3. Does the send list sit on the rules, and does LIMITS stay hidden under the folder?
4. Did versionCode stay 46, and did the phone, the archive pin, and the operator CURRENT stay untouched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Millwork stays closed while Approval is DRAFT. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
----- CURRENT-20261014T120931Z-2577485.md -----
# CURRENT

**Objective:** Mechanicall: You Decide is prototype-quality for one sit. Draft and Decide have their own plates. Plan stays the heading tray. The gate stays the painted plate. The agent's smarts stay files and folders. I still dispose.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-12 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · page-chrome sat on emulator-5554 · Draft opens on the plan tray with NOT ACTIVE and "not the plan" · Decide is one WHY, the YES stamp, and Not yet on a strip · Receipt is the ruled sheet · the gate stays painted WAIT after Wake · the send list sits on the rules · closed-tester, not production
**Next:** draft-decide-millwork
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

New millwork for Draft and Decide. The chassis already matches. Plan's five heading strips stay Plan's. Receipt's ruled sheet stays. Draft is not that heading tray with two words swapped. Decide is not a wiped face. Both plates are painted in the same materials as the machine: cream enamel, the metal well frame, an amber pip, screws.

The sentences stay. The painted gate stays WAIT. No second desk word. No loading bar on the glass.

The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. This halt does not install on the phone and does not upload.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `draft-decide-millwork` — new plates for the Draft well and the Decide well. Then halt.
- **Not this halt:** a version bump, a phone install, Play, a store pack, a second storm, a Confirm tap, a Yes tap, a model inside the APK, a draft_chat or Ollama call, an Onyx call, Join, wol-pi wake, more desk words on the gate, rooms, remint, video, the operator CURRENT, the 24-hour share, the session-memory sidecar, a new receipt plate, a repaint of the five plan headings, a repaint of the send folder.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `draft-decide-millwork` | new Draft and Decide plates |
| Operator | `~/anphuni-project/CURRENT.md` | (that file's own header) | alias roster, mint, INTAKE, LINKS |

Paper: `happy-birthday` `e9b16791a12ac1ef521891b6eac3bf68` only. `DEFAULT_PAPER_TICKETS` stays that id.

## Keep
- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence ≠ permission
- They need not learn the system; Send is hello, not Yes
- Paper only on birthday; not live money
- Room URL is the face; steal grammar, never vendor bitmaps or vendor sites
- Site-play FLAGS before paint
- Pointers not copies; no client CURRENT; no nested CURRENT
- Their opener answers → my Limits for that alias
- Two instances, two Nexts, never merged
- Explicit preview + Yes for destructive or external actions
- Closed-tester debug APK, not a production store release
- The stable layer stays pinned while later tester builds develop on it
- A share of this APK has a deadline
- The agent's smarts stay files and folders
- The archive pin stays versionCode 46 until a later Next
- "files only · not Yes" and "not the plan" stay on the glass
- Plan keeps its heading tray: cream strip, one word, amber pip
- YES stays the metal stamp. Not yet stays a refusal on the plate

## Relax
- The operator is not bound by this file's limits on handing the tester APK onward. Recipient, website, and store limits here do not bind the operator. The operator still disposes and still does not stamp a client CURRENT. This line does not edit or merge the operator CURRENT.
- Approval ceremony for ordinary personal edits
- Birthday two-app desk polish (done enough to share)
- Prospectus ratios/timelines — evidence first

## Reject
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- intake-as-technical-questionnaire
- form-instead-of-hello
- framework-before-three-repeats
- paint-before-sit
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- agent-taste-steal-instead-of-crowd
- kitchen-this-works-in-the-room
- body-as-food-product
- deleting previous experiments because the direction changed
- turning CURRENT into a backlog
- protocol compliance as a substitute for making things

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- This Next may replace `sit_well_draft.png` and `sit_well_decide.png`. Draft is one sheet in the tray, painting NOT ACTIVE and "not the plan". It is not five heading strips. Decide is one painted face: one WHY strip, the metal YES stamp, and one blank lower strip for the drawn "Not yet". The coffee ring stays on that face.
- Both plates stay `1080×2138`. The bank row stays transparent so the four keys still hit. Do not edit `SitCRects` to move those keys.
- Do not edit `sit_well_plan.png`, `sit_well_receipt.png`, `sit_folder_dest.png`, the chassis, the title plaque, the three lamps, the four bank keys, or the gate.
- Do not restyle `decideCopy` or `receiptStrip`. Do not change "not the plan", "NOT ACTIVE", or "files only · not Yes". The drawn "Not yet" stays on its strip.
- Wake may keep calling `desk_probe`. Do not draw QUIET, IDLE, LOAD, STREAM, QUEUE, or WARM on the gate. Join stays a no-op. Do not call `wake_desk`.
- Do not bump versionCode. Do not assemble a store APK. Do not install on the phone. Do not boot a second storm. A look on the already-running storm-0, emulator only, is allowed after the edit. Do not tap Confirm. Do not tap Yes.
- Do not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, deploy apex, or spend an Onyx call
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt. Do not add a workflow and do not pick a vendor

## Parked (following — not this Next)
- **page-chrome** — sat 2026-10-12 on emulator-5554. Draft opened. The gate stays painted WAIT. The send list sits on the rules. The tray-clone for Draft and Decide is what this Next replaces. Not recommitted as the plate.
- **share-desk** — Wake already calls `desk_probe` in the dirty demo. The extra gate word and the bar stay off the glass. Not recommitted here.
- **desk-model-turn** — a local desk or Onyx reading that writes the inline suggestion. Not this halt. No spend until a later Next asks.
- **glass-prototype** — heading peek and the send-slip string drop are in the dirty demo. Not reopened.
- **send-slip seam** — the folder's clear hole is plate cream, and a seam shows where the photograph ends. Not this halt.
- **apk-share-24h** — the loopback share of the pinned APK. Not this week
- **session-memory** — .memory/ sidecar receipt is stage 77. The Next was rejected. Not reopened here
- **remote CI layer** — not considered. `test.yml` is Python only. No Android job. No artifact upload
- **tester-apk-live** — pin and debug APK already on disk
- **apk-ci-prototype** — assemble-only Next; the miss before the pin
- **legal-assimilation-report** — receipt 2026-09-19
- **share-urls-kit** — alias links, not this APK
- **telegram-grammar-paint** on `you-decide-ticket.html` (after wave-1 sit + FLAGS)
- **tradingview-paper-paint** on birthday (after paint above)
- **pocket-playtest-loop** — authority-disposal APK-servicing loop; not this halt
- operator-auth dashboard
- GTK desk; Webull widget desk; thinkorswim
- Sequential ids; `/offers/` index; OpenRouter/Generate
- `aether reject` → `aether next` sequence bug? (observed 08:05)
- Eduwares / ICM templates — only after three repeats
- this-works named product
- Trading project on its own CURRENT — not opened from here
- Join and wol-pi wake — lamps may stay visible; the hits stay closed

## Next allowed action
**Action id:** draft-decide-millwork

Paint new millwork for the Draft well and the Decide well. Leave the sentences. Leave the painted gate. Then halt.

1. Replace `sit_well_draft.png`. One sheet in the tray. Paint NOT ACTIVE and "not the plan". Do not reuse the five heading strips.
2. Replace `sit_well_decide.png`. One painted face: one WHY strip, the metal YES stamp, one blank strip where "Not yet" is drawn. Keep the coffee ring.
3. Keep both plates `1080×2138`, with the bank row transparent.
4. Do not edit the plan plate, the receipt plate, the folder, the chassis, the lamps, the bank keys, or the gate. Do not restyle the sentences.
5. Do not bump versionCode. Do not install on the phone. Do not upload. Do not boot a second storm. Do not tap Confirm. Do not tap Yes. Look on the already-running storm-0, emulator only. Halt.

## Evidence sought
1. Does Draft's well show one sheet with NOT ACTIVE and "not the plan", and not the five heading strips?
2. Does Decide's well show one WHY strip, the metal YES stamp, and Not yet on one strip, as one painted face?
3. Do the four bank keys still change the page, and does the gate stay the painted WAIT?
4. Did versionCode stay 46, and did the phone, the archive pin, and the operator CURRENT stay untouched?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. Millwork stays closed while Approval is DRAFT. Silence is never permission.

## Prohibited
- automatic-approve
- commit-secrets
- dual-concurrent-next
- model-auto-write-current
- proposal-wrapper-as-CURRENT
- their-yes-as-the-product
- teach-aether-as-the-price-of-help
- stamp-client-current-for-them
- nested-current
- stocks-on-every-room
- live-money-as-paper-trading
- ibkr-passing-off
- wrap-vendor-site-as-the-room
- paint-before-sit
- intake-as-technical-questionnaire
- kitchen-this-works-in-the-room
- body-as-food-product
- multi-agent-orchestration
- agent-publish-delete-spend-message-deploy
