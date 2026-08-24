#!/usr/bin/env python3
"""Bake the sit *editor* as one PNG — VSTGUI CBitmap analogue, not tiled Compose.

Camel Space (2005) packed a full panel bitmap into the VST binary (PE resources /
VSTGUI CBitmap). Production quality is that baked millwork, not live rectangles
with a repeating metal shader.

This writes OUR skin (cream / yellow / purple grammar). Not Camel plates.
Packed in the APK as res/drawable-nodpi/sit_skin.png so aapt2 will not
density-scale the grain (Android analogue of a DLL resource).

Not Yes. Not Imagine-as-spec.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_NODPI = ROOT / "android/app/src/main/res/drawable-nodpi"
PREVIEW = ROOT / "dev/39_sit-storm-factory/15_binary-skin/output/sit_skin.png"
LAYOUT = ROOT / "dev/39_sit-storm-factory/15_binary-skin/output/SKIN-LAYOUT.md"

# storm-0 content: 1080 x 2138 after status/nav on 1080x2340 @ 440dpi
W, H = 1080, 2138

# Cream / yellow / purple (sit law). High-key metal like SOS luminance.
CREAM = (243, 236, 221)
INK = (27, 24, 20)
GOLD = (230, 193, 74)
PURPLE = (107, 62, 161)
WELL = (18, 14, 10)


def brushed(h: int, w: int, seed: int, lift: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    extra = 80
    noise = rng.normal(0.55, 0.22, (h, w + extra * 2)).astype(np.float32)
    k = np.ones(extra, dtype=np.float32) / extra
    blur = np.empty((h, w), dtype=np.float32)
    for i in range(h):
        blur[i] = np.convolve(noise[i], k, mode="valid")[:w]
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    light = 0.82 + 0.22 * (1.0 - yy) + 0.10 * (1.0 - xx)
    luma = np.clip((blur - blur.mean()) * 0.42 + lift, 0.05, 1.0) * light
    rgb = np.zeros((h, w, 3), dtype=np.float32)
    rgb[..., 0] = np.clip(luma * 255.0 * 0.98 + 18, 0, 255)
    rgb[..., 1] = np.clip(luma * 244.0 + 14, 0, 255)
    rgb[..., 2] = np.clip(luma * 214.0 + 10, 0, 255)
    return rgb


def shadow_rect(base: Image.Image, box: tuple[int, int, int, int], blur: int = 12, alpha: int = 90, ox: int = 6, oy: int = 8) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0 + ox, y0 + oy, x1 + ox, y1 + oy], radius=10, fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), layer)


def blit_metal(canvas: Image.Image, metal: np.ndarray, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    crop = metal[y0:y1, x0:x1]
    if crop.size == 0:
        return
    im = Image.fromarray(crop.astype(np.uint8), "RGB")
    canvas.paste(im, (x0, y0))


def bevel(canvas: Image.Image, box: tuple[int, int, int, int], rim: int, raised: bool) -> None:
    x0, y0, x1, y1 = box
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    lite = (255, 248, 230, 110 if raised else 0)
    dark = (0, 0, 0, 120 if raised else 0)
    if not raised:
        lite, dark = (255, 248, 230, 70), (0, 0, 0, 140)
        # recessed: dark N/W, lite S/E
        d.rectangle([x0, y0, x1, y0 + rim], fill=dark)
        d.rectangle([x0, y0, x0 + rim, y1], fill=dark)
        d.rectangle([x0, y1 - rim, x1, y1], fill=lite)
        d.rectangle([x1 - rim, y0, x1, y1], fill=lite)
    else:
        d.rectangle([x0, y0, x1, y0 + rim], fill=lite)
        d.rectangle([x0, y0, x0 + rim, y1], fill=lite)
        d.rectangle([x0, y1 - rim, x1, y1], fill=dark)
        d.rectangle([x1 - rim, y0, x1, y1], fill=dark)
    canvas.alpha_composite(overlay)


def rivet(canvas: Image.Image, cx: int, cy: int, r: int = 8) -> None:
    d = ImageDraw.Draw(canvas)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 34, 26, 255))
    d.ellipse([cx - r + 1, cy - r + 1, cx + r - 1, cy + r - 1], fill=(168, 148, 112, 255))
    d.ellipse([cx - r + 3, cy - r + 2, cx - 1, cy - 1], fill=(255, 248, 230, 160))


def well(canvas: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=8, fill=fill + (255,))
    bevel(canvas, box, 10, raised=False)
    # glass specular
    spec = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    h = max(4, int((y1 - y0) * 0.22))
    for i in range(h):
        a = int(70 * (1 - i / h))
        sd.rectangle([x0 + 10, y0 + 8 + i, x1 - 10, y0 + 9 + i], fill=(247, 231, 160, a))
    canvas.alpha_composite(spec)


def pit_row(canvas: Image.Image, box: tuple[int, int, int, int], n: int = 16) -> None:
    x0, y0, x1, y1 = box
    gap = 6
    usable = (x1 - x0) - gap * (n - 1)
    pw = max(8, usable // n)
    d = ImageDraw.Draw(canvas)
    for i in range(n):
        px = x0 + i * (pw + gap)
        d.rounded_rectangle([px, y0, px + pw, y1], radius=3, fill=(12, 10, 8, 255))
        d.line([(px + 1, y1 - 2), (px + pw - 1, y1 - 2)], fill=(80, 70, 50, 160))


def main() -> None:
    OUT_NODPI.mkdir(parents=True, exist_ok=True)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)

    metal_hi = brushed(H, W, seed=7, lift=0.72)
    metal_lo = brushed(H, W, seed=13, lift=0.28)

    canvas = Image.fromarray(metal_hi.astype(np.uint8), "RGB").convert("RGBA")

    m = 22
    title = (m, 22, W - m, 96)
    lcd = (m, 108, W - m, 186)
    gate = (m, 198, W - m, 332)
    desk = (m, 344, W - m, 438)
    tabs = (m, 450, W - m, 528)
    paper = (m, 540, W - m, H - 22)

    plates = [title, lcd, gate, desk, tabs, paper]
    for box in plates:
        canvas = shadow_rect(canvas, box, blur=14, alpha=80, ox=5, oy=7)

    blit_metal(canvas, metal_lo, title)
    bevel(canvas, title, 9, raised=True)
    blit_metal(canvas, metal_lo, lcd)
    bevel(canvas, lcd, 8, raised=True)
    blit_metal(canvas, metal_lo, gate)
    bevel(canvas, gate, 8, raised=True)
    blit_metal(canvas, metal_hi, desk)
    bevel(canvas, desk, 8, raised=True)
    blit_metal(canvas, metal_hi, tabs)
    bevel(canvas, tabs, 7, raised=True)
    blit_metal(canvas, metal_hi, paper)
    bevel(canvas, paper, 10, raised=True)

    well(canvas, (lcd[0] + 14, lcd[1] + 14, lcd[2] - 14, lcd[3] - 12), WELL)
    well(canvas, (gate[0] + 14, gate[1] + 36, gate[2] - 14, gate[3] - 12), WELL)
    pit_row(canvas, (gate[0] + 22, gate[1] + 48, gate[2] - 22, gate[3] - 20), 16)

    # cream paper inset (the score)
    pd = ImageDraw.Draw(canvas)
    inset = (paper[0] + 16, paper[1] + 16, paper[2] - 16, paper[3] - 16)
    pd.rounded_rectangle(inset, radius=6, fill=CREAM + (255,))
    bevel(canvas, inset, 8, raised=False)
    grain = np.random.default_rng(11).random((inset[3] - inset[1], inset[2] - inset[0]))
    ga = Image.fromarray(np.clip((grain - 0.5) * 28 + 243, 200, 255).astype(np.uint8), "L").convert("RGB")
    # tint grain cream
    arr = np.array(ga).astype(np.float32)
    arr[..., 0] *= 0.98
    arr[..., 1] *= 0.96
    arr[..., 2] *= 0.90
    ga = Image.fromarray(arr.astype(np.uint8), "RGB")
    canvas.paste(ga, (inset[0], inset[1]))

    rivet(canvas, title[0] + 22, (title[1] + title[3]) // 2)
    rivet(canvas, title[2] - 22, (title[1] + title[3]) // 2)

    # baked labels (yellow). Live Next/GATE text overlays in Compose.
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 28)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
        small = font
    pd = ImageDraw.Draw(canvas)
    pd.text((title[0] + 44, title[1] + 22), "MECHANICALL", font=font, fill=GOLD + (255,))
    pd.text((gate[0] + 22, gate[1] + 10), "GATE", font=small, fill=GOLD + (255,))

    png = canvas.convert("RGB")
    dest = OUT_NODPI / "sit_skin.png"
    png.save(dest, "PNG", optimize=True)
    png.save(PREVIEW, "PNG")
    LAYOUT.write_text(
        f"""# SKIN-LAYOUT — sit_skin.png {W}x{H}

VSTGUI analogue: one CBitmap. Compose overlays live text/clicks on these CRects.

| plate | l t r b (px at {W}x{H}) |
|-------|-------------------------|
| title | {title} |
| lcd   | {lcd} |
| gate  | {gate} |
| desk  | {desk} |
| tabs  | {tabs} |
| paper | {paper} |

Pack: `res/drawable-nodpi/sit_skin.png` (no density scale).
""",
        encoding="utf-8",
    )
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    print(f"wrote {PREVIEW}")


if __name__ == "__main__":
    main()
