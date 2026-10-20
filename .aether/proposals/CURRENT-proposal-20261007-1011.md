# CURRENT proposal — apk-share-24h — NOT LAW until you apply

**NOT ACTIVE. Not Yes.**

APPLY: human runs `/mechanicall-domain:apply` on this file (`aether apply .aether/proposals/CURRENT-proposal-20261007-1011.md`). That is not a Yes.

**Author:** proposal only. You dispose.

## Summary

The pinned tester APK is on disk. You said the share is where this starts, that the tool limits do not bind the operator, that the share can die after 24 hours, and that the remote CI layer has not been considered yet.

This proposal sets one Next, `apk-share-24h`. Header `**Next:**` and body `**Action id:**` match. It does not share anything by itself.

## What changed (before → after)

| Field | Live file now | This proposal |
| --- | --- | --- |
| Objective | Client download plus a stable layer. You still dispose. | Same objective. The start is the share of the APK already pinned. |
| Phase / Status / Approval | APPROVE / APPROVED / APPROVED | SELECT / READY-FOR-REVIEW / PENDING |
| Next / Action id | `tester-apk-live` | `apk-share-24h` |
| Relax | Ceremony, birthday polish, prospectus | Adds: tool limits on handing this APK onward do not bind the operator |
| This halt | Pin and assemble, then stop. No recipient. | One loopback share of that APK. It expires 24 hours after it starts. |
| Remote CI | Unmentioned | Parked. Not considered. Not this halt. |
| Prohibited | 19 tokens | Same 19 tokens |

Applying this body clears APPROVED until you approve.

## Observations

- The pin and the file already exist. `dev/75_tester-apk-live/output/STABLE-LAYER.md`. `dev/75_tester-apk-live/output/mechanicall-pocket-0.19.21-loop-from-20-vc46-debug.apk` is 62526130 bytes, sha256 `44900cc0adc6b823a99bdca6a2992868e4017202d540b003dc31d31d66ac4d8f`. `aapt` reads `com.mechanicall.pocket.demo`, `versionName` `0.19.21-loop-from-20`, `versionCode` 46.
- The room clip on the operator map caps one file at 8 MiB. This APK is about 60 MiB, so it does not fit that drop.
- `.github/workflows/test.yml` runs Python tests only (`tests/run.sh`, `scripts/ci-control-layer-gates.sh`). It has no Android job and no artifact upload.
- No client address is in this repo.

## Inferences

- A 24-hour share can start on loopback from the file already built. A remote client cannot fetch `127.0.0.1`.
- The remote way to hand a later build out would be a CI layer. That layer is still undesigned, so this halt does not pick a vendor or add a workflow.

## Unknowns

- Who "them" is. This file must not invent a name, an email, or an inbox.
- Which remote host, if any, should serve a later build. Not decided here.

## Fidelity checklist

- One Next: `apk-share-24h`. One matching Action id.
- Models never approve. This file does not approve by itself.
- No secrets, emails, or personal names.
- Silence is not permission. The fence stays PENDING until you approve.
- Prohibited tokens are unchanged. The Next id is not one of them.
- You dispose. The operator is relaxed from the tool's hand-off limit. The operator CURRENT is not edited. The client does not stamp this CURRENT.
- Two instances stay two.

## Conflicts with existing authority

- Live Limits say this halt may not pick a recipient, a website, or a store. You asked for that limit not to bind the operator. The proposal puts that in Relax. The model still does not message, deploy apex, or upload to Play.
- The operator CURRENT's own Next is untouched. Its share is the room clip. This proposal does not merge the two files and does not write `~/anphuni-project`.
- `agent-publish-delete-spend-message-deploy` stays prohibited. This Next is a loopback share of one pinned APK with a 24-hour end. It is not a store, an apex deploy, or a message.

## Human decision required

- [ ] Apply this file
- [ ] Reject and leave `CURRENT.md` unchanged
- [ ] Revise and ask for another proposal

After apply, `aether next apk-share-24h` refuses because Next is already that id.

## Proposed CURRENT

```markdown
# CURRENT

**Objective:** Mechanicall is my Yes. Give the client a downloadable APK, with a stable layer I use to develop the tester's version live. I still dispose.
**Phase:** SELECT
**Status:** READY-FOR-REVIEW
**Baseline:** 2026-10-07 · share starts here · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · closed-tester sit, not production · remote CI not considered
**Next:** apk-share-24h
**Approval:** PENDING
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
```
