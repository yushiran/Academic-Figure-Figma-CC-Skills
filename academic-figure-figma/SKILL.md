---
name: academic-figure-figma
description: Use when the user wants to draw, rebuild, or refine an academic paper figure (framework, pipeline, architecture, method overview) as an editable vector graphic in Figma via Claude Code and the Figma MCP server. Covers Figma MCP connection and quota, paper-accurate canvas sizing (IEEE/Elsevier), sourcing brand logos and concept icons as true SVG vectors, incremental canvas construction with screenshot self-review, and terminology/correctness alignment with the paper source. Also use when a reference/candidate image (e.g. from paper-framework-figure-studio-pro C01-C04) needs to be reproduced as an editable Figma figure.
---

# Academic Figure in Figma (Claude Code)

Turn a paper figure sketch, a ChatGPT-generated candidate image, or a text description
into an **editable, paper-spec vector figure in Figma**, driven entirely from Claude Code
through the official Figma MCP server.

Position in the toolchain: upstream tools (paper-framework-figure-studio-pro, PaperBanana)
produce raster *candidate references*. This skill does the last mile — a real Figma file
the author can hand-tune, with exact paper dimensions and true vector icons.

## Hard rules (learned from real failures)

1. **Correctness before aesthetics.** Before drawing anything, grep the paper source and
   verify EVERY number, term, and metric name that will appear in the figure. Real catches:
   a candidate image said "111 semantic groups" (paper: 11), "Accuracy" (paper's table:
   "Exact Match"), and hard-coded "Section 3.4.1" (numbering had shifted to 3.2.1 — never
   put section numbers in figures). Fix the reference's errors; do not reproduce them.
2. **One term per concept, matching the paper's canon.** If the paper says
   "difficulty-weighted Jaccard reward", the figure must not say "weighted F1". Sweep the
   figure's text labels against the paper before declaring done.
3. **Logo semantics.** A base-model logo (e.g. Qwen) belongs on the *backbone* block only.
   Never put a third-party brand mark on the *final/proposed model* block.
4. **Verify every fetched logo by eye.** Icon CDNs mislabel. Render at scale 4-6 and look
   at it before use (simpleicons' "qwen" is NOT the Qwen logo; lobe-icons' is correct).
5. **Design at final size.** Create the artboard at the true print width in pt (see
   references/paper-canvas-specs.md) and set font sizes directly. Never draw a large
   canvas and shrink it — a 1540px-wide draft compressed to a 516pt column turns 13px
   text into unreadable 4.4pt.
6. **Screenshot after every build stage.** `await node.screenshot()` inside the same
   use_figma call. Check: text overflow/wrapping, arrow direction (single-headed),
   uneven whitespace, terminology. Fix before building the next stage.

## Workflow

### Step 0 — Preflight
- Confirm the Figma MCP server is connected: call `whoami` (quota-exempt).
  Not connected or quota exhausted → references/figma-mcp-setup.md.
- Identify the paper's LaTeX class and pick canvas width → references/paper-canvas-specs.md.
- If a candidate/reference image exists, read it and produce a correctness audit table
  (claim in image vs. paper source vs. verdict) BEFORE drawing. Show it to the user.
- Plan the figure against references/figure-grammar.md: evidence for every arrow,
  variables on edges not boxes, operation chains not just outcomes, repeated entities
  compressed, mainline centred, in-figure vs. caption text ownership decided.

### Step 1 — Skeleton
Build the artboard and top-level containers (stage columns / panel bands) in one
use_figma call. Title row, panel labels ("(a) ...", "(b) ..."), dashed panel divider.
White background, thin coloured strokes (~0.9pt), corner radius 3-4, one accent colour
per stage from a low-saturation palette.

### Step 2 — Content fill
Fill containers stage by stage (≤10 logical operations per call). Chips = tinted
fill + darker stroke of the same hue. Body text via a `txt()` helper with
`textAutoResize:"HEIGHT"` + explicit width (default WIDTH_AND_HEIGHT collapses to a
zero-width thread). Keep per-chip text to 2-4 short lines.

### Step 3 — Icons and logos
Fetch as SVG, inject as true vectors → references/icon-sourcing.md and
scripts/iconfont_search.py. `figma.createNodeFromSvg(svg)` then `rescale(target/width)`.
Concept icons: Lucide first (uniform stroke). Brand logos: lobe-icons first.
Chinese-context concept icons: iconfont search API.

### Step 4 — Arrows and flow
Single-direction arrows: line shaft (`strokeCap:"NONE"`) + small 3-point polygon head
(rotation -90 for rightward, 180 for downward). Colour arrows by flow type (data / SFT /
RL / evaluation) and add a legend. Never rely on `strokeCap:"ARROW_LINES"` for a single
head — it arrows both ends.
When later re-centring arrows, address them by an **explicit id list**. A loop over
`children.filter(type==='LINE')` will also drag panel dividers (this happened; it moved
the divider 112pt into a panel).

### Step 5 — Balance and self-review
Trim artboard to content. Height of a multi-column panel = its fullest column; centre
the other columns' bodies. Screenshot at 2.5-3x, run the rule-6 checklist plus the
error vocabulary at the end of references/figure-grammar.md (false relays, variables
drawn as boxes, unbundled parallel edges, off-centre mainline, excessive whitespace),
fix, repeat until clean. Then ask the user to review in Figma at 100% zoom.

## Recovery notes
- A failed use_figma script is **atomic** — nothing landed; fix and rerun.
- Page/tool context resets between calls; re-fetch nodes by id each call and return all
  created/mutated ids.
- Free-plan quota is 6 calls/month total — do not start drawing on a Starter/View seat;
  fix the seat first (references/figma-mcp-setup.md).
