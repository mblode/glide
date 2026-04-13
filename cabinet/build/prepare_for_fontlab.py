#!/usr/bin/env python3
"""Prepare static TTF masters for FontLab 8 import.

Runs the full 4-master repair chain on ALL glyphs (not just specimen text),
maximizing automatic compatibility fixes before manual Matchmaker work.

Outputs:
  - Repaired TTFs in build/work/fontlab-ready/
  - Detailed compatibility report in build/work/reports/fontlab/fontlab-prep-report.json
  - Markdown summary at build/work/reports/fontlab/fontlab-prep-summary.md
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter
from math import hypot
from pathlib import Path

from fontTools.misc.bezierTools import approximateQuadraticArcLength
from fontTools.pens.basePen import decomposeQuadraticSegment
from fontTools.pens.recordingPen import DecomposingRecordingPen, RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

from source_manifest import load_source_config

ROMAN_MASTERS = [
    ("lineto-circular-book.ttf", "Regular", 400),
    ("lineto-circular-medium.ttf", "Medium", 500),
    ("lineto-circular-bold.ttf", "Bold", 700),
    ("lineto-circular-black.ttf", "Black", 900),
]

ITALIC_MASTERS = [
    ("lineto-circular-bookItalic.ttf", "Regular Italic", 400),
    ("lineto-circular-mediumItalic.ttf", "Medium Italic", 500),
    ("lineto-circular-boldItalic.ttf", "Bold Italic", 700),
    ("lineto-circular-blackItalic.ttf", "Black Italic", 900),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare 4-master TTFs for FontLab 8 by auto-repairing all possible glyphs."
    )
    parser.add_argument(
        "--sample-dir",
        default="build/work/sources/glide-root-derived",
        help="Directory containing the static TTF masters.",
    )
    parser.add_argument(
        "--manifest",
        help="Optional JSON source manifest describing the master sets to repair.",
    )
    parser.add_argument(
        "--output-dir",
        default="build/work/fontlab-ready",
        help="Directory for repaired TTFs.",
    )
    parser.add_argument(
        "--reports-dir",
        default="build/work/reports/fontlab",
        help="Directory for compatibility and summary reports.",
    )
    parser.add_argument(
        "--skip-italic",
        action="store_true",
        help="Only process roman masters.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing outputs.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Glyph parsing (reused from repair_reference_topology.py)
# ---------------------------------------------------------------------------

def parse_contours(font: TTFont, glyph_name: str) -> list[list[tuple]]:
    pen = RecordingPen()
    font.getGlyphSet()[glyph_name].draw(pen)
    contours: list[list[tuple]] = []
    segments: list[tuple] = []
    start = None
    current = None

    for op, args in pen.value:
        if op == "moveTo":
            if segments:
                contours.append(segments)
                segments = []
            start = args[0]
            current = start
        elif op == "lineTo":
            point = args[0]
            segments.append(("line", current, point))
            current = point
        elif op == "qCurveTo":
            for control, end in decomposeQuadraticSegment(args):
                segments.append(("quad", current, control, end))
                current = end
        elif op == "closePath":
            if current != start:
                segments.append(("line", current, start))
            contours.append(segments)
            segments = []

    if segments:
        contours.append(segments)
    return contours


def segment_length(segment: tuple) -> float:
    if segment[0] == "line":
        _, a, b = segment
        return hypot(b[0] - a[0], b[1] - a[1])
    _, a, c, b = segment
    return approximateQuadraticArcLength(a, c, b)


def sample_group(segments: list[tuple]) -> list[tuple[float, float]]:
    samples: list[tuple[float, float]] = []
    for seg in segments:
        if seg[0] == "line":
            _, a, b = seg
            samples.extend([a, ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5), b])
        else:
            _, a, c, b = seg
            samples.extend([a, ((a[0] + 2 * c[0] + b[0]) * 0.25, (a[1] + 2 * c[1] + b[1]) * 0.25), b])
    return samples


def contour_area(points: list[tuple[float, float]]) -> float:
    total = 0.0
    for i, p in enumerate(points):
        n = points[(i + 1) % len(points)]
        total += p[0] * n[1] - n[0] * p[1]
    return total * 0.5


def contour_centroid(points: list[tuple[float, float]]) -> tuple[float, float]:
    xs = sum(p[0] for p in points)
    ys = sum(p[1] for p in points)
    return (xs / len(points), ys / len(points))


# ---------------------------------------------------------------------------
# Contour ordering and matching
# ---------------------------------------------------------------------------

def choose_contour_permutation(
    base_contours: list[list[tuple[float, float]]],
    candidate_contours: list[list[tuple[float, float]]],
) -> list[int]:
    if len(base_contours) <= 1:
        return list(range(len(candidate_contours)))

    best_cost = None
    best_perm = list(range(len(candidate_contours)))

    def _perms(items: list[int]) -> list[list[int]]:
        if len(items) <= 1:
            return [items]
        result = []
        for i, item in enumerate(items):
            for rest in _perms(items[:i] + items[i + 1:]):
                result.append([item, *rest])
        return result

    # For large contour counts, use scipy Hungarian instead of brute force
    n = len(candidate_contours)
    if n > 6:
        try:
            from scipy.optimize import linear_sum_assignment
            cost_matrix = []
            for bi in range(n):
                row = []
                bc = contour_centroid(base_contours[bi])
                ba = abs(contour_area(base_contours[bi]))
                for ci in range(n):
                    cc = contour_centroid(candidate_contours[ci])
                    ca = abs(contour_area(candidate_contours[ci]))
                    row.append(hypot(bc[0] - cc[0], bc[1] - cc[1]) + abs(ba - ca) * 0.001)
                cost_matrix.append(row)
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            return list(col_ind)
        except ImportError:
            pass

    for perm in _perms(list(range(n))):
        cost = 0.0
        for bi, ci in enumerate(perm):
            bc = contour_centroid(base_contours[bi])
            cc = contour_centroid(candidate_contours[ci])
            cost += hypot(bc[0] - cc[0], bc[1] - cc[1])
            cost += abs(abs(contour_area(base_contours[bi])) - abs(contour_area(candidate_contours[ci]))) * 0.001
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_perm = perm

    return best_perm


def ordered_contours(reference: list[list[tuple]], candidate: list[list[tuple]]) -> list[list[tuple]]:
    ref_pts = [sample_group(c) for c in reference]
    cand_pts = [sample_group(c) for c in candidate]
    perm = choose_contour_permutation(ref_pts, cand_pts)
    return [candidate[i] for i in perm]


# ---------------------------------------------------------------------------
# Segment manipulation
# ---------------------------------------------------------------------------

def rotate_segments(segments: list[tuple], start: int) -> list[tuple]:
    return segments[start:] + segments[:start]


def reverse_contour_segments(segments: list[tuple]) -> list[tuple]:
    rev = []
    for seg in reversed(segments):
        if seg[0] == "line":
            _, a, b = seg
            rev.append(("line", b, a))
        else:
            _, a, c, b = seg
            rev.append(("quad", b, c, a))
    return rev


def cost_group(source_group: list[tuple], target_segment: tuple, scale: float) -> float:
    src = sample_group(source_group)
    tgt = sample_group([target_segment])
    so = src[0]
    to = tgt[0]
    total = 0.0
    for i in range(min(len(src), len(tgt))):
        s = ((src[i][0] - so[0]) / scale, (src[i][1] - so[1]) / scale)
        t = ((tgt[i][0] - to[0]) / scale, (tgt[i][1] - to[1]) / scale)
        total += (s[0] - t[0]) ** 2 + (s[1] - t[1]) ** 2
    types = tuple(seg[0] for seg in source_group)
    if len(types) == 1 and types[0] != target_segment[0]:
        total += 0.05
    return total


def split_quad(seg: tuple, t: float) -> tuple[tuple, tuple]:
    _, p0, p1, p2 = seg
    p01 = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
    p12 = (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
    p012 = (p01[0] + (p12[0] - p01[0]) * t, p01[1] + (p12[1] - p01[1]) * t)
    return ("quad", p0, p01, p012), ("quad", p012, p12, p2)


def split_line(seg: tuple, t: float) -> tuple[tuple, tuple]:
    _, p0, p1 = seg
    mid = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
    return ("line", p0, mid), ("line", mid, p1)


def split_segment_at(seg: tuple, t: float) -> tuple[tuple, tuple]:
    return split_quad(seg, t) if seg[0] == "quad" else split_line(seg, t)


def split_segment_many(seg: tuple, ratios: list[float]) -> list[tuple]:
    if not ratios:
        return [seg]
    parts: list[tuple] = []
    remainder = seg
    consumed = 0.0
    total = sum(ratios)
    if total <= 0:
        return [seg]
    for ratio in ratios[:-1]:
        rem_share = 1.0 - consumed
        if rem_share <= 0:
            break
        local_t = (ratio / total) / rem_share
        first, remainder = split_segment_at(remainder, local_t)
        parts.append(first)
        consumed += ratio / total
    parts.append(remainder)
    return parts


def line_as_quad(seg: tuple) -> tuple:
    _, p0, p1 = seg
    mid = ((p0[0] + p1[0]) * 0.5, (p0[1] + p1[1]) * 0.5)
    return ("quad", p0, mid, p1)


def quad_as_line(seg: tuple, tolerance: float = 0.001) -> tuple | None:
    _, p0, c, p1 = seg
    scale = max(1.0, hypot(p1[0] - p0[0], p1[1] - p0[1]))
    expected = ((p0[0] + p1[0]) * 0.5, (p0[1] + p1[1]) * 0.5)
    dev = hypot(c[0] - expected[0], c[1] - expected[1]) / scale
    if dev > tolerance:
        return None
    return ("line", p0, p1)


def coerce_segment(seg: tuple, desired: str) -> tuple | None:
    if seg[0] == desired:
        return seg
    if seg[0] == "line" and desired == "quad":
        return line_as_quad(seg)
    if seg[0] == "quad" and desired == "line":
        return quad_as_line(seg)
    return None


# ---------------------------------------------------------------------------
# Core repair: match contours between adjacent masters and rebuild
# ---------------------------------------------------------------------------

def repair_pair(source_segments: list[tuple], target_segments: list[tuple]) -> list[tuple] | None:
    scale = sum(segment_length(seg) for seg in source_segments)
    if scale <= 0:
        scale = 1.0
    best = None
    max_group = min(4, len(source_segments))

    for do_reverse in (False, True):
        candidate = reverse_contour_segments(target_segments) if do_reverse else target_segments
        for shift in range(len(candidate)):
            rotated = rotate_segments(candidate, shift)
            sc = len(source_segments)
            tc = len(rotated)
            inf = float("inf")
            costs = [[inf] * (tc + 1) for _ in range(sc + 1)]
            back = [[None] * (tc + 1) for _ in range(sc + 1)]
            costs[0][0] = 0.0

            for si in range(sc + 1):
                for ti in range(tc):
                    if costs[si][ti] == inf:
                        continue
                    for gs in range(1, max_group + 1):
                        if si + gs > sc:
                            break
                        c = costs[si][ti] + cost_group(source_segments[si:si + gs], rotated[ti], scale)
                        if c < costs[si + gs][ti + 1]:
                            costs[si + gs][ti + 1] = c
                            back[si + gs][ti + 1] = (si, ti, gs)

            if costs[sc][tc] != inf:
                if best is None or costs[sc][tc] < best[0]:
                    best = (costs[sc][tc], rotated, back)

    if best is None:
        return None

    _, rotated, back = best
    si, ti = len(source_segments), len(rotated)
    groups: list[tuple[int, int]] = []
    while si > 0 and ti > 0:
        psi, pti, gs = back[si][ti]
        groups.append((pti, gs))
        si, ti = psi, pti
    groups.reverse()

    repaired: list[tuple] = []
    si = 0
    for ti, gs in groups:
        tseg = rotated[ti]
        if gs == 1:
            coerced = coerce_segment(tseg, source_segments[si][0])
            if coerced is None:
                return None
            repaired.append(coerced)
        else:
            sgroup = source_segments[si:si + gs]
            ratios = [segment_length(s) for s in sgroup]
            parts = split_segment_many(tseg, ratios)
            if len(parts) != gs:
                return None
            for part, sseg in zip(parts, sgroup):
                coerced = coerce_segment(part, sseg[0])
                if coerced is None:
                    return None
                repaired.append(coerced)
        si += gs

    return repaired


def build_glyph(contours: list[list[tuple]]):
    pen = TTGlyphPen(None)
    for contour in contours:
        pen.moveTo(contour[0][1])
        for seg in contour:
            if seg[0] == "line":
                pen.lineTo(seg[2])
            else:
                pen.qCurveTo(seg[2], seg[3])
        pen.closePath()
    return pen.glyph()


def repair_glyph_chain(fonts: list[TTFont], glyph_name: str) -> bool:
    """Repair a single glyph across all masters using the chain approach.

    Returns True if the glyph was successfully made compatible across all masters.
    """
    contours_by_master = [parse_contours(f, glyph_name) for f in fonts]
    counts = {len(c) for c in contours_by_master}
    if len(counts) != 1:
        return False
    if counts == {0}:
        return True

    # Choose the pivot master (most complex outline, prefer middle masters for stability)
    pivot = max(
        range(len(fonts)),
        key=lambda i: (sum(len(c) for c in contours_by_master[i]), -abs(i - 1.5)),
    )

    ordered = [None] * len(fonts)
    ordered[pivot] = contours_by_master[pivot]
    for i in range(pivot - 1, -1, -1):
        ordered[i] = ordered_contours(ordered[i + 1], contours_by_master[i])
    for i in range(pivot + 1, len(fonts)):
        ordered[i] = ordered_contours(ordered[i - 1], contours_by_master[i])

    n_contours = len(ordered[pivot])
    results: list[list[list[tuple] | None]] = [[None] * n_contours for _ in range(len(fonts))]

    for ci in range(n_contours):
        seg_counts = [len(ordered[i][ci]) for i in range(len(fonts))]
        cpivot = max(range(len(fonts)), key=lambda i: (seg_counts[i], -abs(i - 1.5)))
        results[cpivot][ci] = ordered[cpivot][ci]

        for i in range(cpivot - 1, -1, -1):
            repaired = repair_pair(results[i + 1][ci], ordered[i][ci])
            if repaired is None:
                return False
            results[i][ci] = repaired

        for i in range(cpivot + 1, len(fonts)):
            repaired = repair_pair(results[i - 1][ci], ordered[i][ci])
            if repaired is None:
                return False
            results[i][ci] = repaired

    for mi, font in enumerate(fonts):
        glyph = build_glyph(results[mi])
        glyph.recalcBounds(font["glyf"])
        font["glyf"][glyph_name] = glyph

    return True


# ---------------------------------------------------------------------------
# Normalization: common glyph set, decompose composites
# ---------------------------------------------------------------------------

def common_glyph_order(fonts: list[TTFont]) -> list[str]:
    base_order = fonts[0].getGlyphOrder()
    common = set(base_order)
    for f in fonts[1:]:
        common &= set(f.getGlyphOrder())
    return [g for g in base_order if g in common]


def subset_to_glyphs(font: TTFont, glyph_names: list[str]) -> None:
    opts = Options()
    opts.glyph_names = True
    opts.hinting = False
    opts.layout_closure = False
    sub = Subsetter(opts)
    sub.populate(glyphs=glyph_names)
    sub.subset(font)


def decompose_composites(font: TTFont) -> int:
    glyf = font["glyf"]
    count = 0
    for name in font.getGlyphOrder():
        g = glyf[name]
        if not g.isComposite():
            continue
        rec = DecomposingRecordingPen(font.getGlyphSet())
        font.getGlyphSet()[name].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(pen)
        new_g = pen.glyph()
        if new_g.numberOfContours >= 0:
            new_g.recalcBounds(glyf)
        glyf[name] = new_g
        count += 1
    return count


# ---------------------------------------------------------------------------
# Compatibility check via fonttools interpolatable
# ---------------------------------------------------------------------------

SEVERE_ISSUES = {"missing", "node_count", "path_count", "open_path"}
MODERATE_ISSUES = {"contour_order", "node_incompatibility", "nothing", "underweight", "overweight", "wrong_start_point"}


def run_compat_check(font_paths: list[Path], report_path: Path) -> dict:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "fontTools.varLib.interpolatable",
        *[str(p) for p in font_paths],
        "--json", "--output", str(report_path),
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=False)

    if not report_path.exists():
        return {}
    return json.loads(report_path.read_text())


def summarize_compat(data: dict) -> dict:
    types = Counter()
    severity = Counter()
    for issues in data.values():
        for issue in issues:
            t = issue.get("type", "unknown")
            types[t] += 1
            if t in SEVERE_ISSUES:
                severity["severe"] += 1
            elif t in MODERATE_ISSUES:
                severity["moderate"] += 1
            else:
                severity["cosmetic"] += 1
    return {
        "glyphs_with_issues": len(data),
        "issue_types": dict(types),
        "severity": dict(severity),
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_family(
    family_key: str,
    masters: list[tuple[str, str, int]],
    sample_dir: Path,
    output_dir: Path,
    reports_dir: Path,
    force: bool,
) -> dict:
    print(f"\n{'=' * 60}")
    print(f"Processing {family_key} family (4 masters)")
    print(f"{'=' * 60}")

    # Step 1: Copy masters
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, _, _ in masters:
        src = sample_dir / filename
        dst = output_dir / filename
        if force or not dst.exists():
            shutil.copy2(src, dst)

    # Step 2: Load and normalize (common glyph set + decompose composites)
    print("Step 1: Normalizing masters (common glyphs, decompose composites)...")
    fonts = [TTFont(output_dir / fn, recalcBBoxes=False, recalcTimestamp=False) for fn, _, _ in masters]
    order = common_glyph_order(fonts)
    common_count = len(order)
    print(f"  Common glyph set: {common_count} glyphs")

    decomposed_counts = {}
    for (fn, _, _), font in zip(masters, fonts):
        subset_to_glyphs(font, order)
        dc = decompose_composites(font)
        subset_to_glyphs(font, order)
        decomposed_counts[fn] = dc
        if dc > 0:
            print(f"  {fn}: decomposed {dc} composites")

    for (fn, _, _), font in zip(masters, fonts):
        font.save(output_dir / fn)

    # Step 3: Before-repair compatibility check
    print("Step 2: Running pre-repair compatibility check...")
    font_paths = [output_dir / fn for fn, _, _ in masters]
    before_report_path = reports_dir / f"{family_key}-pre-repair-compat.json"
    before_data = run_compat_check(font_paths, before_report_path)
    before_summary = summarize_compat(before_data)
    print(f"  Before repair: {before_summary.get('glyphs_with_issues', 0)} glyphs with issues")
    if before_summary.get("severity"):
        for sev, count in sorted(before_summary["severity"].items()):
            print(f"    {sev}: {count}")

    # Step 4: Run 4-master repair chain on ALL glyphs
    print("Step 3: Running 4-master repair chain on all glyphs...")
    fonts = [TTFont(output_dir / fn, recalcBBoxes=False, recalcTimestamp=False) for fn, _, _ in masters]

    all_glyphs = [g for g in fonts[0].getGlyphOrder() if g != ".notdef"]
    repaired = []
    skipped_path_count = []  # different contour counts — needs FontLab
    skipped_error = []  # repair failed — needs FontLab
    already_ok = []  # was already compatible

    for i, glyph_name in enumerate(all_glyphs):
        if (i + 1) % 50 == 0:
            print(f"  Processing glyph {i + 1}/{len(all_glyphs)}...")

        # Check if already compatible (same contour & segment counts)
        contours = [parse_contours(f, glyph_name) for f in fonts]
        contour_counts = {len(c) for c in contours}

        if contour_counts == {0}:
            already_ok.append(glyph_name)
            continue

        if len(contour_counts) != 1:
            skipped_path_count.append({
                "glyph": glyph_name,
                "contour_counts": {fn: len(c) for (fn, _, _), c in zip(masters, contours)},
            })
            continue

        # Check if segment counts already match
        seg_counts_per_contour = []
        for ci in range(list(contour_counts)[0]):
            seg_counts_per_contour.append({fn: len(contours[mi][ci]) for mi, (fn, _, _) in enumerate(masters)})

        all_match = all(len(set(sc.values())) == 1 for sc in seg_counts_per_contour)
        if all_match:
            # Quick check: are types also the same?
            type_match = True
            for ci in range(list(contour_counts)[0]):
                for mi in range(1, len(fonts)):
                    if len(contours[mi][ci]) != len(contours[0][ci]):
                        type_match = False
                        break
                    for si in range(len(contours[0][ci])):
                        if contours[mi][ci][si][0] != contours[0][ci][si][0]:
                            type_match = False
                            break
                    if not type_match:
                        break
                if not type_match:
                    break

            if type_match:
                already_ok.append(glyph_name)
                continue

        try:
            success = repair_glyph_chain(fonts, glyph_name)
            if success:
                repaired.append(glyph_name)
            else:
                skipped_error.append({"glyph": glyph_name, "reason": "repair_pair returned None"})
        except Exception as e:
            skipped_error.append({"glyph": glyph_name, "reason": str(e)})

    # Save repaired fonts
    for (fn, _, _), font in zip(masters, fonts):
        font.save(output_dir / fn)

    print(f"  Already compatible: {len(already_ok)}")
    print(f"  Repaired by script: {len(repaired)}")
    print(f"  Needs FontLab (different contour counts): {len(skipped_path_count)}")
    print(f"  Needs FontLab (repair failed): {len(skipped_error)}")

    # Step 5: After-repair compatibility check
    print("Step 4: Running post-repair compatibility check...")
    after_report_path = reports_dir / f"{family_key}-post-repair-compat.json"
    after_data = run_compat_check(font_paths, after_report_path)
    after_summary = summarize_compat(after_data)
    print(f"  After repair: {after_summary.get('glyphs_with_issues', 0)} glyphs with issues")
    if after_summary.get("severity"):
        for sev, count in sorted(after_summary["severity"].items()):
            print(f"    {sev}: {count}")

    return {
        "family_key": family_key,
        "masters": [fn for fn, _, _ in masters],
        "common_glyphs": common_count,
        "decomposed": decomposed_counts,
        "before_repair": before_summary,
        "after_repair": after_summary,
        "already_compatible": len(already_ok),
        "repaired_by_script": len(repaired),
        "repaired_glyphs": repaired,
        "needs_fontlab_path_count": len(skipped_path_count),
        "needs_fontlab_error": len(skipped_error),
        "fontlab_path_count_glyphs": skipped_path_count,
        "fontlab_error_glyphs": skipped_error,
        "fontlab_total_manual": len(skipped_path_count) + len(skipped_error),
    }


def families_from_manifest(manifest_path: Path | None) -> list[tuple[str, list[tuple[str, str, int]]]]:
    if manifest_path is None:
        return [
            ("roman", ROMAN_MASTERS),
            ("italic", ITALIC_MASTERS),
        ]

    config = load_source_config(manifest_path)
    ordered_keys = [key for key in ("roman", "italic") if key in config.families]
    ordered_keys.extend(key for key in config.families if key not in ordered_keys)

    families: list[tuple[str, list[tuple[str, str, int]]]] = []
    for family_key in ordered_keys:
        family = config.families[family_key]
        masters = [
            (master.filename, master.style_name, master.weight)
            for master in sorted(family.masters, key=lambda master: master.weight)
        ]
        if masters:
            families.append((family_key, masters))
    return families


def write_markdown_summary(results: list[dict], summary_path: Path) -> None:
    lines = ["# FontLab Preparation Report\n"]
    for r in results:
        lines.append(f"## {r['family_key'].title()} Family\n")
        lines.append(f"- **Common glyphs:** {r['common_glyphs']}")
        lines.append(f"- **Already compatible:** {r['already_compatible']}")
        lines.append(f"- **Auto-repaired:** {r['repaired_by_script']}")
        lines.append(f"- **Needs FontLab (different contour counts):** {r['needs_fontlab_path_count']}")
        lines.append(f"- **Needs FontLab (repair failed):** {r['needs_fontlab_error']}")
        lines.append(f"- **Total for FontLab Matchmaker:** {r['fontlab_total_manual']}")
        lines.append("")

        before = r["before_repair"]
        after = r["after_repair"]
        lines.append(f"### Compatibility Issues")
        lines.append(f"| Metric | Before | After |")
        lines.append(f"|--------|--------|-------|")
        lines.append(f"| Glyphs with issues | {before.get('glyphs_with_issues', 0)} | {after.get('glyphs_with_issues', 0)} |")
        for sev in ("severe", "moderate", "cosmetic"):
            b = before.get("severity", {}).get(sev, 0)
            a = after.get("severity", {}).get(sev, 0)
            lines.append(f"| {sev.title()} | {b} | {a} |")
        lines.append("")

        if r["fontlab_path_count_glyphs"]:
            lines.append("### Glyphs needing FontLab (different contour counts)\n")
            lines.append("| Glyph | Book | Medium | Bold | Black |")
            lines.append("|-------|------|--------|------|-------|")
            for item in r["fontlab_path_count_glyphs"][:50]:
                counts = item["contour_counts"]
                vals = list(counts.values())
                lines.append(f"| `{item['glyph']}` | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} |")
            if len(r["fontlab_path_count_glyphs"]) > 50:
                lines.append(f"| ... and {len(r['fontlab_path_count_glyphs']) - 50} more | | | | |")
            lines.append("")

        if r["fontlab_error_glyphs"]:
            lines.append("### Glyphs needing FontLab (repair failed)\n")
            for item in r["fontlab_error_glyphs"][:30]:
                lines.append(f"- `{item['glyph']}`: {item['reason']}")
            if len(r["fontlab_error_glyphs"]) > 30:
                lines.append(f"- ... and {len(r['fontlab_error_glyphs']) - 30} more")
            lines.append("")

    summary_path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    sample_dir = (repo_root / args.sample_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    reports_dir = (repo_root / args.reports_dir).resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = (repo_root / args.manifest).resolve() if args.manifest else None
    families = families_from_manifest(manifest_path)

    results = []

    for family_key, masters in families:
        if family_key == "italic" and args.skip_italic:
            continue
        result = process_family(
            family_key, masters, sample_dir, output_dir, reports_dir, args.force,
        )
        results.append(result)

    # Write reports
    report_path = reports_dir / "fontlab-prep-report.json"
    report_path.write_text(json.dumps(results, indent=2))
    print(f"\nDetailed report: {report_path}")

    summary_path = reports_dir / "fontlab-prep-summary.md"
    write_markdown_summary(results, summary_path)
    print(f"Markdown summary: {summary_path}")

    print(f"\nRepaired TTFs ready for FontLab 8: {output_dir}/")
    print("\nNext steps:")
    print("  1. Open FontLab 8")
    if results and results[0]["masters"]:
        print(f"  2. Open {results[0]['masters'][0]} from {output_dir}/")
    else:
        print(f"  2. Open the first repaired master from {output_dir}/")
    print("  3. Font > Merge Fonts to Masters > add the remaining masters for that family")
    print("  4. Press 7 to open Matchmaker")
    print("  5. Click 'Match Masters' for remaining auto-fixes")
    print("  6. Manually fix remaining red glyphs")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
