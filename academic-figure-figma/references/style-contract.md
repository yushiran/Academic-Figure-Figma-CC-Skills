# Style contract for a single-column method figure

This file is the answer to "it looks AI-made, plastic". It was not written from taste. Twelve
agents measured five recent He Kaiming figures at 300 dpi and the component colours of DAPS,
RAM and DAVI, and the numbers below are what the accepted figures actually do. Follow it as a
spec, not as inspiration: every rule is a hex, a point size or a count.

Load this at Step 0 alongside figure-grammar.md, and run its checks at Step 4: one prose size,
three stroke weights, no stroked fill on white, ink inside [19, 217] of a 236 pt frame, at most
two tinted blocks, at most three accent marks.

## The 236 pt method-figure contract

Distilled from measured studies of five flagship figures at this exact size — *Generative Modeling via Drifting* (Figs 1-3), *Improved Mean Flows* (Figs 1, 2, 5), *Back to Basics / JiT* (Figs 1, 3, CVPR 2026), *Bidirectional Normalizing Flow* (Figs 1, 3, 4, CVPR 2026 spotlight), *ARC Is a Vision Problem!* (Figs 1, 3, 5, CVPR 2026). Every number below was read off a 300 dpi page render or the PDF's own drawing operators, not estimated. Where the five disagreed, the resolution is stated inline.

