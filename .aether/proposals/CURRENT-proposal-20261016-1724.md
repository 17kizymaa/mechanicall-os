# CURRENT proposal — park aether bookmark — NOT LAW until you apply

**NOT ACTIVE. Not Yes.**

APPLY: human runs `/mechanicall-domain:apply` on this file (`aether apply .aether/proposals/CURRENT-proposal-20261016-1724.md`). That is not a Yes.

**Author:** proposal only. You dispose.

## Recommendation

Keep **Next** as `advanced-local-model`. Align the body Action id with that header so apply can land. Park **`aether bookmark`** as a potential command. Do not add the verb in this halt.

A snapshot of the live file (header Next `advanced-local-model`, body Action id still `draft-millwork-rapid`) is already on disk:

`.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md`

cksum `3532677481` · 12087 bytes. Identical to `CURRENT.md` at bookmark time. That copy is not a Yes. It does not replace `CURRENT.md`.

## What changed (before → after)

| Field | Live file now | This proposal |
| --- | --- | --- |
| Header Next | `advanced-local-model` | `advanced-local-model` |
| Body Action id | `draft-millwork-rapid` | `advanced-local-model` |
| Phase / Status / Approval | APPROVE / APPROVED / APPROVED | SELECT / DRAFT / DRAFT |
| Bookmark verb | not in `AETHER_VERBS` | parked; not implemented |
| Snapshot | none named | `.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md` |

Applying this body returns the halt to DRAFT. The bookmark verb stays unwritten until a later Next you select after a Yes.

## Command spec (not this Next; not shipped)

```
aether bookmark [label] [path]
  copy CURRENT.md → .aether/bookmarks/CURRENT-<UTC>[-label].md
  append events.jsonl kind=bookmark
  do not change CURRENT.md
  do not approve
  do not apply

aether bookmark list [path]
  list snapshots newest first
```

- **Not** `current-before/` — those files are apply side-effects.
- **Not** `aether approve` — approve stamps Yes. Bookmark copies bytes.
- **Not** `aether event` — event is a line. Bookmark is the file.
- **Restore** is not in this first verb. A restore would be a human hand like `apply`. Do not add it here.
- Models may snapshot. Models still never approve, apply, next, or restore.

Tests, `AETHER_VERBS`, `usage()`, and `SPEC-v0.2.md` stay untouched until a later Next that names the verb.

## Fidelity checklist

- One Next: `advanced-local-model`. One matching Action id.
- Models never approve. This file does not approve by itself.
- No secrets.
- Silence is not permission. DRAFT stays DRAFT until you approve.
- Prohibited tokens are unchanged. None of them contain `advanced-local-model`.
- `model-auto-write-current` stays prohibited. Bookmark copies `CURRENT.md`; it does not become CURRENT.
- Two instances stay two Nexts. This file does not write `~/anphuni-project`.

## Conflicts with existing authority

- Live body Action id is `draft-millwork-rapid`. Header Next is `advanced-local-model`. This body names both the same string so apply will not refuse a split.
- The millwork host-propose steps move to Parked. They are not this Next.
- `aether bookmark` is parked. Implementing it in `aether` is not this halt.

## Human decision required

- [ ] Apply this file
- [ ] Reject and leave `CURRENT.md` unchanged
- [ ] Revise and ask for another proposal

After apply, `aether next advanced-local-model` refuses because Next is already that id. Approve is still yours. Until that approve, the bookmark verb is not added.

## Proposed CURRENT

