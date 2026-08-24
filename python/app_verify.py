#!/usr/bin/env python3
"""Score the demo face against BEHAVIOURS.md. Never Confirm. Not Yes.

Source probes are deterministic. Optional uidump dir adds glass evidence.
Refuse the live A33 serial. Do not tap anything.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android" / "app" / "src" / "main"
JAVA = ANDROID / "java" / "com" / "mechanicall" / "pocket" / "demo"
PY = ROOT / "python"
REFUSE_SERIAL = "RZCW2038KHN"

BEHAVIOURS = (
    "B1-bind-first",
    "B2-plan-readable",
    "B3-plan-manual-edit",
    "B4-draft-is-workshop",
    "B5-propose-not-current",
    "B6-decide-only-yes",
    "B7-gate-instrument",
    "B8-receipt-tomorrow",
    "B9-window-honest",
    "B10-bind-not-repo",
)


def _read(*parts: str | Path) -> str:
    path = Path(parts[0]) if len(parts) == 1 else Path(*parts)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _java(name: str) -> str:
    if name.endswith(".kt"):
        p = JAVA / "modules" / name
        if not p.is_file():
            p = JAVA / name
        return _read(p)
    return _read(JAVA / name)


def _uidump_blob(uidump_dir: Path | None) -> str:
    if uidump_dir is None or not uidump_dir.is_dir():
        return ""
    chunks: list[str] = []
    for p in sorted(uidump_dir.glob("uidump*.xml")):
        chunks.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def _row(bid: str, ok: bool, evidence: str) -> dict:
    return {
        "id": bid,
        "verdict": "PASS" if ok else "FAIL",
        "ok": ok,
        "evidence": evidence,
    }


def score_source(uidump: str = "") -> list[dict]:
    nav = _java("SeatNav.kt")
    plan = _java("PlanModule.kt")
    chat = _java("ChatHome.kt")
    decide = _java("DecideModule.kt")
    bind = _java("BindModule.kt")
    receipt = _java("ReceiptModule.kt")
    theme = _java("SeatTheme.kt")
    manifest = _read(ANDROID / "AndroidManifest.xml")
    pocket = _read(PY / "aether_pocket.py")
    tests = _read(ROOT / "tests" / "test_aether_pocket.py")
    face = _java("FaceBridge.kt")

    out: list[dict] = []

    b1 = (
        "SeatRoute.Bind" in nav
        and "landingFrom" in nav
        and "pocket_one" in nav
        and "operator tree" in bind.lower()
    )
    out.append(
        _row(
            "B1-bind-first",
            b1,
            "landingFrom → Bind when unbound; prefs pocket_one; operator copy on bind",
        )
    )

    b2 = ("CURRENT.md" in plan or "planText" in plan) and "Changes" in plan and "Proposal" in plan
    if uidump:
        b2 = b2 and ("CURRENT" in uidump or "Changes" in uidump)
    out.append(_row("B2-plan-readable", b2, "PLAN shows CURRENT.md plus Changes plus a Proposal segment"))

    draft_editor = "OutlinedTextField" in chat
    draft_writes = "acceptHunk" in chat or "writeSchemaDraft" in chat
    plan_editor = "OutlinedTextField" in plan and "applyHunk" in plan
    b3 = (draft_editor and draft_writes) or plan_editor
    out.append(
        _row(
            "B3-plan-manual-edit",
            b3,
            "Proposal edits write PROPOSE (Plan and/or Draft). "
            f"draft_editor={draft_editor} draft_writes={draft_writes} plan_editor={plan_editor}",
        )
    )

    has_chips = "AUTHORITY_FIELDS" in chat and (
        "schemaDraft" in chat or "readSchemaDraft" in chat
    )
    has_hunks = "listHunks" in chat and "LIVE" in chat and "DRAFT" in chat
    still_thread = "LazyColumn" in chat
    b4 = (has_chips or has_hunks) and not still_thread
    out.append(
        _row(
            "B4-draft-is-workshop",
            b4,
            "PASS only if field chips exist and the page is not a message thread. "
            f"chips={has_chips} hunks={has_hunks} thread={still_thread}",
        )
    )

    b5 = "if stage == \"propose\":" in pocket and "parsed_stage == \"propose\"" in pocket
    b5 = b5 and "test_show_plan_cannot_write_propose" in tests
    out.append(_row("B5-propose-not-current", b5, "local stage owns PROPOSE write; test present"))

    b6 = "armFade" in decide or "AGAIN" in decide
    b6 = b6 and "why.isNotBlank()" in decide
    b6 = b6 and "FaceBridge.yes" in decide
    b6 = b6 and "HunkPickRow" not in decide
    b6 = b6 and "Hunks for this change" not in decide
    out.append(
        _row(
            "B6-decide-only-yes",
            b6,
            "two-tap + Why-required Confirm; Decide is Publish not hunk pick",
        )
    )

    b7 = "GateStrip" in theme and "GATE" in theme
    b7 = b7 and "LOAD" in theme and "STREAM" in theme
    b7 = b7 and "if (busy) \"GATE\"" not in chat
    typing_dots = 'if (busy) "…"' in chat or "if (busy) \"...\"" in chat
    b7 = b7 and not typing_dots
    idle_dark = "else SeatPalette.LcdBg" in theme.replace("\n", " ")
    b7 = b7 and idle_dark
    if uidump:
        b7 = b7 and "GATE" in uidump
    out.append(
        _row(
            "B7-gate-instrument",
            b7,
            "GateStrip LOAD then STREAM; Send not labelled GATE; busy must not be typing dots. "
            f"typing_dots={typing_dots}",
        )
    )

    b8 = "did not pretend you agreed" in receipt.lower() or "No decision recorded" in receipt
    out.append(_row("B8-receipt-tomorrow", b8, "honest empty copy on ReceiptModule"))

    b9 = 'android:resizeableActivity="true"' in manifest
    b9 = b9 and "widthIn(max = 360.dp)" not in theme
    b9 = b9 and "360.dp" not in theme
    out.append(_row("B9-window-honest", b9, "resizeableActivity; painted 360×560 letterbox gone"))

    b10 = "is_operator_tree" in pocket and "test_operator_tree_refused" in tests
    out.append(_row("B10-bind-not-repo", b10, "operator-tree refuse in engine + tests"))

    return out


def render(rows: list[dict]) -> str:
    passed = sum(1 for r in rows if r["ok"])
    lines = [
        "# VERIFICATION",
        "",
        "**Not Decide. Not Yes.** Mechanical score of the demo face against BEHAVIOURS.md.",
        "",
        f"**Score:** {passed}/{len(rows)}",
        "",
        "| id | verdict | evidence |",
        "|----|---------|----------|",
    ]
    for r in rows:
        ev = r["evidence"].replace("|", "/")
        lines.append(f"| {r['id']} | {r['verdict']} | {ev} |")
    lines.append("")
    fails = [r["id"] for r in rows if not r["ok"]]
    if fails:
        lines.append("**Failed:** " + ", ".join(fails))
    else:
        lines.append("**Failed:** none")
    lines.append("")
    lines.append("Walkers did not tap Confirm. Models did not approve.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--uidump-dir", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--serial", default="", help="adb serial; RZCW2038KHN refused")
    args = ap.parse_args(argv)
    if args.serial == REFUSE_SERIAL:
        print("refused: live A33", file=sys.stderr)
        return 3
    uidump = _uidump_blob(args.uidump_dir)
    rows = score_source(uidump)
    if args.json:
        print(json.dumps({"rows": rows, "passed": sum(r["ok"] for r in rows)}, indent=2))
    else:
        print(render(rows), end="")
    return 0 if all(r["ok"] for r in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
