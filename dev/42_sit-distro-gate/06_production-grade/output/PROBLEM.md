# PROBLEM — production-grade APK in git vs live law

**Noted 2026-08-24.** Not CURRENT. Not Yes. Not a silent recant of Play production Reject.

## What you said

1. “I want production-ready stuff.”
2. “I still wanting to PR a production-grade APK to git.”

## What live law says (`CURRENT.md` Next `sit-distro-gate` APPROVED)

- Objective: **closed testers**, Play **internal/closed**, **not production**.
- Reject: **Play production listing this Next**.
- Limits: no `.jks` in git; LTE receipt **before** Console upload; All-files-access is a Console declaration.
- Action (4) LTE is **BLOCKED** this sitting (USB A33 ≠ LTE).
- Action (5) signed AAB exists **off git**; Console login is **human**.

## The mismatch

| You want | What we actually have |
|----------|------------------------|
| Production-**ready** / production-**grade** APK **in a git PR** | Source + listing pack can go in git. **AAB/APK/jks must not** (gitignore + Limits). |
| Play Store as a real store | Live Reject is **production listing**. Internal/closed is allowed after LTE. |
| Merge #7 as the distro | GPT-5.6 `13_*`: merge immediately **No**; Play internal today **No** until zip+stock-phone (those are now in tree, not all on origin until last Go-git). |

## Already true on disk (do not re-ask)

- Zip contain + native Publish + API 36 in working tree / PR #7 after Go-git (`0.17.1-api36`, versionCode 22, target 36).
- Signed release AAB: `android/app/build/outputs/bundle/release/app-release.aab` SHA-256 `5442e455…b5c952`. Keystore `~/.mechanicall/play-upload.jks` (backup; not git).
- Listing copy: `android/play-listing/`.
- PR: https://github.com/17kizymaa/mechanicall-os/pull/7 — human merge only.

## What a grill must decide (not implement until CURRENT recants)

Whether “production-grade in git” means (a) quality bar for closed testers, (b) binaries in the PR, or (c) recant Play **production listing**. Dual-Next still Reject. Models do not `aether next`.
