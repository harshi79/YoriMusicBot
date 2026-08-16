# Artwork sources

This folder holds the **source art** for the branded assets in [`../assets`](../assets).
It is not used at runtime — the bot only reads `assets/`.

## Style

YoriMusic's mascot is a girl music fan drawn in a **1990s cel-animation** style:
hand-inked linework with varying line weight, strictly flat two-tone shading,
hand-painted gouache backgrounds and 35mm film grain. Muted and desaturated, in
the spirit of Satoshi Kon / Studio Ghibli background art.

Deliberately avoided, because they are what make art read as machine-made:
digital airbrushing, glossy skin, neon glow and lens bloom, bokeh orb fields,
sparkle particles, and perfectly symmetric front-facing "doll" poses.

Palette:

| Role | Hex |
| --- | --- |
| Deep indigo (background) | `#1b1a33` |
| Dusty violet | `#5b4a72` |
| Muted teal (hair tips) | `#7ba8a8` |
| Warm amber (lamp/window light) | `#d99b4a` |
| Off-white ink (type) | `#eeeaf4` |

## Files

| File | Purpose |
| --- | --- |
| `ref2.jpg` | Character reference sheet — pass this to an image model to keep the mascot consistent when generating new art |
| `n_start.jpg` | Rooftop at dusk, text-free base for `assets/start.jpg` |
| `n_ping.jpg` | Desk with mixing console, text-free base for `assets/ping.jpg` |
| `n_thumb.jpg` | Listening in moonlight, text-free base for `assets/thumb.jpg` |
| `n_logo.jpg` | Square portrait, text-free base for `assets/logo.png` and `assets/avatar.png` |
| `compose.py` | Overlays the wordmark onto the bases and writes `assets/` |

The base images are generated **without any text**. The "YoriMusic" wordmark is
composited afterwards by `compose.py` using the fonts already bundled with the bot
(`yori/helpers/Raleway-Bold.ttf` and `Inter-Light.ttf`), so the branding typography
matches the text the bot renders onto song thumbnails at runtime — and so the
lettering is always crisp rather than AI-garbled.

To suit the cel style the type is **flat off-white ink with a soft drop shadow**,
not neon. A shared film-grain pass runs over each finished frame, type included,
so the lettering sits inside the picture instead of floating on top of it.

> When prompting for new base art, always exclude signage: background posters and
> labels are where image models produce garbled fake lettering.

## Regenerating

```bash
pip install pillow
python3 art/compose.py
```

To restyle: regenerate the four `n_*.jpg` bases in a new style (keeping the
left / bottom-fifth negative space free for text), then re-run `compose.py`.
