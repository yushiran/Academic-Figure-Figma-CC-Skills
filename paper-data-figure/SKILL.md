---
name: paper-data-figure
description: Draw a paper's DATA figures — budget curves, ablation plots, training curves, scaling laws, bar comparisons, heatmaps — as vector PDFs at the venue's true print width, from result files rather than retyped numbers. Use whenever a figure's content is numbers the experiments produced. Its sibling `academic-figure-figma` covers the hand-drawn framework, pipeline and architecture figures; this one covers everything with an axis.
---

# Paper data figure

The sibling skill draws what has no data behind it. This one draws what does, and the whole
difference in outcome comes from two habits: the numbers are read from the files the experiments
wrote, and the figure is drawn at the size it will be printed at.

## Hard rules

1. **Draw at final print size; `\includegraphics` never scales.** Set `figsize` to the true
   width in inches and include the file with no `width=` at all. `width=0.48\textwidth` on a
   figure drawn at default size is how an 8 pt label silently becomes 5 pt, and nothing in the
   compiled PDF announces it.
2. **A LaTeX point is 1/72.27 inch; a PostScript point is 1/72 inch.** `\the\textwidth` reports
   LaTeX points. Convert through inches. Treating the two as the same number puts a CVPR
   full-width figure 0.4 % over the text width, which is enough for `Overfull \hbox`.
   Measure the venue once, in the document body: `\typeout{\the\textwidth, \the\columnwidth}`.
3. **Numbers come from the result files, never from a message or a memory.** Read the JSONL,
   CSV or summary the run produced. A figure that hardcodes a number is a figure that will
   disagree with its own table after the next run.
4. **Never plot an arm that has not run.** An empty series is left out and said so in the
   caption; it is not interpolated, extrapolated, or filled with a plausible value.
5. **One script per figure, one shared style module, imported not copied.** `scripts/paper_plot_style.py`
   holds the geometry, the type ramp and the palette. A figure script that sets its own
   `rcParams` has left the system and will drift.
6. **Every series separable three ways**: hue, dash and marker. Hue alone dies in greyscale
   and for a colour-deficient reader. The paper's own row is the same hue family, one weight
   heavier — never a different palette.
7. **No title inside the figure.** The caption is the title, and it lives in LaTeX. Same for
   the panel letters when the venue sets them.
8. **Render, then look.** Read the produced PNG back and inspect it before declaring done.
   A script that exits 0 has proved nothing about clipped labels or a legend over the data.

## Workflow

**Step 0 — Find the numbers and name the claim.** Locate the result files. State, in one
sentence, what the figure is for: the claim a reader should be able to check off it. A figure
without that sentence becomes a decorative plot of everything that was measured.

**Step 1 — Clarify the specification.** Figure type, what maps to x, y, hue and panel, which
width (column or full), what is on a log axis, which series is ours. `references/figure-types.md`
gives the type-to-use-case table and the default aspect per type.

**Step 2 — Generate and execute, at most four times.** Write a self-contained script under
`figures/gen_<id>.py` that imports the style module, reads the result file, and calls `save()`.
Run it. On a traceback, read it, fix the script, run again. Stop at four attempts and report
what blocked rather than degrading the figure to make it run.

**Step 3 — Read the render back.** Open the PNG twin and check, in this order: is it the figure
type intended; does every axis carry a label and a unit; is any label clipped; does the legend
sit on data; are the tick labels legible at print size; is the hue order the same as every other
figure in the paper. Fix and re-run. This step is not optional — it is the only one that catches
what the script cannot.

**Step 4 — Emit the LaTeX.** Append to `figures/latex_includes.tex` a block per figure with
`\includegraphics{...}` carrying no width, a `\label`, and a caption stub the author replaces.

**Step 5 — Checklist.** Run the partitioned checklist below, then `audit()` from the style
module for the page-fit and rasterised-type checks.

## Checklist, partitioned

The partition matters: the first list is never negotiable, the second is a set of strong
defaults that a specific figure may justify overriding.

**Correctness — always binding**

- Excluded runs never feed a summary statistic plotted beside included ones.
- The caption is tested against every plotted series; a claim like "best on five of seven
  tasks" is counted off the figure, not remembered.
- Only comparable conditions share an axis. A different budget, protocol or test-set size is
  a separate panel or an annotation, never a silent neighbour.
- `n` and the replication unit appear in the panel or the caption.
- Rendered and looked at: no clipped label, nothing unreadable at print size.

**Guidance — strong defaults**

- Serif face matching the paper body; base 8 pt, floor 6 pt.
- Greyscale-distinguishable, colourblind-safe.
- Axis labels carry units. Log axes are labelled as such.
- Legend outside the data, or in the emptiest quadrant.
- Vector PDF ships; PNG is the preview twin only.
- No grid unless the reader must read values off the plot; then a hairline grid under the data.

## What this skill does not do

Framework, pipeline and architecture diagrams, sample grids, and any figure whose content is
images rather than numbers. Those go to `academic-figure-figma`, which draws them at print size
in Figma through the Plugin API. The two skills share one geometry table and one type ramp, so a
paper's plotted figures and its drawn figures land at the same widths and the same label sizes.
