# Look-closed agent loops

**Not law. Not dual-Next.** Designs for a factory whose halt is dest PNGs + FLAG. Implement only after a human `aether next` / approve of a **named** Action id. This file is research.

## Invariant

```
still dests → score look → one millwork edit → assemble → still again
until FLAG clears or the sitting budget is spent
```

Law probes (`app_verify`) stay **orthogonal**. They may run, but they must not be the halt.

## Loop A — Look-closed ICM (recommended default)

Numbered stages under the Next’s `dev/NN_…/` folder:

| Stage | Behaviour | Halt |
|-------|-----------|------|
| `01_still` | storm-0 dest walker writes PNG+uidump to `output/` | file set complete or walker FAIL |
| `02_score` | visual-reviewer (patched Inputs) + `look_verify.py` | `VISUAL.md` FLAG/FAIL |
| `03_one_plate` | **one** millwork or blit change named in FLAG | diff + RECEIPT |
| `04_assemble` | debug APK; archive | versionName in archive |
| `05_still_again` | same walker | human recants FLAG or budget=0 |

Human reviews `output/` between 02 and 03. Do not auto-advance. Do not A33 until SDK FLAG is boring.

**Why it matches “final output in mind”:** the product of each cycle is a dest still, not a green table.

## Loop B — Budgeted STORM

Cap 2 AVDs (`storm-0`, `storm-1`). Parallel read-only reviewers on a **fixed** still list:

1. bind idle  
2. plan rack (peek)  
3. CRT dest  
4. draft dest  
5. send/FILES dest  
6. decide well  
7. receipt empty  

Never A33. Never Confirm. Round cap 3. Same as today’s STORM skill, but the walk is dests not `home`.

Use as the **environment** for Loop A `01_still`, not a second product.

## Loop C — Script = walk of beauty

Python, not a prompt:

- Tap `SitCRects` centres (pack 1080×2138 → screen).  
- Fail if dest is IsolatedDark dump / letterbox / IME eating Receipt / launcher.  
- Seed a bound pocket **inside the emulator** (not this operator repo).

`app_verify.py` unchanged. New `python/look_verify.py`. Walker: replace `storm-walk.sh`’s single `home` dump; do not grow `sit-look.sh` into a dest tour (USB look stays one honest panel PNG).

## Loop D — Split sessions (cheap, no code)

| Sitting | Owns | Must not own |
|---------|------|----------------|
| Grill | one Action id, Keep/Reject/Limits, name | dest paint, sideload, 19 C-questions mid-blit |
| Factory | stills, one FLAG, one plate | renaming CURRENT, Generate, OpenRouter |

The dest-preview sitting mixed them. That is the half-time-on-Nexts complaint.

## Loop E — Workflow

`.grok/workflows/dest-stills.rhai` (name TBD):

1. Phase Still — one execute agent runs the dest walker on storm-0.  
2. Phase Score — parallel read-only reviewers per L-row / V-row; Inputs = SitRackView + nodpi + PNGs.  
3. Phase Synthesize — one `VISUAL.md`; no CURRENT write.

Halt is files in `output/`. Bounded fan-out. `await_user` after FLAG if a plate edit is required (that edit is a later sitting or Loop A `03_one_plate`).

Do not author the workflow until 02_plan contracts exist (human proceed).

## Loop F — Nyquist against FACE dest + Keep

FACE-SPEC v2 stays the rack grammar. Dest millwork is an **addendum**, not a silent V4 recant:

- Chassis LCD = truncated peek (plan keys), not the whole Objective dump, not “Next + GATE only” if Keep says peek.  
- CRT dest = full pages, caption + body.  
- Draft dest = paper + GATE millwork, not IsolatedDark workshop dump.

visual-reviewer Inputs must cite `SitRackView.kt` / `drawable-nodpi/sit_*.png`, not SeatTheme.

## What not to close the loop on

- 15/15  
- `aether current validate` OK  
- APK install Success  
- A PNG that is a valid image of the **wrong surface** (launcher)  
- Imagine JPG at 720px  
- Tailscale send duration  

Those are receipts. They are not the sit.

## Mapping to the human’s merge intent

Human: merge dest-preview leftover + `sit-bound-draft` under a **new id** (`first-sit-patching` TBD, “new name altogether”).

| Merge | Risk |
|-------|------|
| Dest millwork leftover **and** Generate/OpenRouter/$10/w QC in one Next | Repeats cause 1: Generate eats look budget |
| Dest millwork leftover **with Generate following** | Matches CURRENT Limits already (`sit-bound-draft` following) |
| Factory loops **as the method** of the look Next | This research; not a second Next |

Recommendation (propose-only): **one** Next whose halt is Loop A on dests; Generate stays following. Name should say **look**, not **patching** (patching invites grep-until-green).

Name options for the human (not selected):

1. `first-sit-look` — beauty halt; Generate following  
2. `sit-look-closed` — names the factory  
3. `sit-millwork-dests` — dest leftover only  
4. `first-sit-patching` — operator’s first try; sounds like B-row greps  
5. `sit-bound-look` — bound-folder identity without Generate this halt  

Models do not `aether next` any of these.
