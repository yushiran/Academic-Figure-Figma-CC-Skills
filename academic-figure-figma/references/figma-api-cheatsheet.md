# Figma Plugin API cheatsheet — the paper-figure subset

Self-contained. With this file plus `scripts/figma_lib.js`, you can write every
`use_figma` call for a paper figure WITHOUT loading the official figma-use skill or
the Plugin API typings. Stay inside this subset; it is sufficient and verified.

## The use_figma contract

- `code` is plain JavaScript, auto-wrapped in an async context: use top-level `await`,
  end with `return {...}` — the return value is your ONLY output channel
  (`console.log` is invisible; `figma.notify` throws).
- **Failed scripts are atomic**: an error means nothing was applied. Read the error,
  fix, retry once.
- **Context resets between calls.** Re-include figma_lib.js, re-load fonts, re-fetch
  nodes by id (`await figma.getNodeByIdAsync("12:34")`) every call.
- Always return every created/mutated node id: `return {createdNodeIds:[...], ...}`.
- Screenshot inside the call: `await node.screenshot({scale: 2.6})` — the image comes
  back with the tool result; no separate screenshot call needed.

## Allowed node types (hard rule: nothing else)

`createFrame` `createText` `createLine` `createPolygon` `createNodeFromSvg`

Plus the **component-reuse subset** (canvas-tested): `figma.createComponentFromNode(node)`,
`component.createInstance()`, and `page.findAll(n => n.type === 'COMPONENT')` to locate
components the user made by hand (e.g. Math-X formula objects) and place instances.

**Banned for paper figures** — they add API complexity with zero benefit here:
Auto Layout (`layoutMode`, `layoutSizing*`, `primaryAxisSizingMode`, `createAutoLayout`),
variant sets / component properties / published-library workflows, Variables/Tokens/Styles,
`figma.createImage*`, `loadAllPagesAsync`, `setPluginData`, Sticky/Connector (FigJam-only).
Absolute x/y positioning inside plain frames is the whole layout model.

## Formulas (canvas-tested pipeline)

Real math typesetting (fractions, sums, radicals) comes from LaTeX, not text nodes:

```bash
uv run --with matplotlib python scripts/latex2svg.py 'W_k = \frac{\exp(-R_k)}{\sum_j \exp(-R_j)}' /tmp/eq.svg 10
```

Read the SVG, inline it in the call, `figma.createNodeFromSvg(svg)`, `rescale` to
target width (a display equation ≈ 60-70% of chip width; inline ≈ text cap-height).
STIX fonts match Tinos body text; `<defs>+<use>` glyph structure imports cleanly.
To reuse one formula many times: `createComponentFromNode` once, `createInstance`
per placement. Reserve `mathText()` for plain sub/superscripts inside labels —
never for fractions or operators.

## Core facts (each one is a real trap)

| Fact | Detail |
|---|---|
| Colours are 0-1 | `{r:1,g:0,b:0}` = red. Use `HEX('#3373D9')` from the lib. |
| fills/strokes are read-only arrays | assign whole new arrays: `n.fills = [S(1,1,1)]` |
| Fonts must load first | `await figma.loadFontAsync({family:'Tinos',style:'Bold'})` before ANY text op — per call. Tinos = Times substitute; styles: Regular/Bold/Italic. Inter style names have spaces ("Semi Bold"). |
| Text wrapping | `textAutoResize='HEIGHT'` + `resize(width, anyHeight)`. The default mode ignores width and collapses the node to a thread. |
| lineHeight/letterSpacing | object form: `{unit:'PIXELS', value: 12}` — bare numbers throw |
| resize vs rescale | `resize(w,h)` sets box; `rescale(k)` scales children+strokes too — use rescale for SVG icons (`rescale(target/node.width)`) |
| Line length | `line.resize(len, 0)`; direction via `rotation` (-90 = downward) |
| Arrows = ONE node, always | `lib arrow(parent, pts, opts)`: createVector + `setVectorNetworkAsync`, final vertex `strokeCap:'ARROW_EQUILATERAL'`, others `'NONE'`. Straight/elbow/curved/dashed all single Vector — draggable as a unit. NEVER assemble arrows from line+polygon fragments (uneditable, drift apart, unreadable layer tree). |
| Arrow helpers are async | `await arrow/arrowH/arrowV/elbowArrow/curveArrow/selfLoop(...)` |
| Find nodes | `await figma.getNodeByIdAsync(id)`, `parent.children.filter(...)`, `node.findAll(n=>...)` |
| Batch edits by id | when re-positioning arrows/dividers, use an EXPLICIT id list. Filtering `type==='LINE'` once caught a dashed divider and dragged it 112pt. |
| Dashed lines | `n.dashPattern = [3,3]` |
| Corner radius | `n.cornerRadius = 4` |
| Page switch | `await figma.setCurrentPageAsync(page)` — the sync setter throws. One switch per call max. |
| New top-level nodes | default to (0,0) — set x/y away from existing content |

