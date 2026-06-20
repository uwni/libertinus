"""Scale math italic letters 8% wider in LibertinusMath-Regular.sfd.

Targets:
  U+1D434–U+1D467  Mathematical Italic Latin (A-Z, a-z)
  U+1D6E2–U+1D71B  Mathematical Italic Greek
  Plus their .ssty (script/superscript) variants by name.

FontForge's transform() correctly handles all per-glyph metrics:
advance width, ItalicCorrection, and TopAccentHorizontal are all scaled
automatically. Unset ItalicCorrection (sentinel 32767) is left unchanged.
"""

import fontforge
import psMat
import os

SFD = os.path.join(os.path.dirname(__file__), "..", "sources", "LibertinusMath-Regular.sfd")
SCALE = 1.08

ITALIC_RANGES = [
    (0x1D434, 0x1D467),  # Mathematical Italic Latin
    (0x1D6E2, 0x1D71B),  # Mathematical Italic Greek
]


def in_italic_range(codepoint):
    return any(lo <= codepoint <= hi for lo, hi in ITALIC_RANGES)


def is_target(glyph):
    cp = glyph.unicode
    if cp >= 0 and in_italic_range(cp):
        return True
    name = glyph.glyphname
    if "." in name:
        base = name.split(".")[0]
        if base.startswith("u") or base.startswith("U"):
            try:
                return in_italic_range(int(base[1:], 16))
            except ValueError:
                pass
    return False


def main():
    f = fontforge.open(SFD)
    matrix = psMat.scale(SCALE, 1.0)

    scaled = []
    for glyph in f.glyphs():
        if not is_target(glyph):
            continue
        glyph.transform(matrix)
        scaled.append(glyph.glyphname)

    print(f"Scaled {len(scaled)} glyphs:")
    for name in scaled:
        print(f"  {name}")

    f.save(SFD)
    print(f"\nSaved to {SFD}")
    f.close()


main()
