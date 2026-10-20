#!/usr/bin/env python3
"""P1 splash: instrument boot. Recant plugin words. Keep millwork. Not Yes.

G1=2* G2=1+3. Do not dim lamps. Gears = craft. Exact remaining copy = Pillow.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[4]
NODPI = ROOT / "android/app/src/main/res/drawable-nodpi"
STAGE = Path(__file__).resolve().parents[1]
ARCHIVE = STAGE / "output/archive"
PREVIEW = STAGE / "output/preview"

CREAM_INK = (232, 220, 180, 255)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Bold.ttf", size)


def clone_cover(im: Image.Image, box: tuple[int, int, int, int], sample: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    src = im.crop(sample).resize((max(1, x1 - x0), max(1, y1 - y0)), Image.Resampling.BILINEAR)
    src = src.filter(ImageFilter.GaussianBlur(0.5))
    im.paste(src, (x0, y0))


def inpaint_mask(im: Image.Image, box: tuple[int, int, int, int], mask: np.ndarray, sample: tuple[int, int, int, int]) -> None:
    arr = np.array(im)
    sx0, sy0, sx1, sy1 = sample
    mean = arr[sy0:sy1, sx0:sx1, :3].mean(axis=(0, 1))
    x0, y0, x1, y1 = box
    patch = arr[y0:y1, x0:x1]
    for c in range(3):
        ch = patch[:, :, c]
        ch[mask] = mean[c]
        patch[:, :, c] = ch
    arr[y0:y1, x0:x1] = patch
    im.paste(Image.fromarray(arr))


def center_text(im: Image.Image, box: tuple[int, int, int, int], text: str, size: int, fill: tuple[int, ...]) -> None:
    d = ImageDraw.Draw(im)
    f = font(size)
    x0, y0, x1, y1 = box
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) / 2 - bbox[0]
    y = y0 + (y1 - y0 - th) / 2 - bbox[1]
    d.text((x, y), text, font=f, fill=fill)


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    src = NODPI / "sit_splash.png"
    if not (ARCHIVE / "sit_splash.png").is_file():
        shutil.copy2(src, ARCHIVE / "sit_splash.png")

    im = Image.open(ARCHIVE / "sit_splash.png").convert("RGBA")

    d = ImageDraw.Draw(im)
    silver = tuple(im.getpixel((300, 822))[:3]) + (255,)
    plaque = tuple(im.getpixel((500, 120))[:3]) + (255,)
    cream = tuple(im.getpixel((320, 1248))[:3]) + (255,)
    purple = tuple(im.getpixel((200, 2048))[:3]) + (255,)
    # Glyph-only fills. Keep LED, slots, lights, gears, lamps.
    d.rectangle((468, 814, 628, 842), fill=silver)
    d.rectangle((455, 2008, 735, 2052), fill=purple)
    d.rectangle((900, 88, 1020, 128), fill=plaque)
    for box in (
        (208, 1238, 280, 1274),
        (412, 1238, 490, 1274),
        (616, 1238, 694, 1274),
        (820, 1238, 900, 1274),
    ):
        d.rectangle(box, fill=cream)

    # Instrument name on the plaque (same idea as chassis). Not STATUS.
    center_text(im, (131, 38, 880, 185), "MECHANICALL", 64, CREAM_INK)

    im.save(NODPI / "sit_splash.png")
    im.save(PREVIEW / "p1-splash.png")
    print("wrote", NODPI / "sit_splash.png")
    print("preview", PREVIEW / "p1-splash.png")


if __name__ == "__main__":
    main()
