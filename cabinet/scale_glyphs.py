#!/usr/bin/env python3
"""
scale_glyphs.py — Zone-based piecewise-linear Y-axis scaling for Glide variable font.

Remaps glyph outlines from old metric coordinates to new Inter-proportioned metrics.

Control points (old_y -> new_y):
    -151  ->  -241    descender
       0  ->     0    baseline (fixed)
     481  ->   546    xHeight       (×1.1351 expansion)
     709  ->   728    capHeight     (×0.7982 compression)
     849  ->   969    ascender      (×1.7214 expansion)

X-coordinates and advance widths are unchanged.

Usage:
    .venv/bin/python scale_glyphs.py [--dry-run]
"""

import argparse
from pathlib import Path
import glyphsLib

CONTROL_POINTS = [
    (-151, -172),  # uniform scale (×1.1413) — avoids distortion at baseline
    (   0,    0),
    ( 481,  546),
    ( 709,  728),
    ( 849,  969),
]

FILES = [
    ("glide-variable.glyphs",        "glide-variable-scaled.glyphs"),
    ("glide-variable-italic.glyphs", "glide-variable-italic-scaled.glyphs"),
]

BASE_DIR = Path(__file__).parent


def scale_y(y: float) -> float:
    cp = CONTROL_POINTS
    # Extrapolate below minimum
    if y <= cp[0][0]:
        slope = (cp[1][1] - cp[0][1]) / (cp[1][0] - cp[0][0])
        return cp[0][1] + slope * (y - cp[0][0])
    # Extrapolate above maximum
    if y >= cp[-1][0]:
        slope = (cp[-1][1] - cp[-2][1]) / (cp[-1][0] - cp[-2][0])
        return cp[-2][1] + slope * (y - cp[-2][0])
    # Interpolate within range
    for i in range(len(cp) - 1):
        y0, y1 = cp[i][0], cp[i + 1][0]
        t0, t1 = cp[i][1], cp[i + 1][1]
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return t0 + t * (t1 - t0)
    raise RuntimeError(f"scale_y: no zone matched for y={y}")


def scale_font(input_path: Path, output_path: Path, dry_run: bool) -> None:
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Loading: {input_path.name}")
    font = glyphsLib.load(str(input_path))

    total_nodes = 0
    for glyph in font.glyphs:
        for layer in glyph.layers:
            for shape in layer.shapes:
                for node in shape.nodes:
                    node.position.y = round(scale_y(node.position.y), 3)
                    total_nodes += 1

    print(f"  Scaled {total_nodes:,} nodes across {len(font.glyphs)} glyphs, {len(font.masters)} masters")

    if not dry_run:
        font.save(str(output_path))
        print(f"  Saved -> {output_path.name}")
    else:
        print(f"  Would save -> {output_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print("Glide Y-axis scaler")
    print(f"Control points: {CONTROL_POINTS}")

    for src_name, dst_name in FILES:
        src = BASE_DIR / src_name
        dst = BASE_DIR / dst_name
        if not src.exists():
            print(f"\nWARN: {src_name} not found, skipping")
            continue
        scale_font(src, dst, dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
