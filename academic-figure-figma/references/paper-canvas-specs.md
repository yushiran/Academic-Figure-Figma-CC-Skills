# Paper-accurate canvas specs — widths and fonts by venue

Create the Figma artboard at the figure's true print width in **pt** (1 Figma px =
1 pt) and set text sizes directly — the only way font sizes stay honest.

**Ground truth is the venue's class file, not this table.** Verify in one compile:

```latex
textwidth=\the\textwidth, columnwidth=\the\columnwidth   % put in the doc body
```

Values marked ≈ are from memory/official artwork guides; measure before finalising.

## Conference templates

| Venue | Layout | Column (`figure`) | Full width (`figure*`) |
|---|---|---|---|
| NeurIPS / ICLR | single column | — | 5.5 in = **397 pt** |
| ICML | two column | 3.25 in = **234 pt** | 6.75 in = **486 pt** |
| AAAI | two column | 3.3125 in = **239 pt** | 7.0 in = **504 pt** |
| IJCAI | two column | ≈ 234 pt | ≈ 486 pt |
| CVPR / ICCV / WACV | two column | ≈ **237 pt** | 6.875 in = **497 pt** |
| ECCV (LNCS) | single column | — | 12.2 cm = **347 pt** |
| ACL / EMNLP / NAACL | two column | ≈ 226 pt | 6.5 in = **470 pt** |
| IEEE conf (ICASSP, ICME, …) | two column | 3.5 in = **252 pt** | 7.16 in = **516 pt** |
| Interspeech | two column | ≈ 227 pt | ≈ 482 pt |

## Journal / publisher artwork rules

| Publisher | Sizes (official artwork guides) |
|---|---|
| IEEE journals (IEEEtran: TIP, TASLP, TPAMI…) | column **252 pt**, full **516 pt** — same as IEEE conf |
| Elsevier (Pattern Recognition, Neurocomputing…) | single 90 mm = **255 pt** · 1.5-col 140 mm = **397 pt** · full 190 mm = **539 pt** |
| Springer LNCS | text width 12.2 cm = **347 pt** |
| Springer journals (IJCV, MVAP…) | varies by class — measure with `\the\textwidth` |
| Nature family | single 89 mm = **252 pt** · double 183 mm = **519 pt** |

If the venue may change (e.g. drafting in IEEEtran, submitting to Elsevier), design at
the **narrower** target so text never falls below floor when reflowed. Elsevier
review-format PDFs are single-column ~390 pt wide — a 516 pt figure gets scaled 0.76×.

## Font rules

| Context | Family | In-figure text size (final) |
|---|---|---|
| IEEE | Times (serif) or Helvetica/Arial | ≈8 pt labels, **floor 6 pt** |
| Elsevier | Arial/Helvetica or Times | ≈7-11 pt, uniform across the figure |
| Nature family | sans (Arial/Helvetica) | ≈5-7 pt, min 5 pt |
| ML/CV/NLP confs | no hard rule; match caption family | convention: **≥6-7 pt**, caption is 9-10 pt |

- Figma has no Times New Roman → use **Tinos** (metric-compatible, available by
  default); Noto Serif as fallback. Helvetica venues → Inter or Roboto.
- Converting Inter→Tinos: add ≈0.4 pt (Tinos runs visually smaller).
- Load every family+style via `loadFontAsync` before any text op. Inter's style
  names contain spaces ("Semi Bold").
- Discipline: 1-2 sizes per figure plus a title size; bold only for hierarchy.

## Working ramp that renders well at 516 pt full width

panel titles 9-9.5 bold · stage headers 6.8-7.5 bold · chip titles 6.2-6.6 ·
body 5.4-5.8 · annotations 4.6-5.2 (sparingly; below most floors — keep to tags the
reader can skip). At 252 pt column width, halve the content, not the fonts.

**Never draw oversized then shrink**: a 1540 px mock at 13 px text compressed to
516 pt ends at 4.4 pt — unreadable. Split the figure or cut text instead.

## Layout numbers that survive review

- Full-width pipeline figures: H/W ≈ 0.4-0.8.
- Palette + stroke weights: see PAL in `scripts/figma_lib.js` (low-saturation
  line/fill pairs, strokes 0.6-0.9 pt, corner radius 3-4).
- Panel dividers 0.7 pt dashed [3,3]; arrows 0.9-1 pt shaft + 3.6×4.6 pt head.
