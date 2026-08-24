## Inputs
- Layer 4: `../01_analyze/output/FACE.md`
- Layer 3: `../../android/app/src/main/java/com/mechanicall/pocket/demo/MainActivity.kt`
- Layer 3: `../../python/aether_pocket.py`

## Process
You are **implement**. Orchestrator may spawn **two** subagents only:

1. **face** — edit Kotlin + manifest label only. Keep `applicationId` `com.mechanicall.pocket.demo` so `adb install -r` replaces Brake.
2. **engine** — sync pocket engine into Chaquopy sources; do not change Kotlin.

Do not `aether approve`. Do not tap Yes.

## Outputs
- RECEIPT.md -> output/
