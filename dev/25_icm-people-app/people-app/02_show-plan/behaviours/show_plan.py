#!/usr/bin/env python3
"""Write PLAN.md from the bound folder. Missing CURRENT → MISSING.md. Never writes CURRENT."""
from __future__ import annotations

import re
from pathlib import Path


def field(text: str, name: str) -> str:
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else "(unset)"


def main() -> int:
    bind = Path(__file__).resolve().parents[2] / "01_bind" / "output" / "BIND.md"
    if not bind.is_file():
        print("no BIND.md — run 01_bind first", file=__import__("sys").stderr)
        return 2
    m = re.search(r"- path: `([^`]+)`", bind.read_text())
    if not m:
        print("BIND.md has no path", file=__import__("sys").stderr)
        return 2
    root = Path(m.group(1))
    out_dir = Path(__file__).resolve().parents[1] / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    missing = out_dir / "MISSING.md"
    plan = out_dir / "PLAN.md"
    cur = root / "CURRENT.md"
    if not cur.is_file():
        missing.write_text(
            f"# CURRENT missing\n\n"
            f"Folder `{root}` has no CURRENT.md.\n\n"
            f"Init is a **human Yes** at `04_gate`. "
            f"This script does not run `aether current init`.\n"
        )
        plan.write_text(
            f"# Plan\n\n"
            f"**You have not said yes yet.** Opening this page is not a yes.\n\n"
            f"There is no plan in `{root}` yet.\n\n"
            f"| Face | Now |\n"
            f"|------|-----|\n"
            f"| Plan | missing |\n"
            f"| Draft | seed in `03_propose` — save is not Yes |\n"
            f"| Yes | would create their CURRENT from the visible draft |\n"
            f"| Not yet | leave the folder empty of law |\n"
            f"| Receipt | none yet |\n\n"
            f"GET never Yes. Silence is never permission.\n"
        )
        print("missing", missing)
        print("plan", plan)
        return 0
    if missing.exists():
        missing.unlink()
    text = cur.read_text()
    appr = field(text, "Approval")
    if "APPROVED" in appr.upper():
        banner = (
            "You already said Yes on the last draft. "
            "Opening this page is not a new Yes."
        )
    else:
        banner = "You have not said yes yet. Opening this page is not a yes."
    plan.write_text(
        f"# Plan\n\n"
        f"**{banner}**\n\n"
        f"- Objective: {field(text, 'Objective')}\n"
        f"- Next: {field(text, 'Next')}\n"
        f"- Approval: {appr}\n"
        f"- Limits: see bound CURRENT.md (not operator CURRENT)\n\n"
        f"Bound folder: `{root}`\n"
    )
    print("plan", plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
