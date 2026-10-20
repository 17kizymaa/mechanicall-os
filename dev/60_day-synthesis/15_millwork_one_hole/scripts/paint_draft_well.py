#!/usr/bin/env python3
"""Recycle sit_well_draft: NOT ACTIVE millwork plate, not cream pills.

Not Yes. Not L4. Not sit_chassis.png. Archive first.
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

W, H = 1080, 2138
WELL = (109, 1316, 971, 1836)
# Cream pills from 06 paint_rooms.paint_draft
PILLS = [
    (250, 1398, 830, 1492),
    (250, 1508, 830, 1600),
    (250, 1614, 830, 1706),
    (300, 1746, 780, 1814),
]
PLATE = (200, 1410, 880, 1760)
VIOLET = (92, 61, 138, 255)
QUIET = (106, 100, 88, 255)
METAL = (176, 172, 164, 255)
METAL_EDGE = (120, 116, 108, 255)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    path = (
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
    )
    return ImageFont.truetype(path, size)


def clone_cover(im: Image.Image, box: tuple[int, int, int, int], sample: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    src = im.crop(sample).resize((max(1, x1 - x0), max(1, y1 - y0)), Image.Resampling.BILINEAR)
    src = src.filter(ImageFilter.GaussianBlur(0.5))
    im.paste(src, (x0, y0))


def inpaint_cream(im: Image.Image) -> None:
    """Cover cream / light pills inside the well with nearby dark millwork."""
    arr = np.array(im)
    x0, y0, x1, y1 = WELL
    patch = arr[y0:y1, x0:x1]
    r = patch[:, :, 0].astype(int)
    g = patch[:, :, 1].astype(int)
    b = patch[:, :, 2].astype(int)
    a = patch[:, :, 3]
    cream = (r > 175) & (g > 155) & (b > 115) & (a > 80)
    light = (r > 190) & (g > 185) & (b > 175) & (a > 80)
    mask = cream | light
    sx0, sy0, sx1, sy1 = 400, 1336, 700, 1388
    mean = arr[sy0:sy1, sx0:sx1, :3].mean(axis=(0, 1))
    for c in range(3):
        channel = patch[:, :, c]
        channel[mask] = mean[c]
        patch[:, :, c] = channel
    arr[y0:y1, x0:x1] = patch
    im.paste(Image.fromarray(arr))
    for box in PILLS:
        clone_cover(im, box, (380, 1330, 720, 1384))


def paint_plate(im: Image.Image) -> None:
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(PLATE, radius=22, fill=METAL_EDGE)
    inner = (PLATE[0] + 10, PLATE[1] + 10, PLATE[2] - 10, PLATE[3] - 10)
    d.rounded_rectangle(inner, radius=16, fill=METAL)
    im.alpha_composite(layer)
    d2 = ImageDraw.Draw(im)
    f1 = font(56, bold=True)
    f2 = font(28, bold=False)
    x0, y0, x1, y1 = inner
    t1 = "NOT ACTIVE"
    b1 = d2.textbbox((0, 0), t1, font=f1)
    tw, th = b1[2] - b1[0], b1[3] - b1[1]
    d2.text(
        (x0 + (x1 - x0 - tw) / 2 - b1[0], y0 + (y1 - y0) * 0.28 - th / 2 - b1[1]),
        t1,
        font=f1,
        fill=VIOLET,
    )
    t2 = "not the plan"
    b2 = d2.textbbox((0, 0), t2, font=f2)
    tw2, th2 = b2[2] - b2[0], b2[3] - b2[1]
    d2.text(
        (x0 + (x1 - x0 - tw2) / 2 - b2[0], y0 + (y1 - y0) * 0.68 - th2 / 2 - b2[1]),
        t2,
        font=f2,
        fill=QUIET,
    )


def composite_preview(well: Image.Image) -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    chassis = Image.open(NODPI / "sit_chassis.png").convert("RGBA")
    field = Image.open(NODPI / "sit_field.png").convert("RGBA") if (NODPI / "sit_field.png").is_file() else None
    banks = Image.open(NODPI / "sit_banks.png").convert("RGBA")
    send = Image.open(NODPI / "sit_lamp_send.png").convert("RGBA")
    gate = Image.open(NODPI / "sit_gate.png").convert("RGBA")
    out = Image.new("RGBA", (W, H), (18, 16, 14, 255))
    if field is not None:
        out.alpha_composite(field)
    out.alpha_composite(chassis)
    out.alpha_composite(send)
    out.alpha_composite(banks)
    out.alpha_composite(well)
    out.alpha_composite(gate)
    out.save(PREVIEW / "room-draft.png")


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    src = NODPI / "sit_well_draft.png"
    archived = ARCHIVE / "sit_well_draft.png"
    if src.is_file() and not archived.is_file():
        shutil.copy2(src, archived)
    im = Image.open(archived if archived.is_file() else src).convert("RGBA")
    inpaint_cream(im)
    paint_plate(im)
    im.save(NODPI / "sit_well_draft.png")
    composite_preview(im)
    print("painted", NODPI / "sit_well_draft.png")
    print("preview", PREVIEW / "room-draft.png")
    print("archive", archived)


if __name__ == "__main__":
    main()
