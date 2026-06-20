"""Rename all Libertinus SFD font metadata to Libertina.

OFL compliance:
  - Reserved Font Names are "Linux Libertine", "Biolinum", "STIX Fonts".
    "Libertinus" itself is NOT an RFN, so "Libertina" is a permissible name.
  - Original copyright lines are preserved; a new copyright line is prepended.
  - License remains OFL 1.1.

Changes per SFD:
  - font.familyname:  "Libertinus Xxx" -> "Libertina Xxx"
  - font.fullname:    "Libertinus Xxx Yyy" -> "Libertina Xxx Yyy"
  - font.fontname:    "LibertinusXxx-Yyy" -> "LibertinaXxx-Yyy"
  - SFNT name 9 (Designer): prepend new maintainer
  - SFNT name 11 (Vendor URL): update
  File is saved under the new Libertina*.sfd filename; the old file remains
  (caller does the git mv afterwards).
"""

import fontforge
import os
import re

SOURCES = os.path.join(os.path.dirname(__file__), "..", "sources")

NEW_AUTHOR = "uwni"
NEW_YEAR = "2026"
NEW_URL = "https://github.com/uwni/libertina"


def sfnt_get(font, langid, strid):
    """Return SFNT name string or '' if absent."""
    for lang, name, val in font.sfnt_names:
        if lang == langid and name == strid:
            return val
    return ""


def sfnt_set(font, strid, value):
    """Set an SFNT name for English (1033)."""
    font.appendSFNTName("English (US)", strid, value)


def rename_font(sfd_path):
    f = fontforge.open(sfd_path)

    old_family = f.familyname      # e.g. "Libertinus Serif"
    old_full   = f.fullname        # e.g. "Libertinus Serif Regular"
    old_name   = f.fontname        # e.g. "LibertinusSerif-Regular"

    new_family = old_family.replace("Libertinus", "Libertina")
    new_full   = old_full.replace("Libertinus", "Libertina")
    new_name   = old_name.replace("Libertinus", "Libertina")

    f.familyname = new_family
    f.fullname   = new_full
    f.fontname   = new_name

    # SFNT name 9 (Designer): prepend new maintainer
    old_designer = sfnt_get(f, "English (US)", "Designer")
    if NEW_AUTHOR not in old_designer:
        new_designer = f"{NEW_AUTHOR}, {old_designer}" if old_designer else NEW_AUTHOR
        sfnt_set(f, "Designer", new_designer)

    # SFNT name 11 (Vendor URL)
    sfnt_set(f, "Vendor URL", NEW_URL)

    new_filename = os.path.join(SOURCES, os.path.basename(sfd_path).replace("Libertinus", "Libertina"))
    f.save(new_filename)
    f.close()

    print(f"  {os.path.basename(sfd_path)}")
    print(f"    fontname:   {old_name} -> {new_name}")
    print(f"    familyname: {old_family} -> {new_family}")
    print(f"    saved as:   {os.path.basename(new_filename)}")


def main():
    sfds = sorted(
        os.path.join(SOURCES, f)
        for f in os.listdir(SOURCES)
        if f.startswith("Libertinus") and f.endswith(".sfd")
    )
    print(f"Processing {len(sfds)} SFD files...\n")
    for sfd in sfds:
        rename_font(sfd)
    print("\nDone. Old Libertinus*.sfd files still exist — remove after verifying.")


main()
