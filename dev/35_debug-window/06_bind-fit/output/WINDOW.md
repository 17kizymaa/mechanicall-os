# WINDOW — is true windowed mode unstable outside the A33?

**Not CURRENT. Not Decide.** Written under Next `mechanicall-debug-window`.

## Short answer

**OS `resizeableActivity=true` is stable** on API 26+ (this APK’s minSdk). It does **not** make sideload fail. It only *allows* split-screen / Samsung pop-up / DeX if the OEM offers them.

**OS freeform (a floating plugin with a default size) is not portable.** Galaxy A33 One UI has Multi Window and pop-up view, but the app cannot force itself into a pop-up at launch. `storm-0` (API-34 `google_apis` AVD) launches the activity full-screen unless the emulator’s freeform developer option is on. Adding:

```xml
<layout android:defaultWidth="360dp" android:defaultHeight="560dp" />
```

inside `<activity>` is the thing that actually misbehaves off Samsung / off desktop-mode: some builds ignore it, some launch a tiny unusable task. **We did not add that.** That is the revert.

## What we reverted (painted window, not OS window)

`0.10.0-client` letterboxed a 360×560 card at 0.86×0.74 of the display, with fake traffic-light dots and a heavy shadow on a black host. That was a **painted** window (CURRENT Reject: “Painted maximise / fake window”). Effects on a phone:

- Taps and IME lived in a postage stamp; Send was eaten by the keyboard.
- The sit looked like a VST plugin screenshot, not a folder you can name.
- It did **not** change APK download. It made the downloaded sit unusable.

`0.11.0-bind` fills the activity (6dp inset + system bars + IME padding). Camel Space bevels, yellow LCD, purple GATE stay. DIR / FILES only after one folder is bound.

## Sideload vs windowing

Sideload risk on this APK is **size and USB**, not resizeable:

- Chaquopy + `arm64-v8a` + `x86_64` ≈ 40 MiB. x86_64 stays so `storm-0` can install the same artifact as the A33.
- `MANAGE_EXTERNAL_STORAGE` is granted via `appops` after install; it does not fail `adb install -r`.
- True freeform launch flags were never in the manifest.

Samsung pop-up on the A33 remains available to the human: recents → pop-up view. Opening that is not Decide.
