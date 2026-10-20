#!/usr/bin/env python3
"""Chassis layers: millwork field + alpha face. Recant farm-paint. Recant oak.

Not Yes. Field is a dark rack case, not a desk photo.
"""
from __future__ import annotations

import shutil
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[4]
NODPI = ROOT / "android/app/src/main/res/drawable-nodpi"
STAGE = Path(__file__).resolve().parents[1]
ARCHIVE = STAGE / "output/archive"
PREVIEW = STAGE / "output/preview"
W, H = 1080, 2138
LETTERBOX = (18, 16, 14)


def archive_once(name: str) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    src = NODPI / name
    dst = ARCHIVE / f"layers-{name}"
    if src.is_file() and not dst.is_file():
        shutil.copy2(src, dst)


def is_surround(px: np.ndarray) -> bool:
    r, g, b = int(px[0]), int(px[1]), int(px[2])
    if abs(r - 18) + abs(g - 16) + abs(b - 14) < 30:
        return True
    # oak / warm desk grain
    if r > g >= b - 8 and (r - b) > 28 and 55 < r < 205 and g < 165 and b < 120:
        return True
    return False


def knock_surround(im: Image.Image) -> Image.Image:
    """Flood from the edges: wood + letterbox → alpha. Keep the instrument."""
    arr = np.array(im.convert("RGBA"))
    h, w = arr.shape[:2]
    seen = np.zeros((h, w), dtype=np.bool_)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            q.append((x, y))
            seen[y, x] = True
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y, x]:
                q.append((x, y))
                seen[y, x] = True
    drop = np.zeros((h, w), dtype=np.bool_)
    while q:
        x, y = q.popleft()
        if not is_surround(arr[y, x]):
            continue
        drop[y, x] = True
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((nx, ny))
    grow = Image.fromarray((drop.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(3))
    drop = np.array(grow) > 0
    arr[drop, 3] = 0
    return Image.fromarray(arr)


def sit_field() -> Image.Image:
    """Dark millwork case. Brushed, Letterbox family. Not oak, not a void."""
    rng = np.random.default_rng(17)
    extra = 64
    noise = rng.normal(0.42, 0.16, (H, W + extra * 2)).astype(np.float32)
    k = np.ones(extra, dtype=np.float32) / extra
    blur = np.empty((H, W), dtype=np.float32)
    for i in range(H):
        blur[i] = np.convolve(noise[i], k, mode="valid")[:W]
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    lift = 0.22 + 0.10 * (1.0 - yy) + 0.04 * (1.0 - xx)
    luma = np.clip((blur - blur.mean()) * 0.28 + lift, 0.04, 0.55)
    rgb = np.zeros((H, W, 3), dtype=np.uint8)
    rgb[..., 0] = np.clip(luma * 48 + 10, 0, 255).astype(np.uint8)
    rgb[..., 1] = np.clip(luma * 42 + 9, 0, 255).astype(np.uint8)
    rgb[..., 2] = np.clip(luma * 36 + 8, 0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB").convert("RGBA")


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    archive_once("sit_chassis.png")
    archive_once("sit_splash.png")

    field = sit_field()
    field.save(NODPI / "sit_field.png")

    chassis_src = ARCHIVE / "layers-sit_chassis.png"
    splash_src = ARCHIVE / "layers-sit_splash.png"
    if not chassis_src.is_file():
        chassis_src = NODPI / "sit_chassis.png"
    if not splash_src.is_file():
        splash_src = NODPI / "sit_splash.png"

    face = knock_surround(Image.open(chassis_src))
    face.save(NODPI / "sit_chassis.png")
    splash = knock_surround(Image.open(splash_src))
    splash.save(NODPI / "sit_splash.png")

    Image.alpha_composite(field, face).save(PREVIEW / "layer-rack.png")
    Image.alpha_composite(field, splash).save(PREVIEW / "layer-splash.png")
    print("field + alpha face + alpha splash")


if __name__ == "__main__":
    main()
