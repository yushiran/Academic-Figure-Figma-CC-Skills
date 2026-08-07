# Figure style presets and palette construction

Recognizable academic figure styles come from three sources: (1) **journal art
desks** — Nature redraws accepted figures to house style, so its flat, sparse
look is enforced editorially; (2) **tool defaults that hardened into
conventions** — matplotlib `tab10` and seaborn `deep`/`muted` read as "a
standard results plot" purely because they are defaults; (3) **community
imitation** — the pastel-block architecture style spread by ML authors copying
landmark figures (the *Attention Is All You Need* diagram has no published
palette; its look is transmitted by imitation only). This skill therefore
encodes *derivation rules* plus a few anchored presets, not one fixed list.

## Named style presets

Stroke/fill pairs for a 3-stage pipeline (data / model / output). Sources
in-line; pairs marked **derived** come from the rules below.

| Style | Look | Typical venues | data · model · output (stroke/fill) |
|---|---|---|---|
| Nature–Science editorial | Flat mid-tone fills, hairline `#333333` or no stroke, Helvetica/Arial 5–7 pt, generous whitespace | Nature, Science, Cell, biomedical | Okabe-Ito fills, hairline strokes: `#333333`/`#56B4E9` · `#333333`/`#009E73` · `#333333`/`#E69F00` |
| IEEE engineering wireframe | White fills, solid dark borders, black text; colour never the sole encoder (must survive B/W) | IEEE Transactions, signal processing, comms | `#000000`/`#FFFFFF` × 3; optional accent stroke `#1F77B4` (tab10 blue) on the model stage |
| ML pastel-block (Transformer-style) | Rounded rects, pale fills + mid-saturation same-hue borders, near-black text, thin black arrows | NeurIPS, ICML, ICLR, CVPR, ACL method figures | `#66C2A5`/`#B3E2CD` · `#FC8D62`/`#FDCDAC` · `#8DA0CB`/`#CBD5E8` (ColorBrewer Set2 strokes + Pastel2 fills) |
| seaborn/matplotlib plot family | Saturated lines/markers on white, no fills; the de-facto results-section look | All CS/ML venues (plots, not diagrams) | `#4C72B0`/`#A1C9F4` · `#DD8452`/`#FFB482` · `#55A868`/`#8DE5A1` (seaborn `deep` strokes + `pastel` fills) |
| Paul Tol muted | Slightly desaturated CVD-safe hues; pale scheme for fills, dark scheme for coloured text | Physics, astronomy, climate | `#222255`/`#BBCCEE` · `#225522`/`#CCDDAA` · `#663333`/`#FFCCCC` (Tol `dark` strokes + position-matched `pale` fills) |
| Morandi muted pastel | Grey-tinted low-saturation fills, low-contrast strokes, soft editorial feel | Posters, slides, HCI-adjacent; risky for print-critical journals | **derived**: `#60809F`/`#CED6DE` · `#A67359`/`#E2D6CF` · `#669966`/`#CFDECF` |

## Palette construction rules

- **Derive fills from strokes, not independently.** Keep the stroke's hue
  within ±10°; fill at HSL S 20–60 %, L 78–90 % — the range the documented
  pale companions actually occupy (Pastel2 vs Set2, seaborn `pastel` vs
  `deep`, Tol `pale` vs `dark`). Strokes: S 40–60 %, L 40–60 % for borders;
  L 20–40 % for text-grade colour.
- **Text and arrows stay near-black** (`#000000`–`#333333`) on white.
  Coloured text only from a text-grade dark scheme. Do not colour arrows
  semantically unless data flow itself is the semantic being encoded.
- **Cap semantic hues at 3–4 per figure.** One hue per pipeline stage or
  component ROLE, reused exactly for every box of that role — never one hue
  per box. Grey is free and does not count (Set2 grey `#B3B3B3`, Tol pale
  grey `#DDDDDD` for auxiliary/frozen blocks).
- **Space luminance so the figure survives grayscale**: any two colours that
  must stay distinguishable in B/W need a lightness gap of ≥20 HSL-L points.
  Verify by full desaturation (Nature's own recommended check). Note: muted
  Morandi-type palettes inherently compress this gap — that is their cost.
- **Colourblind safety.** Avoid red↔green pairs and red-on-black (Nature
  warns against both; rainbow maps disallowed). Safe axes: blue↔orange,
  blue↔yellow, purple↔green. CVD-safe-by-design sets: Okabe-Ito
  (`#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000`, Wong
  *Nat. Methods* 2011) or Tol `bright`/`vibrant`/`muted`. Simulate
  deuteranopia before finalizing.
- **Journal hard numbers.** Nature: sRGB, 90/180 mm widths, Arial/Helvetica
  5–7 pt, vector line art. IEEE: 3.5 in / 7.16 in, ≥300 dpi, figures must
  read in B/W, encode with shape as well as colour. Elsevier: RGB preferred,
  300/500/1000 dpi (halftone/combination/line) at final size. Design in RGB.

## Choosing a style

- **Biomedical / Nature-family** → Nature–Science editorial; Okabe-Ito hues
  only, sans-serif, no decorative borders.
- **IEEE / engineering** → wireframe; assume B/W print, line style + shape
  redundant with colour, at most one accent hue.
- **ML conference method figure** → ML pastel-block (Set2/Pastel2); keep
  result-plot colours hue-consistent with the diagram's stage colours.
- **Physics / astronomy / climate** → Tol muted; fills and text colours come
  pre-paired and CVD-safe.
- **Unknown venue or accessibility-critical** → Okabe-Ito strokes with
  rule-derived fills; the only palette a major journal names by
  recommendation.

## Applying a style in Figma (canvas-proven workflow)

1. **Sampler board first, never serial repaints.** Draw one `PALETTE ·
   candidates` frame: one row per candidate style, each row three mini-boxes
   (stage label + hex caption) using that style's stroke/fill pairs. The user
   or group circles a row; a screenshot of the board is also a shareable
   artefact for co-author votes.
2. **Recolour by hex map.** Style switches are a single pass: build
   `MAP = {oldStroke: newStroke, oldFill: newFill, ...}`, walk
   `findAll(() => true)`, and swap any SOLID stroke/fill whose hex is in the
   map (icons recolour with their box; brand logos may be left out of the
   map deliberately). Keep every applied map in the session so any style is
   one inverse map away — reverts are free.
3. **Stage semantics survive restyling.** The map only changes colour VALUES;
   the role→colour assignment (rule: one hue per stage) is decided once and
   re-expressed in every style.

Sources: Nature formatting guide + "Still too many red–green figures"
(*Nature* 510, 340); Wong *Nat. Methods* 8:441 (2011); Tol SRON/EPS/TN/09-002;
matplotlib colour docs; seaborn `palettes.py`; ColorBrewer `colorbrewer.json`;
IEEE Author Center graphics requirements; Elsevier artwork instructions.
