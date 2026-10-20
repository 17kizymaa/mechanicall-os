# CURRENT

**Objective:** Start the APK sprint by scaffolding the modelling work from the aether CLI as it stands.
**Phase:** APPROVE
**Status:** APPROVED
**Baseline:** 2026-10-20 · pin com.mechanicall.pocket.demo 0.19.21-loop-from-20 versionCode 46 · snapshot .aether/bookmarks/CURRENT-20261016T162428Z-this-current.md cksum 3532677481 · aether 0.3 · desk and pre-apply shipped · closed-tester, not production
**Next:** new-apk-sprint-start
**Approval:** APPROVED
**Host:** myarch · local sit :8788 · apex after human deploy · branch `feat/share-urls-readiness`

## What I want now

The aether CLI is confident enough to scaffold the modelling work. This Next writes that scaffold and stops. It does not assemble an APK.

The operator's reason for this suggestion: We should get back to what we was doing - 'aether' CLI is something confident enough to scaffold off of in terms of the modelling work.

## Product (non-negotiable identity)

- **Is:** Mechanicall: You Decide. Inference proposes. I dispose. Models never approve. Silence is never permission.
- **This Next:** `new-apk-sprint-start`. Scaffold only.
- **Not this halt:** assembling an APK, a versionCode change, a phone install, Play, a weight inside `android/`, deleting personas, putting `ctx` on `PATH`.

## Keep

- Plain, inspectable history; one useful Next; files + git to go back
- Mechanicall is my Yes; models never approve; silence is not permission
- versionCode stays 46 for this start
- The pin snapshot cksum stays 3532677481
- Weight stays outside the APK
- Desk, index selection, and pre-apply stay as shipped

## Reject

- automatic-approve
- model-invokes-pre-apply
- assembling during this start
- a second Next beside `new-apk-sprint-start`

## Limits

- I may revise this file directly; agent output is suggestion until I use it
- The model does not run `aether approve`, `aether apply`, `aether next`, or `aether pre-apply`
- Do not assemble an APK in this halt. Do not bump versionCode. Do not install on the phone. Do not upload to Play.
- Do not copy a weight, a blob, or a Modelfile into `android/`
- Do not delete `.grok/personas/` files
- Do not put `ctx` on `PATH`
- The snapshot at `.aether/bookmarks/CURRENT-20261016T162428Z-this-current.md` stays a copy
- Silence is never permission

## Parked (following — not this Next)

- **apk-from-cli** — after this scaffold. Pin stays versionCode 46 until a later Next says otherwise.
- **apk-sprint** — the assemble, after the scaffold.
- **add-pre-apply** — the command exists. Not this Next.
- **aether-desk** — shipped. Not this Next.
- **strike-stale-limit** — leftover Limits wording. Not this halt.

## Next allowed action

**Action id:** new-apk-sprint-start

Write the modelling scaffold under `dev/87_new-apk-sprint-start/output/` and halt.

1. Record the aether CLI surface the scaffold stands on: verbs in use, `aether desk` index selection, and `aether pre-apply` as a human hand.
2. Record the APK constraints the later assemble must keep: versionCode 46, the pin cksum 3532677481, no weight in the package.
3. Write one scaffold note. It is not an assemble script.
4. Halt. Do not assemble. Do not install. Do not open Play.

## Evidence sought

1. Does `dev/87_new-apk-sprint-start/output/` contain the scaffold note?
2. Does the note name the CLI surface and the pin constraints?
3. Does versionCode stay 46?
4. Does the pin snapshot cksum stay 3532677481?
5. Was an APK assembled in this halt? The answer must be no.

## Approval condition

The operator runs `aether pre-apply` with the reason and this file. That stamp is the Yes. The model does not run it. Apply of a proposal is not this path. Silence is never permission.

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
- model-invokes-pre-apply
