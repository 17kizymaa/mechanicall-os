# ACCESS — TalkBack / large-control / first-time sitter

**Not CURRENT. Not Yes. Not an approve.**  
Walk scored: bind → read PLAN → use DRAFT.  
Glass: `08_execute-nexts/output/{plan,draft}.png` + `10_demo-polish/output/storm-0/{home.png,uidump-plan.xml}` + `08_execute-nexts/output/storm-0/uidump-draft.xml`.  
Source: `PlanModule.kt`, `ChatHome.kt`, `SeatTheme.kt` (`DeskStrip`, `PluginTabs`, `ChromeBtn`), `BindModule.kt`, `SeatNav.kt`.  
Role: TalkBack on, fat finger, first afternoon. I would struggle. I would not finish the workshop cleanly.

## Struggle score: **4 / 5**

5 = cannot complete. 0 = I would not notice.  
**4** = bind is possible if I hit the 56.dp pad; PLAN is a markdown wall I can hear but cannot *use*; DRAFT is a protocol chip museum; chrome eats the first twelve TalkBack stops; several verbs are 26.dp gold traps. Sighted large-control and TalkBack both fail the same walk. Not 5 because ink-on-cream plan text exists and banks are still swipe targets.

Not Yes.

---

## Walk (what I actually did)

### Bind

FACE-SPEC: unbound shows **FOLDER** only. After bind, `DIR` is the rebind slot (`SeatTheme.kt` `ChromeBtn("DIR")`). I am looking for the word FOLDER. I hear **DIR**, **FILES**, then JOIN / WAKE. Rebind is a 44.dp title-bar chip named like a file manager.

`BindModule` (source, not on 08/10 bound glass):

- Intro copy is **LCD gold on Host cream** (`SeatPalette.Lcd` on `Host`) — ~**1.2:1**. I cannot read “This sit holds one folder” with low vision.
- Helper copy is **BevelLite on Host** — ~**1.5:1**.
- **Choose your folder** is 56.dp. That one I can hit. System picker is honest.
- **Bind this folder** is **40.dp** and **BevelLite on PanelDark** (~**1.2:1**). Support path is a ghost.

If I am already bound (08/10 glass), I never see that pad. I only see DIR.

### Read PLAN (B2, B3)

Landing after bind is PLAN (`SeatNav.landingFrom` else → Plan). Good intent. The paper I get is not B2.

08 `plan.png` / 10 `home.png` / 10 `uidump-plan.xml`:

- Twelve chrome nodes before “The published plan.”
- Then one `TextView` that *is* the page: `# CURRENT` plus `**Objective:**` markdown, clipped at the fold. Bounds `[70,1106][1010,2248]` — the dump fills the scroll viewport.
- **No `OBJECTIVE` field. No `NEXT` field. No `SAVE DRAFT`.** They are not in the captured tree. Source puts them *under* the dump (`PlanModule.kt` `SeatCard { plan }` then `PRIMARY_FIELDS`). I never scroll that far because TalkBack already recited a protocol novel, including asterisks.
- Banks: PLAN looks selected; DRAFT / DECIDE / RECEIPT are **grey-on-cream**. `selected="false"` on **every** tab, including PLAN.

B2 need: *CAPITALISED live fields. Objective and Next first.*  
B2 not: *Protocol dump as the only page.*  
Captured PLAN **is** the protocol dump as the only page.

B3 need: *Human can edit plan fields on PLAN without chat.*  
Source has `PlanField` + `SAVE DRAFT · not Yes`. Glass + uidump do not present it. A first-time sitter will be told “Edit in Draft, or SAVE DRAFT here” and will not find the control.

### Use DRAFT (B4)

08 `draft.png` / `uidump-draft.xml`: after the same chrome, I get **nineteen** clickable heading chips (PREAMBLE … HUMAN DECISION REQUIRED), then a LIVE body that is still `**Objective:**` markdown, then Suggest Objective + SEND.

B4 need: *Draft is a plan workshop: live vs proposed fields.*  
B4 not: *Chat-app identity* — and, from 11 CONTEXT, *not a chip museum*.

Source tries to hide the museum (`ChatHome.kt` `primary = Objective, Next` unless `more` or `differs`). Glass shows the museum anyway: every hunk heading is a chip, most in **Suggest purple**, so I cannot tell which field I am on without the thin purple border on OBJECTIVE. TalkBack: nineteen “button” stops named protocol, **empty `content-desc`**, **no selected**. LIVE is not “LIVE · Objective” in the dump (source string is `LIVE · $focus`). Composer is reachable only after the museum. SEND is a 45×44.dp grey plate next to a second verb **SEND FOLDER** in the strip.

I can send if I already know the ritual. I cannot *discover* the workshop.

---

## Tap targets (large-control)

