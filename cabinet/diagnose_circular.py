#!/usr/bin/env python3
"""
diagnose_circular.py — Verify cross-master compatibility AFTER full normalization.
Uses the exact same pipeline as import_circular.py.
"""

from pathlib import Path

import glyphsLib
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen

import sys
sys.path.insert(0, str(Path(__file__).parent))

from import_circular import (
    load_ttf, find_ttf_glyph, record_glyph,
    normalize_master_ops, count_segments, parse_contours,
    match_contours_to_reference,
    effective_structure, cubic_node_counts,
)

BASE_DIR = Path(__file__).parent
CIRCULAR_DIR = BASE_DIR / "circular"

ROMAN_TTF = {
    400: "lineto-circular-book.ttf",
    500: "lineto-circular-medium.ttf",
    700: "lineto-circular-bold.ttf",
    900: "lineto-circular-black.ttf",
}


def main():
    font = glyphsLib.load(str(BASE_DIR / "glide-variable.glyphs"))

    master_data = {}
    for master in font.masters:
        weight = int(master.axes[0])
        if weight not in ROMAN_TTF:
            continue
        ttf_path = CIRCULAR_DIR / ROMAN_TTF[weight]
        ttf_font, cmap, glyphset, upm = load_ttf(ttf_path)
        master_data[master.id] = (weight, cmap, glyphset)

    print(f"Loaded {len(master_data)} masters")

    total = ok = contour_count_mismatch = still_bad = 0
    bad_glyphs = []

    for glyph in font.glyphs:
        total += 1
        master_ttf_names = {mid: find_ttf_glyph(glyph, cmap, gs)
                            for mid, (_, cmap, gs) in master_data.items()}

        # Contour count check
        valid_structs = []
        for mid, ttf_name in master_ttf_names.items():
            if ttf_name:
                _, _, gs = master_data[mid]
                s = effective_structure(ttf_name, gs)
                if s is not None:
                    valid_structs.append(s)

        contour_counts = {len(s) for s in valid_structs}
        if len(contour_counts) > 1:
            contour_count_mismatch += 1
            continue

        # Record raw ops
        master_raw = {}
        for mid, ttf_name in master_ttf_names.items():
            if ttf_name:
                _, _, gs = master_data[mid]
                ops = record_glyph(ttf_name, gs)
                if ops:
                    master_raw[mid] = ops

        if len(master_raw) < 2:
            ok += 1
            continue

        # Run FULL normalization (same as import_circular.py)
        master_norm = normalize_master_ops(master_raw)
        if master_norm is None:
            still_bad += 1
            bad_glyphs.append((glyph.name, -1, {}, 0))  # failed normalization
            continue

        # Check post-normalization CUBIC node counts (the actual Glyphs.app metric)
        all_cubic_counts = {mid: tuple(cubic_node_counts(ops))
                            for mid, ops in master_norm.items()}
        if len(set(all_cubic_counts.values())) > 1:
            still_bad += 1
            # Build a per-weight summary for reporting
            w_segs = {master_data[mid][0]: sum(all_cubic_counts[mid])
                      for mid in all_cubic_counts}
            bad_glyphs.append((glyph.name, -1, w_segs, 0))
        else:
            ok += 1

    print(f"\n=== Post-Normalization Results ===")
    print(f"Total glyphs: {total}")
    print(f"Fully compatible: {ok}")
    print(f"Contour count mismatch (fallback): {contour_count_mismatch}")
    print(f"Still incompatible after full normalization: {still_bad}")

    if bad_glyphs:
        print(f"\n--- Remaining incompatibilities (post-normalization) ---")
        bad_glyphs.sort(key=lambda x: -(max(x[2].values(), default=0) - min(x[2].values(), default=0)))
        for gname, k, w_segs, *_ in bad_glyphs[:30]:
            deficit = (max(w_segs.values()) - min(w_segs.values())) if w_segs else -1
            print(f"  {gname:30s} contour {k}: {w_segs}  deficit={deficit}")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
