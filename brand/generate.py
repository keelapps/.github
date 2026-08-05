#!/usr/bin/env python3
"""Generate keelapps brand assets: avatars (dark/light) and wordmarks.

The mark is drawn, not traced: every asset comes from the same `keel_mark`
function, so the stroke gauge and the intervals between waterline, hull, spine
and ballast stay identical at every size. Edit the geometry here, never in an
exported PNG.

Usage:
    pip install cairosvg
    python3 generate.py [output_dir]      # defaults to this file's directory
"""
import os
import shutil
import sys

import cairosvg

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

# Outfit must be installed for the wordmark to render correctly; without it
# cairosvg silently substitutes a default face and the lockup comes out wrong,
# with no error. Point FONT_SRC at a directory holding Outfit-Bold.ttf.
FONT_SRC = os.environ.get("FONT_SRC")
if FONT_SRC and os.path.isdir(FONT_SRC):
    fonts = os.path.expanduser("~/.fonts")
    os.makedirs(fonts, exist_ok=True)
    src = os.path.join(FONT_SRC, "Outfit-Bold.ttf")
    if os.path.exists(src):
        shutil.copy(src, fonts)
    os.system("fc-cache -f > /dev/null 2>&1")

NAVY = "#0F2536"
CREAM = "#F4EFE6"
CORAL = "#E8664A"
NAVY_SOFT = "#1C3A52"   # subtle above-water tint on dark
CREAM_SOFT = "#E5DECF"  # subtle above-water tint on light


def keel_mark(fg, accent, sw=34):
    """The mark: waterline, hull basin, keel spine, ballast bulb.
    Drawn in a 1024x1024 space, centered. Constant stroke gauge."""
    return f'''
    <g fill="none" stroke="{fg}" stroke-width="{sw}" stroke-linecap="round">
      <!-- waterline: two calm segments flanking the hull -->
      <path d="M 196 392 H 304"/>
      <path d="M 720 392 H 828"/>
      <!-- hull basin: hangs from the datum itself, faired deep curve -->
      <path d="M 352 392 C 360 584, 664 584, 672 392"/>
      <!-- keel spine (top hidden inside hull stroke band) -->
      <path d="M 512 552 V 648"/>
    </g>
    <!-- ballast bulb: the one warm point, where the weight lives -->
    <circle cx="512" cy="708" r="30" fill="{accent}"/>'''


def avatar_svg(bg, fg, accent, tint):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <rect width="1024" height="1024" fill="{bg}"/>
  <!-- above the waterline: vast calm, one tone lighter -->
  <rect width="1024" height="392" fill="{tint}" opacity="0.35"/>
  {keel_mark(fg, accent)}
</svg>'''


def wordmark_svg(fg):
    """Transparent lockup: mark + word, 1600x520.

    Two colourways, because a transparent asset has no background to guarantee
    contrast: navy for light surfaces, cream for dark ones. Shipping only the
    navy one makes the wordmark invisible in a dark-theme README.
    """
    mark = keel_mark(fg, CORAL, sw=26)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520">
  <g transform="translate(20,-58) scale(0.6)">{mark}</g>
  <g font-family="Outfit" fill="{fg}">
    <text x="660" y="322" font-size="150" font-weight="bold" letter-spacing="1">keelapps</text>
  </g>
</svg>'''


jobs = [
    ("avatar-dark.png", avatar_svg(NAVY, CREAM, CORAL, NAVY_SOFT), 1024),
    ("avatar-light.png", avatar_svg(CREAM, NAVY, CORAL, CREAM_SOFT), 1024),
    ("wordmark-transparent.png", wordmark_svg(NAVY), 1600),
    ("wordmark-transparent-cream.png", wordmark_svg(CREAM), 1600),
]

for name, svg, width in jobs:
    cairosvg.svg2png(
        bytestring=svg.encode(), write_to=os.path.join(OUT, name), output_width=width
    )
    print("wrote", name)
