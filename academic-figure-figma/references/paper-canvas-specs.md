# Paper-accurate canvas specs

Create the Figma artboard at the figure's true print width in **pt** (1 Figma px = 1 pt
here) and set text sizes directly. This is the only way font sizes stay honest.

## Widths by LaTeX class

| Class | Figure env | Print width | Figma artboard |
|---|---|---|---|
| IEEEtran (two-column: TIP/TASLP/conf) | `\begin{figure}` (one column) | 3.5 in = 252 pt | 252 × H |
| IEEEtran | `\begin{figure*}` (full width) | 7.16 in = 516 pt | 516 × H |
| elsarticle (Elsevier single-column review format, e.g. Pattern Recognition) | `\begin{figure}` | ~5.4 in ≈ 390 pt | 390 × H |
| AAAI two-column | `figure` / `figure*` | 3.3125 in = 239 pt / 7.0 in = 504 pt | 239 / 504 × H |

If the venue may change (e.g. drafting in IEEEtran but submitting to Elsevier), design
at the **narrower** target so text never shrinks below floor when reflowed.

## Font floors and sizes that work at 516 pt

- Absolute floor for any visible text: **6 pt** at final size. IEEE recommends ~8 pt
  for labels; 4.5 pt is unreadable in print.
- Working ramp that renders well in a 516 pt full-width figure:
  panel titles 9-9.5 bold · stage headers 6.8-7.5 bold · chip titles 6.2-6.6 ·
  body 5.4-5.8 · annotations/tags 4.6-5.2 (use sparingly).
- Never draw oversized then shrink: a 1540 px reference mock at ~13 px text compressed
  to 516 pt ends at 4.4 pt. If a reference image is dense, either split it into two
  figures or cut text per box — do not scale it down.

## Fonts

- Figma has no Times New Roman. Use **Tinos** (metric-compatible Times clone, on Figma
  by default) for Times-style venues; Noto Serif as fallback.
- Helvetica-style venues: Inter or Roboto (metrically close enough for figures).
- Convert Inter→Tinos at +0.4 pt: Tinos runs visually smaller at equal point size.
- Load every family+style with `figma.loadFontAsync` before ANY text mutation.
  Note style-name traps: Inter's semi-bold is "Semi Bold" (with space).

## Layout numbers that survive review

- Aspect ratio for a full-width pipeline figure: H/W ≈ 0.4-0.8. Taller than 0.8 starts
  eating a second column of page space.
- Low-saturation academic palette (line / fill pairs, one hue per stage):
  amber `#D98D0D / #FEF6DE`, blue `#3373D9 / #E5F0FD`, orange `#DE5C1A / #FEF0E0`,
  green `#1A8C4D / #E5F7EB`, purple `#7340CC / #F0EBFD`, ink `#212226`,
  muted text `#6B7280`. Strokes 0.6-0.9 pt, corner radius 3-4.
- Panel dividers: 0.7 pt dashed `[3,3]` grey.
- Arrows: shaft 0.9-1 pt + polygon head ~3.6×4.6 pt; colour by flow type; legend
  bottom-left.
