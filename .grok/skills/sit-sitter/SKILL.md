---
name: sit-sitter
description: >
  Sit the live Mechanicall APK on storm-0: walk CRects, look at stills,
  write FLAGS against FIT holes. Never millwork. Never Confirm. Never Yes.
  Never A33. Never aether approve. Use when /sit-sitter, S=1 sitter session,
  or "use the APK" for chassis refinements.
---

# Sit sitter

You **use** the APK. You do not paint. You do not Yes. PASS is not human Yes.

## Law

1. Read root `CURRENT.md`. `aether preflight` the live Next. Do not rewrite CURRENT.
2. Never `aether approve` / `next` / `reject`. Never tap Confirm. Never two-tap Yes. Never `yes()`.
3. Never serial `RZCW2038KHN`. Storm-0 only. Cap **one** sitter on that AVD.
4. Do not millwork. Do not farm-paint. Do not land nodpi. Do not spawn a second sitter.

## Contract

Fit (holes, not a new chassis): `dev/60_day-synthesis/10_interaction_preview/output/FIT.md`  
Landed APK: `0.19.17-fit` vc 42 · archive `~/.mechanicall/apk-archive/mechanicall-0.19.17-fit-vc42.apk`  
Stage: `dev/60_day-synthesis/13_sit_sitter/`

Environment: `/storm-review` (boot if needed). Look scorers after stills: `look_verify.py`, `mum_verify.py`. Behaviours: `app_verify.py` (law, not beauty).

## Process

```bash
# storm-0 already up → skip storm-up
python3 dev/60_day-synthesis/07_sdk_stills/walk_ritual.py \
  --out dev/60_day-synthesis/13_sit_sitter/output/stills \
  --apk android/app/build/outputs/apk/debug/app-debug.apk
python3 python/look_verify.py --png-dir dev/60_day-synthesis/13_sit_sitter/output/stills
python3 python/mum_verify.py --png-dir dev/60_day-synthesis/13_sit_sitter/output/stills
python3 python/app_verify.py --uidump-dir dev/60_day-synthesis/13_sit_sitter/output/stills
```

Then **look at each PNG** (`read_file`). Score FIT holes into `output/FLAGS.md`.

Labour after Yes is **unseen** unless a human already stamped on that pocket. Do not two-tap to see feet. FLAG: `PLAN-labour unseen (no Yes)`.

SAF bind may miss on storm-0; seed pocket is honest. FLAG the miss; do not bind mechanicall-os.

## FLAGS.md rows

Each FIT hole: `KEEP` / `FLAG` / `UNSEEN` + still filename + one sentence. No millwork plan unless the human already stamped FLAGS.

## Halt

`output/FLAGS.md` + stills. Stop. Human stamps which FLAG is Next millwork.

## Never

- Confirm / Yes / A33
- CURRENT paste
- L4 nodpi
- Fake `yes()` / lab jump that stamps
- Worktree isolation (device is shared)
