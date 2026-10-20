#!/usr/bin/env python3
"""Make sit_well_receipt an interchangeable *frame*: paper inner goes alpha.

Live graphite draws in the hole. Not farm-paint on sit_chassis.
Not Yes.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
NODPI = ROOT / "android/app/src/main/res/drawable-nodpi"
SRC = NODPI / "sit_well_receipt.png"
ARCHIVE = Path(__file__).resolve().parents[1] / "output/archive/sit_well_receipt.png"
# cream paper bbox measured 2026-09-08 (pack px)
PAPER = (117, 1380, 965, 1813)


def main() -> None:
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.is_file():
        shutil.copy2(SRC, ARCHIVE)
    im = Image.open(ARCHIVE).convert("RGBA")
    px = im.load()
    l, t, r, b = PAPER
    pad = 4
    for y in range(t + pad, b - pad):
        for x in range(l + pad, r - pad):
            rgba = list(px[x, y])
            rgba[3] = 0
            px[x, y] = tuple(rgba)
    im.save(SRC, "PNG")
    print(f"punched inner {PAPER} pad={pad} → {SRC}")
    print(f"archive {ARCHIVE}")


if __name__ == "__main__":
    main()
