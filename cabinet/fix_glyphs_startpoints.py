#!/usr/bin/env python3
"""
fix_glyphs_startpoints.py  --  Fix contour start-point and order alignment in .glyphs sources.

Operates directly on GSPath.nodes lists:
  1. Matches contours between masters by centroid distance.
  2. Reorders contour paths in non-reference layers to match reference order.
  3. Rotates each path's node list so the start node is as close as possible
     to the reference master's start node.

Nothing else is changed: no nodes are added, removed, or type-converted.
This is the correct way to fix .glyphs sources -- do not use normalize_master_ops
(which adds synthetic handles and converts lineTo→curveTo, distorting shapes).

Usage:
    .venv/bin/python cabinet/fix_glyphs_startpoints.py            # both roman & italic
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --roman
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --italic
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --dry-run
"""

import argparse
import sys
from pathlib import Path

import glyphsLib

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILES = {
    "roman":  REPO_ROOT / "glide-variable.glyphs",
    "italic": REPO_ROOT / "glide-variable-italic.glyphs",
}

OFFCURVE = "offcurve"


# ---------------------------------------------------------------------------
# Path geometry helpers
# ---------------------------------------------------------------------------

def path_centroid(path) -> tuple:
    """Average (x, y) of all on-curve nodes."""
    xs, ys = [], []
    for node in path.nodes:
        if node.type != OFFCURVE:
            xs.append(node.position.x)
            ys.append(node.position.y)
    if not xs:
        return (0.0, 0.0)
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def dist_sq(ax, ay, bx, by) -> float:
    return (ax - bx) ** 2 + (ay - by) ** 2


def centroid_mapping(ref_paths, other_paths) -> list:
    """
    Return mapping[i] = j such that other_paths[j] is the best centroid-match
    for ref_paths[i].  Assumes len(ref_paths) == len(other_paths).
    """
    ref_cens  = [path_centroid(p) for p in ref_paths]
    other_cens = [path_centroid(p) for p in other_paths]

    used: set = set()
    mapping: list = []
    for rx, ry in ref_cens:
        best_j, best_d = 0, float("inf")
        for j, (ox, oy) in enumerate(other_cens):
            if j in used:
                continue
            d = dist_sq(rx, ry, ox, oy)
            if d < best_d:
                best_d = d
                best_j = j
        mapping.append(best_j)
        used.add(best_j)
    return mapping


def find_rotation(ref_path, other_path) -> int:
    """
    Return the index in other_path.nodes of the on-curve node closest to
    ref_path's first on-curve node.  Returns 0 if already aligned.
    """
    # Target: first on-curve in reference path
    rx, ry = None, None
    for rn in ref_path.nodes:
        if rn.type != OFFCURVE:
            rx, ry = rn.position.x, rn.position.y
            break
    if rx is None:
        return 0

    best_i, best_d = 0, float("inf")
    for i, node in enumerate(other_path.nodes):
        if node.type == OFFCURVE:
            continue
        d = dist_sq(rx, ry, node.position.x, node.position.y)
        if d < best_d:
            best_d = d
            best_i = i
    return best_i


def rotate_path_nodes(path, rot: int) -> None:
    """Rotate path.nodes in-place so nodes[rot] becomes nodes[0]."""
    if rot == 0:
        return
    vals = path.nodes.values()   # mutable underlying list
    vals[:] = vals[rot:] + vals[:rot]


def _is_path(shape) -> bool:
    """True if shape is a GSPath (has nodes), not a component."""
    return hasattr(shape, "nodes") and not hasattr(shape, "component")


def reorder_layer_paths(layer, current_paths, mapping) -> None:
    """
    Reorder the GSPath objects within layer.shapes so they follow `mapping`.
    mapping[i] = j means: slot i should hold current_paths[j].
    """
    reordered = [current_paths[j] for j in mapping]
    shapes = list(layer.shapes)
    path_slots = [i for i, s in enumerate(shapes) if _is_path(s)]
    if len(path_slots) != len(reordered):
        return
    for slot, path in zip(path_slots, reordered):
        shapes[slot] = path
    layer.shapes = shapes