### Frame and budget
- Frame **236 pt** wide. **Ink spans x = 19 to x = 217 (198 pt).** Never stretch to the measure. *(Contested: measured ink runs 60-98 % of the column across nine figures; resolved to ARC's single-column method figure, 198.7 pt ink with 19.0 / 18.5 pt gutters, which is the closest analogue and the median.)*
- Height is whatever the content needs: **88-104 pt for a band**, up to 175 pt only for a true vertical architecture.
- **Paper >= 50 %** of the frame. **Hard black ink <= 3 %. Saturated accent <= 2 %.**
- **9.0 pt** from the lowest ink to the caption. The caption is the only place a **bold** word exists.

### Palette — thirteen values, no fourteenth
| hex | L* | role |
|---|---|---|
| `#FFFFFF` | 100 | paper; also the only occluder |
| `#000000` | 0 | claim ink: labels, claim arrows, every filled head, the sum node |
| `#6C6D70` | 46 | structural connectors, ticks, route labels |
| `#929497` | 61 | **type inside frozen machinery** — grey the words, not just the box |
| `#919191` | 60 | the given / baseline lane in a two-lane comparison |
| `#B4B5B8` | 74 | 0.3 pt raster-panel frames; open-barb plumbing arrows |
| `#E6E7E8` | 92 | frozen container fill |
| `#D1D1D3` | 84 | block inside a frozen container; dashed-border colour |
| `#EAEAEB` | 93 | a region that carries no gradient |
| `#C7EAF5` | 91 | **THE claim tint** — at most two blocks, always the controller |
| `#FAAF40` | 77 | accent: 4.0 pt discs, <= 3 of them |
| `#2F9FEA` | 63 | loss arrows only, never a fill |
| `#E0EED4` / `#FCE9F2` | 93 / 94 | optional: an output/loss, or an arm the method deletes |

No fill below **L\* 83**. No saturated fill, ever. One concept, one hue, held across every figure in the paper and across the results plots.

### Type
The two faces are fixed (2026-09-16, from the fonts embedded in MoCo, Mask R-CNN, MAE, MeanFlow, iMF, JiT, BNF and Drifting, read with PyMuPDF): **words in an Arial-class grotesque, symbols in Computer Modern, the body's own maths font.** MAE Fig. 1 is Arial 6.3 pt; MoCo Figs. 1–2 Arial 5.7–6.8 pt beside CMMI8 maths; iMF Fig. 3 Arial 6.1/7.8 pt beside CM 7.8 pt; JiT 5.7–8.1 pt; BNF Fig. 2 Arial 6.4–9.6 pt; Mask R-CNN Myriad 5.9–6.9 pt. No method figure sets its words in the body serif, and none sets a symbol in anything but CM. A CVPR body is Times text with CM maths (FlowDPS, our own build), so a figure symbol in STIX or Times is the mismatch a reader sees first.

- **6.0 pt Arimo Regular for EVERY word in a figure** (Arimo has Arial's metrics and is in Figma's font list; Arial itself is not). One size. No exceptions. This is what removes the invented hierarchy. Frozen machinery uses the same 6.0 pt in `#929497`; only the colour changes.
- **8.0 pt Arimo, black**, for the one or two words the figure is about — at most two instances. *(Contested: iMF sets these at 11 pt, above body size; BNF caps all in-art type below its 7.97 pt sub-caption. Resolved to 8.0 pt so nothing in the art outranks the 9 pt caption.)*
- **Symbols are Computer Modern at 8 pt, placed at 1:1 and never rescaled.** `latex2svg.py` with fontset `cm` writes a viewBox in points and Figma imports one unit as one px, so the symbol on the artboard is exactly its font size (x-height 3.6 pt). **10 pt** for the one hero symbol (the controller's `u_ψ` inside its block). Tick numerals and fractions are maths too: `\genfrac{}{}{0.4}{1}{1}{2}` is the paper's `\tfrac12`, not a Unicode ½ in a text font. Never re-set a symbol in sans; never set a mechanism name in maths.
- **Floor 6.0 pt, absolute.** Three of the five 2026 papers ship 4.5-5.6 pt somewhere; do not copy it.
- No bold, no italic inside the artwork except real maths.
- Plots follow the same two faces: `paper-data-figure/scripts/paper_plot_style.py` sets Arimo 6 pt and `mathtext.fontset = cm`, one size for labels, ticks and legends.

### Strokes
- **0.5 pt is the working weight** and does every job: connectors, bundle rules, box outlines, ticks. *(Contested: measured working weights are 0.48, 0.48, 0.69, 0.72 pt; ARC and BNF each use literally one weight for an entire figure. Resolved to 0.5 pt.)*
- **0.9 pt is the claim weight**, on at most **three** strokes per figure. **Nothing between 0.5 and 0.9, nothing above 0.9.**
- **0.3 pt** hairline: raster-panel frames and a dashed no-gradient border (0.96 on / 0.72 off).
- **Emphasis is colour, never weight**: `#000000` against `#6C6D70`, a filled head against an open one. A 60 pt container and a 3 pt circle carry the same stroke.
- **One arrowhead silhouette.** Filled triangle, **2.8 x 2.8 pt** on a 0.5 pt shaft (5.6x the shaft), **4.2 x 4.2 pt** on a 0.9 pt shaft. Loss arrows take a shallower **4.5 x 2.8 pt** head. Open two-barb **2.8 x 2.4 pt** in `#B4B5B8` for frozen plumbing only.
- Markers: **4.0 pt** filled disc for a knot; **6.0 pt** white-filled circle with a 0.5 pt stroke and 3.6 pt arms for a sum node; ellipsis = three **1.2 pt** discs at **3.0 pt** pitch, drawn on the line.

### Shape
- **Rounded = a module** (r = 2 pt block, 4 pt container, 6 pt region). **Square = a tensor, an image, a panel** (r = 0). Radii are absolute points, never scaled to the shape.
- **A fill on white carries no stroke.** The only exception is a raster panel, which takes a 0.3 pt `#B4B5B8` frame because our g_η / u_ψ / diag maps sit at mean level 127 and would bleed into the paper.
- Every fill flat. No gradient, no shadow, no glow, no bevel, no 3D, no texture — the pixel outside every edge is `#FFFFFF`.
- Real content only: 640 px `pipe_*.png` panels at 20-30 pt. Never a grey placeholder rectangle, never an invented plot.

### Spacing
- Panel gutter **2.0 pt** on a 20-26 pt panel (≈8 %). Panels never touch.
- Block gap in a stack = **0.18 x block height**. Container padding **>= its radius**.
- Minimum arrow length **10 pt**; **0.5 pt** clearance at each end.
- Symbol sits **3.0 pt** from its stroke; a panel label's baseline sits **4.5 pt** below the panel.
- A duplicated lane or panel repeats at an **exact pitch** with identical x extents, so the reader diffs instead of re-reading.
- Grouping is a 0.5 pt rule with stubs, or a brace. Never a tinted band, never a nested outlined box.

### Banned — the tells that make a figure read as generated
Shadows, glows, bevels, 3D, texture. Gradients of any kind. Stretching to 236 pt. Type under 6 pt, or a second prose size. Bold inside the artwork. A second arrowhead shape, an open head on a claim arrow, a curved or elbowed connector. Weight used as emphasis. Outlining a fill that sits on white. A fill darker than L\* 83, a saturated fill, a fourth hue. A legend box on a schematic — the caption names the glyphs. Leader lines, callout bubbles, knockout plates behind text. Axes, ticks or a grid on a diagram that is not a plot. Icons, clip-art, emoji, brains, robots, lightbulbs, database cylinders, snowflakes for "frozen". Placeholder rectangles. Drawing a repeat N times instead of three plus an ellipsis. An "Ours" badge, a highlight box round the contribution, a red ring pointing at something. Mid greys as fills. Pills and cards (radius > 6.5 pt).

### The three devices worth stealing
1. **Grey the whole frozen subtree, including its type** (iMF). Container `#E6E7E8`, inner blocks `#D1D1D3`, their names in `#929497`, plumbing in 0.5 pt `#B4B5B8` with open barbs. Then spend all `#000000` and the one `#C7EAF5` block on the controller. The reader sees "a small adapter on a frozen prior" from the ink distribution before reading a word.
2. **Duplicate one lane at an exact pitch and let hue carry the meaning** (BNF). Identical geometry, `#919191` for the given thing and `#000000` for ours; the difference is then the only thing visible.
3. **One module, one label size, 60-84 % of the column** (JiT, ARC). Refusing the last 38 pt of the measure forces the content down to what genuinely fits at print size, and a single 6.0 pt label size removes every chance to invent a hierarchy the method does not have.

### Two mechanics the contract assumes, learned the hard way

- **Symbols are cloned, never moved.** Every typeset `sym-<key>` is one layer. Placing it in a
  second figure with `appendChild` steals it from the first, and using it twice in one figure
  leaves one instance. Park the uploads once in a `masters-typeset` frame and place
  `master.clone()` every time. The same rule as "never delete then reuse" (cheatsheet): a
  figure that appears to lose a label after another figure was drawn has had its symbol moved.
- **Prose is sans, mathematics is Times, and a number on an axis is mathematics.** Tick values
  set in the sans face beside a Times `1 - t` are the "fonts do not agree" complaint. Set them in
  Tinos with the real fraction glyphs (¼ ½ ¾ ⅞), never as `1/4`.
