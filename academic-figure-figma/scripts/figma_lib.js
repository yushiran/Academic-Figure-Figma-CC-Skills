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

// Single-headed horizontal arrow (pointing right). NEVER strokeCap ARROW_LINES
// for one head — it arrows both ends.
function arrowH(parent, x, y, len, colour, dashed) {
  const l = figma.createLine();
  l.x = x; l.y = y; l.resize(Math.max(1, len - 3.6), 0);
  l.strokes = [colour]; l.strokeWeight = 0.9; l.strokeCap = 'NONE';
  if (dashed) l.dashPattern = [2, 2];
  parent.appendChild(l);
  const h = figma.createPolygon();
  h.pointCount = 3; h.resize(3.6, 4.6); h.fills = [colour]; h.strokes = [];
  h.rotation = -90; h.x = x + len - 3.6; h.y = y - 2.3;
  parent.appendChild(h);
  return [l.id, h.id];
}

// Single-headed vertical arrow (pointing down).
function arrowV(parent, x, y, len, colour) {
  const l = figma.createLine();
  l.x = x; l.y = y; l.resize(Math.max(1, len - 3.6), 0); l.rotation = -90;
  l.strokes = [colour]; l.strokeWeight = 0.9; l.strokeCap = 'NONE';
  parent.appendChild(l);
  const h = figma.createPolygon();
  h.pointCount = 3; h.resize(3.6, 4.6); h.fills = [colour]; h.strokes = [];
  h.rotation = 180; h.x = x - 1.8; h.y = y + len - 4.6;
  parent.appendChild(h);
  return [l.id, h.id];
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
