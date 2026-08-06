// figma_lib.js — battle-tested helpers for paper figures.
// USAGE: paste this whole block at the TOP of every use_figma `code` string,
// then write only composition logic below it. Context resets between calls,
// so the lib must be re-included each call (it is small on purpose).
// All functions assume fonts are already loaded via FONTS() (call it first).

const S = (r, g, b) => ({ type: 'SOLID', color: { r, g, b } });
const HEX = h => { const n = parseInt(h.replace('#',''), 16);
  return S(((n>>16)&255)/255, ((n>>8)&255)/255, (n&255)/255); };

// Low-saturation academic palette: [line, fill] per stage hue.
const PAL = {
  amber:  [HEX('#D98D0D'), HEX('#FEF6DE')],
  blue:   [HEX('#3373D9'), HEX('#E5F0FD')],
  orange: [HEX('#DE5C1A'), HEX('#FEF0E0')],
  green:  [HEX('#1A8C4D'), HEX('#E5F7EB')],
  purple: [HEX('#7340CC'), HEX('#F0EBFD')],
  grey:   [HEX('#4D555F'), HEX('#F4F5F7')],
};
const INK = HEX('#212226'), MUT = HEX('#6B7280');

// Load the Times-substitute family once per call. Await this before any txt().
async function FONTS() {
  for (const style of ['Regular', 'Bold', 'Italic'])
    try { await figma.loadFontAsync({ family: 'Tinos', style }); } catch (e) {}
}

// Wrapping text node. width is mandatory (default autoresize collapses the node).
function txt(parent, x, y, w, str, size, bold, colour, align) {
  const t = figma.createText();
  t.fontName = { family: 'Tinos', style: bold ? 'Bold' : 'Regular' };
  t.fontSize = size; t.characters = str; t.fills = [colour || INK];
  t.textAutoResize = 'HEIGHT'; t.resize(w, 10); t.x = x; t.y = y;
  t.lineHeight = { unit: 'PIXELS', value: size * 1.28 };
  if (align) t.textAlignHorizontal = align;
  parent.appendChild(t); return t;
}

// Rounded content chip inside a column/box.
function chip(parent, x, y, w, h, hue) {
  const f = figma.createFrame();
  f.x = x; f.y = y; f.resize(w, h); f.cornerRadius = 3;
  f.fills = [PAL[hue][1]]; f.strokes = [PAL[hue][0]]; f.strokeWeight = 0.6;
  parent.appendChild(f); return f;
}

// Stage column with a tinted header band. Returns the column frame.
function stageColumn(parent, x, y, w, h, hue, title, titleSize) {
  const box = figma.createFrame();
  box.x = x; box.y = y; box.resize(w, h); box.cornerRadius = 4;
  box.fills = [S(1,1,1)]; box.strokes = [PAL[hue][0]]; box.strokeWeight = 0.9;
  parent.appendChild(box);
  const hdr = figma.createFrame();
  hdr.name = 'header'; hdr.x = 0; hdr.y = 0; hdr.resize(w, 24);
  hdr.fills = [PAL[hue][1]]; hdr.cornerRadius = 4;
  box.appendChild(hdr);
  const t = txt(hdr, 4, 5, w - 8, title, titleSize || 7.2, true, PAL[hue][0], 'CENTER');
  t.lineHeight = { unit: 'PIXELS', value: (titleSize || 7.2) * 1.15 };
  return box;
}

// ---- arrows: ALWAYS single-node, end-to-end (vectorNetwork per-vertex caps) ----
// One arrow = ONE Vector node the user can drag as a unit. Never assemble arrows
// from line+polygon fragments: they are uneditable and drift apart.
// STYLE tokens: define once per figure; every helper reads them. Override before use.
const STYLE = { line: 0.7, blockStroke: 0.7, dash: [2, 2], radius: 2.5 };

// arrow(parent, [[x,y],...], opts) -> single Vector. Straight (2 pts) or elbow (n pts).
// opts: {dashed, noHead, name, curve:{tangentStart:{x,y}, tangentEnd:{x,y}}} (curve: 2 pts only)
async function arrow(parent, pts, opts) {
  const o = opts || {};
  const v = figma.createVector(); parent.appendChild(v);
  const verts = pts.map((q, i) => ({ x: q[0], y: q[1],
    strokeCap: (i === pts.length - 1 && !o.noHead) ? 'ARROW_EQUILATERAL' : 'NONE' }));
  const segs = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const g = { start: i, end: i + 1 };
    if (o.curve && pts.length === 2) { g.tangentStart = o.curve.tangentStart; g.tangentEnd = o.curve.tangentEnd; }
    segs.push(g);
  }
  await v.setVectorNetworkAsync({ vertices: verts, segments: segs, regions: [] });
  v.strokes = [o.colour || INK]; v.strokeWeight = STYLE.line;
  if (o.dashed) v.dashPattern = STYLE.dash;
  v.x = Math.min(...pts.map(q => q[0])); v.y = Math.min(...pts.map(q => q[1]));
  v.name = o.name || 'arrow';
  return v;
}