# ---------------------------------------------------------------------------
# Per-layer fix
# ---------------------------------------------------------------------------

def fix_layer(ref_layer, other_layer, dry_run: bool) -> tuple:
    """
    Align contours in other_layer to ref_layer.
    Returns (rotations_applied, reorders_applied).
    """
    ref_paths   = list(ref_layer.paths)
    other_paths = list(other_layer.paths)

    if not ref_paths or not other_paths:
        return 0, 0
    if len(ref_paths) != len(other_paths):
        return 0, 0  # different contour count -- skip silently

    mapping = centroid_mapping(ref_paths, other_paths)

    # Reorder if contour order differs
    reorders = 0
    if mapping != list(range(len(mapping))):
        if not dry_run:
            reorder_layer_paths(other_layer, other_paths, mapping)
        reorders = 1
        other_paths = [other_paths[j] for j in mapping]

    # Rotate start points
    rotations = 0
    for ref_p, other_p in zip(ref_paths, other_paths):
        if len(ref_p.nodes) != len(other_p.nodes):
            continue  # incompatible node count -- skip
        rot = find_rotation(ref_p, other_p)
        if rot != 0:
            if not dry_run:
                rotate_path_nodes(other_p, rot)
            rotations += 1

    return rotations, reorders


# ---------------------------------------------------------------------------
# Per-glyph fix
# ---------------------------------------------------------------------------

def fix_glyph(font, glyph_name: str, dry_run: bool) -> tuple:
    """Returns (total_rotations, total_reorders) across all non-reference masters."""
    glyph = font.glyphs[glyph_name]
    if glyph is None:
        return 0, 0

    master_ids = [m.id for m in font.masters]
    if len(master_ids) < 2:
        return 0, 0

    # Collect master layers (only the "real" master layers, not bracket/brace layers)
    layers = {}
    for layer in glyph.layers:
        if (layer.associatedMasterId in master_ids
                and layer.layerId == layer.associatedMasterId):
            layers[layer.associatedMasterId] = layer

    ref_id = master_ids[0]
    ref_layer = layers.get(ref_id)
    if ref_layer is None or not list(ref_layer.paths):
        return 0, 0

    total_rot = 0
    total_reorder = 0
    for mid in master_ids[1:]:
        other_layer = layers.get(mid)
        if other_layer is None:
            continue
        rot, reorder = fix_layer(ref_layer, other_layer, dry_run)
        total_rot += rot
        total_reorder += reorder

    return total_rot, total_reorder


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(path: Path, dry_run: bool) -> None:
    label = "DRY RUN: " if dry_run else ""
    print(f"\n{'='*60}")
    print(f"{label}Processing {path.name}")
    print("=" * 60)

    font = glyphsLib.load(str(path))
    total_rot     = 0
    total_reorder = 0
    changed_glyphs = 0

    for glyph in font.glyphs:
        rot, reorder = fix_glyph(font, glyph.name, dry_run)
        if rot or reorder:
            changed_glyphs += 1
            total_rot     += rot
            total_reorder += reorder

    print(f"  Glyphs touched:              {changed_glyphs}")
    print(f"  Start-point rotations:       {total_rot}")
    print(f"  Contour reorders:            {total_reorder}")

    if dry_run:
        print("  (dry-run — file not saved)")
    else:
        font.save(str(path))
        print(f"  Saved → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fix .glyphs contour start-point and order alignment (no node changes)"
    )
    parser.add_argument("--roman",   action="store_true", help="Process roman only")
    parser.add_argument("--italic",  action="store_true", help="Process italic only")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without saving")
    args = parser.parse_args()

    files = dict(SOURCE_FILES)
    if args.roman and not args.italic:
        files = {"roman": SOURCE_FILES["roman"]}
    elif args.italic and not args.roman:
        files = {"italic": SOURCE_FILES["italic"]}

    for path in files.values():
        if not path.exists():
            print(f"ERROR: {path} not found.")
            sys.exit(1)
        process_file(path, dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
