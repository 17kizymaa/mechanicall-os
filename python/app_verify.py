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
    "B11-crt-isolated",
    "B12-send-overlay",
    "B13-draft-workshop-page",
    "B14-send-folder-smoke",
    "B15-receipt-honest",
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
    nav = _java("MainActivity.kt")
    rack = _java("SitRackView.kt")
    crects = _java("SitCRects.kt")
    leftover = "\n".join(
        (
            _java("SeatNav.kt"),
            _java("SeatTheme.kt"),
            _java("LcdViewer.kt"),
            _java("SkinLayout.kt"),
            _java("PlanModule.kt"),
            _java("ChatHome.kt"),
            _java("DecideModule.kt"),
        )
    )
    manifest = _read(ANDROID / "AndroidManifest.xml")
    pocket = _read(PY / "aether_pocket.py")
    tests = _read(ROOT / "tests" / "test_aether_pocket.py")
    face = _java("FaceBridge.kt")

    out: list[dict] = []

    b1 = (
        "SitPlate.BIND" in nav
        and "pocket_one" in nav
        and "operator tree" in nav.lower()
        and "OpenDocumentTree" in nav
    )
    out.append(
        _row(
            "B1-bind-first",
            b1,
            "unbound SitPlate.BIND; prefs pocket_one; operator tree refused copy; SAF picker",
        )
    )

    b2 = (
        "SitRackView" in nav
        and "LawPages" in nav
        and ("sit_plan" in rack or "sit_well_plan" in rack)
        and "setContentView(rack)" in nav
        and "clipRect" in rack
        and leftover.strip() == ""
    )
    if uidump:
        b2 = b2 and ("LCD" in uidump or "LAW" in uidump or "sit millwork" in uidump)
    out.append(
        _row(
            "B2-plan-readable",
            b2,
            "PLAN is SitRackView CBitmap + LCD clipped to glass; leftover Compose millwork gone",
        )
    )

    draft_editor = "EditText" in rack and "editDraftWriter" in rack
    draft_writes = "savePropose" in nav and "write_propose" in _read(PY / "aether_pocket.py")
    b3 = draft_editor and draft_writes
    out.append(
        _row(
            "B3-plan-manual-edit",
            b3,
            "Draft writer EditText saves PROPOSE via savePropose/write_propose. "
            f"draft_editor={draft_editor} draft_writes={draft_writes}",
        )
    )

    still_thread = "LazyColumn" in rack
    b4 = "IsolatedMode.DRAFT" in nav and draft_writes and not still_thread
    b4 = b4 and "IME_FLAG_NO_ENTER_ACTION" in rack
    out.append(
        _row(
            "B4-draft-is-workshop",
            b4,
            "PASS if Draft dest is a text editor (not a message thread). "
            f"draft_dest={'IsolatedMode.DRAFT' in nav} writes={draft_writes} thread={still_thread}",
        )
    )

    b5 = "if stage == \"propose\":" in pocket and "parsed_stage == \"propose\"" in pocket
    b5 = b5 and "test_show_plan_cannot_write_propose" in tests
    out.append(_row("B5-propose-not-current", b5, "local stage owns PROPOSE write; test present"))

    b6 = "decideArmed" in nav
    b6 = b6 and "why required" in nav
    b6 = b6 and "FaceBridge.yes" in nav
    b6 = b6 and "HunkPickRow" not in nav
    b6 = b6 and "Hunks for this change" not in nav
    out.append(
        _row(
            "B6-decide-only-yes",
            b6,
            "two-tap paper + Why-required; Decide is Yes not hunk pick",
        )
    )

    b7 = "LOAD" in nav and "STREAM" in nav
    b7 = b7 and "SitCRects.gate" in rack
    b7 = b7 and "if (busy) \"GATE\"" not in rack
    typing_dots = 'if (busy) "…"' in rack or "if (busy) \"...\"" in rack
    b7 = b7 and not typing_dots
    if uidump:
        b7 = b7 and ("GATE" in uidump or "IDLE" in uidump or "LOAD" in uidump)
    out.append(
        _row(
            "B7-gate-instrument",
            b7,
            "LCD LOAD then STREAM; GATE SEQ CRect pages law; busy must not be typing dots. "
            f"typing_dots={typing_dots}",
        )
    )

    b8 = "empty receipt" in nav.lower() or "(empty receipt)" in rack
    out.append(_row("B8-receipt-tomorrow", b8, "honest empty copy on RECEIPT LCD"))

    b9 = 'android:resizeableActivity="true"' in manifest
    b9 = b9 and leftover.strip() == ""
    out.append(_row("B9-window-honest", b9, "resizeableActivity; leftover Compose letterbox host gone"))

    b10 = "is_operator_tree" in pocket and "test_operator_tree_refused" in tests
    out.append(_row("B10-bind-not-repo", b10, "operator-tree refuse in engine + tests"))

    b11 = "IsolatedMode.CRT" in nav and "isolatedCrt" in crects and "LcdViewer" not in leftover
    b11 = b11 and ("clipPreview" in rack or "PREVIEW_CHARS" in rack)
    b11 = b11 and "sit_crt" in rack
    out.append(
        _row(
            "B11-crt-isolated",
            b11,
            "CRT dest is IsolatedMode.CRT + sit_crt millwork; truncated peek; no LcdViewer host",
        )
    )

    send_block = nav.split("SitHit.Send")[-1].split("SitHit.")[0] if "SitHit.Send" in nav else ""
    b12 = "sendOverlay" in rack and "openSendOverlay" in nav
    b12 = b12 and "stageSendFolder" in nav and "sendFolder" in nav
    b12 = b12 and "yes(" not in send_block and "FaceBridge.yes" not in send_block
    b12 = b12 and "SitHit.Files" in nav
    b12 = b12 and "openSendOverlay()" in nav
    b12 = b12 and "folderOem" in crects and "folderSend" in crects
    out.append(
        _row(
            "B12-send-overlay",
            b12,
            "Send and FILES open one dest; FOLDER plaque stages; OEM FILES; not yes()",
        )
    )

    b13 = "IsolatedMode.DRAFT" in nav and "editDraftWriter" in rack and "savePropose" in nav
    b13 = b13 and "LazyColumn" not in rack
    b13 = b13 and "DRAFT writer" in nav and "NOT ACTIVE" in nav
    out.append(
        _row(
            "B13-draft-workshop-page",
            b13,
            "Draft bank opens isolated whole-file writer; PROPOSE only",
        )
    )

    b14 = "SEND overlay" in nav and "tap outside to dismiss" in rack
    b14 = b14 and "sit-send-smoke" in _read(ROOT / "scripts" / "sit-send-smoke.sh")
    out.append(_row("B14-send-folder-smoke", b14, "overlay copy + scripts/sit-send-smoke.sh (USB look optional)"))

    b15 = "receiptText" in nav and "(empty receipt)" in rack
    out.append(_row("B15-receipt-honest", b15, "RECEIPT bank loads FaceBridge.receiptText; empty stays empty"))

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