Device glass is 1080×2340; 48.dp ≈ 144.px at ~3.0 density. Material / fat-finger bar is 48.dp.

| Control | Uidump bounds (px) | ≈ dp | Verdict |
|---------|--------------------|------|---------|
| DIR / FILES | DIR `[755,146][887,278]` → 132×132 | ~44 | Short of 48; title bar is 36.dp in source |
| WAKE SLEEPING | `[314,480][549,558]` → 235×**78** | **~26 tall** | Fail. Gold lure, tiny hit |
| SEND FOLDER · not Yes | `[560,480][917,558]` → 357×**78** | **~26 tall** | Fail |
| JOIN NOT-ON-NET | `[37,480][303,612]` → 266×132 | ~44 tall | Disabled (`enabled="false"`) until paste; overlaps paste well (JOIN bottom 612, paste top 558 on 10 dump) |
| PLAN/DRAFT/DECIDE/RECEIPT | `[37,710][282,820]` → 245×**110** | **~37 tall** | Source `PluginTabs` **height(32.dp)** |
| DRAFT chips (PHASE) | `[459,849][591,981]` → 132×132 | ~44 | Tight; 19 of them |
| SEND (composer) | `[900,2097][1035,2229]` → 135×132 | ~45 | Almost; next to IME |

Source padding that produces the 26.dp strip:

```167:201:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/SeatTheme.kt
            Text(
                "JOIN ${joinStatus.uppercase()}",
                ...
                fontSize = 9.sp,
                ...
                    .padding(horizontal = 6.dp, vertical = 3.dp),
            )
            Text(
                "WAKE ${wakeStatus.uppercase()}",
                ...
                fontSize = 9.sp,
                ...
                    .background(if (wakeEnabled) SeatPalette.Lcd else SeatPalette.Panel)
                    .clickable(enabled = wakeEnabled, onClick = onWake)
                    .padding(horizontal = 6.dp, vertical = 3.dp),
            )
            Text(
                "SEND FOLDER · not Yes",
                ...
                fontSize = 9.sp,
                ...
                    .padding(horizontal = 6.dp, vertical = 3.dp),
            )
```

```303:327:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/SeatTheme.kt
fun PluginTabs(...) {
    Row(
        Modifier
            .fillMaxWidth()
            .height(32.dp)
            ...
```

PLAN save is also a small `Text` pad, not a 48.dp plate:

```114:136:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/modules/PlanModule.kt
        Text(
            "SAVE DRAFT · not Yes",
            ...
            fontSize = 11.sp,
            ...
                .padding(horizontal = 10.dp, vertical = 8.dp),
        )
        Text(
            if (detailed) "Hide the rest" else "Detailed plan",
            color = SeatPalette.Lcd,
            ...
            fontSize = 11.sp,
            ...
                .padding(horizontal = 10.dp, vertical = 6.dp),
        )
```

`BindPad` “Bind this folder” is **height(40.dp)** vs “Choose your folder” 56.dp.

Preauth well: source `BasicTextField` **height(22.dp)**; 10 uidump stretched it to ~44.dp. Either way it has **no content-desc**. First sit is asked to paste Headscale into a strip the FACE-SPEC still calls a well; 11 CONTEXT already wants that well gone.

---

## Contrast

Approx WCAG against `SeatPalette` (`SeatTheme.kt` 36–54). Paper ink (`Ink` `#1B1814` on `Panel` `#F3ECDD`) is ~15:1 — the only comfortable reading. LCD gold on `LcdBg` is ~11:1 — fine **on the rack**, not as the document.

| Pair | Where | ~ratio | |
|------|--------|--------|--|
| `BevelLite` `#C8C4BC` on `Panel` `#F3ECDD` | **Unselected PLAN/DRAFT/DECIDE/RECEIPT** | **~1.5:1** | Ghost banks. 08/10 glass. |
| `Lcd` `#E6C14A` on `PanelDark` `#E2D8C6` | **“Detailed plan”** | **~1.2:1** | Invisible disclosure |
| `BevelLite` on `PanelDark` | Plan field names `name.uppercase()`; BindPad outline | **~1.2:1** | |
| `Lcd` on `Host` | Bind intro 14.sp | **~1.2:1** | |
| `BevelLite` on `Host` | Bind helper 11.sp | **~1.5:1** | |
| `Purple` `#6A3EA1` on `LcdBg` `#14120A` | `PlanField` draft `OutlinedTextField` | **~2.6:1** | Typed draft unreadable on the dark well |
| `Purple` on cream | DRAFT chips that `differs` | ~6.3:1 | Passes large text, still “everything is urgent” |
| `Ink` on `Lcd` gold | WAKE SLEEPING fill | ~10:1 | Passes, and therefore **looks like the primary CTA** |

