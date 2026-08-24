## Inputs
- Layer 4: ../01_analyze/output/FACE-WALK.md
- Layer 3: ../../python/aether_pocket.py
- Layer 3: ../../android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt
- Layer 3: ../../android/app/src/main/python/aether_bridge.py
- Layer 1: ../CONTEXT.md

## Process
You are **implement**. Operator skipped halt (proceed with the phone face).

1. Add `face_state` to `python/aether_pocket.py`. Open is not Yes. Refuse operator tree as a dict, not a crash.
2. Expose `face_state` from `aether_bridge.py`.
3. Tests in `tests/test_aether_pocket.py`.
4. Rewrite `DemoFace` so the walk is the screen. Word aether not on the face.
5. `sh scripts/sync-pocket-engine.sh`
6. Bump `versionName` to `0.3.0-walk`. Keep `applicationId`.

Do not `aether approve`. Do not tap Yes. Do not write operator CURRENT.

## Outputs
- RECEIPT.md -> output/
- summary.md -> output/
