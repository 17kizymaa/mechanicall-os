#!/usr/bin/env python3
"""Opinionated sit stills on storm-0. Never Confirm. Never Yes. Never A33.

Does not tap Yes plaque twice. Does not tap Decide Not yet.
Does not BankPlan/BankDraft while on Decide (P0: that rejects CURRENT).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Reuse ritual walker primitives.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "07_sdk_stills"))
from walk_ritual import (  # noqa: E402
    ADB,
    PKG,
    adb,
    grant,
    launch,
    pick_serial,
    seed,
    shot,
    tap,
    tap_ui,
    wm,
)

FIRST_PLAN = """# Proposed CURRENT update (draft — not authority)

NOT ACTIVE. First Plan for this sit. Not the live plan.

**Next:** strengthen-core-loop
**Why (on glass, not Yes):** receipt is leftover; not_yet rejects CURRENT; CRT entry is dead.

She has not said Yes.
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--apk",
        type=Path,
        default=Path.home() / ".mechanicall/apk-archive/mechanicall-0.19.20-inbox-net-vc45.apk",
    )
    args = ap.parse_args(argv)
    serial = pick_serial()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    if args.apk.is_file():
        adb(serial, "install", "-r", "-d", str(args.apk))
    grant(serial)
    seed(serial, out)
    pocket = "/sdcard/Download/sit-pocket/PROPOSE-CURRENT.md"
    local = out / "_seed" / "PROPOSE-CURRENT.md"
    local.write_text(FIRST_PLAN, encoding="utf-8")
    adb(serial, "push", str(local), pocket)
    sw, sh = wm(serial)
    print("serial", serial, "wm", sw, sh)
    launch(serial)
    time.sleep(1.2)
    shot(serial, out, "01-open")
    tap(serial, "bank_plan", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "02-plan")
    tap(serial, "well", sw, sh)
    time.sleep(0.45)
    shot(serial, out, "03-plan-key")
    tap(serial, "lcd", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "04-plan-terminal")
    tap(serial, "title", sw, sh)
    time.sleep(0.35)
    tap(serial, "bank_draft", sw, sh)
    time.sleep(0.55)
    shot(serial, out, "05-draft-well")
    tap(serial, "well", sw, sh)
    time.sleep(0.7)
    shot(serial, out, "06-draft-writer")
    tap(serial, "title", sw, sh)
    time.sleep(0.4)
    tap(serial, "bank_decide", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "07-decide")
    tap(serial, "why", sw, sh)
    time.sleep(0.5)
    shot(serial, out, "08-decide-why")
    # Leave Decide via RECEIPT bank — not Plan, not Not yet (P0).
    tap(serial, "title", sw, sh)
    time.sleep(0.35)
    tap(serial, "bank_receipt", sw, sh)
    time.sleep(0.55)
    shot(serial, out, "09-receipt")
    tap(serial, "bank_plan", sw, sh)
    time.sleep(0.4)
    tap(serial, "send", sw, sh)
    time.sleep(0.55)
    shot(serial, out, "10-folder")
    print("Confirm was not tapped. Yes was not two-tapped. Decide Not yet was not tapped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
