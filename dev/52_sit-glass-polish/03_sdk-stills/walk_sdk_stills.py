#!/usr/bin/env python3
"""SDK module stills after dest millwork. Never Confirm. Never A33."""
from __future__ import annotations

import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

SERIAL_REFUSE = "RZCW2038KHN"
PKG = "com.mechanicall.pocket.demo"
PACK_W, PACK_H = 1080, 2138
# SitCRects centres (pack px) after 02 dest millwork.
HITS = {
    "lcd": (540, 510),
    "title": (540, 110),
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
    "iso_right": (980, 560),
    "iso_left": (120, 560),
    "draft_alpha": (540, 1381),
    "draft_beta": (540, 1511),
    "decide_plaque": (540, 1576),
}

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "output"
ADB = Path.home() / ".android-sdk-mechanicall" / "platform-tools" / "adb"


def adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    cmd = [str(ADB), "-s", serial(), *args]
    return subprocess.run(cmd, check=check, capture_output=True)


def serial() -> str:
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


def wm() -> tuple[int, int]:
    out = adb("shell", "wm", "size").stdout.decode()
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


def tap(name: str, sw: int, sh: int) -> None:
    px, py = HITS[name]
    x, y = pack_to_screen(px, py, sw, sh)
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(0.55)


def shot(name: str) -> None:
    png = OUT / f"{name}.png"
    adb("shell", "screencap", "-p", "/data/local/tmp/sit-still.png")
    adb("pull", "/data/local/tmp/sit-still.png", str(png))
    adb("shell", "uiautomator", "dump", "/sdcard/uidump.xml", check=False)
    adb("pull", "/sdcard/uidump.xml", str(OUT / f"uidump-{name}.xml"), check=False)
    print("still", png.name, png.stat().st_size)


def hide_ime() -> None:
    """DONE only. Never BACK — BACK leaves the activity when IME is already down."""
    out = adb("shell", "dumpsys", "input_method", check=False).stdout.decode(errors="replace")
    shown = "mInputShown=true" in out or "mIsInputViewShown=true" in out
    if not shown:
        return
    adb("shell", "input", "keyevent", "66", check=False)
    time.sleep(0.35)


def wait_boot(timeout: int = 180) -> None:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            serial()
            boot = subprocess.check_output(
                [str(ADB), "-s", serial(), "shell", "getprop", "sys.boot_completed"]
            ).decode().strip()
            if boot == "1":
                return
        except Exception:
            pass
        time.sleep(2)
    sys.exit("emulator boot timeout")


def seed_pocket() -> str:
    path = "/sdcard/sit-sdk-pocket"
    adb("shell", "mkdir", "-p", path)
    local = OUT / "_seed"
    local.mkdir(exist_ok=True)
    (local / "CURRENT.md").write_text(
        "# CURRENT\n\n"
        "**Objective:** SDK stills pocket. Not operator law.\n"
        "**Phase:** SELECT\n"
        "**Status:** DRAFT\n"
        "**Baseline:** sit-glass-polish sdk\n"
        "**Next:** look-only\n"
        "**Approval:** PENDING\n\n"
        "## Keep\n- one Next\n\n"
        "## Reject\n- dual-concurrent-next\n\n"
        "## Limits\n- SDK lab\n\n"
        "## Next allowed action\nlook-only\n\n"
        "## Approval condition\nnone\n\n"
        "## Prohibited\n- automatic-approve\n",
        encoding="utf-8",
    )
    adb("push", str(local / "CURRENT.md"), f"{path}/CURRENT.md")
    return path


def grant() -> None:
    adb("shell", "appops", "set", PKG, "MANAGE_EXTERNAL_STORAGE", "allow", check=False)
    adb("shell", "cmd", "appops", "set", PKG, "MANAGE_EXTERNAL_STORAGE", "allow", check=False)
    adb("shell", "pm", "grant", PKG, "android.permission.READ_EXTERNAL_STORAGE", check=False)
    adb("shell", "pm", "grant", PKG, "android.permission.WRITE_EXTERNAL_STORAGE", check=False)


def dump_ui() -> Path:
    xmlp = OUT / "_uidump.xml"
    adb("shell", "uiautomator", "dump", "/sdcard/uidump.xml", check=False)
    adb("pull", "/sdcard/uidump.xml", str(xmlp), check=False)
    return xmlp


def tap_ui(*needles: str) -> bool:
    xmlp = dump_ui()
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
        x, y = (l + r) // 2, (t + bot) // 2
        adb("shell", "input", "tap", str(x), str(y))
        time.sleep(0.7)
        print("tap_ui", needles, x, y)
        return True
    print("tap_ui miss", needles)
    return False


def focus_pkg() -> str:
    p = subprocess.run(
        [str(ADB), "-s", serial(), "shell", "dumpsys", "activity", "activities"],
        capture_output=True,
        timeout=8,
    )
    text = p.stdout.decode(errors="replace")
    for ln in text.splitlines():
        if "topResumedActivity" in ln or "mResumedActivity" in ln:
            return ln
    return text[-200:]