FACE-SPEC: *Paper = cream/ink inside the rack. Do not flood the score with yellow.*  
`PlanField` live body is **gold on LcdBg** — LCD chrome used as the published Objective. I read the score as another instrument, not as paper.

```171:207:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/modules/PlanModule.kt
        Text(
            name.uppercase(),
            color = SeatPalette.BevelLite,
            ...
            fontSize = 10.sp,
        )
        Text(
            live.ifBlank { "(none)" },
            color = SeatPalette.Lcd,
            ...
                .background(SeatPalette.LcdBg)
        )
        ...
        OutlinedTextField(
            ...
                focusedTextColor = SeatPalette.Purple,
                unfocusedTextColor = SeatPalette.Purple,
                ...
                focusedContainerColor = SeatPalette.LcdBg,
                unfocusedContainerColor = SeatPalette.LcdBg,
```

Unselected banks:

```313:326:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/SeatTheme.kt
            Text(
                label,
                color = if (on) SeatPalette.Lcd else SeatPalette.BevelLite,
                fontSize = 11.sp,
                ...
                    .border(1.dp, if (on) SeatPalette.Lcd else SeatPalette.BevelDark)
                    .background(if (on) SeatPalette.LcdBg else SeatPalette.Panel)
```

I can swipe DRAFT. I cannot *see* DRAFT.

---

## TalkBack

Semantics in the whole demo: **Splash “Mechanicall”** + **ChatHome field chips / MORE / hunks / composer / SEND**. Nothing on DeskStrip, tabs, title, PLAN, bind pads, GATE.

08 `uidump-draft.xml`: chips are `text="OBJECTIVE"` **`content-desc=""`** despite source:

```108:116:/mnt/kingston-nixos-sync/opt/mechanicall-os/android/app/src/main/java/com/mechanicall/pocket/demo/modules/ChatHome.kt
                        modifier = Modifier
                            .semantics { contentDescription = "Field ${row.id}" }
                            .border(
                                1.dp,
                                if (on) SeatPalette.Suggest else SeatPalette.BevelDark,
                            )
                            .background(if (on) SeatPalette.PanelDark else SeatPalette.Panel)
                            .clickable(enabled = !busy) { focus = row.id }
                            .padding(horizontal = 10.dp, vertical = 10.dp),
```

No `selected`, no `Role.Button` (none in the app). 10 `uidump-plan.xml`: PLAN tab `selected="false"`. Preauth `EditText` `text=""` `content-desc=""` — TalkBack: “edit box”. GATE is two static labels (`GATE IDLE`, `DESK`) plus 16 non-nodes; not a live region. JOIN is `clickable="true" enabled="false"` with no reason announced.

Swipe tax before paper (10 plan dump, order): MECHANICALL → bound name → DIR → FILES → Next · IDLE → GATE IDLE → DESK → JOIN (disabled) → WAKE → SEND FOLDER → preauth edit → “JOIN and WAKE are not Yes.” → PLAN → DRAFT → DECIDE → RECEIPT → “The published plan.” → the not-Yes sentence → **the entire CURRENT with markdown**. That is the walk. Objective is not a heading. Next is not a heading.

PLAN `PlanField` editors have **no `label`** on the `OutlinedTextField`. If I ever reach them, TalkBack says “edit box” in purple, not “Objective, draft, not Yes”.

Clickable `Text` everywhere (JOIN, tabs, SAVE DRAFT, chips, SEND). Compose will often expose them as buttons; uidump still classes them `TextView`. Scrim on `PluginDialogFrame` is a full-screen clickable with no name — gray-outside-closes (FACE-SPEC) is an accidental dismiss for TalkBack.

---

## Cognitive load (B2 / B3 / B4 vs FACE-SPEC)

I am a first-time sitter. The pitch is *You decide. AI does the point-and-clicking — under a plan you can read.*

What the face taught me instead:

1. **Rack first, score last.** Title, LCD, GATE pits, JOIN/WAKE/SEND FOLDER, preauth, four banks — then paper. FACE-SPEC wants compact rack around the document. The document never gets the first glance.
2. **PLAN is CURRENT.md with asterisks.** B2 wanted CAPITALISED Objective and Next first. I got `# CURRENT` / `**Objective:**`. One TalkBack node. Editors (B3) live below a dump I already think is the whole page.
3. **Two workshops.** PLAN says “Edit in Draft, or SAVE DRAFT here”. DRAFT is Suggesting + SEND. I do not know which desk is the desk.
4. **Chip museum.** DRAFT exposes hunk ids: PREAMBLE, NEXT ALLOWED ACTION, CONFLICTS WITH EXISTING AUTHORITY, HUMAN DECISION REQUIRED. That is operator schema, not an afternoon plan. Purple means “differs” and also means “all of them”.
5. **Verbs that are not Yes, that sound like Yes.** ACCEPT HUNK, Accept is not Yes, SEND, SEND FOLDER · not Yes, JOIN, WAKE. FACE-SPEC: *Hunk accept / JOIN / WAKE / LOAD / STREAM are not Yes.* The face keeps saying “not Yes” because the labels keep sounding like Yes. WAKE SLEEPING is the only gold plate on the strip, so I tap the sleeping machine instead of reading the plan.
6. **DIR is not FOLDER.** Unbound law uses FOLDER. Bound chrome uses DIR. I will not rebind on purpose.
7. **Preauth in the score’s forehead.** A secret paste well with 9.sp hint “preauth / login-server · not stored” is not a first sit. 11 CONTEXT: *JOIN paste well gone.*

