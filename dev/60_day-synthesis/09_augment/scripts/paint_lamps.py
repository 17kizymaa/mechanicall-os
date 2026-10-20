#!/usr/bin/env python3
"""P2 lamp row: Send stays. JOIN/WAKE become millwork blanks, not dimmed icons.

G1=2* G2=1+3. Keep metal rings. Inner disc = cream + screw. Not Yes.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
NODPI = ROOT / "android/app/src/main/res/drawable-nodpi"
STAGE = Path(__file__).resolve().parents[1]
ARCHIVE = STAGE / "output/archive"
PREVIEW = STAGE / "output/preview"

# Disc centres from chassis dark-fill (not SitCRects hit boxes).
JOIN = (247, 1009)
WAKE = (840, 1010)
R_INNER = 90
CREAM = (200, 193, 164)


def archive_once(name: str) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    src = NODPI / name
    dst = ARCHIVE / name
    if src.is_file() and not dst.is_file():
        shutil.copy2(src, dst)


def cream_disc(im: Image.Image, cx: int, cy: int, r: int) -> None:
    arr = np.array(im)
    yy, xx = np.ogrid[: arr.shape[0], : arr.shape[1]]
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    ys, xs = np.where(mask)
    rng = np.random.default_rng(cx * 1000 + cy)
    noise = rng.normal(0, 3.2, (ys.size, 3))
    fill = np.clip(np.array(CREAM, dtype=np.float64) + noise, 0, 255).astype(np.uint8)
    arr[ys, xs, :3] = fill
    im.paste(Image.fromarray(arr))


def screw(im: Image.Image, cx: int, cy: int) -> None:
    d = ImageDraw.Draw(im)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=(72, 70, 66, 255))
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(176, 172, 162, 255))
    d.ellipse((cx - 9, cy - 10, cx + 10, cy + 9), fill=(198, 194, 184, 255))
    d.rectangle((cx - 2, cy - 8, cx + 2, cy + 8), fill=(58, 56, 52, 255))
    d.rectangle((cx - 8, cy - 2, cx + 8, cy + 2), fill=(58, 56, 52, 255))


def blank_lamps(im: Image.Image) -> None:
    for cx, cy in (JOIN, WAKE):
        cream_disc(im, cx, cy, R_INNER)
        screw(im, cx, cy)


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for name in ("sit_chassis.png", "sit_splash.png"):
        archive_once(name)

    chassis = Image.open(ARCHIVE / "sit_chassis.png").convert("RGBA")
    # If P2 already ran, archive is pre-P2 chassis (STATUS recant from 06). Good.
    # Current nodpi chassis may already be that archive. Always paint from archive.
    blank_lamps(chassis)
    chassis.save(NODPI / "sit_chassis.png")
    chassis.crop((140, 850, 950, 1130)).save(PREVIEW / "p2-lamps-chassis.png")

    splash_src = ARCHIVE / "sit_splash.png"
    # Prefer P1 splash (current nodpi) as splash source if archive is pre-P1.
    # P1 wrote nodpi; P2 archive_once won't overwrite sit_splash if P1 already archived pre-P1.
    # Use nodpi splash (P1) as the plate to re-lay lamps on, after copying to sit_splash-p1.png once.
    p1 = ARCHIVE / "sit_splash-p1.png"
    nodpi_splash = NODPI / "sit_splash.png"
    if not p1.is_file():
        shutil.copy2(nodpi_splash, p1)
    splash = Image.open(p1).convert("RGBA")
    blank_lamps(splash)
    splash.save(NODPI / "sit_splash.png")
    splash.crop((140, 850, 950, 1130)).save(PREVIEW / "p2-lamps-splash.png")

    print("chassis + splash JOIN/WAKE blanks; Send kept")
    print("preview", PREVIEW)


if __name__ == "__main__":
    main()
