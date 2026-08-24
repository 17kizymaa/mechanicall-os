# 08_execute-nexts — one remaining pass

**Not Yes. Not four Nexts.** Live `sit-storm-factory` APPROVED. Boot storm-0, sideload, `/app-reviewer` + `/visual-reviewer`. Never Confirm. Never A33. tsnet stays named if no gomobile.

## Inputs
- `../07_chips/output/` · `../06_leftover/output/` · `python/app_verify.py`

## Process
1. `aether preflight sit-storm-factory`
2. `sh scripts/storm-up.sh storm-0` — emulator-5554 only
3. assembleDebug + `adb -s emulator-5554 install -r`
4. storm-walk + DRAFT dump (NEXT visible)
5. app_verify source+glass; visual vs FACE-SPEC
6. `build-tsnet-aar.sh` — named gap if no gomobile

## Outputs
- EXECUTE.md, VERIFICATION.md, VISUAL.md, storm-0/
