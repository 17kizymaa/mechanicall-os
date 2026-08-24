#!/usr/bin/env python3
"""Brushed-metal tiles for the sit rack. Photoshop 2005 recipe, not Camel bitmaps.

2004–2006 VST editors (Camel Space included) were **bitmap skins**: one panel PNG
plus filmstrip knobs, drawn in Photoshop (Filter → Noise → Motion Blur → Lighting)
and composited in VSTGUI 2.x. JUCE is later (Alchemy). KnobMan is 2007+.

This script repeats that optical chain in numpy/PIL so the APK can host a *skin*
the same way Compose ImageShader hosts a tile — without stealing Camel assets.

Not Yes. Not Imagine-as-spec.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DRAWABLE = ROOT / "android/app/src/main/res/drawable"
PREVIEW = ROOT / "dev/39_sit-storm-factory/14_sos-luminance/output/metal-preview.png"
N = 256


def _box_blur_h(src: np.ndarray, width: int) -> np.ndarray:
    k = np.ones(width, dtype=np.float32) / float(width)
    pad = width // 2
    out = np.empty_like(src)
    for i in range(src.shape[0]):
        row = np.pad(src[i], (pad, pad), mode="wrap")
        out[i] = np.convolve(row, k, mode="valid")[: src.shape[1]]
    return out


def brushed_luma(seed: int, contrast: float, blur: int = 42) -> np.ndarray:
    """Tileable horizontal grain: wrap-padded noise + motion blur + contrast."""
    rng = np.random.default_rng(seed)
    big = N * 3
    noise = rng.normal(0.52, 0.28, (big, big)).astype(np.float32)
    noise = np.clip(noise, 0.0, 1.0)
    blurred = _box_blur_h(noise, blur)
    crop = blurred[N : 2 * N, N : 2 * N]
    crop = (crop - crop.mean()) * contrast + 0.5
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32)
    light = 0.78 + 0.22 * (1.0 - yy / N) + 0.10 * (1.0 - xx / N)
    return np.clip(crop * light, 0.0, 1.0)


def colorize(luma: np.ndarray, rgb: tuple[float, float, float], lift: float) -> Image.Image:
    """Map luma onto a warm cream-silver (or dark chocolate) so yellow/cream survive."""
    r0, g0, b0 = rgb
    arr = np.zeros((N, N, 3), dtype=np.float32)
    arr[..., 0] = np.clip(luma * r0 + lift, 0, 255)
    arr[..., 1] = np.clip(luma * g0 + lift, 0, 255)
    arr[..., 2] = np.clip(luma * b0 + lift, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def paper_grain() -> Image.Image:
    rng = np.random.default_rng(11)
    n = rng.random((N, N)).astype(np.float32)
    # Fine fibre: slight horizontal smear, very low alpha, warm ink specks.
    n = _box_blur_h(n, 3)
    alpha = np.clip((n - 0.45) * 55, 0, 36).astype(np.uint8)
    rgb = np.zeros((N, N, 4), dtype=np.uint8)
    rgb[..., 0] = 72
    rgb[..., 1] = 54
    rgb[..., 2] = 36
    rgb[..., 3] = alpha
    return Image.fromarray(rgb, "RGBA")


def lcd_glass() -> Image.Image:
    """Dark glass: vertical falloff + speckle. Warm, not teal."""
    h, w = 256, 64
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    base = 38 - yy * 26
    rng = np.random.default_rng(5)
    speckle = rng.normal(0, 2.2, (h, w))
    r = np.clip(base + 8 + speckle, 8, 70)
    g = np.clip(base + speckle, 6, 58)
    b = np.clip(base - 6 + speckle, 4, 48)
    rgb = np.dstack([r, g, b]).astype(np.uint8)
    img = Image.fromarray(rgb, "RGB").convert("RGBA")
    # Specular strip at the top of the well (light from above).
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(int(h * 0.22)):
        a = int(70 * (1 - y / (h * 0.22)))
        for x in range(w):
            overlay.putpixel((x, y), (247, 231, 160, a))
    return Image.alpha_composite(img, overlay)


def main() -> None:
    DRAWABLE.mkdir(parents=True, exist_ok=True)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)

    light_luma = np.clip(brushed_luma(seed=7, contrast=0.50) * 0.40 + 0.62, 0.0, 1.0)
    # High-key cream-silver (SOS luminance) — not mid-grey.
    light = colorize(light_luma, (255.0, 244.0, 220.0), lift=28)
    dark_luma = np.clip(brushed_luma(seed=13, contrast=0.62) * 0.50 + 0.28, 0.0, 1.0)
    dark = colorize(dark_luma, (150.0, 126.0, 94.0), lift=12)
    paper = paper_grain()
    glass = lcd_glass()

    (DRAWABLE / "metal_light.png").parent.mkdir(parents=True, exist_ok=True)
    light.save(DRAWABLE / "metal_light.png")
    dark.save(DRAWABLE / "metal_dark.png")
    paper.save(DRAWABLE / "paper_grain.png")
    glass.save(DRAWABLE / "lcd_glass.png")

    preview = Image.new("RGB", (N * 2 + 24, N + 16), (30, 26, 22))
    preview.paste(light, (8, 8))
    preview.paste(dark, (N + 16, 8))
    preview.save(PREVIEW)
    print(f"wrote {DRAWABLE / 'metal_light.png'}")
    print(f"wrote {DRAWABLE / 'metal_dark.png'}")
    print(f"wrote {DRAWABLE / 'paper_grain.png'}")
    print(f"wrote {DRAWABLE / 'lcd_glass.png'}")
    print(f"wrote {PREVIEW}")


if __name__ == "__main__":
    main()
