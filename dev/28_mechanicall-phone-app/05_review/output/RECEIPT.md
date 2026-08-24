# Receipt — phone app (not Yes)

**When:** 2026-08-19  
**Operator CURRENT:** still SELECT / REJECTED. Model did not `aether approve`. Opening/Load is not Yes.

## Built

APK **Mechanicall** `0.2.0-seat` at `android/app/build/outputs/apk/debug/app-debug.apk`.  
Face: Plan · Draft · Yes (two-tap) · Not yet · Receipt. Launcher name Mechanicall.

Specialists: face (Kotlin) + engine (sync + 16 tests). Orchestrator assembled.

## Sideload — on the A33 (2026-08-19)

`adb` state **device**. `sh scripts/sideload-apk-via-edge.sh`:

```
Performing Streamed Install
Success
versionName=0.2.0-seat
```

Package `com.mechanicall.pocket.demo` (replaces Brake). Launcher name **Mechanicall**. Opened with monkey (Load/open is not Yes). Pocket `CURRENT.md` is at `/sdcard/mechanicall-pocket/` (dated 2026-08-16). Model did not tap Yes. Operator CURRENT still REJECTED.

## What you do

1. Unlock the A33. Accept **Allow USB debugging** (RSA fingerprint for the Mac).
2. Say **retry sideload**.
3. Open **Mechanicall**. Load is not Yes. **You** tap Yes if you mean it.
4. Then **you** `aether approve` with a real reason if this is the product you wanted.

Silence is never permission.
