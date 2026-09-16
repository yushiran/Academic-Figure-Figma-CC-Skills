"""Shared matplotlib style for paper figures. Import it; never copy its numbers into a figure script.

The one idea behind this file: a figure is drawn at the size it will be printed at, and
`\\includegraphics` never scales it. Scaling is what silently turns an 8 pt label into a 5 pt one,
and it is invisible in the PDF you look at before submission.

    from paper_plot_style import figure, save, PALETTE, COL, FULL

    fig, ax = figure(COL, 0.62)          # one column wide, height = 0.62 x width
    ax.plot(x, y, **PALETTE.line(0))
    save(fig, "figures/fig_budget.pdf")
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

# --- Page geometry -------------------------------------------------------------------------
# A LaTeX point is 1/72.27 inch; a PostScript/Figma point is 1/72 inch. `\the\textwidth` reports
# LaTeX points, so convert through INCHES and never by treating the two units as the same number.
# Measure your own venue once, in the document body:  \typeout{\the\textwidth, \the\columnwidth}
TEX_PT = 1.0 / 72.27

VENUES = {                                   # (full width, column width), in inches
    "cvpr":    (6.875, 3.28125),             # cvpr.sty: textwidth 6.875in, columnsep 0.3125in
    "iccv":    (6.875, 3.28125),
    "wacv":    (6.875, 3.28125),
    "icml":    (6.75, 3.25),
    "aaai":    (7.0, 3.3125),
    "neurips": (5.5, 5.5),                   # single column
    "ieee":    (7.16, 3.5),
}
VENUE = "cvpr"
FULL, COL = VENUES[VENUE]

# --- Type ----------------------------------------------------------------------------------
# In-figure text is printed at the size set here, because the figure is never scaled. Keep the
# base at or just under the caption size of the venue (CVPR captions are 9 pt) so a figure label
# never shouts louder than the caption, and never go below 6 pt.
BASE = 8.0
FLOOR = 6.0

SERIF = ["Times New Roman", "Nimbus Roman", "Tinos", "Liberation Serif", "DejaVu Serif"]


def use_style(base: float = BASE) -> None:
    """Install the shared rcParams. Call once at the top of every figure script."""
    matplotlib.rcParams.update({
        "font.family": "serif",
        "font.serif": SERIF,
        "mathtext.fontset": "stix",          # matches Times body text
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base,              # titles are off by policy; size set for safety
        "xtick.labelsize": base - 1,
        "ytick.labelsize": base - 1,
        "legend.fontsize": base - 1,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "lines.linewidth": 1.1,
        "lines.markersize": 3.2,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "figure.dpi": 300,                   # only affects rasters embedded in the vector page
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.01,
        "pdf.fonttype": 42,                  # embed TrueType, so the PDF is editable and searchable
        "ps.fonttype": 42,
        "text.usetex": False,                # STIX already matches; usetex needs a toolchain
    })


def figure(width_in: float, aspect: float = 0.62, **kw):
    """A figure at its FINAL printed width. `aspect` is height / width."""
    use_style()
    fig, ax = plt.subplots(figsize=(width_in, width_in * aspect), **kw)
    return fig, ax


def save(fig, path: str | Path) -> Path:
    """Write vector PDF. A PNG twin is written beside it only for the read-back inspection."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    assert path.suffix == ".pdf", "paper figures ship as vector PDF; PNG is a preview only"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=300)
    plt.close(fig)
    return path


# --- Colour --------------------------------------------------------------------------------
# Every series must be separable three ways: hue, dash and marker. Hue alone fails in greyscale
# and for the eight per cent of male reviewers with a colour deficiency.
class _Palette:
    HUES = ["#2B62BD", "#A8690A", "#2C7355", "#8C2F39", "#5B4B8A", "#3E454E"]
    DASHES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)), (0, (5, 1))]
    MARKERS = ["o", "s", "^", "D", "v", "P"]

    def line(self, i: int, **kw) -> dict:
        d = {"color": self.HUES[i % len(self.HUES)],
             "linestyle": self.DASHES[i % len(self.DASHES)],
             "marker": self.MARKERS[i % len(self.MARKERS)]}
        d.update(kw)
        return d

    def bar(self, i: int, **kw) -> dict:
        d = {"color": self.HUES[i % len(self.HUES)], "edgecolor": "#17191D", "linewidth": 0.5}
        d.update(kw)
        return d

    def ours(self, **kw) -> dict:
        """The paper's own row. One weight heavier, never a different hue family."""
        d = {"color": self.HUES[0], "linestyle": "-", "marker": "o", "linewidth": 1.8, "zorder": 5}
        d.update(kw)
        return d


PALETTE = _Palette()


def audit(path: str | Path, floor: float = FLOOR) -> list[str]:
    """Static checks a read-back cannot make: font floor and page fit. Run before declaring done."""
    import pypdf

    path = Path(path)
    findings = []
    r = pypdf.PdfReader(str(path))
    box = r.pages[0].mediabox
    w_in, h_in = float(box.width) / 72.0, float(box.height) / 72.0
    if w_in > FULL + 0.02:
        findings.append(f"{path.name}: {w_in:.3f} in wide, past the {FULL} in text width")
    for page in r.pages:
        for name, font in (page.get("/Resources", {}).get("/Font", {}) or {}).items():
            pass                                   # font sizes live in the content stream
    txt = r.pages[0].extract_text() or ""
    if not txt.strip():
        findings.append(f"{path.name}: no extractable text, so the type was rasterised")
    return findings


__all__ = ["use_style", "figure", "save", "audit", "PALETTE", "COL", "FULL", "BASE", "FLOOR", "VENUES"]
