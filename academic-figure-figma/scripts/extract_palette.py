"""Measure colours in a reference figure image (never guess them by eye).

Modes:
  palette  dominant colours by median-cut, with pixel share; --crop limits to
           one component so its fill/stroke/text trio comes back directly
  probe    median colour of a small patch at normalized (x,y) points; probe a
           block centre for its fill, its border midpoint for the stroke

Usage:
  uv run --with pillow python extract_palette.py palette ref.png -n 10
  uv run --with pillow python extract_palette.py palette ref.png --crop 0.0,0.1,0.25,0.5
  uv run --with pillow python extract_palette.py probe ref.png 0.07,0.20 0.78,0.15
"""

import argparse
import json
import sys

from PIL import Image

MAX_SIDE = 800  # downscale bound for palette mode


def load_image(path, crop=None):
    """Open as RGB; crop is normalized (x0,y0,x1,y1)."""
    img = Image.open(path).convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        w, h = img.size
        img = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    return img


def dominant_palette(img, n_colours, keep_white):
    """Median-cut palette as [{hex, share}] sorted by share.

    Near-white pixels are dropped BEFORE quantizing (figures are mostly white
    page background, which otherwise eats every median-cut bucket and leaves
    muddy averages); share is relative to the coloured pixels kept.
    """
    if max(img.size) > MAX_SIDE:
        k = MAX_SIDE / max(img.size)
        img = img.resize((int(img.width * k), int(img.height * k)))
    pixels = list(img.getdata())
    if not keep_white:
        pixels = [p for p in pixels if min(p) < 240]
    if not pixels:
        return []
    flat = Image.new("RGB", (len(pixels), 1))
    flat.putdata(pixels)
    quant = flat.quantize(colors=min(n_colours, len(pixels)), method=Image.Quantize.MEDIANCUT)
    pal = quant.getpalette()
    out = []
    for count, idx in sorted(quant.getcolors(), reverse=True):
        r, g, b = pal[3 * idx : 3 * idx + 3]
        out.append({"hex": f"#{r:02x}{g:02x}{b:02x}", "share": round(count / len(pixels), 4)})
    return out


def _patch_median(img, cx, cy, half):
    """Per-channel median of a (2*half+1)^2 patch centred at pixel (cx, cy)."""
    w, h = img.size
    vals = [
        img.getpixel((min(max(cx + dx, 0), w - 1), min(max(cy + dy, 0), h - 1)))
        for dx in range(-half, half + 1)
        for dy in range(-half, half + 1)
    ]
    return [sorted(c[i] for c in vals)[len(vals) // 2] for i in range(3)]


def probe_points(img, points, half=3):
    """Median patch colour at each normalized (x, y) point."""
    out = []
    for nx, ny in points:
        r, g, b = _patch_median(img, int(nx * img.width), int(ny * img.height), half)
        out.append({"at": [nx, ny], "hex": f"#{r:02x}{g:02x}{b:02x}"})
    return out


def parse_floats(text):
    """Parse 'a,b,...' into a tuple of floats."""
    return tuple(float(v) for v in text.split(","))


def main():
    """CLI entry point."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=["palette", "probe"])
    ap.add_argument("image")
    ap.add_argument("points", nargs="*", help="probe mode: x,y normalized 0-1")
    ap.add_argument("-n", type=int, default=10, help="palette size")
    ap.add_argument("--crop", type=parse_floats, help="x0,y0,x1,y1 normalized")
    ap.add_argument("--keep-white", action="store_true")
    args = ap.parse_args()

    img = load_image(args.image, args.crop)
    if args.mode == "palette":
        result = dominant_palette(img, args.n, args.keep_white)
    else:
        if not args.points:
            sys.exit("probe mode needs at least one x,y point")
        result = probe_points(img, [parse_floats(p) for p in args.points])
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