## Most-used canvas widths (full table: paper-canvas-specs.md)

IEEEtran `figure*` = **516pt**, `figure` = **252pt**; elsarticle single-column ≈ **390pt**.

## Canonical call skeleton

```js
/* --- paste figma_lib.js here --- */
await FONTS();
const art = await figma.getNodeByIdAsync("9:2");   // or figma.createFrame() on call 1

// ... composition using stageColumn / chip / txt / arrowH / placeSvg ...

await art.screenshot({ scale: 2.6 });
return { createdNodeIds: [/* every id */] };
```

## Consistency discipline (the "细看全是问题" killer)

- One `STYLE` token table per figure (line weight, font-size ramp, radius, dash);
  every element reads tokens — no inline magic numbers.
- Same-kind blocks come from one data table + one loop, never hand-placed one by one.
- Before declaring done run `auditFigure(art)` — structured lint returning
  `{findings, errors, warnings, consistency}`. Checks: text below 6pt (WARN),
  text INK outside its parent frame (ERROR; judged on renderBounds, so an
  oversized-but-empty text node is not flagged), partial overlap of sibling
  blocks (ERROR; full containment = layering, OK), an arrow segment crossing a
  block interior (ERROR; tail/head endpoints exempt, interior corner vertices
  NOT — a corner inside a block means the route goes through it), arrow head
  buried >3pt inside a block (WARN). Fix every ERROR before user review.
- Grouping frames arrows may legitimately cross must be named `*-stack`,
  `*-group`, `*-region`, `*-panel` or `*-container` (or passed via
  `auditFigure(art, {passThrough: ['name']})`) — they are exempt from the
  arrow and overlap checks.
- Style drift: `auditConsistency` (also embedded in the auditFigure result) —
  distinct strokeWeights beyond plan = drift. Known trap it catches: SVG symbols
  change stroke weight under `rescale` (a 1.2 stroke at 0.55 scale becomes 0.66)
  — after rescaling an injected SVG, reset its vectors' strokeWeight to STYLE.line.

## Error → fix table

| Error | Fix |
|---|---|
| `Cannot write to node with unloaded font` | `await FONTS()` (or load the exact family/style) before the text op |
| `in set_layoutSizingHorizontal: ...` | you touched Auto Layout — banned; use absolute x/y |
| `Expected 'FIXED' \| 'AUTO'...` | same — Auto Layout property, banned |
| `Setting figma.currentPage is not supported` | use `await figma.setCurrentPageAsync(page)` |
| `no such property 'createPage'` | you are in FigJam/Slides — this skill targets /design/ files only |
| colour out of range | you passed 0-255; divide by 255 or use HEX() |
| `The node with id X does not exist` | stale id from a previous call — re-fetch, or the node was removed |
| text shows but width 0 / vertical thread | missing `textAutoResize='HEIGHT'` + `resize(w, h)` |
