#!/usr/bin/env python3
"""Blit CURRENT essentials into the *existing* STATUS LCD well.

Not a second terminal. Not Yes. Preview only (01_plates halt).
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "output"
PLAN = OUT / "plan.png"
CURRENT = ROOT / "CURRENT.md"
# Preview pixels on plan.png (576x1248) — existing amber STATUS glass.
LCD = (72, 176, 504, 452)
GOLD = (230, 193, 74)
DIM = (20, 16, 10)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
    ):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def inner_current(raw: str) -> str:
    """Prefer the fenced body if CURRENT.md is still a proposal wrapper."""
    m = re.search(r"```markdown\n(# CURRENT\n.*)\n```\s*\Z", raw, re.S)
    return m.group(1) if m else raw


def essentials(text: str) -> dict[str, str]:
    pages: dict[str, str] = {}
    for name, pat in (
        ("objective", r"^\*\*Objective:\*\*\s*(.+)$"),
        ("next", r"^\*\*Next:\*\*\s*(.+)$"),
        ("phase", r"^\*\*Phase:\*\*\s*(.+)$"),
        ("status", r"^\*\*Status:\*\*\s*(.+)$"),
    ):
        m = re.search(pat, text, re.M)
        pages[name] = m.group(1).strip() if m else ""
    def section(header: str) -> str:
        m = re.search(
            rf"^## {re.escape(header)}\n(.*?)(?=^## |\Z)",
            text,
            re.M | re.S,
        )
        return (m.group(1).strip() if m else "")[:800]
    pages["keep"] = section("Keep")
    pages["reject"] = section("Reject")
    pages["limits"] = section("Limits")
    return pages


def blit(page: str, lines: list[str], dest: Path) -> None:
    im = Image.open(PLAN).convert("RGB")
    l, t, r, b = LCD
    well = Image.new("RGB", (r - l, b - t), DIM)
    d = ImageDraw.Draw(well)
    font = _font(14)
    y = 8
    d.text((8, y), f"LAW · {page.upper()}", font=font, fill=GOLD)
    y += 22
    d.line((8, y, well.size[0] - 8, y), fill=GOLD, width=1)
    y += 8
    body = _font(12)
    x0, width = 8, well.size[0] - 16
    for line in lines:
        line = line.replace("\t", "  ")
        while line:
            cut = len(line)
            while cut > 1 and body.getlength(line[:cut]) > width:
                cut -= 1
            if cut < len(line):
                sp = line.rfind(" ", 0, cut)
                if sp > 0:
                    cut = sp
            d.text((x0, y), line[:cut], font=body, fill=GOLD)
            line = line[cut:].lstrip()
            y += 16
            if y > well.size[1] - 20:
                d.text((x0, well.size[1] - 18), "… GATE SEQ →", font=body, fill=GOLD)
                break
        if y > well.size[1] - 20:
            break
    im.paste(well, (l, t))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG")


def main() -> None:
    text = inner_current(CURRENT.read_text(encoding="utf-8"))
    p = essentials(text)
    blit(
        "idle",
        [f"NEXT {p['next']}", f"{p['phase']} · {p['status']}"],
        OUT / "lcd-idle.png",
    )
    blit("objective", [p["objective"]], OUT / "lcd-objective.png")
    blit("next", [f"**Next:** {p['next']}"], OUT / "lcd-next.png")
    blit("keep", p["keep"].splitlines() or ["(empty keep)"], OUT / "lcd-keep.png")
    print("wrote lcd-idle/objective/next/keep.png")


if __name__ == "__main__":
    main()
