# Figure types: what each one is for, and its default shape

Widths are the venue's true print widths from `paper_plot_style.VENUES`, used verbatim as
`figsize`. `aspect` is height divided by width. Neither is scaled afterwards.

| Type | The claim it can carry | Width | aspect |
|---|---|---|---|
| Line plot | a quantity against a budget, a step count or a scale | column | 0.62 |
| Budget / Pareto plot | quality against cost, with each method a point or a short track | full | 0.40 |
| Bar chart | a handful of methods on one metric | column | 0.62 |
| Grouped bar | methods on several metrics that share a unit | full | 0.38 |
| Scatter | a correlation, or a frontier with each point a run | column | 0.80 |
| Heatmap | a matrix a reader will read cell by cell | column | 0.85 |
| Box / violin | a distribution whose spread is the point | column | 0.62 |
| Multi-panel | one claim shown on several datasets | full | 0.30 per panel row |

## Choosing

Pick from the claim, not from the data's shape. The same table of numbers supports a bar chart
("ours is highest"), a line plot ("ours degrades least as the budget falls") and a scatter
("ours sits outside the frontier the others trace"). Only one of those is the paper's sentence.

Two defaults worth stating because they are so often got wrong:

- **Cost on the x axis belongs on a log scale** whenever the budgets span more than one order of
  magnitude, which they do as soon as a training-free solver at 500 evaluations shares an axis
  with a four-step method. Label the axis as logarithmic; do not leave the reader to infer it
  from the tick spacing.
- **A Pareto plot needs its dominated region visible.** If every method sits in a thin diagonal
  band the plot says nothing; either clip the axes to the band and say so, or pick the two axes
  where the methods actually separate.

## Multi-panel

Build panels with `plt.subplots(1, n)` at the full width and an aspect divided by `n`, sharing
the y axis when the panels share a unit. One legend for the whole figure, placed above the
panels or in the first panel, never repeated. Panel letters come from the LaTeX caption when the
venue numbers them; otherwise set them as `ax.text` in the top-left corner at the base size, bold.

## Anti-patterns seen in submitted papers

- A figure drawn at matplotlib's 6.4 × 4.8 inch default and pulled down with `width=0.48\textwidth`,
  so its 10 pt labels print at about 4.7 pt.
- Twelve series in one panel, distinguished only by hue, with a legend covering the interesting
  corner.
- A y axis starting at a non-zero value on a bar chart, which exaggerates a difference that the
  table shows to be within noise.
- Error bars with no statement of what they are. Say it: standard deviation over images, a
  paired bootstrap interval, or the spread over seeds are three different claims.
- A second y axis. Almost always two figures pretending to be one.
