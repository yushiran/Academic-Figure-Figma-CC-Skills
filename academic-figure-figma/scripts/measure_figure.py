#!/usr/bin/env python3
"""Measure a figure the way a reader sees it: from the rendered pixels, never from node boxes.

    uv run --with pymupdf --with pillow --with numpy python scripts/measure_figure.py fig/fig2.pdf
    uv run ... measure_figure.py paper.pdf --figure 2          # a reference paper's Figure 2
    uv run ... measure_figure.py render.png --width 236   # a PNG render of a known column width

Reports, in points of the target column:

    ink %      fraction of pixels below 245 luminance. Flagship single-column method figures run
               8-37 % (BNF Fig. 2 8.3, FlowDPS Fig. 2 12.9, JiT Fig. 4 19.9, iMF Fig. 1 23.6,
               ARC Fig. 1 36.9). Under about 15 % the figure reads as empty.
    gutters    white margin left and right of the ink. Those same papers run 0-9 pt in a 236 pt
               column. A figure whose gutters exceed 10 pt looks narrower than the text block,
               which is the first thing a reader notices.
    aspect     width / height.

Every one of those reference numbers came from this script, not from a caption bbox: measuring the
text block that holds a caption gives the caption's width, which is the column, and says nothing
about where the artwork's ink actually starts. One such mis-measurement put a 19 pt gutter into the
style contract and left four figures visibly inset. Measure the render.
"""
import argparse
import re
import sys

# Each reader is imported where it is used, so a PNG measurement runs without pymupdf installed.
# pylint: disable=import-outside-toplevel


def ink_stats(gray, width_pt):
    """(ink fraction, left gutter, right gutter, top, bottom) in points, from a luminance array."""
    mask = gray < 245
    cols, rows = mask.any(0), mask.any(1)
    if not cols.any():
        return 0.0, width_pt / 2, width_pt / 2, 0.0, 0.0
    s = width_pt / gray.shape[1]
    l, r = int(cols.argmax()), gray.shape[1] - int(cols[::-1].argmax())
    t, b = int(rows.argmax()), gray.shape[0] - int(rows[::-1].argmax())
    return float(mask.mean()), l * s, (gray.shape[1] - r) * s, t * s, (gray.shape[0] - b) * s


def from_pdf(path, scale=8):
    """Page 1 of a figure PDF as a luminance array, with its size and its embedded font types."""
    import fitz
    import numpy as np
    d = fitz.open(path)
    p = d[0]
    pix = p.get_pixmap(matrix=fitz.Matrix(scale, scale))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return a[..., :3].mean(2), p.rect.width, p.rect.height, [f[2] for f in p.get_fonts()]


def from_paper_figure(path, fignum, scale=6):
    """The region of a reference paper between a `Figure N.` caption and the block above it."""
    import fitz
    import numpy as np
    d = fitz.open(path)
    for p in d:
        blocks = p.get_text("dict")["blocks"]
        for b in blocks:
            txt = "".join(s["text"] for l in b.get("lines", []) for s in l["spans"])
            if not re.match(rf"Figure {fignum}[.:]", txt):
                continue
            cap = b["bbox"]
            top = max((bb["bbox"][3] for bb in blocks
                       if bb["bbox"][3] <= cap[1] + 1 and bb["bbox"][1] > 40), default=45)
            clip = fitz.Rect(cap[0], top + 2, cap[2], cap[1] - 1)
            if clip.height < 25:                    # the block above is part of the figure
                clip = fitz.Rect(cap[0], max(45, cap[1] - 220), cap[2], cap[1] - 1)
            pix = p.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip)
            a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            return a[..., :3].mean(2), clip.width, clip.height, []
    raise SystemExit(f"no Figure {fignum} caption found in {path}")


def main():
    """Print the measurements, and exit non-zero on any reading the contract does not allow."""
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="a figure PDF, a PNG render, or a paper PDF with --figure")
    ap.add_argument("--figure", type=int,
                    help="measure Figure N of a reference paper instead of page 1")
    ap.add_argument("--width", type=float, default=236.0,
                    help="column width in points, for a PNG (default 236)")
    a = ap.parse_args()
    if a.figure:
        gray, w, h, fonts = from_paper_figure(a.path, a.figure)
    elif a.path.lower().endswith(".pdf"):
        gray, w, h, fonts = from_pdf(a.path)
    else:
        import numpy as np
        from PIL import Image
        gray = np.asarray(Image.open(a.path).convert("RGB")).mean(2)
        w, h, fonts = a.width, a.width * gray.shape[0] / gray.shape[1], []
    frac, gl, gr, gt, gb = ink_stats(gray, w)
    print(f"{a.path}")
    print(f"  page      {w:.1f} x {h:.1f} pt   aspect {w / h:.2f}")
    print(f"  ink       {frac * 100:.1f} %"
          + ("   LOW, reads as empty (flagships 8-37 %)" if frac < 0.15 else ""))
    print(f"  gutters   L {gl:.1f}  R {gr:.1f} pt"
          + ("   WIDE, flagships run 0-9 pt" if max(gl, gr) > 10 else ""))
    print(f"  margins   T {gt:.1f}  B {gb:.1f} pt")
    if fonts:
        bad = [f for f in fonts if f == "Type3"]
        print(f"  fonts     {sorted(set(fonts))}"
              + ("   FAIL: Type 3, outline the text before export" if bad else ""))
    else:
        print("  fonts     none (text outlined)")
    return 1 if (frac < 0.15 or max(gl, gr) > 10 or any(f == "Type3" for f in fonts)) else 0


if __name__ == "__main__":
    sys.exit(main())
