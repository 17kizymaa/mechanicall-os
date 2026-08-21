# FACE-SPEC — Mechanicall debug window

**Not CURRENT. Not Decide.** For Next `mechanicall-debug-window` after a human applies the proposal.

## Window (actual)

- OS-resizeable (`android:resizeableActivity=true`). Compact default size. **Does not maximise.**
- On a phone: letterbox the plugin on a dark host so the window is visibly smaller than the display. Not a 92% card with a fake title bar filling the glass.
- If Samsung freeform/DeX exists on the A33, use it. If not, letterbox is the honest stand-in — say so on the receipt.

## Camel Space compact

- Gunmetal panels, **tight** 1–2px bevels (highlight + shadow), dense banks.
- **Yellow-gold** LCD for Next / fields.
- **Purple** for live debug: GATE LEDs, armed Decide.
- Title bar: MECHANICALL + DIR + FILES. Bind is not a page.

## Pages (four)

| Bank | Role |
|------|------|
| PLAN | CAPITALISED fields |
| DRAFT | slim desk; GATE row is the thinking surface |
| DECIDE | two pads fill the **plugin** (not the phone); Why on Confirm |
| RECEIPT | trail + events |

DIR = folder slot. Law copy stays on DECIDE.

## GATE (thinking — not a chat ellipsis)

While myarch Ollama streams:

- A **16-step trance-gate** (purple LEDs left → right) and/or a tiny scope.
- Labels: IDLE · WARM · GATE · QUIET.
- No “…” bubble, no “is typing”, no three bouncing dots.
- Stream `draft_chat` (`stream: true`). Fail closed: GATE goes QUIET, short “desk quiet”.

## Desk-hop (anyone boots myarch)

```text
ollama serve          # already a systemd unit on this host
personal-llm-sft-v4   # local model
private binds only    # 127.0.0.1 / LAN / Tailscale — never 0.0.0.0 as product
```

Script: `scripts/boot-desk.sh` (to write after Yes) prints URLs and model ready. Face DESK lamp yellow = reachable.

## STORM

Install once: emulator + `system-images;android-34;google_apis;x86_64`.  
Two AVDs max. Isolated pockets. Never RZCW2038KHN. Never Confirm.

## Mark (this update: simplify only)

Two shapes: **slab** (yellow) + **disc** (purple) on gunmetal. No chair legs, no cream tile. Preview: `icon-simplified.jpg`.
