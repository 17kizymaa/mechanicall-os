#!/usr/bin/env python3
"""Score sit dest millwork look. Never Confirm. Not Yes. Not 15/15.

Law probes stay in app_verify.py. This scorer fail-closes on launcher frames
and IsolatedDark dump chrome. Human FLAG recants a green L-row.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android" / "app" / "src" / "main"
JAVA = ANDROID / "java" / "com" / "mechanicall" / "pocket" / "demo"
REFUSE_SERIAL = "RZCW2038KHN"
SIT_PKG = "com.mechanicall.pocket.demo"
LAUNCHER_PKGS = (
    "com.sec.android.app.launcher",
    "com.google.android.apps.nexuslauncher",
    "com.android.launcher3",
    "com.miui.home",
)

# dest-walk names → aliases from older SDK stills
NEED_STILLS = {
    "rack-plan": ("rack-plan.png", "17-bank-plan.png", "03-bind-idle.png"),
    "dest-crt": ("dest-crt.png", "10-crt-isolated.png"),
    "dest-draft": ("dest-draft.png", "20-draft-isolated.png"),
    "dest-folder": ("dest-folder.png", "14-send-overlay.png"),
    "rack-decide": ("rack-decide.png", "23-decide.png"),
    "rack-receipt": ("rack-receipt.png", "25-receipt.png"),
}

L_ROWS = (
    "L0-frame",
    "L1-peek",
    "L2-crt-dest",
    "L3-draft-dest",
    "L4-folder-dest",
    "L5-title",
    "L6-decide-well",
    "L7-gate",
    "L8-receipt",
)


def _read(*parts: str | Path) -> str:
    path = Path(parts[0]) if len(parts) == 1 else Path(*parts)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _java(name: str) -> str:
    return _read(JAVA / name)


def _row(lid: str, verdict: str, evidence: str) -> dict:
    return {
        "id": lid,
        "verdict": verdict,
        "ok": verdict == "PASS",
        "evidence": evidence,
    }


def _find_still(png_dir: Path | None, key: str) -> Path | None:
    if png_dir is None or not png_dir.is_dir():
        return None
    for name in NEED_STILLS[key]:
        p = png_dir / name
        if p.is_file():
            return p
    return None


def _uidump_for(png: Path | None) -> str:
    if png is None:
        return ""
    stem = png.stem
    for cand in (
        png.with_name(f"uidump-{stem}.xml"),
        png.with_suffix(".xml"),
        png.parent / f"uidump-{stem}.xml",
    ):
        if cand.is_file():
            return _read(cand)
    return ""


def _blob_uidumps(png_dir: Path | None) -> str:
    if png_dir is None or not png_dir.is_dir():
        return ""
    chunks: list[str] = []
    for p in sorted(png_dir.glob("uidump*.xml")):
        chunks.append(_read(p))
    return "\n".join(chunks)


def _fracs(png: Path | None) -> dict[str, float]:
    out = {"millwork": 0.0, "sky": 0.0, "dark": 0.0, "amber": 0.0, "n": 0.0}
    if png is None or not png.is_file():
        return out
    try:
        from PIL import Image
    except ImportError:
        return out
    im = Image.open(png).convert("RGB")
    small = im.resize((54, 120))
    px = small.load()
    w, h = small.size
    n = w * h or 1
    millwork = sky = dark = amber = 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            luma = (r * 3 + g * 6 + b) / 10
            if luma < 18:
                dark += 1
            if r > 170 and g > 140 and b > 90 and (r - b) > 20:
                millwork += 1
            if b > r + 15 and b > 140:
                sky += 1
            if r > 180 and g > 130 and b < 110 and r > g:
                amber += 1
    out["millwork"] = millwork / n
    out["sky"] = sky / n
    out["dark"] = dark / n
    out["amber"] = amber / n
    out["n"] = float(n)
    return out


def _is_png(path: Path | None) -> bool:
    if path is None or not path.is_file():
        return False
    return path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def score_source() -> dict[str, str]:
    """Source hints for L-rows. Not the look by themselves."""
    nav = _java("MainActivity.kt")
    rack = _java("SitRackView.kt")
    crects = _java("SitCRects.kt")
    leftover = "\n".join(
        (
            _java("SeatNav.kt"),
            _java("SeatTheme.kt"),
            _java("LcdViewer.kt"),
        )
    )
    return {
        "nav": nav,
        "rack": rack,
        "crects": crects,
        "leftover": leftover,
        "has_crt": "IsolatedMode.CRT" in nav and "R.drawable.sit_crt" in rack,
        "has_peek": "PREVIEW_CHARS" in rack or "clipPreview" in rack,
        "draft_early_dark": "IsolatedMode.DRAFT" in rack
        and "IsolatedDark" in rack
        and "if (isolated == IsolatedMode.DRAFT)" in rack
        and "drawColor(SitCRects.IsolatedDark)" in rack.split("IsolatedMode.DRAFT")[0][-400:],
        "alpha_chrome": "SitHit.FieldAlpha" in nav or '"ALPHA"' in rack,
        "field_dump": "Field Objective" in rack,
        "law_prefix": '"LAW ' in rack or "LAW  {" in rack or "LAW {" in rack,
        "same_folder_dest": "SitHit.Send -> openSendOverlay" in nav
        and "openSendOverlay()" in nav
        and "SitHit.Files" in nav,
        "folder_oem": "folderOem" in crects,
        "gate_opens_crt": "openTerminal"
        in nav.split("SitHit.Gate")[-1].split("SitHit.")[0],
        "leftover_compose": leftover.strip() != "",
        "title_control": "SitHit.Title" in crects or "SitHit.Title" in nav,
    }


def score(png_dir: Path | None = None) -> list[dict]:
    src = score_source()
    uidump_all = _blob_uidumps(png_dir)
    rows: list[dict] = []

    crt_png = _find_still(png_dir, "dest-crt")
    draft_png = _find_still(png_dir, "dest-draft")
    folder_png = _find_still(png_dir, "dest-folder")
    plan_png = _find_still(png_dir, "rack-plan")
    decide_png = _find_still(png_dir, "rack-decide")
    receipt_png = _find_still(png_dir, "rack-receipt")
    sample = plan_png or crt_png or draft_png or folder_png or decide_png or receipt_png
    if png_dir and png_dir.is_dir():
        looks = sorted(png_dir.glob("*.png"))
        if sample is None and looks:
            sample = looks[0]

    fr = _fracs(sample)
    ud = _uidump_for(sample) or uidump_all
    launcher = any(p in ud for p in LAUNCHER_PKGS)
    sit = SIT_PKG in ud
    l0_fail = False
    l0_flag = False
    ev = []
    if sample is None:
        l0_fail = True
        ev.append("no PNG in dir")
    elif not _is_png(sample):
        l0_fail = True
        ev.append(f"{sample.name} not a PNG")
    else:
        ev.append(
            f"{sample.name} millwork={fr['millwork']:.2f} sky={fr['sky']:.2f} "
            f"dark={fr['dark']:.2f} sit={sit} launcher={launcher}"
        )
    if launcher or (fr["sky"] > 0.05 and fr["millwork"] < 0.02 and fr["dark"] < 0.35):
        l0_fail = True
        ev.append("launcher/wallpaper frame")
    if sample is not None and not sit and ud:
        l0_fail = True
        ev.append("uidump is not the sit package")
    if sample is not None and not ud:
        l0_flag = True
        ev.append("no uidump; pixel heuristic only")
    if l0_fail:
        rows.append(_row("L0-frame", "FAIL", "; ".join(ev)))
    elif l0_flag:
        rows.append(_row("L0-frame", "FLAG", "; ".join(ev)))
    else:
        rows.append(_row("L0-frame", "PASS", "; ".join(ev)))

    peek_ok = src["has_peek"] and not src["law_prefix"]
    rows.append(
        _row(
            "L1-peek",
            "PASS" if peek_ok else "FLAG",
            f"clipPreview={src['has_peek']} LAW-prefix={src['law_prefix']}",
        )
    )

    crt_fr = _fracs(crt_png)
    crt_ud = _uidump_for(crt_png)
    crt_sit = SIT_PKG in crt_ud or sit
    if crt_png is None:
        rows.append(_row("L2-crt-dest", "FLAG", "no dest-crt still"))
    elif src["law_prefix"]:
        rows.append(_row("L2-crt-dest", "FAIL", "LAW dump still in SitRackView"))
    elif crt_fr["dark"] > 0.55 and crt_fr["millwork"] < 0.08:
        rows.append(
            _row(
                "L2-crt-dest",
                "FLAG",
                f"{crt_png.name} IsolatedDark-heavy dark={crt_fr['dark']:.2f} "
                f"millwork={crt_fr['millwork']:.2f} sit={crt_sit}",
            )
        )
    elif src["has_crt"]:
        rows.append(
            _row(
                "L2-crt-dest",
                "PASS",
                f"{crt_png.name} sit_crt blit dark={crt_fr['dark']:.2f} amber={crt_fr['amber']:.2f}",
            )
        )
    else:
        rows.append(_row("L2-crt-dest", "FAIL", "no IsolatedMode.CRT + sit_crt"))

    if src["field_dump"] or src["alpha_chrome"]:
        rows.append(
            _row(
                "L3-draft-dest",
                "FLAG",
                f"dump chrome Field Objective={src['field_dump']} ALPHA hits={src['alpha_chrome']}",
            )
        )
    elif draft_png is None:
        rows.append(_row("L3-draft-dest", "FLAG", "no dest-draft still"))
    else:
        dfr = _fracs(draft_png)
        if dfr["dark"] > 0.72 and dfr["millwork"] < 0.04:
            rows.append(
                _row(
                    "L3-draft-dest",
                    "FLAG",
                    f"{draft_png.name} IsolatedDark-heavy dark={dfr['dark']:.2f}",
                )
            )
        else:
            rows.append(_row("L3-draft-dest", "PASS", f"{draft_png.name} millwork={dfr['millwork']:.2f}"))

    if not src["same_folder_dest"]:
        rows.append(_row("L4-folder-dest", "FAIL", "Send/FILES do not share openSendOverlay"))
    elif not src["folder_oem"]:
        rows.append(_row("L4-folder-dest", "FLAG", "folderOem CRect missing"))
    elif folder_png is None:
        rows.append(_row("L4-folder-dest", "FLAG", "no dest-folder still"))
    else:
        rows.append(_row("L4-folder-dest", "PASS", f"{folder_png.name}; Send+FILES one dest"))

    if src["title_control"]:
        rows.append(_row("L5-title", "FAIL", "title is a SitHit control"))
    elif plan_png is None and decide_png is None:
        rows.append(_row("L5-title", "FLAG", "no rack still for title plaque"))
    else:
        rows.append(_row("L5-title", "PASS", "title is not a control; plaque Keep"))

    if decide_png is None:
        rows.append(_row("L6-decide-well", "FLAG", "no rack-decide still"))
    else:
        rows.append(_row("L6-decide-well", "FLAG", f"{decide_png.name} needs human millwork fill review"))

    if src["gate_opens_crt"]:
        rows.append(_row("L7-gate", "FAIL", "SitHit.Gate opens CRT dest"))
    else:
        rows.append(_row("L7-gate", "PASS", "Gate is not a CRT door in MainActivity"))

    law = _java("LawPages.kt")
    order_list = ""
    if "val order" in law:
        order_list = law.split("val order", 1)[-1].split(")", 1)[0]
    receipt_in_order = "receipt" in order_list.lower()
    if receipt_in_order:
        rows.append(_row("L8-receipt", "FAIL", "receipt still in LawPages CRT order"))
    elif receipt_png is None:
        rows.append(_row("L8-receipt", "FLAG", "no rack-receipt still"))
    else:
        rows.append(_row("L8-receipt", "PASS", f"{receipt_png.name}; empty stays empty in source"))

    return rows


def render(rows: list[dict]) -> str:
    passed = sum(1 for r in rows if r["verdict"] == "PASS")
    flags = sum(1 for r in rows if r["verdict"] == "FLAG")
    fails = [r["id"] for r in rows if r["verdict"] == "FAIL"]
    lines = [
        "# VISUAL",
        "",
        "**Not Decide. Not Yes. Not 15/15.** Look score of dest millwork (L0–L8).",
        "",
        f"**Score:** {passed}/{len(rows)} PASS · {flags} FLAG · {len(fails)} FAIL",
        "",
        "| id | verdict | evidence |",
        "|----|---------|----------|",
    ]
    for r in rows:
        ev = r["evidence"].replace("|", "/")
        lines.append(f"| {r['id']} | {r['verdict']} | {ev} |")
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
    ap.add_argument("--png-dir", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--serial", default="", help="adb serial; RZCW2038KHN refused")
    args = ap.parse_args(argv)
    if args.serial == REFUSE_SERIAL:
        print("refused: live A33", file=sys.stderr)
        return 3
    rows = score(args.png_dir)
    if args.json:
        print(
            json.dumps(
                {
                    "rows": rows,
                    "passed": sum(r["verdict"] == "PASS" for r in rows),
                    "flag": sum(r["verdict"] == "FLAG" for r in rows),
                },
                indent=2,
            )
        )
    else:
        print(render(rows), end="")
    if any(r["verdict"] == "FAIL" for r in rows):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
