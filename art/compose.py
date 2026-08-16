#!/usr/bin/env python3
"""Compose the YoriMusic branded assets.

Takes the hand-drawn-style, text-free anime base art in art/ and overlays the
"YoriMusic" wordmark using the fonts already bundled with the bot
(yori/helpers/Raleway-Bold.ttf and Inter-Light.ttf), so the typography in the
artwork matches the typography the bot renders on song thumbnails.

The art style is 1990s cel-animation: flat two-tone shading, hand-inked line
work, muted film palette. The lettering is therefore kept FLAT too — an
off-white ink colour with a soft drop shadow for legibility, plus a shared
film-grain pass over the whole frame so the type sits inside the picture
instead of floating on top of it. No neon glow: that would read as digital and
fight the artwork.

Usage:  python3 art/compose.py
Writes: assets/logo.png, assets/avatar.png,
        assets/start.jpg, assets/ping.jpg, assets/thumb.jpg
"""

from __future__ import annotations

import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "art")
ASSETS = os.path.join(ROOT, "assets")

BOLD = os.path.join(ROOT, "yori", "helpers", "Raleway-Bold.ttf")
LIGHT = os.path.join(ROOT, "yori", "helpers", "Inter-Light.ttf")

BANNER = (1376, 768)

# Muted cel-animation palette, sampled to match the base art.
INK_LIGHT = (238, 234, 244)   # off-white title ink
INK_SUB = (198, 191, 214)     # dimmer subtitle ink
SHADOW = (10, 8, 20)


def fit_font(path: str, text: str, max_width: int, start_size: int) -> ImageFont.FreeTypeFont:
    """Shrink the font until `text` fits inside `max_width`."""
    size = start_size
    while size > 10:
        font = ImageFont.truetype(path, size)
        box = font.getbbox(text)
        if box[2] - box[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(path, size)


def draw_text(
    size: tuple[int, int],
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    anchor: str = "la",
    shadow_offset: int = 3,
    shadow_blur: int = 9,
    shadow_alpha: int = 190,
) -> Image.Image:
    """Flat text with a soft drop shadow (no glow — keeps the cel look)."""
    shadow_layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow_layer).text(
        (xy[0] + shadow_offset, xy[1] + shadow_offset),
        text, font=font, fill=SHADOW + (shadow_alpha,), anchor=anchor,
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

    body = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(body).text(xy, text, font=font, fill=fill + (255,), anchor=anchor)

    return Image.alpha_composite(shadow_layer, body)


def scrim(size, box, opacity=120, blur=70):
    """Very soft dark panel so text stays readable over painted background."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=48, fill=SHADOW + (opacity,))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def film_grain(size, amount=9, seed=7):
    """Monochrome grain matching the 35mm-scan look of the base art."""
    rnd = random.Random(seed)
    w, h = size
    small = Image.new("L", (w // 2, h // 2))
    small.putdata([128 + rnd.randint(-amount, amount) for _ in range(small.size[0] * small.size[1])])
    grain = small.resize(size, Image.BILINEAR)
    return grain


def apply_grain(img: Image.Image, seed=7) -> Image.Image:
    """Overlay-blend grain across the finished frame, type included."""
    grain = film_grain(img.size, seed=seed).convert("RGB")
    return Image.blend(img, Image.composite(img, grain, Image.new("L", img.size, 205)), 0.35)


def load_base(name: str, size: tuple[int, int] | None = None) -> Image.Image:
    img = Image.open(os.path.join(ART, name)).convert("RGB")
    if size and img.size != size:
        # normalise slight aspect drift from the generator
        img = img.resize(size, Image.LANCZOS)
    return img


def build_banner(src, dst, title, subtitle, seed=7, quality=90):
    base = load_base(src, BANNER).convert("RGBA")
    w, h = base.size

    title_font = fit_font(BOLD, title, int(w * 0.44), 96)
    sub_font = fit_font(LIGHT, subtitle, int(w * 0.44), 38)

    x, y = int(w * 0.07), int(h * 0.37)

    base = Image.alpha_composite(
        base, scrim((w, h), (x - 70, y - 80, x + int(w * 0.50), y + 175))
    )
    base = Image.alpha_composite(
        base, draw_text((w, h), (x, y), title, title_font, INK_LIGHT)
    )
    base = Image.alpha_composite(
        base,
        draw_text(
            (w, h), (x + 3, y + int(title_font.size * 1.25)), subtitle, sub_font,
            INK_SUB, shadow_offset=2, shadow_blur=6, shadow_alpha=160,
        ),
    )

    out = apply_grain(base.convert("RGB"), seed=seed)
    out.save(dst, quality=quality, optimize=True)
    print(f"wrote {dst}")


def build_logo(src, dst_logo, dst_avatar):
    base = load_base(src).convert("RGBA")
    w, h = base.size

    title = "YoriMusic"
    title_font = fit_font(BOLD, title, int(w * 0.80), 120)
    sub_font = fit_font(LIGHT, "TELEGRAM MUSIC BOT", int(w * 0.58), 28)

    y = int(h * 0.855)

    logo = Image.alpha_composite(
        base, scrim((w, h), (-50, y - 105, w + 50, h + 50), opacity=150, blur=60)
    )
    logo = Image.alpha_composite(
        logo, draw_text((w, h), (w // 2, y), title, title_font, INK_LIGHT, anchor="mm")
    )
    logo = Image.alpha_composite(
        logo,
        draw_text(
            (w, h), (w // 2, y + 70), "TELEGRAM MUSIC BOT", sub_font, INK_SUB,
            anchor="mm", shadow_offset=2, shadow_blur=5, shadow_alpha=150,
        ),
    )
    apply_grain(logo.convert("RGB"), seed=3).save(dst_logo, optimize=True)
    print(f"wrote {dst_logo}")

    # Text-free avatar: Telegram renders profile photos small, so a wordmark
    # would turn to mush. Crop tight on the face, drop the reserved text band.
    crop = base.convert("RGB").crop((int(w * 0.04), int(h * 0.01), int(w * 0.96), int(h * 0.80)))
    s = min(crop.size)
    cw, _ = crop.size
    crop = crop.crop(((cw - s) // 2, 0, (cw - s) // 2 + s, s))
    avatar = apply_grain(crop.resize((512, 512), Image.LANCZOS), seed=11)
    avatar.save(dst_avatar, optimize=True)
    print(f"wrote {dst_avatar}")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    build_logo(
        "n_logo.jpg",
        os.path.join(ASSETS, "logo.png"),
        os.path.join(ASSETS, "avatar.png"),
    )
    build_banner("n_start.jpg", os.path.join(ASSETS, "start.jpg"),
                 "YoriMusic", "Advanced Telegram Music Bot", seed=5)
    build_banner("n_ping.jpg", os.path.join(ASSETS, "ping.jpg"),
                 "YoriMusic", "System Status", seed=13)
    build_banner("n_thumb.jpg", os.path.join(ASSETS, "thumb.jpg"),
                 "YoriMusic", "Now Playing", seed=21)


if __name__ == "__main__":
    main()