// Convenience wrappers (all async now)
async function arrowH(parent, x, y, len, colour, dashed) {
  return arrow(parent, [[x, y], [x + len, y]], { colour, dashed });
}
async function arrowV(parent, x, y, len, colour) {
  return arrow(parent, [[x, y], [x, y + len]], { colour });
}
async function elbowArrow(parent, pts, colour, dashed) {
  return arrow(parent, pts, { colour, dashed, name: 'elbow' });
}
async function curveArrow(parent, x1, y1, x2, y2, bend, colour, dashed) {
  const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
  const nx = -dy / len * bend, ny = dx / len * bend;
  return arrow(parent, [[x1, y1], [x2, y2]],
    { colour, dashed, name: 'curve',
      curve: { tangentStart: { x: dx * 0.3 + nx, y: dy * 0.3 + ny },
               tangentEnd:   { x: -dx * 0.3 + nx, y: -dy * 0.3 + ny } } });
}
async function selfLoop(parent, x, y, w, rise, colour) {
  return curveArrow(parent, x + w, y, x, y, (rise || 12), colour, true);
}

// Consistency audit: distinct style values across a subtree. Run before declaring
// done; more than the expected count of any list = style drift to fix.
function auditConsistency(root) {
  const sw = new Set(), fs = new Set();
  for (const n of root.findAll(() => true)) {
    if ('strokeWeight' in n && n.strokes && n.strokes.length)
      sw.add(Math.round(n.strokeWeight * 100) / 100);
    if (n.type === 'TEXT' && typeof n.fontSize === 'number') fs.add(n.fontSize);
  }
  return { strokeWeights: [...sw].sort(), fontSizes: [...fs].sort(),
           arrowNodes: root.findAll(n => n.type === 'VECTOR').length };
}

// Flow-type legend, laid out 2xN. items = [[label, colourPaint, dashed], ...]
function legendRow(parent, x, y, w, items, textSize) {
  const box = figma.createFrame();
  box.x = x; box.y = y; box.resize(w, 12 + Math.ceil(items.length / 2) * 11);
  box.cornerRadius = 3; box.fills = [S(1,1,1)];
  box.strokes = [HEX('#B3B9C2')]; box.strokeWeight = 0.7;
  parent.appendChild(box);
  items.forEach(([label, colour, dashed], i) => {
    const cx = 6 + (i % 2) * (w / 2 - 4), cy = 6 + Math.floor(i / 2) * 11;
    const ln = figma.createLine();
    ln.x = cx; ln.y = cy + 3; ln.resize(11, 0);
    ln.strokes = [colour]; ln.strokeWeight = 1;
    if (dashed) ln.dashPattern = [2, 2];
    box.appendChild(ln);
    txt(box, cx + 15, cy - 0.5, w / 2 - 22, label, textSize || 5, false, MUT);
  });
  return box;
}

// Vertically centre a column's body between regionTop and the box bottom.
// Excludes the header band and any node ids listed in pinnedIds.
function balanceColumn(box, regionTop, pinnedIds) {
  const pinned = pinnedIds || [];
  const body = box.children.filter(n => n.name !== 'header' && !pinned.includes(n.id));
  if (!body.length) return 0;
  const top = Math.min(...body.map(n => n.y));
  const bot = Math.max(...body.map(n => n.y + n.height));
  const d = Math.round(((box.height - 8) - regionTop - (bot - top)) / 2 + (regionTop - top));
  body.forEach(n => { n.y += d; });
  return d;
}

// Inject a cleaned SVG string as a true vector. colour replaces currentColor.
function placeSvg(parent, svg, colour, x, y, size, name) {
  const node = figma.createNodeFromSvg(colour ? svg.split('currentColor').join(colour) : svg);
  node.name = name || 'icon';
  parent.appendChild(node);
  node.rescale(size / node.width); node.x = x; node.y = y;
  return node;
}