```markdown
# CURRENT

**Objective:** Mechanicall: You Decide is prototype-quality for one sit. Next is a complete advanced local-model framework I would approve of. personal-llm-sft-v6:latest stays the host tag. The weight stays outside the APK. aether bookmark stays parked. I still dispose.
**Phase:** SELECT
**Status:** DRAFT
**Baseline:** 2026-10-16 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · snapshot .aether/bookmarks/CURRENT-20261016T162428Z-this-current.md cksum 3532677481 · ollama has personal-llm-sft-v6:latest ee279269b24a · closed-tester, not production
**Next:** advanced-local-model
**Approval:** DRAFT
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

Grill and write a complete, advanced, standardised local-model framework I would approve of. The host tag is `personal-llm-sft-v6:latest`. A later update of that tag may land. This halt does not add `aether bookmark` to the CLI.

The weight stays in the local model store. No weight file is added under `android/`. The Draft well stays the one sheet that reads NOT ACTIVE and "not the plan".

The pin stays `com.mechanicall.pocket.demo` `0.19.21-loop-from-20` versionCode 46. This halt does not install on the phone and does not upload.

## Product (non-negotiable identity)
- **Is:** **Mechanicall: You Decide** — my decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **Aether's job:** gate my approval for covenants and for destructive or external actions. Ordinary personal edits to this file I may make myself.
- **They:** do not learn aether, CURRENT, or Yes. The client gets the tester build. They do not stamp this file.
- **This Next:** `advanced-local-model` — one written framework for the local host model, for my later Yes. The bookmark command stays parked.
- **Not this halt:** adding `aether bookmark` to the CLI, a restore-from-bookmark verb, a model weight inside the APK, a second host call as the product, an Onyx call, a version bump, a phone install, Play, a store pack, a second storm, a Confirm tap, a Yes tap, Join, wol-pi wake, rooms, remint, video, the operator CURRENT, the 24-hour share, the session-memory sidecar, a new workflow file, a new vendor, installing Refly, installing Aegis, an auto approval, a hot-reloaded policy, Maestro, Appium, a second Next for the bookmark verb.

## Rooms (pointers live in the operator map, not here)

| Instance | Path | Next | Owns |
|----------|------|------|------|
| Tool (this file) | `mechanicall-os/CURRENT.md` | `advanced-local-model` | local-model framework; bookmark parked |
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
- Sidecar personalities quote the logs. A green score is not a Yes
- The Draft desk model is `personal-llm-sft-v6:latest` on the host. The weight stays outside the APK
- A host call writes `PROPOSE-CURRENT.md` only. It does not write `CURRENT.md`
- A bookmark of CURRENT.md is a snapshot of bytes. It is not a Yes. It does not replace CURRENT.md. It is not apply.

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
- bookmark-as-yes
- restore-bookmark-by-model

## Limits
- I may revise this file directly; agent output is suggestion until I use it
- Do not add `bookmark` to `AETHER_VERBS`. Do not implement `aether bookmark`. Do not add a restore verb.
- The snapshot at `.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md` stays a copy. Do not copy it onto CURRENT.md as apply.
- Do not copy a weight, a blob, or a Modelfile into `android/`. Do not add a model asset to the APK.
- Do not draw a model on `sit_well_draft.png`. That plate stays the one sheet, NOT ACTIVE and "not the plan".
- Do not edit `sit_well_plan.png`, `sit_well_receipt.png`, `sit_folder_dest.png`, the chassis, the title plaque, the three lamps, the four bank keys, or the gate.
- Do not restyle `decideCopy` or `receiptStrip`. Do not change "not the plan", "NOT ACTIVE", or "files only · not Yes".
- Wake may keep calling `desk_probe`. Do not draw QUIET, IDLE, LOAD, STREAM, QUEUE, or WARM on the gate. Join stays a no-op. Do not call `wake_desk`. Do not spend an Onyx call.
- Sidecar personas may speak read-only. They do not edit this file.
- Do not install Refly, Aegis, an npm CLI, or a policy package. Do not treat `approval: auto` as a Yes.
- Do not add a workflow file. Do not pick a vendor. Do not install Maestro or Appium.
- Do not bump versionCode. Do not assemble a store APK. Do not install on the phone. Do not boot a second storm. Do not tap Confirm. Do not tap Yes.
- Do not write `~/anphuni-project` or a trading tree
- No emails, names, or secrets in git
- Local `:8788` stays the room sit; apex only after human deploy
- No `aether approve` / `aether apply` / `aether next` by the model
- The model does not invent a recipient, message a person, upload to Play, deploy apex, or spend an Onyx call
- Signing keys stay off git (`~/.mechanicall/play-upload.jks`)
- Rename/delete in `~/anphuni-project` or `~/clients` is the operator Next, with preview + Yes there
- Remote CI is not this halt.

## Parked (following — not this Next)
- **aether-bookmark** — `aether bookmark [label]` copies CURRENT.md to `.aether/bookmarks/`. Spec in `.aether/proposals/CURRENT-proposal-20261016-1724.md`. Restore is a later human hand. Not this halt.
- **draft-millwork-rapid** — one host propose of v6 into a `/tmp` PROPOSE-CURRENT.md. Body Action id was this string until the header moved. Snapshot preserves that split.
- **desk-model-turn** — an Onyx reading stays parked.
- **aether-run** — ollama-shaped `aether run` then approve or reject. Not this halt.
- **cmd-aether-approve** — protect typed approve reasons. Not this halt.
- **event-inject-hook** — on-toggle inject of events into conversations. Not this halt.
- **draft-decide-millwork** — the Draft sheet is recorded. Decide's own-plate paint is not this call.
- **page-chrome** — sat 2026-10-12 on emulator-5554. The gate stays painted WAIT.
- **share-desk** — Wake already calls `desk_probe` in the dirty demo. The extra gate word and the bar stay off the glass.
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
**Action id:** advanced-local-model

Write the local-model framework I would approve of. Keep the bookmark verb parked. Then halt.

1. Grill and write one framework document for the host tag `personal-llm-sft-v6:latest`.
2. Do not add `bookmark` to `aether`. Do not restore from the snapshot onto CURRENT.md.
3. Do not copy a weight into `android/`. Do not draw a model on the Draft sheet. Leave NOT ACTIVE and "not the plan" as they are.
4. Do not spend Onyx. Do not tap Confirm. Do not tap Yes. Do not bump versionCode. Halt.

## Evidence sought
1. Does header Next and body Action id both read `advanced-local-model`?
2. Is `aether bookmark` still absent from `AETHER_VERBS`?
3. Does `.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md` still match cksum `3532677481`?
4. Is there a weight file under `android/`? The answer sought is no.
5. Did versionCode stay 46, and was Yes left untapped until a later human approve?

## Approval condition
Human applies the proposal, then `aether approve` with a real reason. Apply is not a Yes. Do not `aether next` this same id after apply; the body already sets it. The bookmark verb stays closed while Approval is DRAFT. Silence is never permission.

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
```
