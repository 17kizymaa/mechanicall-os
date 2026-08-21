#!/usr/bin/env python3
"""Create the copyable people-app workspace from the stage map. Empty output/ only."""
from __future__ import annotations

from pathlib import Path

FACTORY = Path(__file__).resolve().parents[2]
DEST = FACTORY / "people-app"

ROOT_CONTEXT = """# People-app (copy this folder)

Workspace is the app. One agent. One bound folder that is **not** mechanicall-os.

You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.

Opening this folder is not a Yes.

## Pipeline

1. `01_bind/` — name *their* project folder; refuse the operator tree
2. `02_show-plan/` — put the plan on a page (or say CURRENT is missing)
3. `03_propose/` — agent drafts only
4. `04_gate/` — human Yes / Not yet
5. `05_do/` — only after Yes
6. `06_receipt/` — something they can open tomorrow

One-way. Do not read a later `output/`. Edit any `output/` before saying proceed.

## Not this workspace

Operator CURRENT. Pocket `:8765`. OpenHands/Compose. Play Store. Tailscale-as-me.
"""

README = """# People-app

Copy this folder off mechanicall-os. Bind **your** project folder.

You have not said yes yet. Opening these files is not a yes.

See `CONTEXT.md`. Start at `01_bind/`.
"""

STAGES = {
    "01_bind": """## Inputs
- Layer 4: the path they name
- Layer 3: `../references/refuse-operator.md`

## Process
You are **binding**. Resolve the path. Refuse if it is the mechanicall-os operator tree. Else write the bind. Use `behaviours/bind.py` when present. Do not write CURRENT.

## Outputs
- BIND.md -> output/
""",
    "02_show-plan": """## Inputs
- Layer 4: `../01_bind/output/BIND.md`
- Layer 4: bound `CURRENT.md` if it exists
- Layer 3: `../references/pitch.md`

## Process
You are **showing the plan**. If CURRENT is missing, write a seed *proposal* and MISSING.md — do not run `aether current init`, do not invent law. If present, copy Objective / Next / Limits onto a short page. Never bind operator CURRENT. Opening this page is not a Yes.

## Outputs
- PLAN.md -> output/
- MISSING.md -> output/ (only if no CURRENT)
""",
    "03_propose": """## Inputs
- Layer 4: `../01_bind/output/BIND.md`, `../02_show-plan/output/PLAN.md`
- Layer 4: bound folder (scoped — not the whole disk)
- Layer 3: `../references/yes-rules.md`

## Process
You are **drafting**. Write PROPOSE only (workspace `output/PROPOSE.md` and/or bound `PROPOSE-CURRENT.md`). Do not write CURRENT. Do not approve.

## Outputs
- PROPOSE.md -> output/
""",
    "04_gate": """## Inputs
- Layer 4: BIND.md, PLAN.md, PROPOSE.md
- Layer 3: `../references/yes-rules.md`

## Process
You are **the gate recorder**, not the Yes. Human Yes applies propose into bound CURRENT + `aether approve` with a real reason. Not yet leaves CURRENT. Agent never clicks Yes. Silence is not Yes.

## Outputs
- GATE.md -> output/
""",
    "05_do": """## Inputs
- Layer 4: `../04_gate/output/GATE.md` (must say yes)
- Layer 4: BIND.md, bound CURRENT Next

## Process
You are **doing the approved Next** in the bound folder. Preflight that Next there. Do not change CURRENT. Do not start a swarm. Do not write the operator tree.

## Outputs
- WORK.md -> output/
""",
    "06_receipt": """## Inputs
- Layer 4: GATE.md, WORK.md
- Layer 4: bound `.aether/events.jsonl` tail, DECISIONS.md if any

## Process
You are **leaving a receipt** they can open tomorrow without mechanicall-os.

## Outputs
- RECEIPT.md -> output/
""",
}

REFS = {
    "refuse-operator.md": """# Refuse the operator tree

Markers (all must exist): `PRODUCT.md`, `bin/aether`, `CORE_PRINCIPLES.md`, `AGENTS.md`.

If the named folder is that tree — refuse. Bind a different folder.

Same idea as `python/aether_pocket.py` `refuse_if_operator`. Do not clone the protocol; call aether from AETHER_HOME when a CLI is needed.
""",
    "yes-rules.md": """# Yes rules

- GET / open / clone / read PLAN.md is **not** Yes.
- Silence is **not** Yes.
- Agent writes PROPOSE only.
- Yes = human applies the visible draft + `aether approve` in the **bound** folder.
- Not yet = leave the plan. The machine lives with that.
- Do not POST Yes for them. Do not Funnel. Do not public-bind Ollama.
- Receipt lands in their folder (and `06_receipt/output/`).
""",
    "pitch.md": """# Pitch

You decide. AI does the point-and-clicking — under a plan you can read and a yes only you can give.

One screen: plan, draft, Yes, Not yet, receipt.
""",
    "lessons.md": """# Sitting lessons (lab)

Source: `dev/23_mobile-planning-demo/12_leave-for-people-app/output/LESSONS.md`

- Their folder, their identity. Not “log in as the operator.”
- Tailscale-as-me is not a front door.
- Chrome without aether is decoration.
- OpenHands / Compose / Play Store are not this workspace.
""",
}


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "CONTEXT.md").write_text(ROOT_CONTEXT)
    (DEST / "README.md").write_text(README)
    refs = DEST / "references"
    refs.mkdir(exist_ok=True)
    for name, text in REFS.items():
        (refs / name).write_text(text)
    for folder, ctx in STAGES.items():
        stage = DEST / folder
        out = stage / "output"
        out.mkdir(parents=True, exist_ok=True)
        (stage / "CONTEXT.md").write_text(ctx)
        keep = out / ".gitkeep"
        if not keep.exists():
            keep.write_text("")
    print(f"scaffolded {DEST}")


if __name__ == "__main__":
    main()
