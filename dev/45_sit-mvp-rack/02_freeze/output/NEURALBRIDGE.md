# NeuralBridge — look pipe (lab, not product)

**Not CURRENT. Not Funnel.** Companion is `com.neuralbridge.companion` from `https://github.com/dondetir/neuralbridge_mcp`, cloned to `~/.mechanicall/NeuralBridge_mcp` (not this repo). HTTP MCP has **no auth**. Bind is **adb forward tcp:7474** on mbp-edge USB only. Do not Funnel. Do not `0.0.0.0` from this tree.

## Why

Freeze look was not the imagined millwork. NeuralBridge is how the agent **sees and taps** the A33 (~60ms screenshot) instead of a broken `screencap` SSH pipe.

## Done from this sitting

- Companion debug APK built (JDK 17) and `adb install` **Success** on `RZCW2038KHN`
- Accessibility setting written: `com.neuralbridge.companion/.service.NeuralBridgeAccessibilityService`
- `adb forward tcp:7474 tcp:7474` (host→device). Reverse was the wrong direction.
- Sit debug rebuilt: Compose **PluginTabs millwork** removed; banks are invisible CRects. Skin is still `plan.png`.

## Blocked — you on glass

Samsung often **ignores adb a11y enable** until the human grants it.

1. Settings → Apps → NeuralBridge → **Allow restricted settings** (if shown).
2. Settings → Accessibility → NeuralBridge → **On**.
3. Open NeuralBridge. Note the IP. First screenshot: tap **Start now** on the MediaProjection dialog.
4. Leave USB in. Say **Go** — then MCP `screenshot` / `get_ui_tree` against `http://127.0.0.1:7474/mcp` via the forward.

**2026-08-25 Go:** MCP is up (`/health` 0.4.0). `android_launch_app` + `android_get_ui_tree` work over USB forward. `android_screenshot` still needs MediaProjection: NeuralBridge → Setup → MediaProjection **GRANT** → system **Start now**. Until then screenshots error; the tree is enough to see overlay bugs.

**2026-08-25 capture fix (companion `0.1.1-capture`, local clone, not this repo):**

- Root cause: `SecurityException: Services don't have the capability of taking the screenshot.` XML lacked `android:canTakeScreenshot="true"`. `dumpsys accessibility` capabilities were **41**; after patch **169** (41+128).
- MediaProjection GRANT from a translucent activity started by AccessibilityService is what Samsung drops. GRANT now fires `createScreenCaptureIntent` from **foreground MainActivity**. Human still taps **Start now** for the fast path. A11y screenshots **no longer need GRANT**.
- Proof: `output/nb-screenshot-after-capture-fix.jpg` (MCP JPEG of sit). USB ground truth: `scripts/sit-look.sh` via mbp-edge. Not LTE. Not Funnel.

Unbound sit tree after millwork bind (no Compose essays):

- `sit millwork` [0,80,1080,2281]
- `LCD idle` “Name your folder. One project.”
- `Choose your folder` paper hit [54,938,1037,2193]

Before: Bind essays covering the plates (13 interactive nodes). After: 5.

## Sit still later

Mesh / doorbell are CURRENT 03–04. This is freeze **look**.
