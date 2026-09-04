#!/usr/bin/env python3
"""A33 USB looks of 0.19.3 dests. Never Confirm. USB ≠ LTE. Not testers."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

SERIAL = "RZCW2038KHN"
PKG = "com.mechanicall.pocket.demo"
PACK_W, PACK_H = 1080, 2138
EDGE = "anphuni@100.70.86.90"
HITS = {
    "lcd": (540, 510),
    "title": (540, 110),
    "send": (543, 990),
    "bank_plan": (243, 1209),
    "bank_draft": (446, 1209),
    "bank_decide": (649, 1209),
    "bank_receipt": (851, 1209),
    "well": (540, 1576),
    "outside_send": (80, 400),
    "iso_top": (540, 80),
    "iso_right": (980, 560),
    "draft_alpha": (540, 1381),
}

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "output"
LOOK = ROOT / "scripts" / "sit-look.sh"


def ssh_adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    remote = "adb -s " + SERIAL + " " + " ".join(args)
    return subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", EDGE, remote],
        check=check,
        capture_output=True,
    )


def pack_to_screen(px: int, py: int, sw: int, sh: int) -> tuple[int, int]:
    scale = min(sw / PACK_W, sh / PACK_H)
    ox = (sw - PACK_W * scale) / 2
    oy = (sh - PACK_H * scale) / 2
    return int(ox + px * scale), int(oy + py * scale)


def tap(name: str, sw: int, sh: int) -> None:
    x, y = pack_to_screen(*HITS[name], sw, sh)
    ssh_adb("shell", "input", "tap", str(x), str(y))
    time.sleep(0.7)


def look(name: str) -> None:
    out = OUT / f"{name}.png"
    env = {
        **dict(**{k: str(v) for k, v in __import__("os").environ.items()}),
        "SIT_LOOK_HOST": EDGE,
        "SIT_LOOK_SERIAL": SERIAL,
        "POCKET_EDGE": EDGE,
        "POCKET_SERIAL": SERIAL,
    }
    r = subprocess.run([str(LOOK), str(out)], env=env, capture_output=True, text=True)
    print("look", name, r.stdout.strip() or r.stderr.strip()[-200:], "rc", r.returncode)
    if r.returncode != 0:
        raise SystemExit(f"look failed {name}: {r.stderr}")


def hide_ime() -> None:
    ssh_adb("shell", "input", "keyevent", "66", check=False)
    time.sleep(0.3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    state = ssh_adb("get-state").stdout.decode().strip()
    if state != "device":
        sys.exit(f"adb state={state}")
    wm = ssh_adb("shell", "wm", "size").stdout.decode()
    sw, sh = 1080, 2400
    for ln in wm.splitlines():
        if ":" in ln:
            w, h = ln.split(":")[-1].strip().split("x")
            sw, sh = int(w), int(h)
    print("wm", sw, sh)

    ssh_adb("shell", "am", "force-stop", PKG)
    time.sleep(0.4)
    ssh_adb(
        "shell",
        "am",
        "start",
        "-n",
        f"{PKG}/.MainActivity",
        "-a",
        "android.intent.action.MAIN",
    )
    time.sleep(1.7)
    look("01-splash")
    time.sleep(1.6)
    look("02-land")

    tap("lcd", sw, sh)
    time.sleep(0.5)
    look("10-crt-isolated")
    tap("iso_right", sw, sh)
    time.sleep(0.4)
    look("11-crt-page")
    tap("iso_top", sw, sh)
    time.sleep(0.4)
    look("12-crt-dismiss")

    tap("send", sw, sh)
    time.sleep(0.6)
    look("14-send-overlay")
    tap("outside_send", sw, sh)
    time.sleep(0.4)
    look("15-send-dismiss")

    tap("bank_draft", sw, sh)
    time.sleep(0.55)
    look("20-draft-isolated")
    tap("draft_alpha", sw, sh)
    time.sleep(0.45)
    look("21-draft-field")
    hide_ime()
    tap("iso_top", sw, sh)
    time.sleep(0.4)
    look("22-draft-dismiss")

    tap("bank_decide", sw, sh)
    time.sleep(0.5)
    look("23-decide")
    # Why glass only — never arm/Yes/Confirm
    tap("lcd", sw, sh)
    time.sleep(0.4)
    look("24-decide-why")
    hide_ime()
    tap("title", sw, sh)
    time.sleep(0.35)
    hide_ime()

    tap("bank_receipt", sw, sh)
    time.sleep(0.55)
    look("25-receipt")

    tap("bank_plan", sw, sh)
    time.sleep(0.4)
    look("17-plan")

    print("Confirm was not tapped. USB ≠ LTE. Opening is not Yes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
