# Receipt — phone face on the A33 (not Yes)

**When:** 2026-08-19  
**Operator CURRENT:** still SELECT / REJECTED / Next `people-app-phone-seat`.  
Model did not `aether approve`. Opening the app is not Yes. Bind is not Yes.

## Sideload

`sh scripts/sideload-apk-via-edge.sh`

```
Performing Streamed Install
Success
versionName=0.3.0-walk
versionCode=2
```

Package `com.mechanicall.pocket.demo` on serial `RZCW2038KHN`. Launcher **Mechanicall**.

## What is on the glass

Screenshots (open only — no Yes tap):

- `face.png` — Bind + Plan fields (Objective, Next, Decision)
- `face-lower.png` — Draft · Yes / Not yet · Receipt empty: *No decision recorded yet. The machine did not pretend you agreed.*

Bound pocket: `/storage/emulated/0/mechanicall-pocket`  
Plan Next still `name-the-outcome` (pocket leftover, not rewritten from this tree).

## What you do

Unlock the A33. Open **Mechanicall**. Scroll the walk. **You** tap Yes if you mean it. Then **you** `aether approve` with a real reason if this is the face you wanted.

Silence is never permission.
