#!/usr/bin/env python3
"""
export_designspace.py — Convert a .glyphs source to UFOs + designspace,
fixing the axis range that glyphsLib mis-computes.

The glyphsLib to_designspace() call emits a broken axis definition
(min=max=default=400, avar map=[(400,900)]) because it confuses instance
axesValues with avar mapping points. This script corrects the axis before
writing the designspace so fontmake can build a proper variable font.

Usage:
    cd <repo-root> && .venv/bin/python cabinet/export_designspace.py
    # Then build variable font:
    cd <repo-root> && .venv/bin/fontmake -m master_ufo/Glide.designspace \
        -o variable --keep-overlaps --output-dir cabinet/input/roman/

    # For italic:
    cd <repo-root> && .venv/bin/python cabinet/export_designspace.py --italic
    .venv/bin/fontmake -m master_ufo/GlideItalic.designspace \
        -o variable --keep-overlaps --output-dir cabinet/input/italic/
"""

import argparse
import shutil
from pathlib import Path

import glyphsLib
import ufoLib2
from glyphsLib.builder import to_designspace

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_UFO_DIR = REPO_ROOT / "master_ufo"


def fix_designspace_axis(ds):
    """
    Correct the wght axis definition.

    glyphsLib sets min=max=default=400 with a broken avar map.
    The correct definition is inferred from the source locations.
    """
    for axis in ds.axes:
        if axis.tag != "wght":
            continue
        # Collect all design-space locations for this axis
        locs = []
        for src in ds.sources:
            val = src.location.get(axis.name) or src.location.get(axis.tag)
            if val is not None:
                locs.append(val)
        if not locs:
            continue
        axis.minimum = min(locs)
        axis.maximum = max(locs)
        default_candidates = []
        for src in ds.sources:
            if src.layerName is not None:
                continue
            val = src.location.get(axis.name) or src.location.get(axis.tag)
            if val is not None:
                default_candidates.append(val)
        if default_candidates:
            ordered_defaults = sorted(default_candidates)
            axis.default = ordered_defaults[len(ordered_defaults) // 2]
        else:
            axis.default = min(locs)
        axis.map = []   # drop incorrect avar mapping
        print(f"  Fixed {axis.tag}: min={axis.minimum} default={axis.default} max={axis.maximum}")


def export(glyphs_path: Path, ds_name: str, ufo_prefix: str) -> Path:
    print(f"Loading {glyphs_path.name}...")
    font = glyphsLib.load(str(glyphs_path))

    print("Converting to designspace + UFOs...")
    ds = to_designspace(font, ufo_module=ufoLib2)

    fix_designspace_axis(ds)

    # Write UFOs to master_ufo/
    MASTER_UFO_DIR.mkdir(exist_ok=True)
    for src in ds.sources:
        # Sanitise the source name for filesystem use
        safe_name = src.name.replace(" ", "_").replace("/", "_")
        ufo_filename = f"{ufo_prefix}_{safe_name}.ufo"
        ufo_path = MASTER_UFO_DIR / ufo_filename
        if ufo_path.exists():
            shutil.rmtree(ufo_path)
        print(f"  Saving {ufo_filename}...")
        src.font.save(str(ufo_path))
        src.filename = ufo_filename
        src.path = str(ufo_path)

    ds_path = MASTER_UFO_DIR / ds_name
    ds.write(str(ds_path))
    print(f"  Designspace written: {ds_path}")
    return ds_path


def main():
    parser = argparse.ArgumentParser(description="Export .glyphs → UFO + designspace")
    parser.add_argument("--italic", action="store_true", help="Export italic source")
    args = parser.parse_args()

    if args.italic:
        glyphs_path = REPO_ROOT / "glide-variable-italic.glyphs"
        ds_name = "GlideItalic.designspace"
        ufo_prefix = "GlideItalic"
    else:
        glyphs_path = REPO_ROOT / "glide-variable.glyphs"
        ds_name = "Glide.designspace"
        ufo_prefix = "Glide"

    ds_path = export(glyphs_path, ds_name, ufo_prefix)
    print(f"\nDone. Now run:")
    print(f"  .venv/bin/fontmake -m {ds_path} -o variable --keep-overlaps --output-dir cabinet/input/{'italic' if args.italic else 'roman'}/")


if __name__ == "__main__":
    main()
