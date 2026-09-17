#!/usr/bin/env python3
"""Score mum-class benchmark statements. Never Confirm. Not Yes.

Mum-class is a mother–son relationship, not simple-mode.
Mum = sitter: judgment, rare Yes, Not yet is enough, no CLI.
Son = agent + sit: runs, drafts, stages, receipt, never stamps CURRENT.

Law stays app_verify. Look millwork stays look_verify. This scorer asks
whether the sit keeps that relationship.

FLAG is iterate. PASS is not human Yes. USB ≠ LTE.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android" / "app" / "src" / "main"
JAVA = ANDROID / "java" / "com" / "mechanicall" / "pocket" / "demo"
PY = ROOT / "python"
REFUSE_SERIAL = "RZCW2038KHN"

if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from app_verify import score_source as law_score  # noqa: E402

M_ROWS = (
    "M0-open-not-yes",
    "M1-folder-first",
    "M2-plan-is-a-file",
    "M3-draft-is-writing",
    "M4-send-not-yes",
    "M5-decide-only-yes",
    "M6-not-yet-keeps",
    "M7-receipt-honest",
    "M8-no-cli-required",
    "M9-casual-language",
)

STATEMENTS = {
    "M0-open-not-yes": "Opening the sit does not approve CURRENT.",
    "M1-folder-first": "Unbound sit names a folder. Operator tree refused.",
    "M2-plan-is-a-file": "Bound sit shows live CURRENT as a readable plan, not a chat.",
    "M3-draft-is-writing": "Draft writes PROPOSE-CURRENT.md. CURRENT bytes unchanged.",
    "M4-send-not-yes": "Send stages a folder. Send is not Yes.",
    "M5-decide-only-yes": "Only Decide (two-tap + Why) publishes.",
    "M6-not-yet-keeps": "Leaving Decide without Yes keeps Next. Propose is not applied.",
    "M7-receipt-honest": "Receipt is what they said. Empty is empty.",
    "M8-no-cli-required": "Bind → Plan → Draft → Decide → Receipt is available on the sit.",
    "M9-casual-language": "Language of the house, not the workshop: she is not asked to learn a plugin or a terminal.",
}


def _read(*parts: str | Path) -> str:
    path = Path(parts[0]) if len(parts) == 1 else Path(*parts)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _java(name: str) -> str:
    return _read(JAVA / name)


def _row(mid: str, verdict: str, evidence: str) -> dict:
    return {
        "id": mid,
        "verdict": verdict,
        "ok": verdict == "PASS",
        "statement": STATEMENTS[mid],
        "evidence": evidence,
    }


def parse_gauntlet(path: Path | None) -> dict[str, str]:
    """Map G-id → PASS/FAIL/SKIP from GAUNTLET.md."""
    out: dict[str, str] = {}
    if path is None or not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "| G" not in line:
            continue
        parts = [p.strip() for p in line.strip().split("|")]
        parts = [p for p in parts if p]
        if len(parts) < 2:
            continue
        gid, verdict = parts[0], parts[1]
        if gid.startswith("G") and verdict in {"PASS", "FAIL", "SKIP"}:
            out[gid] = verdict
    return out


def _law_map(uidump: str = "") -> dict[str, dict]:
    return {r["id"]: r for r in law_score(uidump)}


def score(
    *,
    gauntlet_md: Path | None = None,
    png_dir: Path | None = None,
    uidump: str = "",
) -> list[dict]:
    nav = _java("MainActivity.kt")
    rack = _java("SitRackView.kt")
    leftover = "\n".join(
        (
            _java("SeatNav.kt"),
            _java("SeatTheme.kt"),
            _java("LcdViewer.kt"),
        )
    )
    g = parse_gauntlet(gauntlet_md)
    if not uidump and png_dir is not None and png_dir.is_dir():
        chunks = [_read(p) for p in sorted(png_dir.glob("uidump*.xml"))]
        uidump = "\n".join(chunks)
    law = _law_map(uidump)
    rows: list[dict] = []

    def law_ok(bid: str) -> bool:
        return bool(law.get(bid, {}).get("ok"))

    def g_ok(gid: str) -> bool | None:
        if gid not in g:
            return None
        return g[gid] == "PASS"

    # yes() lives in decideTap only — not launch, bind, send, or draft.
    yes_hits = [m.start() for m in re.finditer(r"FaceBridge\.yes", nav)]
    decide_at = nav.find("private fun decideTap")
    m0 = bool(yes_hits) and decide_at >= 0 and all(i > decide_at for i in yes_hits)
    if g_ok("G0-launch") is False:
        m0 = False
    rows.append(
        _row(
            "M0-open-not-yes",
            "PASS" if m0 else "FAIL",
            "onCreate does not yes(); Decide owns yes(). "
            f"g0={g.get('G0-launch', 'none')}",
        )
    )

    m1 = law_ok("B1-bind-first") and law_ok("B10-bind-not-repo")
    if g_ok("G1-bound") is False:
        m1 = False
    rows.append(
        _row(
            "M1-folder-first",
            "PASS" if m1 else "FAIL",
            f"B1={law_ok('B1-bind-first')} B10={law_ok('B10-bind-not-repo')} "
            f"g1={g.get('G1-bound', 'none')}",
        )
    )

    m2 = law_ok("B2-plan-readable") and "chat bubbles" not in rack.lower()
    if g_ok("G2-plan-disk") is False:
        m2 = False
    rows.append(
        _row(
            "M2-plan-is-a-file",
            "PASS" if m2 else "FAIL",
            f"B2={law_ok('B2-plan-readable')} leftover={bool(leftover.strip())} "
            f"g2={g.get('G2-plan-disk', 'none')}",
        )
    )

    m3 = law_ok("B3-plan-manual-edit") and law_ok("B5-propose-not-current")
    if g_ok("G7-draft-propose") is False:
        m3 = False
    rows.append(
        _row(
            "M3-draft-is-writing",
            "PASS" if m3 else "FAIL",
            f"B3={law_ok('B3-plan-manual-edit')} B5={law_ok('B5-propose-not-current')} "
            f"g7={g.get('G7-draft-propose', 'none')}",
        )
    )

    m4 = law_ok("B12-send-overlay") and "stageSendFolder" in nav
    send_block = nav.split("SitHit.Send")[-1].split("SitHit.")[0] if "SitHit.Send" in nav else ""
    m4 = m4 and "FaceBridge.yes" not in send_block
    if g_ok("G11-send-stage") is False:
        m4 = False
    rows.append(
        _row(
            "M4-send-not-yes",
            "PASS" if m4 else "FAIL",
            f"B12={law_ok('B12-send-overlay')} stageSendFolder={'stageSendFolder' in nav} "
            f"g11={g.get('G11-send-stage', 'none')}",
        )
    )

    m5 = law_ok("B6-decide-only-yes")
    if g_ok("G8-decide-why") is False:
        m5 = False
    rows.append(
        _row(
            "M5-decide-only-yes",
            "PASS" if m5 else "FAIL",
            f"B6={law_ok('B6-decide-only-yes')} g8={g.get('G8-decide-why', 'none')}",
        )
    )

    m6 = "leaveDecideWithoutYes" in nav and "notYet" in nav
    if g_ok("G9-not-yet") is False:
        m6 = False
    rows.append(
        _row(
            "M6-not-yet-keeps",
            "PASS" if m6 else "FAIL",
            f"leaveDecideWithoutYes={'leaveDecideWithoutYes' in nav} "
            f"g9={g.get('G9-not-yet', 'none')}",
        )
    )

    m7 = law_ok("B8-receipt-tomorrow") and law_ok("B15-receipt-honest")
    rows.append(
        _row(
            "M7-receipt-honest",
            "PASS" if m7 else "FAIL",
            f"B8={law_ok('B8-receipt-tomorrow')} B15={law_ok('B15-receipt-honest')}",
        )
    )

    m8 = (
        "SitPlate.BIND" in nav
        and "SitPlate.PLAN" in nav
        and "SitPlate.DRAFT" in nav
        and "SitPlate.DECIDE" in nav
        and "SitPlate.RECEIPT" in nav
        and leftover.strip() == ""
    )
    rows.append(
        _row(
            "M8-no-cli-required",
            "PASS" if m8 else "FAIL",
            "banks BIND/PLAN/DRAFT/DECIDE/RECEIPT on the sit; leftover Compose gone",
        )
    )

    millwork_host = "SitRackView" in nav and "R.drawable.sit_chassis" in rack
    casual_marker = "mum-class" in rack.lower() or "casual language" in nav.lower()
    if millwork_host and not casual_marker:
        rows.append(
            _row(
                "M9-casual-language",
                "FLAG",
                "SitRackView + sit_chassis is workshop language. "
                "Mother–son face would not ask her to learn a plugin. "
                "Not a FAIL of protocol. Iterate = household language, not more nodpi.",
            )
        )
    elif casual_marker:
        rows.append(
            _row(
                "M9-casual-language",
                "PASS",
                "casual-language marker present; workshop host recanted",
            )
        )
    else:
        rows.append(
            _row(
                "M9-casual-language",
                "FLAG",
                "no millwork host and no casual marker; human still reviews language",
            )
        )

    return rows


def render(rows: list[dict]) -> str:
    passed = sum(1 for r in rows if r["verdict"] == "PASS")
    flags = sum(1 for r in rows if r["verdict"] == "FLAG")
    fails = [r["id"] for r in rows if r["verdict"] == "FAIL"]
    lines = [
        "# MUM",
        "",
        "**Not Decide. Not Yes.** Mum-class benchmark statements.",
        "",
        "Mum-class = mother–son: she stamps, he runs. "
        "No CLI required of her. Language of the house, not the workshop.",
        "",
        f"**Score:** {passed}/{len(rows)} PASS · {flags} FLAG · {len(fails)} FAIL",
        "",
        "| id | verdict | statement | evidence |",
        "|----|---------|-----------|----------|",
    ]
    for r in rows:
        st = r["statement"].replace("|", "/")
        ev = r["evidence"].replace("|", "/")
        lines.append(f"| {r['id']} | {r['verdict']} | {st} | {ev} |")
    lines.append("")
    if fails:
        lines.append("**Failed:** " + ", ".join(fails))
    else:
        lines.append("**Failed:** none")
    lines.append("")
    lines.append("FLAG is iterate. PASS is not human Yes. Confirm was not tapped.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gauntlet-md", type=Path, default=None)
    ap.add_argument("--png-dir", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None, help="write MUM.md here")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--serial", default="")
    args = ap.parse_args(argv)
    if args.serial == REFUSE_SERIAL:
        print("refused: live A33", file=sys.stderr)
        return 3
    rows = score(gauntlet_md=args.gauntlet_md, png_dir=args.png_dir)
    text = render(rows)
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "MUM.md").write_text(text, encoding="utf-8")
    if args.json:
        print(json.dumps({"rows": rows}, indent=2))
    else:
        print(text, end="")
    if any(r["verdict"] == "FAIL" for r in rows):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
