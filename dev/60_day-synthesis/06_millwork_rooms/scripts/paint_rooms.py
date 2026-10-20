#!/usr/bin/env python3
"""Recycle sit millwork plates for the ritual walk. Exact labels. Not Yes.

Archive first. Paint on copies. Imagine is not this script.
Pack is 1080×2138. CRects from SitCRects.kt.
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

CREAM = (243, 230, 200, 255)
GRAPHITE = (42, 36, 24, 255)
VIOLET = (92, 61, 138, 255)
QUIET = (106, 100, 88, 255)
GOLD = (196, 158, 74, 255)
METAL = (168, 164, 156, 255)
PURPLE = (72, 48, 92, 255)


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
    src = src.filter(ImageFilter.GaussianBlur(0.6))
    im.paste(src, (x0, y0))


def inpaint_mask(im: Image.Image, box: tuple[int, int, int, int], mask: np.ndarray, sample: tuple[int, int, int, int]) -> None:
    """Replace masked pixels with the mean of a nearby millwork sample."""
    arr = np.array(im)
    sx0, sy0, sx1, sy1 = sample
    mean = arr[sy0:sy1, sx0:sx1, :3].mean(axis=(0, 1))
    x0, y0, x1, y1 = box
    patch = arr[y0:y1, x0:x1]
    for c in range(3):
        channel = patch[:, :, c]
        channel[mask] = mean[c]
        patch[:, :, c] = channel
    arr[y0:y1, x0:x1] = patch
    im.paste(Image.fromarray(arr))


def gold_mask(patch: np.ndarray) -> np.ndarray:
    r = patch[:, :, 0].astype(int)
    g = patch[:, :, 1].astype(int)
    b = patch[:, :, 2].astype(int)
    a = patch[:, :, 3]
    sat = (r + g) / 2 - b
    return (sat > 22) & (a > 180) & (r > 110)


def dark_mask(patch: np.ndarray, luma: int = 90) -> np.ndarray:
    r = patch[:, :, 0].astype(int)
    g = patch[:, :, 1].astype(int)
    b = patch[:, :, 2].astype(int)
    a = patch[:, :, 3]
    return (r < luma) & (g < luma) & (b < luma) & (a > 180)


def fill_round(im: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, ...], radius: int = 18) -> None:
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill)
    im.alpha_composite(layer)


def center_text(
    im: Image.Image,
    box: tuple[int, int, int, int],
    text: str,
    size: int,
    fill: tuple[int, ...],
    bold: bool = True,
) -> None:
    d = ImageDraw.Draw(im)
    f = font(size, bold=bold)
    x0, y0, x1, y1 = box
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = x0 + (x1 - x0 - tw) / 2 - bbox[0]
    y = y0 + (y1 - y0 - th) / 2 - bbox[1]
    d.text((x, y), text, font=f, fill=fill)


def archive() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for name in (
        "sit_chassis.png",
        "sit_gate.png",
        "sit_well_draft.png",
        "sit_well_decide.png",
        "sit_well_plan.png",
        "sit_well_receipt.png",
        "sit_folder_dest.png",
    ):
        src = NODPI / name
        if src.is_file() and not (ARCHIVE / name).is_file():
            shutil.copy2(src, ARCHIVE / name)


def paint_chassis(im: Image.Image) -> None:
    # Recant STATUS. Clone a clean silver strip over the gold word.
    clone_cover(im, (448, 798, 658, 846), (330, 798, 440, 846))
    clone_cover(im, (430, 2020, 760, 2074), (140, 2020, 340, 2074))


def paint_gate(im: Image.Image) -> None:
    clone_cover(im, (430, 2016, 760, 2074), (110, 2016, 300, 2074))
    center_text(im, (450, 2020, 750, 2072), "WAIT", 28, GOLD, bold=True)


def paint_decide(im: Image.Image) -> None:
    # Recant DECIDE stencil; stamp YES. Keep WHY millwork.
    clone_cover(im, (318, 1564, 772, 1690), (330, 1534, 760, 1560))
    center_text(im, (318, 1564, 772, 1692), "YES", 88, (28, 24, 20, 255), bold=True)


def paint_draft(im: Image.Image) -> None:
    keys = [
        ((250, 1398, 830, 1492), "NOT ACTIVE", VIOLET, 44),
        ((250, 1508, 830, 1600), "LIVE", GRAPHITE, 40),
        ((250, 1614, 830, 1706), "PROPOSED", GRAPHITE, 40),
    ]
    for box, label, fill, sz in keys:
        fill_round(im, box, CREAM, radius=40)
        center_text(im, box, label, sz, fill, bold=True)
    tbc = (300, 1746, 780, 1814)
    fill_round(im, tbc, (210, 205, 198, 255), radius=16)
    center_text(im, tbc, "not the plan", 28, QUIET, bold=False)


def paint_next(src_decide: Image.Image) -> Image.Image:
    im = src_decide.copy()
    clone_cover(im, (430, 1348, 650, 1410), (280, 1348, 400, 1410))
    clone_cover(im, (430, 1418, 650, 1476), (280, 1418, 400, 1476))
    clone_cover(im, (318, 1564, 772, 1690), (330, 1534, 760, 1560))
    top = (140, 1328, 940, 1568)
    bot = (140, 1576, 940, 1824)
    fill_round(im, (200, 1368, 880, 1528), (*CREAM[:3], 220), radius=28)
    fill_round(im, (200, 1620, 880, 1780), (220, 214, 204, 220), radius=28)
    center_text(im, top, "I DID IT", 64, GRAPHITE, bold=True)
    center_text(im, bot, "NOT YET", 56, QUIET, bold=True)
    return im


def paint_folder(im: Image.Image) -> None:
    # Packing slip reminder on the lined paper, above the listing ink.
    center_text(im, (140, 880, 940, 940), "files only  ·  not Yes", 28, QUIET, bold=False)


def composite_preview(chassis: Image.Image, well: Image.Image, extra: list[Image.Image]) -> Image.Image:
    out = Image.new("RGBA", (W, H), (18, 16, 14, 255))
    out.alpha_composite(chassis)
    for layer in extra:
        out.alpha_composite(layer)
    out.alpha_composite(well)
    return out


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    archive()

    chassis = Image.open(ARCHIVE / "sit_chassis.png").convert("RGBA")
    paint_chassis(chassis)
    chassis.save(NODPI / "sit_chassis.png")

    gate = Image.open(ARCHIVE / "sit_gate.png").convert("RGBA")
    paint_gate(gate)
    gate.save(NODPI / "sit_gate.png")

    decide = Image.open(ARCHIVE / "sit_well_decide.png").convert("RGBA")
    next_well = paint_next(decide)
    next_well.save(NODPI / "sit_well_next.png")
    paint_decide(decide)
    decide.save(NODPI / "sit_well_decide.png")

    draft = Image.open(ARCHIVE / "sit_well_draft.png").convert("RGBA")
    paint_draft(draft)
    draft.save(NODPI / "sit_well_draft.png")

    folder = Image.open(ARCHIVE / "sit_folder_dest.png").convert("RGBA")
    paint_folder(folder)
    folder.save(NODPI / "sit_folder_dest.png")

    banks = Image.open(NODPI / "sit_banks.png").convert("RGBA")
    send = Image.open(NODPI / "sit_lamp_send.png").convert("RGBA")
    plan = Image.open(NODPI / "sit_well_plan.png").convert("RGBA")
    receipt = Image.open(NODPI / "sit_well_receipt.png").convert("RGBA")

    extras = [send, banks, gate]
    composite_preview(chassis, plan, extras).save(PREVIEW / "room-plan.png")
    composite_preview(chassis, draft, extras).save(PREVIEW / "room-draft.png")
    composite_preview(chassis, decide, extras).save(PREVIEW / "room-decide.png")
    composite_preview(chassis, next_well, extras).save(PREVIEW / "room-next.png")
    composite_preview(chassis, receipt, extras).save(PREVIEW / "room-receipt.png")

    print("painted", NODPI)
    print("preview", PREVIEW)


if __name__ == "__main__":
    main()
