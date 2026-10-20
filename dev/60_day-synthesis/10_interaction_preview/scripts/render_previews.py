#!/usr/bin/env python3
"""G3=1 preview bake — L=1 freeze slots + L=4 no-freeze plates.

Quiet Next *room* recanted. After Yes = Plan ticket + labour feet.
S=1 = optional packing-slip popup. Imagine ≠ spec. Not nodpi.

Not Yes. Not CURRENT.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "output"
PREV = OUT / "preview"
LAYOUT = OUT / "SKIN-LAYOUT.md"

W, H = 1080, 2138
CREAM = (243, 236, 221)
INK = (27, 24, 20)
GOLD = (230, 193, 74)
PURPLE = (107, 62, 161)
WELL = (18, 14, 10)
GRAPHITE = (42, 36, 24)
HOST = (18, 16, 14)
VIOLET = (92, 61, 138)

# SitCRects freeze slots
TITLE = (131, 38, 949, 185)
LCD = (146, 254, 934, 767)
GLASS = (176, 292, 904, 728)
JOIN = (165, 877, 375, 1110)
SEND = (435, 870, 652, 1110)
WAKE = (705, 877, 922, 1110)
BANK_PLAN = (165, 1158, 322, 1261)
BANK_DRAFT = (368, 1158, 525, 1261)
BANK_DECIDE = (570, 1158, 728, 1261)
BANK_RECEIPT = (772, 1158, 930, 1261)
WELL_BOX = (109, 1316, 971, 1836)
GATE = (75, 1864, 1005, 2107)
SEND_POP = (110, 720, 970, 1580)

# L4 interaction pack (no freeze lamp row)
L4_TITLE = (22, 22, 1058, 118)
L4_PEEK = (22, 130, 1058, 300)
L4_BANKS = (22, 312, 1058, 418)
L4_PAPER = (22, 430, 1058, 1968)
L4_WAIT = (22, 1980, 1058, 2116)
L4_POP = (70, 640, 1010, 1680)


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


def fonts() -> tuple:
    paths = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    )
    try:
        huge = ImageFont.truetype(paths[0], 72)
        poster = ImageFont.truetype(paths[0], 108)
        title = ImageFont.truetype(paths[0], 40)
        body = ImageFont.truetype(paths[1], 32)
        small = ImageFont.truetype(paths[2], 24)
        peek = ImageFont.truetype(paths[2], 28)
    except OSError:
        d = ImageFont.load_default()
        huge = poster = title = body = small = peek = d
    return huge, poster, title, body, small, peek


HUGE, POSTER, FONT, BODY, SMALL, PEEK = fonts()
METAL_HI = None
METAL_LO = None


def metals() -> tuple[np.ndarray, np.ndarray]:
    global METAL_HI, METAL_LO
    if METAL_HI is None:
        METAL_HI = brushed(H, W, seed=7, lift=0.72)
        METAL_LO = brushed(H, W, seed=13, lift=0.28)
    return METAL_HI, METAL_LO


def shadow_rect(base: Image.Image, box, blur: int = 12, alpha: int = 90, ox: int = 6, oy: int = 8) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0 + ox, y0 + oy, x1 + ox, y1 + oy], radius=10, fill=(0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), layer)


def blit_metal(canvas: Image.Image, metal: np.ndarray, box) -> None:
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    crop = metal[y0:y1, x0:x1]
    if crop.size == 0:
        return
    canvas.paste(Image.fromarray(crop.astype(np.uint8), "RGB"), (x0, y0))


def bevel(canvas: Image.Image, box, rim: int, raised: bool) -> None:
    x0, y0, x1, y1 = box
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    lite = (255, 248, 230, 110 if raised else 70)
    dark = (0, 0, 0, 120 if raised else 140)
    if not raised:
        lite, dark = dark, lite
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


def plate(canvas: Image.Image, metal: np.ndarray, box, raised: bool = True, rim: int = 8) -> None:
    canvas_rgba = canvas if canvas.mode == "RGBA" else canvas.convert("RGBA")
    shadowed = shadow_rect(canvas_rgba, box)
    canvas.paste(shadowed, (0, 0))
    blit_metal(canvas, metal, box)
    bevel(canvas, box, rim, raised)


def phosphor(canvas: Image.Image, box) -> None:
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=8, fill=WELL + (255,))
    bevel(canvas, box, 8, raised=False)
    spec = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(spec)
    h = max(4, int((y1 - y0) * 0.18))
    for i in range(h):
        a = int(70 * (1 - i / h))
        sd.rectangle([x0 + 12, y0 + 8 + i, x1 - 12, y0 + 9 + i], fill=(247, 231, 160, a))
    canvas.alpha_composite(spec)


def cream_paper(canvas: Image.Image, box) -> None:
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=6, fill=CREAM + (255,))
    bevel(canvas, box, 6, raised=False)
    gh, gw = max(1, y1 - y0), max(1, x1 - x0)
    grain = np.random.default_rng(11).random((gh, gw))
    arr = np.clip((grain - 0.5) * 22 + 243, 200, 255).astype(np.float32)
    rgb = np.stack([arr * 0.98, arr * 0.96, arr * 0.90], axis=-1).astype(np.uint8)
    canvas.paste(Image.fromarray(rgb, "RGB"), (x0, y0))


def pit_row(canvas: Image.Image, box, n: int = 16) -> None:
    x0, y0, x1, y1 = box
    gap = 6
    usable = (x1 - x0) - gap * (n - 1)
    pw = max(8, usable // n)
    d = ImageDraw.Draw(canvas)
    for i in range(n):
        px = x0 + i * (pw + gap)
        d.rounded_rectangle([px, y0, px + pw, y1], radius=3, fill=(12, 10, 8, 255))


def center_text(d: ImageDraw.ImageDraw, box, text: str, font, fill) -> None:
    x0, y0, x1, y1 = box
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((x0 + x1 - tw) // 2, (y0 + y1 - th) // 2 - bbox[1]), text, font=font, fill=fill)


def wrap(d: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textbbox((0, 0), trial, font=font)[2] <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def draw_lines(d: ImageDraw.ImageDraw, x: int, y: int, lines: list[str], font, fill, gap: int = 8) -> int:
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=font)
        d.text((x, y), line, font=font, fill=fill)
        y += (bbox[3] - bbox[1]) + gap
    return y


def lamp_blank(canvas: Image.Image, box) -> None:
    hi, _ = metals()
    plate(canvas, hi, box, raised=True, rim=7)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    rivet(canvas, cx, cy, r=14)


def send_led(canvas: Image.Image, box) -> None:
    hi, _ = metals()
    plate(canvas, hi, box, raised=True, rim=7)
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 12
    d = ImageDraw.Draw(canvas)
    r = 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 32, 18, 255))
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], fill=GOLD + (255,))
    d.ellipse([cx - 10, cy - 16, cx - 2, cy - 8], fill=(255, 248, 220, 180))
    center_text(d, (x0, cy + 28, x1, y1 - 8), "SEND", SMALL, GOLD + (255,))


def banks(canvas: Image.Image, active: str, boxes: list[tuple], labels: list[str]) -> None:
    hi, lo = metals()
    d = ImageDraw.Draw(canvas)
    for box, lab in zip(boxes, labels):
        on = lab == active
        plate(canvas, lo if on else hi, box, raised=not on, rim=6)
        fill = GOLD + (255,) if on else INK + (255,)
        center_text(d, box, lab, SMALL, fill)


def wait_row(canvas: Image.Image, box, label: str = "WAIT") -> None:
    _, lo = metals()
    plate(canvas, lo, box, raised=True, rim=7)
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    d.text((x0 + 22, y0 + 10), label, font=SMALL, fill=GOLD + (255,))
    pit_row(canvas, (x0 + 22, y0 + 44, x1 - 22, y1 - 18), 16)


def popup_slip(canvas: Image.Image) -> None:
    hi, _ = metals()
    dim = Image.new("RGBA", canvas.size, (10, 10, 12, 140))
    canvas.alpha_composite(dim)
    plate(canvas, hi, SEND_POP if canvas.size[1] == H else L4_POP, raised=True, rim=10)
    box = SEND_POP
    inner = (box[0] + 28, box[1] + 28, box[2] - 28, box[3] - 28)
    cream_paper(canvas, inner)
    d = ImageDraw.Draw(canvas)
    d.text((inner[0] + 24, inner[1] + 28), "PACKING SLIP", font=FONT, fill=INK + (255,))
    d.text((inner[0] + 24, inner[1] + 84), "files only  ·  not the live plan  ·  not Yes", font=SMALL, fill=GRAPHITE + (255,))
    y = inner[1] + 140
    for name in ("CURRENT.md", "PROPOSE-CURRENT.md", "RECEIPT.md"):
        d.rectangle([inner[0] + 24, y, inner[2] - 24, y + 56], outline=GRAPHITE + (255,), width=2)
        d.text((inner[0] + 40, y + 14), name, font=BODY, fill=INK + (255,))
        y += 68
    yesish = (inner[0] + 24, inner[3] - 200, inner[2] - 24, inner[3] - 112)
    noish = (inner[0] + 24, inner[3] - 96, inner[2] - 24, inner[3] - 28)
    d.rounded_rectangle(yesish, radius=8, outline=INK + (255,), width=4)
    center_text(d, yesish, "OFFER FOLDER", FONT, INK + (255,))
    d.rounded_rectangle(noish, radius=8, outline=GRAPHITE + (180,), width=2)
    center_text(d, noish, "not now", BODY, GRAPHITE + (255,))


def well_content(canvas: Image.Image, room: str, box) -> None:
    cream_paper(canvas, box)
    d = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    pad = 28
    if room == "bind":
        face = POSTER if (y1 - y0) > 700 else HUGE
        center_text(d, box, "Name a folder.", face, INK + (255,))
        return
    if room == "plan":
        d.text((x0 + pad, y0 + pad), "THIS IS THE PLAN", font=SMALL, fill=GRAPHITE + (255,))
        y = draw_lines(d, x0 + pad, y0 + 80, wrap(d, "Mechanicall: You Decide — mum stamps, he runs.", FONT, x1 - x0 - 2 * pad), FONT, INK + (255,))
        d.text((x0 + pad, y + 16), "SKU  you-decide-ritual", font=PEEK, fill=GOLD + (255,))
        keys = ["Objective", "Next", "Keep", "Reject", "Limits"]
        hh = (y1 - (y + 70)) // 5
        top = y + 56
        for i, k in enumerate(keys):
            r = (x0 + pad, top + i * hh, x1 - pad, top + (i + 1) * hh - 8)
            d.rectangle(r, outline=GRAPHITE + (160,), width=1)
            d.text((r[0] + 12, r[1] + 10), k, font=SMALL, fill=GRAPHITE + (255,))
        return
    if room == "plan_labour":
        d.text((x0 + pad, y0 + pad), "YOU SAID YES", font=SMALL, fill=GRAPHITE + (255,))
        sku_font = HUGE if (y1 - y0) > 700 else FONT
        y = draw_lines(d, x0 + pad, y0 + 72, wrap(d, "you-decide-ritual", sku_font, x1 - x0 - 2 * pad), sku_font, INK + (255,))
        mid = (y + y1) // 2
        did = (x0 + pad, y + 24, x1 - pad, mid - 8)
        notyet = (x0 + pad, mid + 8, x1 - pad, y1 - pad)
        d.rounded_rectangle(did, radius=10, outline=INK + (255,), width=8)
        center_text(d, did, "I did it", POSTER if (y1 - y0) > 700 else HUGE, INK + (255,))
        d.rounded_rectangle(notyet, radius=10, outline=GRAPHITE + (180,), width=3)
        center_text(d, notyet, "Not yet", HUGE, GRAPHITE + (255,))
        return
    if room == "draft":
        d.text((x0 + pad, y0 + pad), "NOT ACTIVE", font=HUGE, fill=VIOLET + (255,))
        d.text((x0 + pad, y0 + 100), "not the plan  ·  suggestion only", font=SMALL, fill=GRAPHITE + (255,))
        y = y0 + 160
        d.rectangle([x0 + pad, y, x1 - pad, y1 - pad], outline=VIOLET + (180,), width=3)
        d.text((x0 + pad + 16, y + 20), "PROPOSE-CURRENT.md", font=SMALL, fill=VIOLET + (255,))
        draw_lines(d, x0 + pad + 16, y + 64, wrap(d, "Editable draft. Save does not stamp. She has not said yes.", BODY, x1 - x0 - 2 * pad - 32), BODY, INK + (255,))
        return
    if room in ("decide", "decide_send"):
        d.text((x0 + pad, y0 + 20), "You have not said yes yet.", font=BODY, fill=GRAPHITE + (255,))
        d.text((x0 + pad, y0 + 64), "WHY", font=SMALL, fill=GOLD + (255,))
        why_h = 120 if (y1 - y0) > 700 else 100
        d.rectangle([x0 + pad, y0 + 100, x1 - pad, y0 + 100 + why_h], outline=GRAPHITE + (200,), width=2)
        d.text((x0 + pad + 12, y0 + 124), "because this is the plan we can cat", font=BODY, fill=INK + (255,))
        gap = y0 + 100 + why_h + 28
        if (y1 - y0) > 700:
            yes = (x0 + pad, gap, x1 - pad, gap + 280)
            ny = (x0 + pad, gap + 304, x1 - pad, gap + 420)
        else:
            yes = (x0 + pad, gap, x1 - pad, gap + 150)
            ny = (x0 + pad, gap + 168, x1 - pad, min(y1 - pad, gap + 250))
        d.rounded_rectangle(yes, radius=12, outline=INK + (255,), width=8, fill=(230, 193, 74, 255))
        center_text(d, yes, "Yes", POSTER if (y1 - y0) > 700 else HUGE, INK + (255,))
        d.rounded_rectangle(ny, radius=8, outline=GRAPHITE + (160,), width=3)
        center_text(d, ny, "Not yet", HUGE, GRAPHITE + (255,))
        return
    if room == "receipt":
        d.text((x0 + pad, y0 + pad), "RECEIPT", font=SMALL, fill=GRAPHITE + (255,))
        lines = [
            "when   2026-09-08",
            "you said   Yes",
            "Next    you-decide-ritual",
            "what happened",
            "(empty receipt)",
        ]
        draw_lines(d, x0 + pad, y0 + 90, lines, PEEK, INK + (255,), gap=18)
        return
    if room == "splash":
        center_text(d, box, "MECHANICALL", HUGE, GOLD + (255,))


def l1(room: str) -> Image.Image:
    hi, lo = metals()
    canvas = Image.fromarray(hi.astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    canvas.paste(tuple(HOST) + (255,), [0, 0, W, H])
    blit_metal(canvas, lo, (0, 0, W, H))
    plate(canvas, hi, TITLE, True, 9)
    rivet(canvas, TITLE[0] + 28, (TITLE[1] + TITLE[3]) // 2)
    rivet(canvas, TITLE[2] - 28, (TITLE[1] + TITLE[3]) // 2)
    center_text(d, TITLE, "MECHANICALL", FONT, GOLD + (255,))
    plate(canvas, lo, LCD, True, 8)
    phosphor(canvas, GLASS)
    peek = {
        "splash": "power on",
        "bind": "Name a folder.",
        "plan": "This is the plan.  you-decide-ritual",
        "plan_labour": "you-decide-ritual",
        "draft": "NOT ACTIVE",
        "decide": "Why. Then Yes.",
        "decide_send": "Why. Then Yes.",
        "receipt": "(empty receipt)",
    }.get(room, "")
    fill = VIOLET + (255,) if room == "draft" else GOLD + (255,)
    center_text(d, GLASS, peek, PEEK, fill)
    if room != "splash":
        lamp_blank(canvas, JOIN)
        send_led(canvas, SEND)
        lamp_blank(canvas, WAKE)
        active = {
            "plan": "PLAN",
            "plan_labour": "PLAN",
            "draft": "DRAFT",
            "decide": "DECIDE",
            "decide_send": "DECIDE",
            "receipt": "RECEIPT",
            "bind": "PLAN",
        }.get(room, "PLAN")
        banks(canvas, active, [BANK_PLAN, BANK_DRAFT, BANK_DECIDE, BANK_RECEIPT], ["PLAN", "DRAFT", "DECIDE", "RECEIPT"])
        well_content(canvas, room if room != "decide_send" else "decide", WELL_BOX)
        wait_row(canvas, GATE, "WAIT")
    else:
        well_content(canvas, "splash", WELL_BOX)
    if room == "decide_send":
        popup_slip(canvas)
    return canvas


def l4(room: str) -> Image.Image:
    hi, lo = metals()
    canvas = Image.fromarray(hi.astype(np.uint8), "RGB").convert("RGBA")
    canvas.paste(tuple(HOST) + (255,), [0, 0, W, H])
    blit_metal(canvas, hi, (0, 0, W, H))
    d = ImageDraw.Draw(canvas)
    plate(canvas, lo, L4_TITLE, True, 9)
    rivet(canvas, L4_TITLE[0] + 28, (L4_TITLE[1] + L4_TITLE[3]) // 2)
    rivet(canvas, L4_TITLE[2] - 28, (L4_TITLE[1] + L4_TITLE[3]) // 2)
    house = "sitrae" if room != "bind" else ""
    label = "MECHANICALL" + (f"   {house}" if house else "")
    center_text(d, L4_TITLE, label, FONT, GOLD + (255,))
    plate(canvas, lo, L4_PEEK, True, 8)
    phosphor(canvas, (L4_PEEK[0] + 16, L4_PEEK[1] + 16, L4_PEEK[2] - 16, L4_PEEK[3] - 16))
    peek = {
        "splash": "You Decide",
        "bind": "Name a folder.",
        "plan": "This is the plan.",
        "plan_labour": "you-decide-ritual",
        "draft": "NOT ACTIVE",
        "decide": "Nothing changes until you decide",
        "decide_send": "Nothing changes until you decide",
        "receipt": "(empty receipt)",
    }.get(room, "")
    fill = VIOLET + (255,) if room == "draft" else GOLD + (255,)
    center_text(d, L4_PEEK, peek, PEEK, fill)
    if room != "splash":
        bw = (L4_BANKS[2] - L4_BANKS[0] - 36) // 4
        by0, by1 = L4_BANKS[1], L4_BANKS[3]
        boxes = []
        for i in range(4):
            x0 = L4_BANKS[0] + 6 + i * (bw + 12)
            boxes.append((x0, by0, x0 + bw, by1))
        active = {
            "plan": "PLAN",
            "plan_labour": "PLAN",
            "draft": "DRAFT",
            "decide": "DECIDE",
            "decide_send": "DECIDE",
            "receipt": "RECEIPT",
            "bind": "PLAN",
        }.get(room, "PLAN")
        banks(canvas, active, boxes, ["PLAN", "DRAFT", "DECIDE", "RECEIPT"])
        plate(canvas, hi, L4_PAPER, True, 10)
        inner = (L4_PAPER[0] + 20, L4_PAPER[1] + 20, L4_PAPER[2] - 20, L4_PAPER[3] - 20)
        well_content(canvas, room if room != "decide_send" else "decide", inner)
        wait_row(canvas, L4_WAIT, "WAIT")
    else:
        plate(canvas, hi, L4_PAPER, True, 10)
        well_content(canvas, "splash", (L4_PAPER[0] + 20, L4_PAPER[1] + 20, L4_PAPER[2] - 20, L4_PAPER[3] - 20))
        gears = ImageDraw.Draw(canvas)
        for cx, cy, r in ((280, 900, 90), (800, 1100, 120), (540, 1500, 70)):
            gears.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD + (180,), width=6)
            rivet(canvas, cx, cy, 12)
    if room == "decide_send":
        # L4 popup uses L4_POP coords via a local overlay
        dim = Image.new("RGBA", canvas.size, (10, 10, 12, 140))
        canvas.alpha_composite(dim)
        plate(canvas, hi, L4_POP, True, 10)
        inner = (L4_POP[0] + 28, L4_POP[1] + 28, L4_POP[2] - 28, L4_POP[3] - 28)
        cream_paper(canvas, inner)
        dd = ImageDraw.Draw(canvas)
        dd.text((inner[0] + 24, inner[1] + 28), "PACKING SLIP", font=FONT, fill=INK + (255,))
        dd.text((inner[0] + 24, inner[1] + 84), "files only  ·  not Yes  ·  optional", font=SMALL, fill=GRAPHITE + (255,))
        y = inner[1] + 150
        for name in ("CURRENT.md", "PROPOSE-CURRENT.md", "RECEIPT.md"):
            dd.rectangle([inner[0] + 24, y, inner[2] - 24, y + 56], outline=GRAPHITE + (255,), width=2)
            dd.text((inner[0] + 40, y + 14), name, font=BODY, fill=INK + (255,))
            y += 68
        offer = (inner[0] + 24, inner[3] - 200, inner[2] - 24, inner[3] - 112)
        dismiss = (inner[0] + 24, inner[3] - 96, inner[2] - 24, inner[3] - 28)
        dd.rounded_rectangle(offer, radius=8, outline=INK + (255,), width=4)
        center_text(dd, offer, "OFFER FOLDER", FONT, INK + (255,))
        dd.rounded_rectangle(dismiss, radius=8, outline=GRAPHITE + (180,), width=2)
        center_text(dd, dismiss, "not now", BODY, GRAPHITE + (255,))
    return canvas


ROOMS = ("splash", "bind", "plan", "draft", "decide", "decide_send", "plan_labour", "receipt")


def main() -> None:
    PREV.mkdir(parents=True, exist_ok=True)
    written = []
    for room in ROOMS:
        a = l1(room).convert("RGB")
        b = l4(room).convert("RGB")
        pa = PREV / f"l1-{room}.png"
        pb = PREV / f"l4-{room}.png"
        a.save(pa, "PNG", optimize=True)
        b.save(pb, "PNG", optimize=True)
        written.append(pa)
        written.append(pb)
        print(f"wrote {pa.name} {pb.name}")
    LAYOUT.write_text(
        f"""# SKIN-LAYOUT — interaction previews {W}x{H}

