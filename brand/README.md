# XMAI logo

The mark is a 2×2 block of the letters X M A I. Three closed cells are the model; the X cell is lifted out of its slot: the part of the model we open and explain.

## Files

| Use | File |
|---|---|
| GitHub / Slack / Zoom avatar | `png/xmai-avatar-500.png` (dark: `png/xmai-avatar-dark-500.png`) |
| Slides and posters, light background | `svg/xmai-wordmark-light.svg` or `svg/xmai-mark-light.svg` |
| Dark background | `svg/xmai-wordmark-dark.svg`, `svg/xmai-mark-dark.svg` |
| One colour (print, stamps, embossing) | `svg/*-mono-black.svg`, `svg/*-mono-white.svg` |
| Square avatar as vector | `svg/xmai-avatar.svg`, `svg/xmai-avatar-dark.svg` |

All SVGs have the letters converted to outlines: no font needed. In the closed cells the letters are cut out, so the background shows through.

## Colours

| Token | Light | Dark |
|---|---|---|
| Ink | `#13283D` | `#E8EEF4` |
| Accent | `#0B8F8A` | `#3CC4BD` |
| Ground | `#FFFFFF` | `#121A22` |

Type: Space Grotesk Bold (letters, name), Inter Medium (tagline). Both under the SIL Open Font License.

## Rules

- Keep clear space around the mark of at least one cell gutter on every side.
- Do not recolour single cells, stretch the block or move the X cell elsewhere.
- Below 32 px the dashed slot fades; use the mark as it is, do not draw a simplified version.

## Regenerating

`tools/make_logo.py` builds every SVG from the geometry and the two fonts (variable TTFs from google/fonts):

```bash
python -I tools/make_logo.py <dir with SpaceGrotesk.ttf and Inter.ttf> svg/
```

Needs `fonttools`. PNGs are exported from the SVGs in a browser at 500 px.
