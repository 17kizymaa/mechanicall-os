# RUN-TEST — one sit on storm-1 (storm-0 left alive)

**Not Yes.** Live repo `CURRENT.md` was not written. Serial `emulator-5556` only. Confirm not tapped. A33 not used.

## What we did

| | |
|--|--|
| Left alive | `emulator-5554` storm-0 (`adb get-state` = device) + this repo CURRENT |
| New SDK | `storm-1` AVD, boot `-port 5556` |
| Pocket | `/tmp/sitrun1/CURRENT.md` (sitter text, 309 B). **Not** mechanicall-os. |
| APK | `0.15.2-luminance` after a stale `0.15.1-sos` first install |
| Walk | Bind → PLAN → DRAFT → SEND (attempt) → DECIDE first tap only |

Throwaway CURRENT we seeded (recreate the *shape*, not the operator file):

```
**Objective:** Sit with a client on their own folder. One Next. Yes only they can give.
**Next:** name-the-sit
**Approval:** PENDING
```

Glass never showed that file because bind landed on **`/sdcard/si`** (truncated path). Title bar: `MECHANICALL si`. PLAN: *No CURRENT.md in this folder.* That is honest. Confirm still not Yes.

## Flow on glass

| Step | File | Result |
|------|------|--------|
| Bind | `bind.png` / `typed2.png` | Path typing is the bottleneck (below) |
| PLAN | `plan2.png` | CURRENT body + Changes. Empty folder. No “hunk”. |
| DRAFT | `draft2.png` | LIVE (none). Change Objective + SEND. |
| SEND | `sent.png` | Composer had text; IME covered SEND; 4s later still “No desk say” |
| DECIDE | `decide2.png` → `armed2.png` | YES gold plate → AGAIN. **Confirm not tapped.** |

## Bottlenecks → standardised solutions

| # | Bottleneck | Standardised solution |
|---|------------|------------------------|
| B1 | Second AVD without `-port` can collide with 5554 | Always `emulator -avd storm-1 -port 5556`. Cap 2. Leave storm-0. |
| B2 | `uiautomator dump` fails until `sys.boot_completed=1` | Wait on that prop; retry dump 5×. |
| B3 | `adb shell input text /sdcard/sit-run-1` treats `-run-1` as **adb flags** → path becomes `/sdcard/si` | Pocket ids **without hyphens** (`sitrun1`). Quote the string. Prefer SAF “Choose your folder”. |
| B4 | `KEYCODE_BACK` to dismiss IME can **leave the activity** | Never BACK from bind. Tap the Bind pad through the IME, or `ime disable`. |
| B5 | Bind label is a child `Text`; `clickable="true"` is on the parent `Box` | Tap **bounds of the text**, not only nodes with `clickable="true"`. |
| B6 | `install -r` **keeps SharedPreferences** (`pocket_one=/sdcard/si`) | Lab: `adb uninstall` then install, or clear `mechanicall_seat` prefs. |
| B7 | Stale `app-debug.apk` (0.15.1-sos cyan vs 0.15.2-luminance) | `assembleDebug` immediately before install; print `versionName`. |
| B8 | API-34 bind of `/sdcard/...` needs `MANAGE_EXTERNAL_STORAGE` | Lab `appops set … allow`. Product path = SAF picker. |
| B9 | 48× `KEYCODE_DEL` to clear the field is slow and lossy | `adb uninstall` or set prefs; don’t DEL-loop. |
| B10 | SEND while IME is up misses the pad | Hide IME with a tap **outside** (not BACK), then SEND. |
| B11 | Desk SEND vs 7B LOAD (68s+) / QUEUE | GATE LOAD is the instrument. Don’t treat quiet as Yes. One generate. Pause extra AVDs if RAM fights. |
| B12 | JOIN still NOT-ON-NET | Key is backend provision; tsnet JNI still named gap. Don’t paste-well. Don’t lie connected. |
| B13 | Host `java` 26 vs Gradle | `JAVA_HOME=$HOME/.jdk/temurin-17`. |
| B14 | Two AVDs + 7B | Cap 2 is the standard. Kill **storm-1** when the run is done; **do not** kill storm-0 unless asked. |

## What this is not

- Not a rewrite of live CURRENT.
- Not a Play Store listing.
- Not a Yes (Decide armed only).
- Not bind-phone-to-this-repo.

## Standard lab recipe (next run)

```bash
# leave storm-0
python3 python/aether_storm.py create --name storm-1
# boot: emulator -avd storm-1 -port 5556 -no-snapshot -gpu swiftshader_indirect
adb -s emulator-5556 uninstall com.mechanicall.pocket.demo || true
JAVA_HOME=$HOME/.jdk/temurin-17 ./gradlew :app:assembleDebug
adb -s emulator-5556 install -r app/build/outputs/apk/debug/app-debug.apk
adb -s emulator-5556 shell appops set com.mechanicall.pocket.demo MANAGE_EXTERNAL_STORAGE allow
# pocket path: /sdcard/sitrun1  (no hyphens)
# walk: Choose folder or type path; never BACK; never Confirm
```
