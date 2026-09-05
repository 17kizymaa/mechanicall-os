# CURRENT proposal — 2026-09-05 sit-dest-preview (Go)

**Not Yes.** Toy is the schema CURRENT. Human still `aether next` / `approve`.

Round 16 pins: C20b=1, C27=1, C28=1. C22=0 rack GATE = ETA. C21=1 one CRT dest.

Live CURRENT was the **memo** (validate FAIL). This Go pastes the **toy**.

Toy: `examples/propose-current/CURRENT-sit-dest-preview.md`

---

## C28 — CRT yellow implementation (review)

The tube millwork (`sit_crt.png`) **already has a yellow-brown phosphor glow** in the glass. Kotlin then paints a **second** neon layer on top.

One `TextPaint lcdPaint`:

- colour `SitCRects.LcdAmber` `#E6C14A`
- `Typeface.MONOSPACE` + `isFakeBoldText = true`
- used for **everything**: on-rack STATUS `idleLine`, isolated CRT `lcdBody()`, Draft workshop dump, Receipt well, Send overlay, CRT `EditText`

Isolated CRT path (`SitRackView.onDraw`):

1. fill `IsolatedDark` `#0A0A0C`
2. blit `sit_crt` into `isolatedCrt`
3. `drawLcd` on `glassIn(isolatedCrt)` unless IME visible

`lcdBody()` when isolated/zoomed:

```
LAW  {OBJECTIVE|NEXT|…}
{page body}
```

`LawPages.order` is `objective, next, keep, reject, limits, receipt` — **receipt is a CRT page**. C27 recants that.

Chassis `SitHit.Gate` / `LcdNext` → `IsolatedMode.CRT` (`MainActivity.onHit`). C22=0 recants Gate as a CRT door. LcdNext may still page **while already on** CRT dest.

On-rack idle (`refreshLcd`): `"PLAN  STREAM n/m\nNext: …\nTap a key. Glass holds law."` — same neon paint on the in-chassis STATUS glass.

Glitch: full-glass `LcdFlash` wash + red/cyan tear lines.

**Patch (C28=1 quieter phosphor), not a new host:**

| Keep | Change |
|------|--------|
| `sit_crt` millwork + darkened room | stop fighting the millwork glow with `#E6C14A` bold |
| composed pages (C16) | drop `LAW ` prefix; title as header, body wrapped |
| one CRT dest (C21) | split paints: `phosphorPaint` for CRT glass only |
| | paper/settings dests get their own ink (not amber dump) |
| | recant `receipt` from `LawPages` CRT list |
| | CRT `EditText` matches phosphor, not neon |

Ink rec: sit **in** the millwork glow — dimmer than `#E6C14A`, not fake-bold (e.g. `#C4B07A` or darker). Human looks at one still before freeze. Not green terminal. Not paper-black on CRT (that was C28 option 2, not selected).

---

## C27 — Receipt printer dest (clearer)

**Not CRT. Not IsolatedDark dump. Not zoom-stretch of `sit_chassis`.**

### Idle (RECEIPT bank)

- Well millwork with a **printer mouth** at the paper edge (`sit_well_receipt` — does not exist; `sit_well_decide` is 8% opaque plaque in empty alpha — do not reuse as receipt).
- Preview: last lines of the receipt **on the paper in the well**. Empty = empty mouth (B15).
- Tap the **well** → printer dest. Tap STATUS LCD on this plate does **not** isolate CRT.

### Phase 1 — extend (print out)

- Chassis stays on screen (darkened room optional around, not instead of millwork).
- A **paper tongue** grows out of the well mouth as the user scrolls. Height = scroll offset, capped at screen.
- Tongue is a **new plate** (`sit_receipt_tongue` repeatable grain), attached to the well mouth CRect. Do not scale `sit_chassis`.

### Phase 2 — lock + feed

- When tongue height hits the remaining viewport, the **frame locks**.
- Further scroll moves **content inside** the locked frame (clip + scroll). Looks like a printer feeding.
- Dismiss: snap/retract to well.

### Empty

- Mouth opens; nothing feeds. Honest.

### Hits

- Well / tongue: scroll + isolate.
- Banks: leave dest.
- GATE on rack: still ETA, not CRT, not print.

---

## C20b=1

Send lamp **and** FILES → one dest. Listing + send status. Button: open OEM file manager. Send ≠ Yes.

---

```bash
# human, after this paste:
aether next sit-dest-preview
aether approve "dest millwork look; receipt printer; Send+FILES one dest; quieter CRT phosphor; not Generate"
```

Silence is not approve. Models do not `aether next`.
