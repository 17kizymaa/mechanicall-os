#!/usr/bin/env python3
"""Play listing bitmaps from the sit launcher. Not Yes. Not Camel PNGs."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png"
OUT = ROOT / "android/play-listing"


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ):
        p = Path(path)
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    logo = Image.open(SRC).convert("RGBA")
    icon = Image.new("RGB", (512, 512), (24, 28, 22))
    mark = logo.copy()
    mark.thumbnail((420, 420))
    icon.paste(mark, ((512 - mark.size[0]) // 2, (512 - mark.size[1]) // 2), mark)
    icon.save(OUT / "icon-512.png")

    feat = Image.new("RGB", (1024, 500), (24, 28, 22))
    draw = ImageDraw.Draw(feat)
    mark = logo.copy()
    mark.thumbnail((280, 280))
    feat.paste(mark, (64, (500 - mark.size[1]) // 2), mark)
    draw.text((380, 160), "Mechanicall", fill=(232, 220, 180), font=_font(64))
    draw.text((380, 250), "Bind a folder. Publish with Why.", fill=(180, 190, 160), font=_font(28))
    draw.text((380, 310), "Closed testers — not production", fill=(140, 150, 130), font=_font(22))
    feat.save(OUT / "feature-1024x500.png")
    print(f"wrote {OUT / 'icon-512.png'}")
    print(f"wrote {OUT / 'feature-1024x500.png'}")


if __name__ == "__main__":
    main()
