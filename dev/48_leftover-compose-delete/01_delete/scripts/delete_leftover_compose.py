#!/usr/bin/env python3
"""Remove leftover Compose millwork. Not Yes. Does not assemble."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve()
while not ((ROOT / "aether").is_file() and (ROOT / "android").is_dir()):
    if ROOT.parent == ROOT:
        raise SystemExit("cannot find mechanicall-os root")
    ROOT = ROOT.parent
JAVA = ROOT / "android/app/src/main/java/com/mechanicall/pocket/demo"
REL = [
    "SeatNav.kt",
    "SeatTheme.kt",
    "LcdViewer.kt",
    "SkinLayout.kt",
    "modules/BindModule.kt",
    "modules/ChatHome.kt",
    "modules/DecideModule.kt",
    "modules/PlanModule.kt",
    "modules/ReceiptModule.kt",
    "modules/SplashScreen.kt",
]


def main() -> int:
    removed = []
    missing = []
    for rel in REL:
        p = JAVA / rel
        if p.is_file():
            p.unlink()
            removed.append(str(p.relative_to(ROOT)))
        else:
            missing.append(str(p.relative_to(ROOT)))
    mods = JAVA / "modules"
    if mods.is_dir() and not any(mods.iterdir()):
        mods.rmdir()
        removed.append(str(mods.relative_to(ROOT)) + "/")
    print("removed:")
    for r in removed:
        print(" ", r)
    if missing:
        print("already gone:")
        for m in missing:
            print(" ", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
