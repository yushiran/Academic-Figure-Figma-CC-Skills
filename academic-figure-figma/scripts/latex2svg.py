#!/usr/bin/env python3
"""Render a LaTeX math expression to an injectable SVG via matplotlib mathtext.

No TeX installation needed. Glyphs become vector paths (svg.fonttype defaults
to 'path'), so the result scales losslessly inside Figma. STIX fonts give a
Times-compatible look matching Tinos body text.

Usage:  python3 latex2svg.py 'W_k = \\exp(-R_k)' out.svg [fontsize] [#colour]
"""
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # pylint: disable=wrong-import-position


def render(latex, out_path, fontsize=10.0, colour="#212226"):
    """Write a tight, transparent SVG of `latex`; return cleaned SVG string."""
    matplotlib.rcParams["mathtext.fontset"] = "stix"
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${latex}$", fontsize=fontsize, color=colour)
    fig.savefig(out_path, format="svg", bbox_inches="tight",
                pad_inches=0.02, transparent=True)
    plt.close(fig)
    with open(out_path, encoding="utf-8") as f:
        svg = f.read()
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r'(?<![\w-])(width|height)="[^"]*"', "", svg, count=2)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return svg


def main():
    """CLI: latex2svg.py '<latex>' out.svg [fontsize] [#colour]."""
    size = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
    colour = sys.argv[4] if len(sys.argv) > 4 else "#212226"
    svg = render(sys.argv[1], sys.argv[2], size, colour)
    print(f"{sys.argv[2]}: {len(svg)} bytes")


if __name__ == "__main__":
    main()
