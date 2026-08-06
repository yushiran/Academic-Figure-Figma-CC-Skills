---
name: academic-figure-figma
description: Use when the user wants a paper figure (framework, pipeline, architecture, method overview) drawn, rebuilt, or refined as an editable vector in Figma via Claude Code — including reproducing a candidate/reference image (e.g. studio-pro C01-C04) at exact print size. Also use when the user needs to set up or fix the Claude Code-Figma connection: installing the Figma MCP plugin, OAuth/authentication (incl. remote sessions), seat or quota problems, "figma 连不上/怎么配置", or a first-run guided setup.
---

# Academic Figure in Figma (Claude Code)

Land a sketch, candidate image, or text description as an **editable, paper-exact
vector figure in Figma**, drawn directly through the Figma MCP server.

**Draw from this skill alone.** `references/figma-api-cheatsheet.md` +
`scripts/figma_lib.js` contain the complete verified API subset — do NOT load the
official figma-use skill, the Plugin API typings, or explore the API by trial: that
is the slow path this skill replaces. Icons come from the local cache first
(`scripts/assets/icons/icons.json`, pre-cleaned, injection-ready).

## Hard rules

1. **Correctness before aesthetics.** Grep the paper for every number, term, metric
   name, and section reference the figure will carry; show the audit table before
   drawing. Fix the reference image's errors, never reproduce them. Terminology must
   match the paper canon verbatim; when the paper is inconsistent, ask the user to
   pick. Never hard-code section numbers into a figure.
2. **Basic building blocks only.** Frame, Text, Line, Polygon, SVG import, absolute
   x/y, plus the component-reuse subset (createComponentFromNode / createInstance).
   Auto Layout, variant sets, Variables, Styles are banned (cheatsheet §Allowed).
3. **Design at final print size** (references/paper-canvas-specs.md). Never draw big
   and shrink — fonts fall below the 6pt floor.
4. **Figure grammar** (references/figure-grammar.md): evidence for every arrow, no
   false relays, variables on edges not boxes, operation chains not just outcomes,
   repeated entities compressed, mainline centred, restrained palette.
5. **Logo semantics + eye check.** Base-model logos on the backbone block only; never
   a brand mark on the proposed-model block. Screenshot every fetched logo before use
   — CDNs mislabel (cache manifest records which marks are already verified).
6. **Screenshot after every wave**, inside the same call. Check: text overflow,
   single-headed arrows pointing with the flow, whitespace balance, terminology.
7. **One element, one node; one figure, one style table.** Arrows are single
   vectorNetwork nodes (never line+polygon fragments). Same-kind elements are
   generated from one data table with STYLE tokens; end every session with
   `auditConsistency()` and fix any unplanned distinct value.
8. **Formulas are typeset, not typed.** Any fraction, sum, radical or operator goes
   through the latex2svg pipeline (cheatsheet §Formulas); `mathText()` only for
   simple sub/superscripts in labels. User-made formula components (e.g. Math-X)
   are reused via `findAll` + `createInstance`, never redrawn.

## Workflow

**First run / connection problems — guided setup.** If Figma MCP tools are missing,
auth fails, or whoami shows a View seat, switch to the five-step tutorial in
references/figma-mcp-setup.md (§Tutorial): Claude leads, verifies each step, and
returns here when drawing-ready.

**Step 0 — Preflight.** `whoami` (quota-exempt) → seat must be Full with a paid or
education plan, else run the setup tutorial first (references/figma-mcp-setup.md). Pick canvas width
from the venue (references/paper-canvas-specs.md). Produce the Step-0 correctness
audit table (rule 1) and the figure-grammar plan (rule 4). Read
`scripts/figma_lib.js` and the icon cache manifest now — every later call pastes the
lib verbatim at the top of its code.

**Step 1 — Skeleton (1 call).** Artboard at print width + all stage/panel containers
via `stageColumn()`; panel titles, dashed divider. Return every container id.

**Step 2 — Parallel fill (N calls, one message).** One call per container, following
references/parallel-drawing.md: paste lib, `await FONTS()`, fill chips/text/icons for
that container only (`chip()`, `txt()`, `placeSvg()` with cached icons). Fan out all
containers simultaneously; never touch siblings or globals.

**Step 3 — Assembly (1 call).** Arrows between stages (`arrowH`/`arrowV`, colour per
flow type), legend (`legendRow`), per-column balance (`balanceColumn`), artboard trim.
Keep the returned arrow ids for later adjustments — never re-find arrows by type.

**Step 4 — Review loop.** Screenshot at 2.5-3x AND re-read the reference image
side-by-side (structure being right is not enough — compare density, spacing,
line routing against the original). Run rule 6, `auditConsistency()`, plus the
error vocabulary at the end of references/figure-grammar.md. Independent fixes may fan out again.
Stop when clean; ask the user to review in Figma at 100% zoom; user exports PDF.

## References

| File | Load when |
|---|---|
| references/figma-api-cheatsheet.md | before writing the first use_figma call (always) |
| references/parallel-drawing.md | at Step 2 |
| references/paper-canvas-specs.md | at Step 0 (canvas + fonts + palette numbers) |
| references/figure-grammar.md | at Step 0 planning and Step 4 review |
| references/icon-sourcing.md | only when an icon is NOT in the local cache |
| references/figma-mcp-setup.md | connection/quota problems only |
| references/build-workflow.md | deep dives: balancing math, pitfalls, export |
