#!/usr/bin/env python3
"""You Decide functional gauntlet on storm-0.

Disk + uidump, not source greps. Never tap Yes/Confirm. Never A33.
Fail-closed on the first broken step. PASS is not human Yes.
USB ≠ LTE.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

PY = Path(__file__).resolve().parent
ROOT = PY.parent
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from sit_dest_walk import (  # noqa: E402
    PKG,
    SERIAL_REFUSE,
    adb,
    grant,
    pick_serial,
    seed,
    shot,
    tap,
    wm,
)

DEFAULT_APK = ROOT / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"

POCKET = "/sdcard/Download/sit-pocket"
SEED_NEXT = "gauntlet-seed"
EXIT_PASS = 0
EXIT_BUDGET = 1
EXIT_ITERATE = 2
EXIT_REFUSE = 3
EXIT_ENV = 4

STEPS = (
    "G0-launch",
    "G1-bound",
    "G2-plan-disk",
    "G3-crt-open",
    "G4-crt-dismiss",
    "G5-send-open",
    "G11-send-stage",
    "G6-send-dismiss",
    "G7-draft-propose",
    "G8-decide-why",
    "G9-not-yet",
    "G10-relaunch",
)


def _out(proc) -> str:
    raw = proc.stdout or b""
    if isinstance(raw, bytes):
        return raw.decode("utf-8", errors="replace")
    return str(raw)


def pocket_cat(serial: str, name: str) -> str:
    proc = adb(serial, "shell", "cat", f"{POCKET}/{name}", check=False)
    return _out(proc)


def pocket_sha(serial: str, name: str) -> str:
    blob = pocket_cat(serial, name)
    return hashlib.sha256(blob.encode("utf-8", errors="replace")).hexdigest()[:16]


def uidump_blob(serial: str, out: Path) -> str:
    xmlp = out / "_uidump.xml"
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/uidump.xml", check=False)
    adb(serial, "pull", "/sdcard/uidump.xml", str(xmlp), check=False)
    if xmlp.is_file():
        return xmlp.read_text(encoding="utf-8", errors="replace")
    return ""


def desc(blob: str) -> str:
    bits = []
    for token in ("content-desc=", "text="):
        i = 0
        while True:
            j = blob.find(token, i)
            if j < 0:
                break
            q = blob.find('"', j + len(token) + 1)
            if q < 0:
                break
            bits.append(blob[j + len(token) + 1 : q])
            i = q + 1
    return " ".join(bits)


def start_bound(serial: str) -> None:
    adb(serial, "shell", "am", "force-stop", PKG, check=False)
    time.sleep(0.3)
    adb(
        serial,
        "shell",
        "am",
        "start",
        "-n",
        f"{PKG}/.MainActivity",
        "--es",
        "pocket",
        POCKET,
        check=False,
    )
    time.sleep(4.5)


def row(gid: str, ok: bool, evidence: str) -> dict:
    return {
        "id": gid,
        "verdict": "PASS" if ok else "FAIL",
        "ok": ok,
        "evidence": evidence,
    }


def run_steps(serial: str, out: Path, apk: Path) -> list[dict]:
    rows: list[dict] = []
    sw, sh = wm(serial)
    if apk.is_file():
        adb(serial, "install", "-r", "-d", str(apk), check=False)
    grant(serial)
    seed(serial, out)
    current = pocket_cat(serial, "CURRENT.md")
    if f"**Next:** {SEED_NEXT}" not in current:
        patched = current.replace("**Next:** look-only", f"**Next:** {SEED_NEXT}")
        if f"**Next:** {SEED_NEXT}" not in patched:
            patched = current.rstrip() + f"\n\n**Next:** {SEED_NEXT}\n"
        local = out / "_seed" / "CURRENT.md"
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(patched, encoding="utf-8")
        adb(serial, "push", str(local), f"{POCKET}/CURRENT.md", check=False)
    start_bound(serial)
    shot(serial, out, "g0-launch")
    blob = uidump_blob(serial, out)
    sit = PKG in blob
    rows.append(row("G0-launch", sit, f"sit={sit} launcher={('launcher' in blob.lower())}"))
    if not sit:
        return rows

    blob = uidump_blob(serial, out)
    d = desc(blob)
    current = pocket_cat(serial, "CURRENT.md")
    bound = ("PLAN" in d or "published" in d.lower()) and SEED_NEXT in current
    rows.append(row("G1-bound", bound, f"desc={d[:80]!r} next_on_disk={SEED_NEXT in current}"))
    if not bound:
        return rows

    sha0 = pocket_sha(serial, "CURRENT.md")
    rows.append(
        row(
            "G2-plan-disk",
            SEED_NEXT in current and sha0 != "",
            f"sha={sha0} next={SEED_NEXT in current}",
        )
    )

    tap(serial, "lcd", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "g3-crt")
    sha = pocket_sha(serial, "CURRENT.md")
    rows.append(row("G3-crt-open", sha == sha0, f"current_sha {sha0} -> {sha}"))
    if sha != sha0:
        return rows

    tap(serial, "iso_top", sw, sh)
    time.sleep(0.4)
    sha = pocket_sha(serial, "CURRENT.md")
    rows.append(row("G4-crt-dismiss", sha == sha0, f"current_sha {sha}"))

    tap(serial, "send", sw, sh)
    time.sleep(0.55)
    shot(serial, out, "g5-send")
    sha = pocket_sha(serial, "CURRENT.md")
    rows.append(row("G5-send-open", sha == sha0, f"current_sha {sha}"))
    tap(serial, "folder_send", sw, sh)
    time.sleep(1.4)
    shot(serial, out, "g11-send-stage")
    sha = pocket_sha(serial, "CURRENT.md")
    notice = pocket_cat(serial, ".aether/upload-stage/NOTICE.json")
    staged = sha == sha0 and "not_yes" in notice and "offered" in notice
    rows.append(
        row(
            "G11-send-stage",
            staged,
            f"current_stable={sha == sha0} notice_len={len(notice)} not_yes={'not_yes' in notice}",
        )
    )
    if sha != sha0:
        return rows
    tap(serial, "outside_send", sw, sh)
    time.sleep(0.35)
    sha = pocket_sha(serial, "CURRENT.md")
    rows.append(row("G6-send-dismiss", sha == sha0, f"current_sha {sha}"))

    tap(serial, "bank_draft", sw, sh)
    time.sleep(0.8)
    tap(serial, "lcd", sw, sh)
    time.sleep(0.4)
    adb(serial, "shell", "input", "text", "gauntlet-next", check=False)
    time.sleep(1.0)
    shot(serial, out, "g7-draft")
    propose = pocket_cat(serial, "PROPOSE-CURRENT.md")
    sha = pocket_sha(serial, "CURRENT.md")
    typed = "gauntlet-next" in propose
    draft_ok = sha == sha0 and typed
    rows.append(
        row(
            "G7-draft-propose",
            draft_ok,
            f"current_stable={sha == sha0} propose_len={len(propose)} has_type={typed}",
        )
    )
    if sha != sha0:
        return rows

    tap(serial, "iso_top", sw, sh)
    time.sleep(0.35)
    tap(serial, "bank_decide", sw, sh)
    time.sleep(0.5)
    tap(serial, "well", sw, sh)
    time.sleep(0.45)
    shot(serial, out, "g8-decide")
    blob = uidump_blob(serial, out)
    d = desc(blob)
    why = "why" in d.lower() or "DECIDE" in d
    rows.append(row("G8-decide-why", why, f"desc={d[:100]!r}"))

    tap(serial, "bank_plan", sw, sh)
    time.sleep(1.2)
    shot(serial, out, "g9-not-yet")
    current = pocket_cat(serial, "CURRENT.md")
    receipt = pocket_cat(serial, "RECEIPT.md")
    next_kept = f"**Next:** {SEED_NEXT}" in current
    not_applied = "gauntlet-next" not in current
    receipt_ok = "Not yet" in receipt
    not_yet = next_kept and not_applied and receipt_ok
    rows.append(
        row(
            "G9-not-yet",
            not_yet,
            f"next_kept={next_kept} propose_not_applied={not_applied} receipt_not_yet={receipt_ok}",
        )
    )
    if not not_yet:
        return rows

    adb(serial, "shell", "am", "force-stop", PKG)
    time.sleep(0.4)
    start_bound(serial)
    shot(serial, out, "g10-relaunch")
    current = pocket_cat(serial, "CURRENT.md")
    receipt = pocket_cat(serial, "RECEIPT.md")
    propose = pocket_cat(serial, "PROPOSE-CURRENT.md")
    blob = uidump_blob(serial, out)
    d = desc(blob)
    ok = (
        f"**Next:** {SEED_NEXT}" in current
        and "gauntlet-next" not in current
        and "gauntlet-next" in propose
        and "Not yet" in receipt
        and ("PLAN" in d or PKG in blob)
    )
    rows.append(
        row(
            "G10-relaunch",
            ok,
            f"next_kept={SEED_NEXT in current} propose_kept={'gauntlet-next' in propose} "
            f"receipt_not_yet={'Not yet' in receipt} desc={d[:60]!r}",
        )
    )
    return rows


def render(rows: list[dict]) -> str:
    passed = sum(1 for r in rows if r["ok"])
    fails = [r["id"] for r in rows if not r["ok"]]
    lines = [
        "# GAUNTLET",
        "",
        "**Not Decide. Not Yes.** Stateful play on storm-0. Never Confirm.",
        "",
        f"**Score:** {passed}/{len(STEPS)} ran={len(rows)}",
        "",
        "| id | verdict | evidence |",
        "|----|---------|----------|",
    ]
    seen = {r["id"] for r in rows}
    for r in rows:
        ev = r["evidence"].replace("|", "/")
        lines.append(f"| {r['id']} | {r['verdict']} | {ev} |")
    for gid in STEPS:
        if gid not in seen:
            lines.append(f"| {gid} | SKIP | previous FAIL |")
    lines.append("")
    if fails:
        lines.append("**Failed:** " + ", ".join(fails))
        lines.append("")
        lines.append("First FAIL is the next patch. Do not tap Confirm to green this table.")
    else:
        lines.append("**Failed:** none")
        lines.append("")
        lines.append("PASS is not human Yes. Confirm was not tapped.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "dev" / "57_first-sit-look" / "08_gauntlet" / "output",
    )
    ap.add_argument("--serial", default="")
    ap.add_argument("--apk", type=Path, default=DEFAULT_APK)
    args = ap.parse_args(argv)
    if args.serial == SERIAL_REFUSE:
        print("refused: live A33", file=sys.stderr)
        return EXIT_REFUSE
    try:
        serial = pick_serial()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else EXIT_ENV
        return code
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    rows = run_steps(serial, out, args.apk.resolve())
    text = render(rows)
    (out / "GAUNTLET.md").write_text(text, encoding="utf-8")
    print(text, end="")
    try:
        from mum_verify import render as mum_render
        from mum_verify import score as mum_score

        mum_rows = mum_score(gauntlet_md=out / "GAUNTLET.md", png_dir=out)
        mum_text = mum_render(mum_rows)
        (out / "MUM.md").write_text(mum_text, encoding="utf-8")
        print(mum_text, end="")
    except Exception as exc:  # noqa: BLE001 — loop still prints gauntlet if mum import fails
        print(f"mum_verify skipped: {exc}", file=sys.stderr)
    if any(not r["ok"] for r in rows):
        return EXIT_ITERATE
    if len(rows) < len(STEPS):
        return EXIT_ITERATE
    return EXIT_PASS


if __name__ == "__main__":
    raise SystemExit(main())