**Not nodpi. Not Yes.** L=1 freeze slots (SitCRects) + L=4 no-freeze pack.
Quiet Next room recanted. After Yes = `plan_labour` on PLAN well.
S=1 = `decide_send` packing-slip popup.

## L1 freeze (SitCRects)

| plate | l t r b |
|-------|---------|
| title | {TITLE} |
| lcd | {LCD} |
| glass | {GLASS} |
| join blank | {JOIN} |
| send LED | {SEND} |
| wake blank | {WAKE} |
| bank PLAN | {BANK_PLAN} |
| bank DRAFT | {BANK_DRAFT} |
| bank DECIDE | {BANK_DECIDE} |
| bank RECEIPT | {BANK_RECEIPT} |
| well | {WELL_BOX} |
| wait | {GATE} |
| send popup | {SEND_POP} |

No NEXT bank. `didIt` / `notYetFeet` occupy the well on **plan_labour** only.

## L4 no-freeze

| plate | l t r b |
|-------|---------|
| title | {L4_TITLE} |
| peek | {L4_PEEK} |
| banks | {L4_BANKS} |
| paper | {L4_PAPER} |
| wait | {L4_WAIT} |
| send popup | {L4_POP} |

Files: `preview/l1-*.png` `preview/l4-*.png`
""",
        encoding="utf-8",
    )
    print(f"wrote {len(written)} pngs → {PREV}")


if __name__ == "__main__":
    main()
