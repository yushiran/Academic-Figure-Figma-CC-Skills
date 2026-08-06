# Incremental build workflow — details and pitfalls

Companion to SKILL.md steps 1-5. Everything here was learned on a real figure
(GeoAT-LM framework, 516×402 pt, ~30 use_figma calls including reworks; a clean run
takes ~15).

## Correctness audit first (Step 0)

Before drawing, produce this table for every text element that will appear:

| Figure will say | Paper says (line ref) | Verdict |
|---|---|---|
| 11 semantic groups | L167 "11 semantic feature groups" | ok |
| Exact Match | table header L772 | renamed from candidate's "Accuracy" |

Rules of thumb:
- Never hard-code section/figure/table numbers into a figure — they shift.
- Metric names must match the results-table headers verbatim.
- When the paper itself is inconsistent (e.g. "constructed" vs "synthetic rationale"),
  surface it and let the user pick the canonical term — do not pick silently.

## Helper pattern

Define these once per call (context resets between use_figma calls):

```js
const S=(r,g,b)=>({type:'SOLID',color:{r,g,b}});
function txt(p,x,y,w,str,size,bold,colour,align){
  const t=figma.createText();
  t.fontName={family:"Tinos",style:bold?"Bold":"Regular"};
  t.fontSize=size; t.characters=str; t.fills=[colour];
  t.textAutoResize="HEIGHT";           // wrap: explicit width + height-hug
  t.resize(w,10); t.x=x; t.y=y;
  t.lineHeight={unit:"PIXELS",value:size*1.28};
  if(align)t.textAlignHorizontal=align;
  p.appendChild(t); return t;
}
```

`textAutoResize:"HEIGHT"` + explicit width is mandatory for wrapping text; the default
WIDTH_AND_HEIGHT mode ignores the width and collapses the node into a thread.

## Arrows

```js
// shaft
const l=figma.createLine(); l.x=x; l.y=y; l.resize(len,0);
l.strokes=[col]; l.strokeWeight=1; l.strokeCap="NONE";
// head (rightward): 3-point polygon, rotation -90, tip at x+len
const h=figma.createPolygon(); h.pointCount=3; h.resize(3.6,4.6);
h.fills=[col]; h.strokes=[]; h.rotation=-90;
h.x=x+len-3.6; h.y=y-2.3;
// downward: rotation=180, h.x=cx-1.8, h.y=y+len-4.6
```

- `strokeCap:"ARROW_LINES"` on a Line arrows **both ends** — only use for double-headed.
- Keep a written list of arrow node ids. Re-centring by
  `children.filter(n=>n.type==='LINE')` once captured the dashed panel divider too and
  dragged it 112 pt into the panel. Explicit id lists only.

## Balancing multi-column panels

1. Panel height = content bottom of the fullest column + padding.
2. For each other column: `delta = ((H-pad) - regionTop - contentH)/2 + (regionTop - top)`;
   shift body nodes (exclude the header and any pinned tag rows).
3. Re-centre arrow rows to `panelTop + H/2` (by id list).
4. Compact tricks that bought 46 pt on a real figure: merge two single-fact chips into
   one two-line chip; delete a footer that repeats a header tag; tighten chip stack gap
   to 3 pt.

## Screenshot self-review checklist (every stage)

- Text overflow: any line touching/crossing its chip border; any unintended wrap
  (long tokens like `<answer> label set </answer>` need a smaller size or shorter text).
- Arrow heads: one per arrow, pointing with the flow.
- Whitespace: no column with > ~25% empty bottom; no panel gap > 14 pt.
- Terminology: labels vs. paper canon.
- Icons: right mark, right block (base-model logo on backbone only).

## Interplay with candidate generators (studio-pro etc.)

Treat C01-C04/F01-F02 candidates as **layout references only**:
- Steal their narrative structure freely (e.g. a supervision-asymmetry framing that
  makes the figure argue the paper's C1).
- Re-verify every fact against the paper — candidates routinely contain hallucinated
  numbers and stale terminology.
- Their S0 fact sheets (paper-foundation-report.md) speed up the Step-0 audit but the
  paper source stays authoritative.

## Export

User exports from Figma directly (File → Export → PDF, 1x) — the artboard is already
at print size. PNG exports for quick sharing at 2-3x. Keep the artboard free of
off-canvas scratch nodes before export.