---

## What a researcher would say

“We sat a first-time TalkBack user on the storm APK and asked them to bind a folder, read what they were about to do, and change Objective.

They found a folder if we pointed at Choose your folder. After bind they landed on PLAN and heard a markdown file. They never found Objective or Next as fields. They could not see DRAFT. When we put their finger on DRAFT they got a wall of purple protocol chips and a Send next to Send Folder. They tapped WAKE because it was yellow. They thought JOIN was broken. They never met SAVE DRAFT.

Large-control users missed WAKE/SEND FOLDER (26.dp) and the 32.dp banks. Low-vision users lost unselected tabs (~1.5:1) and bind copy (~1.2:1).

The product story is paper you can read. The face is still a plugin chrome with the score trapped under CURRENT.txt and a chip museum. That is a failed B2/B3/B4 sitting, not a visual-polish leftover.”

---

## Five concrete face fixes

Do not implement in this eval. Face only. Not Yes.

1. **PLAN is Objective then Next, cream/ink, then the rest.**  
   Lead with two CAPITALISED paper cards (live text, 16.sp Ink on Panel, heading semantics). Put the raw CURRENT dump behind **Detailed plan**. **SAVE DRAFT** is a 48.dp labelled button under those two cards, Ink on a clear plate, `contentDescription = "Save draft of Objective and Next. Not Yes."` Stop painting live law as LCD gold.

2. **DRAFT is a workshop of two fields plus diffs, not 19 chips.**  
   Default `shown` = Objective + Next + hunks that actually differ — and cap the first paint at those. MORE is 48.dp. Selected chip: `selected=true`, Role.Button, 48.dp min, Ink (not a purple sea). LIVE / SUGGESTING bodies strip `**markdown**`. One SEND, 48.dp, `Send suggestion for Objective`. ACCEPT/REJECT HUNK only when a suggestion exists; never named Accept without Hunk.

3. **Banks you can see and hear.**  
   `PluginTabs` height ≥ 48.dp. Unselected: **Ink** on Panel (≥ 4.5:1), not BevelLite. Selected: announce “PLAN, selected, tab”. `selected` in semantics must match `currentRoute`.

4. **Strip is not the sitting.**  
   JOIN / WAKE / SEND FOLDER ≥ 48.dp, equal height, no gold hero on WAKE. Rename **DIR → FOLDER**. Remove the preauth well from the first sit (provision off-glass). Paste field, if lab-only, needs a name: “Headscale preauth, not stored”. JOIN disabled must speak “paste an invite first”.

5. **TalkBack pass on bind → PLAN → DRAFT only.**  
   Role.Button on every clickable `Text`. Bind intro **Ink on Host**. PlanField `OutlinedTextField` labelled “Draft Objective”. GATE as one live-region node (“GATE idle, desk quiet”), not sixteen pits. Do not put a nameless scrim under the first bind. Twelve chrome stops before paper is a bug: collapse LCD+GATE to one node so the next stop is Objective.

---

## Evidence index

- B2/B3/B4: `dev/36_actual-app-verification/01_contract/output/BEHAVIOURS.md` lines 14–16.  
- FACE-SPEC PLAN/DRAFT + DESK: `dev/38_sit-vst-headscale/01_research/output/FACE-SPEC.md` lines 8–12, 48–67.  
- Glass: `dev/39_sit-storm-factory/08_execute-nexts/output/plan.png`, `draft.png`; `10_demo-polish/output/storm-0/home.png`.  
- Trees: `10_demo-polish/output/storm-0/uidump-plan.xml` (dump is the only plan page; tabs `selected="false"`); `08_execute-nexts/output/storm-0/uidump-draft.xml` (19 chips, empty content-desc, SEND `[900,2097][1035,2229]`).  
- Source quotes: `SeatTheme.kt` DeskStrip / PluginTabs / palette; `PlanModule.kt` dump-then-fields / SAVE DRAFT / Lcd live well; `ChatHome.kt` chip FlowRow / semantics.

Walker did not tap Confirm. Model did not `aether approve`. Device RZCW2038KHN was not used. CURRENT.md was not rewritten.
