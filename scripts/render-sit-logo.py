#!/usr/bin/env python3
"""Draw the sit rack glyph from SeatPalette hex. Not Imagine. Not Yes.

Identifiable millwork (title, cyan LCD, paper, GATE pits) sits inside an
ellipse so OEM adaptive masks (A33 squircle/circle) do not crop the mark.
Metal full-bleed outside the ellipse. Not a Camel bitmap.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DRAWABLE = ROOT / "android/app/src/main/res/drawable/logo_mechanicall.png"
LAUNCHER = ROOT / "android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png"

HOST = (228, 216, 196, 255)
PANEL = (217, 204, 182, 255)
TITLE = (58, 50, 40, 255)
BEVEL_LITE = (247, 241, 230, 255)
BEVEL_DARK = (42, 36, 28, 255)
LCD_BG = (26, 20, 12, 255)
LCD = (230, 193, 74, 255)
PURPLE = (107, 62, 161, 255)
INK = (27, 24, 20, 255)

W = 192
CX = CY = W // 2
# Adaptive-icon safe zone is ~66% circle. Ellipse slightly inside that.
RX, RY = 62, 70


def main() -> None:
    img = Image.new("RGBA", (W, W), HOST)
    d = ImageDraw.Draw(img)
    box = [CX - RX, CY - RY, CX + RX, CY + RY]
    d.ellipse([box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3], fill=BEVEL_DARK)
    d.ellipse([box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1], fill=BEVEL_LITE)
    d.ellipse(box, fill=PANEL)

    inner = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    di = ImageDraw.Draw(inner)
    x0, y0, x1, y1 = CX - 44, CY - 48, CX + 44, CY + 48
    di.rectangle([x0, y0, x1, y0 + 18], fill=TITLE)
    di.rectangle([x0, y0 + 18, x1, y0 + 40], fill=TITLE)
    di.rectangle([x0 + 4, y0 + 22, x1 - 4, y0 + 38], fill=LCD_BG)
    di.rectangle([x0 + 10, y0 + 27, x1 - 10, y0 + 33], fill=LCD)
    di.rectangle([x0 + 6, y0 + 44, x1 - 6, y1 - 18], fill=PANEL)
    di.rectangle([x0 + 6, y0 + 44, x1 - 6, y1 - 18], outline=INK)
    gy = y1 - 14
    pits, gap = 6, 3
    usable = (x1 - 8) - (x0 + 8)
    pw = max(4, (usable - gap * (pits - 1)) // pits)
    for i in range(pits):
        px = x0 + 8 + i * (pw + gap)
        di.rectangle([px, gy, px + pw, gy + 10], fill=BEVEL_DARK)
        di.rectangle([px + 1, gy + 1, px + pw, gy + 10], fill=PURPLE if i < 2 else LCD_BG)

    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse(box, fill=255)
    img.paste(inner, (0, 0), mask)

    DRAWABLE.parent.mkdir(parents=True, exist_ok=True)
    LAUNCHER.parent.mkdir(parents=True, exist_ok=True)
    img.save(DRAWABLE, "PNG")
    img.save(LAUNCHER, "PNG")
    print(f"wrote {DRAWABLE}")
    print(f"wrote {LAUNCHER}")


if __name__ == "__main__":
    main()
