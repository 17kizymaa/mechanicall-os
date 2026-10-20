#!/usr/bin/env python3
"""JOIN/WAKE/GATE stills on storm-0. Never Confirm. Never Yes. Never A33."""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "07_sdk_stills"))
from walk_ritual import (  # noqa: E402
    HITS,
    adb,
    grant,
    launch,
    pack_to_screen,
    pick_serial,
    seed,
    shot,
    tap,
    tap_ui,
    wm,
)

HITS["join"] = (270, 993)
HITS["wake"] = (813, 993)

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "output" / "stills"
APK = ROOT / "android/app/build/outputs/apk/debug/app-debug.apk"


def main() -> int:
    serial = pick_serial()
    OUT.mkdir(parents=True, exist_ok=True)
    adb(serial, "install", "-r", "-d", str(APK))
    grant(serial)
    seed(serial, OUT)
    sw, sh = wm(serial)
    print("serial", serial, "wm", sw, sh)
    launch(serial)
    time.sleep(2.4)
    shot(serial, OUT, "01-bind-idle")
    tap(serial, "bind_pad", sw, sh)
    time.sleep(1.0)
    tap_ui(serial, OUT, "sit-pocket") or tap_ui(serial, OUT, "Download")
    time.sleep(0.6)
    tap_ui(serial, OUT, "use this folder")
    time.sleep(0.8)
    tap_ui(serial, OUT, "allow")
    time.sleep(1.2)
    shot(serial, OUT, "02-plan")
    tap(serial, "join", sw, sh)
    time.sleep(0.7)
    shot(serial, OUT, "03-join-network")
    tap(serial, "wake", sw, sh)
    time.sleep(0.5)
    shot(serial, OUT, "04-wake-network")
    tap(serial, "gate", sw, sh)
    time.sleep(0.4)
    shot(serial, OUT, "05-gate")
    print("done", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
