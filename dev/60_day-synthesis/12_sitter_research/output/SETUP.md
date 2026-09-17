# SETUP — agent that uses the APK

**Not Yes. Not CURRENT. Not a spawn.** Research for “final refinements; another agent that actually uses the APK.”

Live APK: **`0.19.17-fit` vc 42** on storm-0 (`emulator-5554` was up). Fit: `10_interaction_preview/output/FIT.md`. Identity = archived chassis. Never Confirm. Never two-tap Yes. Never serial `RZCW2038KHN`. USB ≠ LTE.

---

## What already exists (do not reinvent)

| Piece | Uses the APK? | Job |
|-------|----------------|-----|
| `walk_ritual.py` | **Yes** — CRect taps + SAF ui taps on storm-0 | Ritual stills; **never Yes** |
| `sit_dest_walk.py` | **Yes** | Dest stills |
| `you_decide_gauntlet.py` | **Yes** — disk + uidump on storm-0 | Functional G-steps; fail-closed; never Yes |
| `scripts/storm-walk.sh` | Barely | Launch + one home dump |
| `app_verify.py` | Usually **source grep** | Law 15/15. Optional `--uidump-dir` |
| `look_verify.py` / `mum_verify.py` | Stills **after** a walker | Look / mum-son. FLAG ≠ Yes |
| `/storm-review` | Environment | Cap 2 AVDs. Never A33 |
| `/visual-reviewer` | Stills + source | FACE-SPEC. Called “from STORM” but does not tap |
| `/app-reviewer` | Source + optional uidump | Behaviours. Does not tap |
| `actual-app-verification.rhai` | Source swarm | Read-only children. **Do not tap** |
| `/sit-lab` | A33 USB binaries | Sideload/look. Not a sitter loop |
| `/handoff` | Docs | New **session**, not a device walker |
| This chat | Can adb | Compaction + millwork load; bad sitter |

FRAMEWORKS.md already rejected Appium as product and parked Maestro. AGENT-CI.md: reviewers = read-only + `output/`; writers = worktree; human Yes only.

---

## The actual gap

Walkers **tap and dump**. Reviewer agents **read files**. Nobody is contracted to:

1. Drive `0.19.17-fit` on storm-0 (CRect hits from FIT).
2. **Look at** each PNG (vision), not only `look_verify` strings.
3. Write `FLAGS.md` against **FIT holes** (ticket peek, NOT ACTIVE, Send overlay one line, JOIN/WAKE blanks, Plan labour untested, cream-pill draft bitmap, etc.).
4. **Stop.** Not millwork. Not CURRENT. Not Yes.

That is the “uses the APK” agent. Final refinements are FLAG rows a human stamps, then this factory millworks **one hole**.

Labour after Yes **cannot** be walked without a Yes. Sitter must **not** two-tap. Honest FLAG: “PLAN labour feet unseen.” Do not add a fake-`yes()` debug jump (FIT: never fake Yes).

---

## Isolation (easy to get wrong)

| Mode | APK? | Use |
|------|------|-----|
| `isolation=worktree` | **No** — child git tree, same or no emulator, fights parent files | Writers of Kotlin later, not the sitter |
| `isolation=none` + adb | **Yes** — one storm-0 | **One** sitter. Two sitters dual-tap = junk stills |
| New Grok **session** | **Yes** if it loads sit-lab/storm + FIT | Clean context; this compact chat is the reason you asked |
| `grok -p` headless | Yes if tools include bash + read_file on PNGs | Scriptable; still never `--yolo` / approve |

Device is not a git worktree. Sitters share **one** AVD.

---

## Options

### S=1 — New chat session + sitter contract (recommended)

New Grok TUI session in this repo. Load: CURRENT, FIT.md, `11_land_fit/RECEIPT.md`, `/storm-review`, `/visual-reviewer`. Run `walk_ritual.py` (extend hits for send dismiss / draft dest only if missing). `read_file` each PNG. Write `12_sitter/output/FLAGS.md`. Halt.

**Cost:** one sitting of context, $0 vendor. Matches “another agent.” This session stays the millwork parent after FLAGS stamp.

### S=2 — `spawn_subagent` from this chat (`isolation=none`)

One `general-purpose` child. Prompt: storm-0 only, never Yes, walk + look + FLAGS.md, do not edit Kotlin. Parent does not millwork until you stamp FLAGS.

**Cost:** cheaper than a new session; inherits this compaction noise; one live child vs storm-0.

### S=3 — Workflow: walker script then parallel visual reviewers on PNGs

Parent/script walks. `parallel()` read-only agents score stills. One FLAGS synthesis.

**Cost:** AGENT-CI shape. Children **do not** use the APK; the script does. Fine for mass taste, weaker for “sit it.”

### S=4 — Maestro / Appium / hosted QA

FRAMEWORKS already: Maestro later, Appium no, hosted QA no. Do not install for this refinement pass.

### S=5 — A33 as the sitter’s phone

sit-lab is USB look. **Testers ≠ A33.** A sitter that taps Yes on the lab phone is forbidden. A33 = human look after FLAGS millwork, not the refinement agent.

---

## Recommended contract (if you pick S=1 or S=2)

Skill name (not written until you say write it): **sit-sitter**.

```
Inputs:  FIT.md, 0.19.17-fit, storm-0, walk_ritual.py
Process: install → walk (never Yes) → stills+uidump → vision each PNG → FLAGS vs FIT
Never:   Confirm, yes(), A33, CURRENT, millwork, second AVD
Halt:    output/FLAGS.md  (PASS is not Yes)
```

Python already: `walk_ritual.py` + `look_verify.py` + `mum_verify.py`. Do not add a second walker kit.

Storm-0 is the box. Cap **1** sitter. Pause if 7B desk is hot (storm-review RAM note).

---

## What this research does not do

- Spawn a child
- Write the skill file
- Tap the APK again
- Two-tap Yes to see labour feet

**Selected:** **S=1** (2026-09-08). New session. Skill `.grok/skills/sit-sitter/SKILL.md`. Stage `13_sit_sitter/`. Start text: `13_sit_sitter/output/START.md`. This chat did not spawn.
