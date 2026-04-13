#!/usr/bin/env python3
"""
fix_glyphs_startpoints.py -- Fix Glyphs source compatibility from the .glyphs masters.

Pass 1 operates directly on GSPath.nodes:
  1. Match contours between masters with a structure-aware assignment.
  2. Reorder contour paths in non-reference layers when order differs.
  3. Rotate path.nodes so exact node-sequence matches are preferred when possible.

Pass 2 is intentionally narrow:
  4. Find the small residual set of glyphs that are still incompatible.
  5. Apply the existing topology normalizer only to those glyphs.

This keeps most edits as pure path reordering / start-point rotation in the
source file, and only adds nodes or changes types where compatibility still
cannot be achieved without topology edits.

Usage:
    .venv/bin/python cabinet/fix_glyphs_startpoints.py
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --roman
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --italic
    .venv/bin/python cabinet/fix_glyphs_startpoints.py --dry-run
"""

import argparse
import shutil
import sys
import tempfile
import uuid
from collections import Counter
from functools import lru_cache
from pathlib import Path

import glyphsLib
import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.varLib.interpolatable import test
from fontTools.varLib.models import normalizeLocation

from export_designspace import MASTER_UFO_DIR, export
from fix_source_files import fix_glyph, layer_to_ops, master_layers_for_glyph
from import_circular import verify_cubic_compat

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILES = {
    "roman": REPO_ROOT / "glide-variable.glyphs",
    "italic": REPO_ROOT / "glide-variable-italic.glyphs",
}

OFFCURVE = "offcurve"
ORDER_MISMATCH_PENALTY = 1_000_000.0


def _is_path(shape) -> bool:
    return hasattr(shape, "nodes") and not hasattr(shape, "component")


def path_node_signature(path) -> tuple[str, ...]:
    return tuple(str(node.type) for node in path.nodes)


def canonical_path_signature(path) -> tuple[str, ...]:
    sig = list(path_node_signature(path))
    if not sig:
        return ()
    n = len(sig)
    forward = {tuple(sig[i:] + sig[:i]) for i in range(n)}
    reverse_sig = sig[::-1]
    reverse = {tuple(reverse_sig[i:] + reverse_sig[:i]) for i in range(n)}
    return min(forward | reverse)


def path_centroid(path) -> tuple[float, float]:
    xs = []
    ys = []
    for node in path.nodes:
        if node.type == OFFCURVE:
            continue
        xs.append(node.position.x)
        ys.append(node.position.y)
    if not xs:
        return (0.0, 0.0)
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def path_bbox(path) -> tuple[float, float, float, float]:
    xs = [node.position.x for node in path.nodes]
    ys = [node.position.y for node in path.nodes]
    return (min(xs), min(ys), max(xs), max(ys))


