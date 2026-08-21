## Inputs
- Layer 1: ../CONTEXT.md
- Layer 3: EDGE anphuni@100.70.86.90 SERIAL RZCW2038KHN PKG com.mechanicall.pocket.demo
- Layer 4: prior glass only if adb empty: ../../30_modular-seat/05_review/output/{splash,home,menu}.png

## Process
You are **walker 01_home**. Sequential. Do not spawn further walkers.

1. Try live: `ssh anphuni@100.70.86.90 'adb devices -l'`. If SERIAL missing, try `adb kill-server; adb start-server; adb devices`.
2. If `device`: force-stop, start MainActivity, wait ~1.3s, screencap splash (if you can catch it), home, tap Menu at ~1016,168, screencap menu. Dump uiautomator texts. **Do not tap Approve/Confirm/Yes.**
3. If no device: say BLOCKED-LIVE and score from the Layer 4 screenshots only.
4. Be harsh against the four-part definition. Opening is not Yes.

Write screenshots to this stage `output/` when live.

## Outputs
- WALK.md -> output/
- screenshots if live
