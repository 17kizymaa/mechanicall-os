# 02_plan: Portable Grok USB — Reconciliation Plan

**Date**: 2026-07-10 (sprint 0710, gate G4: "run 02_plan")
**Author**: Claude Code (sprint executor CC-6)
**Status**: awaiting human review at this output/ gate

## Why this plan exists (honest pipeline state)

The ICM pipeline for this stage ran out of order:

| Stage | State | Date |
|-------|-------|------|
| 01_analyze | done | 2026-06-26 |
| 02_plan | **skipped** — this document closes the gap | 2026-07-10 |
| 03_implement | done (USB wiped + rebuilt, user consented) | 2026-06-26 |
| 04_verify | not run | — |
| 05_review | not run | — |

Implementation diverged from the analysis' preferred Option 1 (augment the
Alpine live USB): the USB was instead fully wiped and rebuilt as a
**non-bootable ext4 data volume** carrying the awareness-agent tree plus a
bootstrap script. The user explicitly consented ("ready to wipe") at the
time, so this is a documented deviation, not an error. This plan therefore
plans **forward**: verify what exists, then close the stage.

## Reality as of 2026-07-10 (sprint inventory)

- USB is attached to the desktop as `sdb`, label `GROK-PORTABLE-DE` (note:
  execution report says `GROK-PORTABLE-DEV` — ext4's 16-char label limit
  truncated the trailing `V`; verify, don't "fix").
- Mounted **read-only** at `/tmp/grok-portable` on desktop `myarch`.
- Canonical tree moved on: `/home/awareness-agent` on mbp-edge was
  git-initialized today (commit `298dc73`, 118 files) and is backed up to
  desktop `~/backups/awareness-agent-2026-07-10/`. The USB copy is a
  June 26 snapshot and is expected to be stale.

## Plan for 04_verify

Goal: establish exactly what the USB carries and whether it still fulfils
its job ("portable way to continue the same workflow on another machine").

1. **Layout check** (read-only): confirm the five expected top-level items
   — `awareness-agent/`, `aether`, `bootstrap-replicate-grok-env.sh`,
   `packages-from-current-env.txt`, `README.txt`.
2. **Staleness diff** (read-only): `diff -rq /tmp/grok-portable/awareness-agent/`
   vs the canonical tree (git 298dc73). Record added/changed/removed files.
   Expected drift: everything committed after June 26.
3. **Bootstrap integrity** (read-only): shellcheck-style read of
   `bootstrap-replicate-grok-env.sh`; confirm it installs the essential
   set, places `aether` in PATH, and makes no network assumptions beyond
   `apk`.
4. **aether smoke test** (safe): run the USB's `aether` from a throwaway
   temp dir on the desktop (`aether init` in scratch) — proves the POSIX
   script executes outside Alpine.
5. Write `04_verify/output/verification.md` with pass/fail per item.

## Decision the verify output must tee up (human gate)

**Refresh or retire?** If drift is large, choose one:
- (a) Refresh USB from canonical tree (needs RW remount — gated action,
  propose exact commands, human approves).
- (b) Accept USB as a frozen June snapshot and label it as such in
  README.txt (also RW — gated).
- (c) Retire the USB role now that a proper backup triangle
  (MBP + desktop + GitHub, pending G1 push) exists.

No RW mount, no writes to the USB, under this plan — proposals only.

## Plan for 05_review

- Read 04_verify output, confirm acceptance criteria met.
- One-paragraph closure in `05_review/output/review.md`: stage outcome,
  deviation note (02 after 03), refresh/retire decision as taken.
- Mark stage 05 complete in the tree's `.context.md` if aether is in use.

## Acceptance criteria for closing stage 05

- [ ] 04_verify output exists with explicit pass/fail per check above.
- [ ] Staleness quantified (file counts: same/changed/only-USB/only-canonical).
- [ ] Refresh/retire/freeze decision recorded by the human.
- [ ] 05_review closure paragraph written.

## File list (deliverables of remaining stages)

- `04_verify/output/verification.md`
- `04_verify/output/drift-file-list.txt` (mechanical diff output)
- `05_review/output/review.md`

## Constraints carried forward

- CORE_PRINCIPLES: plain files, sh/md/py only, everything cat-able.
- USB writes are gated: propose → human approves → execute.
- `/dev/sda` (desktop system disk) is never a target for anything.