def dist_sq(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def best_path_mapping(ref_paths, other_paths) -> list[int]:
    n = len(ref_paths)
    if n <= 1:
        return list(range(n))

    ref_signatures = [canonical_path_signature(path) for path in ref_paths]
    other_signatures = [canonical_path_signature(path) for path in other_paths]
    ref_centroids = [path_centroid(path) for path in ref_paths]
    other_centroids = [path_centroid(path) for path in other_paths]
    ref_bboxes = [path_bbox(path) for path in ref_paths]
    other_bboxes = [path_bbox(path) for path in other_paths]

    costs = [[0.0] * n for _ in range(n)]
    for ref_index in range(n):
        ref_bbox = ref_bboxes[ref_index]
        ref_width = ref_bbox[2] - ref_bbox[0]
        ref_height = ref_bbox[3] - ref_bbox[1]
        ref_scale = max(ref_width * ref_height, 1.0)

        for other_index in range(n):
            penalty = 0.0
            if ref_signatures[ref_index] != other_signatures[other_index]:
                penalty = ORDER_MISMATCH_PENALTY

            other_bbox = other_bboxes[other_index]
            centroid_cost = dist_sq(
                ref_centroids[ref_index],
                other_centroids[other_index],
            ) / ref_scale
            size_cost = abs(ref_width - (other_bbox[2] - other_bbox[0]))
            size_cost += abs(ref_height - (other_bbox[3] - other_bbox[1]))
            costs[ref_index][other_index] = penalty + centroid_cost + size_cost

    @lru_cache(None)
    def solve(ref_index: int, used_mask: int) -> tuple[float, tuple[int, ...]]:
        if ref_index == n:
            return (0.0, ())

        best_score = float("inf")
        best_mapping: tuple[int, ...] = ()
        for other_index in range(n):
            if used_mask & (1 << other_index):
                continue
            sub_score, sub_mapping = solve(ref_index + 1, used_mask | (1 << other_index))
            score = costs[ref_index][other_index] + sub_score
            if score < best_score:
                best_score = score
                best_mapping = (other_index,) + sub_mapping
        return (best_score, best_mapping)

    return list(solve(0, 0)[1])


def reorder_layer_paths(layer, current_paths, mapping) -> None:
    reordered = [current_paths[index] for index in mapping]
    shapes = list(layer.shapes)
    path_slots = [index for index, shape in enumerate(shapes) if _is_path(shape)]
    for slot, path in zip(path_slots, reordered):
        shapes[slot] = path
    layer.shapes = shapes


def reference_start(ref_path) -> tuple[float, float] | None:
    for node in ref_path.nodes:
        if node.type != OFFCURVE:
            return (node.position.x, node.position.y)
    return None


def rotated_signature(signature: tuple[str, ...], rotation: int) -> tuple[str, ...]:
    if not signature:
        return signature
    rotation %= len(signature)
    return signature[rotation:] + signature[:rotation]


def rotated_nodes(nodes: list, rotation: int) -> list:
    if not nodes:
        return nodes
    rotation %= len(nodes)
    return nodes[rotation:] + nodes[:rotation]


def rotations_for_signature(path, target_signature: tuple[str, ...]) -> list[int]:
    signature = path_node_signature(path)
    if len(signature) != len(target_signature):
        return []
    return [
        offset
        for offset in range(len(signature))
        if rotated_signature(signature, offset) == target_signature
    ]


def node_distance_cost(ref_nodes, other_nodes) -> float:
    total = 0.0
    for ref_node, other_node in zip(ref_nodes, other_nodes):
        total += dist_sq(
            (ref_node.position.x, ref_node.position.y),
            (other_node.position.x, other_node.position.y),
        )
    return total


def choose_group_rotations(paths: list) -> list[int] | None:
    if not paths:
        return []

    signatures = [path_node_signature(path) for path in paths]
    if len({len(signature) for signature in signatures}) != 1:
        return None

    candidate_signatures = {
        rotated_signature(signatures[0], offset)
        for offset in range(len(signatures[0]))
    }
    shared_signatures = []
    for target_signature in candidate_signatures:
        if all(rotations_for_signature(path, target_signature) for path in paths):
            shared_signatures.append(target_signature)

    if not shared_signatures:
        return None

    oncurve_first = [sig for sig in shared_signatures if sig and sig[0] != OFFCURVE]
    if oncurve_first:
        shared_signatures = oncurve_first

    base_nodes = list(paths[0].nodes)
    best_cost = float("inf")
    best_offsets: list[int] | None = None

    for target_signature in shared_signatures:
        for base_offset in rotations_for_signature(paths[0], target_signature):
            rotated_base = rotated_nodes(base_nodes, base_offset)
            offsets = [base_offset]
            total_cost = 0.0

            for path in paths[1:]:
                path_nodes = list(path.nodes)
                candidate_offsets = rotations_for_signature(path, target_signature)
                best_path_offset = min(
                    candidate_offsets,
                    key=lambda offset: node_distance_cost(
                        rotated_base,
                        rotated_nodes(path_nodes, offset),
                    ),
                )
                total_cost += node_distance_cost(
                    rotated_base,
                    rotated_nodes(path_nodes, best_path_offset),
                )
                offsets.append(best_path_offset)

            if total_cost < best_cost:
                best_cost = total_cost
                best_offsets = offsets

    return best_offsets


def rotation_cost(ref_nodes, other_nodes, offset: int) -> float:
    total = 0.0
    node_count = len(ref_nodes)
    for index, ref_node in enumerate(ref_nodes):
        other_node = other_nodes[(index + offset) % node_count]
        total += dist_sq(
            (ref_node.position.x, ref_node.position.y),
            (other_node.position.x, other_node.position.y),
        )
    return total


def find_rotation(ref_path, other_path) -> tuple[int, bool]:
    target = reference_start(ref_path)
    if target is None:
        return (0, False)

    ref_signature = path_node_signature(ref_path)
    nodes = list(other_path.nodes)

    exact_matches: list[tuple[float, int]] = []
    fallbacks: list[tuple[float, int]] = []
    for index, node in enumerate(nodes):
        rotated_signature = tuple(
            str(rotated.type) for rotated in (nodes[index:] + nodes[:index])
        )
        if rotated_signature == ref_signature:
            exact_matches.append((rotation_cost(list(ref_path.nodes), nodes, index), index))

        if node.type == OFFCURVE:
            continue
        distance = dist_sq((node.position.x, node.position.y), target)
        fallbacks.append((distance, index))

    if exact_matches:
        exact_matches.sort()
        return (exact_matches[0][1], True)

    if not fallbacks:
        return (0, False)

    fallbacks.sort()
    return (fallbacks[0][1], False)


def rotate_path_nodes(path, rotation: int) -> None:
    if rotation == 0:
        return
    values = path.nodes.values()
    values[:] = values[rotation:] + values[:rotation]


def fix_layer(ref_layer, other_layer) -> tuple[int, int, int]:
    ref_paths = list(ref_layer.paths)
    other_paths = list(other_layer.paths)

    if not ref_paths or not other_paths:
        return (0, 0, 0)
    if len(ref_paths) != len(other_paths):
        return (0, 0, 0)

    mapping = best_path_mapping(ref_paths, other_paths)
    reordered = 0
    if mapping != list(range(len(mapping))):
        reorder_layer_paths(other_layer, other_paths, mapping)
        reordered = 1
        other_paths = [other_paths[index] for index in mapping]

    rotations = 0
    exact_rotations = 0
    for ref_path, other_path in zip(ref_paths, other_paths):
        if len(ref_path.nodes) != len(other_path.nodes):
            continue
        rotation, used_exact_match = find_rotation(ref_path, other_path)
        if rotation != 0:
            rotate_path_nodes(other_path, rotation)
            rotations += 1
            if used_exact_match:
                exact_rotations += 1

    return (rotations, exact_rotations, reordered)


def align_contour_group(paths: list) -> tuple[int, int]:
    offsets = choose_group_rotations(paths)
    if offsets is None:
        return (0, 0)

    rotations = 0
    exact_rotations = 0
    for path, offset in zip(paths, offsets):
        if offset != 0:
            rotate_path_nodes(path, offset)
            rotations += 1
            exact_rotations += 1
    return (rotations, exact_rotations)


def fix_glyph_order_and_startpoints(font, glyph_name: str) -> tuple[int, int, int]:
    glyph = font.glyphs[glyph_name]
    if glyph is None:
        return (0, 0, 0)

    master_ids = [master.id for master in font.masters]
    if len(master_ids) < 2:
        return (0, 0, 0)

    layers = {}
    for layer in glyph.layers:
        if (
            layer.associatedMasterId in master_ids
            and layer.layerId == layer.associatedMasterId
        ):
            layers[layer.associatedMasterId] = layer

    ref_layer = layers.get(master_ids[0])
    if ref_layer is None or not list(ref_layer.paths):
        return (0, 0, 0)

    ordered_layers = [ref_layer]
    total_rotations = 0
    total_exact_rotations = 0
    total_reorders = 0
    for master_id in master_ids[1:]:
        other_layer = layers.get(master_id)
        if other_layer is None:
            continue
        rotations, exact_rotations, reordered = fix_layer(ref_layer, other_layer)
        total_rotations += rotations
        total_exact_rotations += exact_rotations
        total_reorders += reordered
        ordered_layers.append(other_layer)

    ref_paths = list(ref_layer.paths)
    for path_index in range(len(ref_paths)):
        grouped_paths = [layer.paths[path_index] for layer in ordered_layers]
        rotations, exact_rotations = align_contour_group(grouped_paths)
        total_rotations += rotations
        total_exact_rotations += exact_rotations

    return (total_rotations, total_exact_rotations, total_reorders)


def collect_incompatible_glyphs(font) -> list[str]:
    incompatible = []
    for glyph in font.glyphs:
        layers = master_layers_for_glyph(font, glyph.name)
        if len(layers) < 2:
            continue

        master_ops = {master_id: layer_to_ops(layer) for master_id, layer in layers.items()}
        if not any(master_ops.values()):
            continue
        if not verify_cubic_compat(master_ops):
            incompatible.append(glyph.name)
    return incompatible


def issue_type_name(issue) -> str:
    issue_type = issue["type"]
    return issue_type.name if hasattr(issue_type, "name") else str(issue_type)


def _cleanup_export_artifacts(ds_path: Path, prefix: str) -> None:
    if ds_path.exists():
        ds_path.unlink()
    for ufo_path in MASTER_UFO_DIR.glob(f"{prefix}_*.ufo"):
        if ufo_path.is_dir():
            shutil.rmtree(ufo_path)


def collect_interpolatable_issues(font, source_name: str, prefix: str) -> tuple[Counter, list[tuple[str, dict]]]:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / source_name
        font.save(str(temp_path))
        ds_path = export(temp_path, f"{prefix}.designspace", prefix)
        try:
            document = DesignSpaceDocument.fromfile(ds_path)
            axis_triples = {
                axis.name: (
                    axis.map_forward(axis.minimum),
                    axis.map_forward(axis.default),
                    axis.map_forward(axis.maximum),
                )
                for axis in document.axes
            }
            glyphsets = []
            names = []
            locations = []
            for source in document.sources:
                glyphsets.append(ufoLib2.Font.open(source.path, lazy=False).layers.defaultLayer)
                names.append(source.name)
                locations.append(normalizeLocation(source.location, axis_triples))
            problems = test(glyphsets, glyphs=None, names=names, locations=locations)
        finally:
            _cleanup_export_artifacts(ds_path, prefix)

    counts: Counter = Counter()
    wrong_start_points: list[tuple[str, dict]] = []
    for glyph_name, issues in problems.items():
        for issue in issues:
            issue_name = issue_type_name(issue)
            counts[issue_name] += 1
            if issue_name == "wrong_start_point":
                wrong_start_points.append((glyph_name, issue))
    return counts, wrong_start_points


def apply_pairwise_issue_rotation(font, glyph_name: str, issue: dict) -> bool:
    master_ids = [master.id for master in font.masters]
    master_index = int(issue["master_2_idx"])
    if master_index >= len(master_ids):
        return False

    glyph = font.glyphs[glyph_name]
    if glyph is None:
        return False

    target_master_id = master_ids[master_index]
    target_layer = next(
        (
            layer
            for layer in glyph.layers
            if layer.layerId == target_master_id and layer.associatedMasterId == target_master_id
        ),
        None,
    )
    if target_layer is None:
        return False

    contour_index = int(issue["contour"])
    if contour_index >= len(target_layer.paths):
        return False

    path = target_layer.paths[contour_index]
    values = path.nodes.values()
    if not values:
        return False

    rotation = int(issue["value_2"]) % len(values)
    if rotation == 0:
        return False
    values[:] = values[rotation:] + values[:rotation]
    return True


def refine_pairwise_startpoints(font, source_name: str, dry_run: bool) -> list[dict]:
    history: list[dict] = []
    normalized_reversed_glyphs: set[str] = set()

    for round_number in range(1, 8):
        prefix = f"pairwise_{Path(source_name).stem}_{round_number}_{uuid.uuid4().hex[:6]}"
        counts, wrong_start_points = collect_interpolatable_issues(font, source_name, prefix)
        history.append(
            {
                "round": round_number,
                "counts": dict(counts),
                "wrong_start_point": counts.get("wrong_start_point", 0),
            }
        )
        if not wrong_start_points:
            break

        changed = False

        for glyph_name, issue in wrong_start_points:
            if not issue.get("reversed") or glyph_name in normalized_reversed_glyphs:
                continue
            if fix_glyph(font, glyph_name, dry_run=False, force=True):
                normalized_reversed_glyphs.add(glyph_name)
                changed = True

        seen_rotations: set[tuple[str, int, int]] = set()
        for glyph_name, issue in wrong_start_points:
            if issue.get("reversed"):
                continue
            rotation_key = (
                glyph_name,
                int(issue["master_2_idx"]),
                int(issue["contour"]),
            )
            if rotation_key in seen_rotations:
                continue
            seen_rotations.add(rotation_key)
            if apply_pairwise_issue_rotation(font, glyph_name, issue):
                changed = True

        if not changed or dry_run:
            break

    return history


def process_file(path: Path, dry_run: bool) -> None:
    label = "DRY RUN: " if dry_run else ""
    print(f"\n{'=' * 60}")
    print(f"{label}Processing {path.name}")
    print("=" * 60)

    font = glyphsLib.load(str(path))

    changed_glyphs = 0
    total_rotations = 0
    total_exact_rotations = 0
    total_reorders = 0

    for glyph in font.glyphs:
        rotations, exact_rotations, reorders = fix_glyph_order_and_startpoints(font, glyph.name)
        if rotations or reorders:
            changed_glyphs += 1
            total_rotations += rotations
            total_exact_rotations += exact_rotations
            total_reorders += reorders

    print(f"  Glyphs touched in pass 1:    {changed_glyphs}")
    print(f"  Start-point rotations:       {total_rotations}")
    print(f"  Exact-sequence rotations:    {total_exact_rotations}")
    print(f"  Contour reorders:            {total_reorders}")

    incompatible_before = collect_incompatible_glyphs(font)
    print(f"  Residual incompatible glyphs before pass 2: {len(incompatible_before)}")
    if incompatible_before:
        print(f"    {', '.join(incompatible_before)}")

    topology_fixed = 0
    topology_failed = []
    for glyph_name in incompatible_before:
        if fix_glyph(font, glyph_name, dry_run=False, force=True):
            topology_fixed += 1
        else:
            topology_failed.append(glyph_name)

    incompatible_after = collect_incompatible_glyphs(font)
    print(f"  Glyphs normalized in pass 2: {topology_fixed}")
    print(f"  Residual incompatible glyphs after pass 2: {len(incompatible_after)}")
    if incompatible_after:
        print(f"    {', '.join(incompatible_after)}")
    if topology_failed:
        print(f"  Topology fixes that failed:  {', '.join(topology_failed)}")

    pairwise_history = refine_pairwise_startpoints(font, path.name, dry_run=dry_run)
    if pairwise_history:
        print("  Pairwise fontTools refinement:")
        for round_info in pairwise_history:
            counts = round_info["counts"]
            wrong = counts.get("wrong_start_point", 0)
            underweight = counts.get("underweight", 0)
            kink = counts.get("kink", 0)
            print(
                f"    round {round_info['round']}: "
                f"wrong_start_point={wrong} underweight={underweight} kink={kink}"
            )

    if dry_run:
        print("  (dry-run — file not saved)")
        return

    font.save(str(path))
    print(f"  Saved -> {path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix Glyphs contour order/start points and residual topology issues"
    )
    parser.add_argument("--roman", action="store_true", help="Process roman only")
    parser.add_argument("--italic", action="store_true", help="Process italic only")
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
            return 1
        process_file(path, dry_run=args.dry_run)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
