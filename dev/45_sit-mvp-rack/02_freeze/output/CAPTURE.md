# CAPTURE — NeuralBridge 0.1.1-capture

**Not product. Not Funnel.** Clone: `~/.mechanicall/NeuralBridge_mcp`. Device: `RZCW2038KHN` SM-A336B Android 14 via mbp-edge USB.

## Failure

`android_screenshot` → `MediaProjection unavailable and AccessibilityService fallback failed.`

Log: `SecurityException: Services don't have the capability of taking the screenshot.`  
`dumpsys accessibility` `capabilities=41` (gestures + filter keys + window content). Missing `CAPABILITY_CAN_TAKE_SCREENSHOT` (128).

GRANT path: Setup tab MediaProjection **red**. Service auto-launched a translucent `ScreenshotConsentActivity` from the AccessibilityService. Android 14 / Samsung drop that dialog.

USB `adb exec-out screencap -p` on mbp-edge already worked. myarch `adb` is empty — that was the earlier “empty screencap.”

## Fix (lab clone)

1. `accessibility_service_config.xml`: `android:canTakeScreenshot="true"`.
2. Stop service auto-popup of MediaProjection.
3. MainActivity GRANT / MCP `android_request_screenshot_consent` fire the system dialog from a **foreground** activity.
4. After MediaProjection grant, `startForeground` also sets `FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION` (API 34).
5. Version `0.1.1-capture` / versionCode 2. Sideload Success. capabilities **169**.

## Proof

MCP thumbnail JPEG: `nb-screenshot-after-capture-fix.jpg` (sit glass, Compose overlay still visible — that is the sit bug, not capture).

A11y screenshot does **not** require Start now. Fast MediaProjection still does.
