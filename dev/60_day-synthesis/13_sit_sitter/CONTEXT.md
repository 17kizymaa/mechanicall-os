# 13_sit_sitter

**Not Yes. Not millwork. Not this compact chat.** Human pick **S=1**: a **new Grok session** sits `0.19.17-fit` on storm-0 and writes FLAGS.

Cold start that session with: read this file, then `/sit-sitter`.

## Inputs
- Layer 0: `CURRENT.md` · `aether preflight you-decide-ritual`
- Layer 3: `.grok/skills/sit-sitter/SKILL.md` · `/storm-review` · `/visual-reviewer`
- Layer 4: `../10_interaction_preview/output/FIT.md` · `../11_land_fit/output/RECEIPT.md`
- APK: debug assemble or `~/.mechanicall/apk-archive/mechanicall-0.19.17-fit-vc42.apk`

## Process
You are the **sitter**. Use the APK. Look at stills. Write FLAGS vs FIT holes. Never two-tap Yes. Never A33. Never millwork. Never CURRENT.

1. Boot storm-0 if needed (`scripts/storm-up.sh storm-0`). Cap one sitter.
2. `walk_ritual.py --out output/stills --apk <apk>`
3. `look_verify` + `mum_verify` + `app_verify --uidump-dir output/stills`
4. Vision each PNG. Fill `output/FLAGS.md` from `output/FLAGS-TEMPLATE.md`.
5. Halt.

## Outputs
- `output/stills/*.png` + uidump
- `output/FLAGS.md`
- `output/RECEIPT.md` (one screen: walked, never Yes)

## Halt
Human stamps FLAGS. Millwork is a **later** agent/session, one hole.