def wait_focus(substr: str, seconds: float = 8.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < seconds:
        if substr in focus_pkg():
            return True
        time.sleep(0.3)
    print("wait_focus miss", substr, focus_pkg())
    return False


def launch(splash_wait: float) -> None:
    adb("shell", "am", "force-stop", PKG)
    adb("shell", "am", "force-stop", "com.google.android.documentsui", check=False)
    time.sleep(0.3)
    adb(
        "shell",
        "am",
        "start",
        "-n",
        f"{PKG}/.MainActivity",
        "-a",
        "android.intent.action.MAIN",
    )
    time.sleep(splash_wait)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    wait_boot()
    ser = serial()
    print("serial", ser)
    apk = ROOT / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
    if not apk.is_file():
        sys.exit(f"missing {apk}")
    adb("install", "-r", "-d", str(apk))
    grant()
    seed_pocket()
    sw, sh = wm()
    print("wm", sw, sh)
    adb("shell", "mkdir", "-p", "/sdcard/Download/sit-pocket")
    adb("push", str(OUT / "_seed" / "CURRENT.md"), "/sdcard/Download/sit-pocket/CURRENT.md")

    launch(1.1)
    shot("01-splash")
    time.sleep(1.6)
    shot("02-after-splash")
    shot("03-bind-idle")
    wait_focus(PKG, 6.0)
    tap("bind_pad", sw, sh)
    time.sleep(1.2)
    shot("04-bind-picker")
    tap_ui("sit-pocket") or tap_ui("sit-sdk-pocket") or tap_ui("Download")
    time.sleep(0.7)
    shot("05-inside-pocket")
    tap_ui("use this folder")
    time.sleep(1.0)
    shot("06-allow-or-land")
    tap_ui("allow")
    time.sleep(1.4)
    shot("07-post-bind")
    if not wait_focus(PKG, 5.0):
        adb("shell", "input", "keyevent", "4", check=False)
        time.sleep(0.4)
        wait_focus(PKG, 4.0)
    shot("08-land-after-allow")

    tap("lcd", sw, sh)
    time.sleep(0.5)
    shot("10-crt-isolated")
    tap("iso_right", sw, sh)
    time.sleep(0.4)
    shot("11-crt-page-next")
    tap("iso_top", sw, sh)
    time.sleep(0.4)
    shot("12-crt-dismiss")

    tap("join", sw, sh)
    time.sleep(0.5)
    shot("13-join")
    tap("send", sw, sh)
    time.sleep(0.6)
    shot("14-send-overlay")
    tap("outside_send", sw, sh)
    time.sleep(0.4)
    shot("15-send-dismiss")
    tap("wake", sw, sh)
    time.sleep(0.5)
    shot("16-wake")

    tap("bank_plan", sw, sh)
    time.sleep(0.45)
    shot("17-bank-plan")
    tap("well", sw, sh)
    time.sleep(0.45)
    shot("18-plan-key-crt")
    tap("iso_top", sw, sh)
    time.sleep(0.4)
    shot("19-plan-dismiss")

    tap("bank_draft", sw, sh)
    time.sleep(0.55)
    shot("20-draft-isolated")
    tap("draft_alpha", sw, sh)
    time.sleep(0.45)
    shot("21-draft-field")
    hide_ime()
    tap("iso_top", sw, sh)
    time.sleep(0.4)
    shot("22-draft-dismiss")

    tap("bank_decide", sw, sh)
    time.sleep(0.5)
    shot("23-decide")
    tap("lcd", sw, sh)
    time.sleep(0.45)
    shot("24-decide-why")
    hide_ime()
    tap("title", sw, sh)
    time.sleep(0.35)
    hide_ime()

    tap("bank_receipt", sw, sh)
    time.sleep(0.55)
    shot("25-receipt")

    tap("files", sw, sh)
    time.sleep(0.9)
    shot("26-files")
    adb("shell", "input", "keyevent", "4", check=False)
    time.sleep(0.5)
    shot("27-files-back")

    tap("gate", sw, sh)
    time.sleep(0.5)
    shot("28-gate")
    tap("lcd", sw, sh)
    time.sleep(0.4)
    shot("29-crt-isolated-again")

    names = sorted(p.name for p in OUT.glob("*.png"))
    idx = [
        "# SDK module stills — 0.19.3-glass-polish",
        "",
        "**Not Yes. Not A33. Not LTE. Not Play.** SDK lab FLAG only.",
        "",
        f"serial `{ser}` · wm {sw}x{sh} · APK 0.19.3-glass-polish vc 28",
        "",
        "Confirm was not tapped. Opening the emulator is not Yes.",
        "",
    ]
    (OUT / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")
    print("wrote", len(names), "pngs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
