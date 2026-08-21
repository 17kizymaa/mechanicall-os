# Proposed CURRENT update (draft — not authority)

**Project:** mechanicall-os  
**Date:** 2026-08-18  
**Author:** forensics follow-on `dev/24_repair-current-one-next` (propose only)

`APPLY:` human must choose A, B, or C and merge — model must not overwrite CURRENT without human gate.

## Summary

Repair the split file so **one** Next exists. Do not change the product into a Play Store app in this propose.

Full replacement texts:

- A: `dev/24_repair-current-one-next/01_propose/output/CURRENT-A-mobile-planning-demo.md`
- B: `dev/24_repair-current-one-next/01_propose/output/CURRENT-B-casual-core-interface.md`
- C: `dev/24_repair-current-one-next/01_propose/output/CURRENT-C-hold-one-next.md`

Commands: `dev/24_repair-current-one-next/01_propose/output/APPLY.md`

## Observations

- Header `**Next:**` = `mobile-planning-demo`.
- Body `**Action id:**` = `casual-core-interface`.
- Last `next_selected` = `casual-core-interface` (2026-08-11). No NS to `mobile-planning-demo`.
- `aether current validate` is OK with warnings; it does not detect the split.
- `docs/CASUAL-CORE-INTERFACE.md` is missing.
- Phone sitting PARKED 2026-08-16.

## Inferences

- Applying A makes the file match what `aether` already pins.
- Applying B makes the file match the last CLI re-SELECT.
- Applying C stops both stories until a new id is chosen.

## Unknowns

- Whether the parked sitting should resume (A) or die (C).
- Whether casual-core is still this week’s work (B).

## Proposed CURRENT change

See the three full files. Do not mix fields across them.

## Conflicts with existing authority

- A pauses casual-core (already paused in prose) and leaves events without an NS row for the demo id.
- B moves header off `mobile-planning-demo`; `android/` must not proceed as this Next.
- C rejects implementing either until re-SELECT. Closed `decision-tree.md` still says not Play Store; a store rewrite is a later propose.

## Fidelity checklist

- [x] Still one Next (per option)
- [x] Models never approve
- [x] No secrets
- [x] Silence ≠ permission
- [x] No `model-auto-write-current`
- [x] Header and body match **inside each option file**

## Human decision required

- [ ] Apply **A** (`cp` A file over `CURRENT.md`; do not `aether next`)
- [ ] Apply **B** (`aether next casual-core-interface` then `cp` B, or `cp` B only)
- [ ] Apply **C** (`aether next hold-one-next` then `cp` C)
- [ ] Reject and leave CURRENT unchanged
- [ ] Revise and re-propose

**Do not** run `aether approve` from a model or agent.