// ---------- extended shapes (v0.3) — all SVG-template based ----------

// Solid/tinted ellipse node (e.g. state, dataset bubble).
function ellipse(parent, x, y, w, h, hue) {
  const e = figma.createEllipse();
  e.x = x; e.y = y; e.resize(w, h);
  e.fills = [PAL[hue][1]]; e.strokes = [PAL[hue][0]]; e.strokeWeight = 0.8;
  parent.appendChild(e); return e;
}

const _hex = p => { const c = p.color;
  return '#' + [c.r, c.g, c.b].map(v => Math.round(v * 255).toString(16).padStart(2, '0')).join(''); };




// Curly brace spanning `len` pt. side: 'left'|'right'|'top'|'bottom' (tip points away).
// After rotating a node, its x/y no longer mean its visual top-left.
// placeAt fixes that using bounding boxes (works inside any parent frame).
function placeAt(node, parent, x, y) {
  const nb = node.absoluteBoundingBox, pb = parent.absoluteBoundingBox;
  if (nb && pb) { node.x += x - (nb.x - pb.x); node.y += y - (nb.y - pb.y); }
}

function brace(parent, x, y, len, side, colour) {
  const t = 4;   // tip depth
  const d = `M 0 0 C ${t} ${len*0.12} ${t*0.4} ${len*0.38} ${t} ${len/2} C ${t*0.4} ${len*0.62} ${t} ${len*0.88} 0 ${len}`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${t+1} ${len}">` +
    `<path d="${d}" fill="none" stroke="${_hex(colour)}" stroke-width="${STYLE.line}" stroke-linecap="round"/></svg>`;
  const node = figma.createNodeFromSvg(svg);
  node.name = 'brace'; parent.appendChild(node);
  if (side === 'left')  node.rotation = 180;
  if (side === 'top')   node.rotation = -90;
  if (side === 'bottom') node.rotation = 90;
  placeAt(node, parent, x, y);
  return node;
}

// Dashed grouping container with a small corner label. Content goes on top of it.
function dashedGroup(parent, x, y, w, h, label, hue, labelSize) {
  const f = figma.createFrame();
  f.x = x; f.y = y; f.resize(w, h); f.cornerRadius = 4;
  f.fills = []; f.strokes = [PAL[hue][0]]; f.strokeWeight = 0.7;
  f.dashPattern = [3, 3]; f.clipsContent = false;
  parent.appendChild(f);
  if (label) {
    const tag = figma.createFrame();
    tag.x = 6; tag.y = -5; tag.resize(4 + label.length * (labelSize || 5) * 0.55, 10);
    tag.fills = [S(1, 1, 1)]; tag.cornerRadius = 2;
    f.appendChild(tag);
    txt(tag, 2, 1, tag.width - 3, label, labelSize || 5, true, PAL[hue][0]);
  }
  return f;
}

// Small capsule badge (xN markers, dataset sizes, tags).
function badge(parent, x, y, label, hue, size) {
  const s = size || 4.8;
  const b = figma.createFrame();
  b.x = x; b.y = y; b.resize(6 + label.length * s * 0.55, s + 4.5);
  b.cornerRadius = (s + 4.5) / 2;
  b.fills = [PAL[hue][1]]; b.strokes = [PAL[hue][0]]; b.strokeWeight = 0.5;
  parent.appendChild(b);
  txt(b, 3, 2, b.width - 4, label, s, true, PAL[hue][0], 'CENTER');
  return b;
}

// Rotated text for y-axis style labels (reads bottom-to-top).
function rotText(parent, x, y, w, str, size, colour) {
  const t = txt(parent, 0, 0, w, str, size, false, colour, 'CENTER');
  t.rotation = 90; placeAt(t, parent, x, y);
  return t;
}

// Grid cell coordinates (pure math, no nodes): returns [[x,y],...] row-major.
function gridCells(x, y, cols, rows, cellW, cellH, gap) {
  const out = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++)
    out.push([x + c * (cellW + gap), y + r * (cellH + gap)]);
  return out;
}

// Unicode sub/superscripts for simple math in labels: mathText("x_1 y^2 W_k")
function mathText(s) {
  const sub = {'0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','k':'ₖ','i':'ᵢ','j':'ⱼ','n':'ₙ','t':'ₜ'};
  const sup = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ','i':'ⁱ'};
  return s.replace(/_([0-9a-z])/g, (m, c) => sub[c] || m)
          .replace(/\^([0-9a-z])/g, (m, c) => sup[c] || m);
}
