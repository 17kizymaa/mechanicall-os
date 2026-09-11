#!/usr/bin/env python3
"""Dest stills on storm-0. Never Confirm. Never A33. Not testers."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

SERIAL_REFUSE = "RZCW2038KHN"
PKG = "com.mechanicall.pocket.demo"
PACK_W, PACK_H = 1080, 2138
HITS = {
    "lcd": (540, 510),
    "title": (540, 111),
    "join": (270, 993),
    "send": (543, 990),
    "wake": (813, 993),
    "bank_plan": (243, 1209),
    "bank_draft": (446, 1209),
    "bank_decide": (649, 1209),
    "bank_receipt": (851, 1209),
    "bind_pad": (540, 1559),
    "files": (544, 1775),
    "gate": (540, 1985),
    "well": (540, 1576),
    "outside_send": (80, 400),
    "iso_top": (540, 80),
    "folder_send": (540, 750),
}

ROOT = Path(__file__).resolve().parent.parent
ADB = Path.home() / ".android-sdk-mechanicall" / "platform-tools" / "adb"


def adb(serial: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    cmd = [str(ADB), "-s", serial, *args]
    return subprocess.run(cmd, check=check, capture_output=True)


def pick_serial() -> str:
    out = subprocess.check_output([str(ADB), "devices"]).decode()
    lines = [ln.split()[0] for ln in out.splitlines()[1:] if "\tdevice" in ln]
    if SERIAL_REFUSE in lines:
        sys.stderr.write("refused: live A33\n")
        sys.exit(3)
    emus = [s for s in lines if s.startswith("emulator-")]
    if not emus:
        sys.stderr.write("no emulator device\n")
        sys.exit(2)
    return emus[0]


def wm(serial: str) -> tuple[int, int]:
    out = adb(serial, "shell", "wm", "size").stdout.decode()
    for ln in out.splitlines():
        if ":" in ln:
            w, h = ln.split(":")[-1].strip().split("x")
            return int(w), int(h)
    return 1080, 2400


def pack_to_screen(px: int, py: int, sw: int, sh: int) -> tuple[int, int]:
    scale = min(sw / PACK_W, sh / PACK_H)
    ox = (sw - PACK_W * scale) / 2
    oy = (sh - PACK_H * scale) / 2
    return int(ox + px * scale), int(oy + py * scale)


def tap(serial: str, name: str, sw: int, sh: int) -> None:
    px, py = HITS[name]
    x, y = pack_to_screen(px, py, sw, sh)
    adb(serial, "shell", "input", "tap", str(x), str(y))
    time.sleep(0.55)


def shot(serial: str, out: Path, name: str) -> None:
    png = out / f"{name}.png"
    adb(serial, "shell", "screencap", "-p", "/data/local/tmp/sit-still.png")
    adb(serial, "pull", "/data/local/tmp/sit-still.png", str(png))
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/uidump.xml", check=False)
    adb(serial, "pull", "/sdcard/uidump.xml", str(out / f"uidump-{name}.xml"), check=False)
    print("still", png.name, png.stat().st_size)


def dump_ui(serial: str, out: Path) -> Path:
    xmlp = out / "_uidump.xml"
    adb(serial, "shell", "uiautomator", "dump", "/sdcard/uidump.xml", check=False)
    adb(serial, "pull", "/sdcard/uidump.xml", str(xmlp), check=False)
    return xmlp


def tap_ui(serial: str, out: Path, *needles: str) -> bool:
    xmlp = dump_ui(serial, out)
    if not xmlp.is_file() or xmlp.stat().st_size < 20:
        return False
    try:
        root = ET.parse(xmlp).getroot()
    except ET.ParseError:
        return False
    want = [n.lower() for n in needles]
    for node in root.iter("node"):
        blob = " ".join(
            filter(None, (node.get("text"), node.get("content-desc"), node.get("resource-id")))
        ).lower()
        if not any(w in blob for w in want):
            continue
        b = node.get("bounds") or ""
        m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", b)
        if not m:
            continue
        l, t, r, bot = map(int, m.groups())
        adb(serial, "shell", "input", "tap", str((l + r) // 2), str((t + bot) // 2))
        time.sleep(0.7)
        print("tap_ui", needles)
        return True
    print("tap_ui miss", needles)
    return False


def seed(serial: str, out: Path) -> None:
    path = "/sdcard/Download/sit-pocket"
    adb(serial, "shell", "mkdir", "-p", path)
    local = out / "_seed"
    local.mkdir(exist_ok=True)
    (local / "CURRENT.md").write_text(
        "# CURRENT\n\n"
        "**Objective:** Dest look seed. Not operator law.\n"
        "**Phase:** SELECT\n"
        "**Status:** DRAFT\n"
        "**Baseline:** first-sit-look storm\n"
        "**Next:** look-only\n"
        "**Approval:** PENDING\n\n"
        "## Keep\n- one Next\n\n"
        "## Reject\n- dual-concurrent-next\n\n"
        "## Limits\n- storm lab\n\n"
        "## Next allowed action\nlook-only\n\n"
        "## Approval condition\nnone\n\n"
        "## Prohibited\n- automatic-approve\n",
        encoding="utf-8",
    )
    (local / "PROPOSE-CURRENT.md").write_text(
        "# Proposed CURRENT update (draft — not authority)\n\n"
        "Type here. This file is PROPOSE-CURRENT.md. Not CURRENT.\n",
        encoding="utf-8",
    )
    adb(serial, "push", str(local / "CURRENT.md"), f"{path}/CURRENT.md")
    adb(serial, "push", str(local / "PROPOSE-CURRENT.md"), f"{path}/PROPOSE-CURRENT.md")


def grant(serial: str) -> None:
    adb(serial, "shell", "appops", "set", PKG, "MANAGE_EXTERNAL_STORAGE", "allow", check=False)
    adb(serial, "shell", "cmd", "appops", "set", PKG, "MANAGE_EXTERNAL_STORAGE", "allow", check=False)
    adb(serial, "shell", "pm", "grant", PKG, "android.permission.READ_EXTERNAL_STORAGE", check=False)


def launch(serial: str) -> None:
    adb(serial, "shell", "am", "force-stop", PKG)
    adb(serial, "shell", "am", "force-stop", "com.google.android.documentsui", check=False)
    time.sleep(0.3)
    adb(serial, "shell", "am", "start", "-n", f"{PKG}/.MainActivity", "-a", "android.intent.action.MAIN")
    time.sleep(2.2)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--apk", type=Path, default=ROOT / "android/app/build/outputs/apk/debug/app-debug.apk")
    args = ap.parse_args(argv)
    serial = pick_serial()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.apk.is_file():
        adb(serial, "install", "-r", "-d", str(args.apk))
    grant(serial)
    seed(serial, out)
    sw, sh = wm(serial)
    print("serial", serial, "wm", sw, sh)
    launch(serial)
    shot(serial, out, "bind-idle")
    tap(serial, "bind_pad", sw, sh)
    time.sleep(1.0)
    tap_ui(serial, out, "sit-pocket") or tap_ui(serial, out, "Download")
    time.sleep(0.6)
    tap_ui(serial, out, "use this folder")
    time.sleep(0.8)
    tap_ui(serial, out, "allow")
    time.sleep(1.2)
    shot(serial, out, "rack-plan")
    tap(serial, "lcd", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "dest-crt")
    tap(serial, "iso_top", sw, sh)
    time.sleep(0.4)
    tap(serial, "bank_draft", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "dest-draft")
    tap(serial, "lcd", sw, sh)
    time.sleep(0.7)
    shot(serial, out, "dest-draft-edit")
    tap(serial, "iso_top", sw, sh)
    time.sleep(0.4)
    tap(serial, "title", sw, sh)
    time.sleep(0.35)
    tap(serial, "send", sw, sh)
    time.sleep(0.55)
    shot(serial, out, "dest-folder")
    tap(serial, "folder_send", sw, sh)
    time.sleep(1.2)
    shot(serial, out, "dest-folder-staged")
    tap(serial, "outside_send", sw, sh)
    time.sleep(0.35)
    tap(serial, "bank_decide", sw, sh)
    time.sleep(0.45)
    shot(serial, out, "rack-decide")
    tap(serial, "bank_receipt", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "rack-receipt")
    tap(serial, "gate", sw, sh)
    time.sleep(0.4)
    shot(serial, out, "rack-gate")
    print("Confirm was not tapped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
