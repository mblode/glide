#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
from copy import deepcopy
from pathlib import Path

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

from source_manifest import FamilyConfig, load_source_config


DONOR_ROMAN_FILES = {
    400: "lineto-circular-book.ttf",
    900: "lineto-circular-black.ttf",
}

DONOR_ITALIC_FILES = {
    400: "lineto-circular-bookItalic.ttf",
    900: "lineto-circular-blackItalic.ttf",
}

# Glyphs whose Circular donor deltas are structurally compatible on paper but
# visually destructive when transferred onto Glide outlines. These should take
# the safer slant-based seed path first, then be refined manually.
DEFAULT_DIRECT_DELTA_DENYLIST = (
    "plus",
    "four",
    "A",
    "E",
    "F",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "T",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "bracketleft",
    "backslash",
    "bracketright",
    "asciicircum",
    "underscore",
    "grave",
    "k",
    "l",
    "slash",
    "v",
    "w",
    "y",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed Glide italic masters from root-derived Glide romans and Circular italic donors."
    )
    parser.add_argument(
        "--roman-dir",
        default="build/work/sources/glide-root-derived",
        help="Directory containing extracted Glide roman checkpoints.",
    )
    parser.add_argument(
        "--roman-manifest",
        default="build/work/manifests/glide-root-derived.json",
        help="Source manifest describing the extracted Glide roman checkpoints.",
    )
    parser.add_argument(
        "--donor-dir",
        default="src/donors/circular",
        help="Directory containing Circular donor roman/italic statics.",
    )
    parser.add_argument(
        "--output-dir",
        default="build/work/sources/glide-root-derived",
        help="Directory to write the seeded Glide italic masters.",
    )
    parser.add_argument(
        "--manifest-out",
        default="build/work/manifests/glide-root-plus-seeded-italic.json",
        help="Path to write the combined roman+italic manifest.",
    )
    parser.add_argument(
        "--report-out",
        default="build/work/reports/glide-italic-seed-report.json",
        help="Path to write the glyph-method report.",
    )
    parser.add_argument(
        "--family-name",
        default="Glide",
        help="Family name for the combined source manifest.",
    )
    parser.add_argument(
        "--style-family-name",
        default="Glide Seed Source",
        help="Family name written into the seeded italic static masters.",
    )
    parser.add_argument(
        "--italic-angle",
        type=float,
        default=-12.0,
        help="Fallback italic angle for slant-based glyph seeding.",
    )
    parser.add_argument(
        "--direct-delta-denylist",
        default=",".join(DEFAULT_DIRECT_DELTA_DENYLIST),
        help="Comma-separated glyph names that must bypass direct_delta and use slant fallback.",
    )
    return parser.parse_args()


def set_name_record(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    for platform_id, plat_enc_id, lang_id in ((3, 1, 0x409), (1, 0, 0)):
        name_table.setName(value, name_id, platform_id, plat_enc_id, lang_id)


def patch_italic_metadata(font: TTFont, family_name: str, style_name: str, weight: int, italic_angle: float) -> None:
    full_name = f"{family_name} {style_name}"
    postscript_name = f"{family_name.replace(' ', '')}-{style_name.replace(' ', '')}"

    set_name_record(font, 1, family_name)
    set_name_record(font, 2, style_name)
    set_name_record(font, 4, full_name)
    set_name_record(font, 6, postscript_name)
    set_name_record(font, 16, family_name)
    set_name_record(font, 17, style_name)

    head = font["head"]
    os2 = font["OS/2"]
    post = font["post"]

    head.macStyle &= ~0x03
    os2.fsSelection &= ~0x61
    head.macStyle |= 0x02
    os2.fsSelection |= 0x01
    if weight == 700:
        head.macStyle |= 0x01
        os2.fsSelection |= 0x20
    os2.usWeightClass = weight
    post.italicAngle = italic_angle


def decompose_composites(font: TTFont) -> None:
    glyf = font["glyf"]
    glyph_set = font.getGlyphSet()
    for glyph_name in font.getGlyphOrder():
        glyph = glyf[glyph_name]
        if not glyph.isComposite():
            continue
        recording_pen = DecomposingRecordingPen(glyph_set)
        glyph_set[glyph_name].draw(recording_pen)
        tt_pen = TTGlyphPen(None)
        recording_pen.replay(tt_pen)
        new_glyph = tt_pen.glyph()
        if new_glyph.numberOfContours >= 0:
            new_glyph.recalcBounds(glyf)
        glyf[glyph_name] = new_glyph


def glyph_signature(font: TTFont, glyph_name: str) -> tuple[int, tuple[int, ...], int] | None:
    glyph = font["glyf"][glyph_name]
    if glyph.numberOfContours < 0:
        return None
    coords, end_points, _ = glyph.getCoordinates(font["glyf"])
    return (glyph.numberOfContours, tuple(end_points), len(coords))


def glyph_coords(font: TTFont, glyph_name: str) -> tuple[list[tuple[float, float]], list[int], bytes]:
    glyph = font["glyf"][glyph_name]
    coords, end_points, flags = glyph.getCoordinates(font["glyf"])
    return [(float(x), float(y)) for x, y in coords], list(end_points), bytes(flags)


def split_contours(
    points: list[tuple[float, float]],
    end_points: list[int],
) -> list[list[tuple[float, float]]]:
    contours: list[list[tuple[float, float]]] = []
    start = 0
    for end in end_points:
        contours.append(points[start:end + 1])
        start = end + 1
    return contours


def normalize_contour(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    width = max(1.0, max_x - min_x)
    height = max(1.0, max_y - min_y)
    return [
        ((x - min_x) / width, (y - min_y) / height)
        for x, y in points
    ]


def point_distance(
    points_a: list[tuple[float, float]],
    points_b: list[tuple[float, float]],
) -> float:
    if len(points_a) != len(points_b):
        return math.inf
    return sum(
        math.hypot(ax - bx, ay - by)
        for (ax, ay), (bx, by) in zip(points_a, points_b)
    ) / max(1, len(points_a))


def apply_contour_transform(
    points: list[tuple[float, float]],
    reverse: bool,
    shift: int,
) -> list[tuple[float, float]]:
    transformed = list(reversed(points)) if reverse else list(points)
    if not transformed:
        return transformed
    shift %= len(transformed)
    return transformed[shift:] + transformed[:shift]


def best_contour_transform(
    reference_points: list[tuple[float, float]],
    candidate_points: list[tuple[float, float]],
) -> tuple[bool, int]:
    reference_norm = normalize_contour(reference_points)
    best = (False, 0)
    best_score = math.inf

    for reverse in (False, True):
        transformed = list(reversed(candidate_points)) if reverse else list(candidate_points)
        transformed_norm = normalize_contour(transformed)
        for shift in range(len(transformed_norm)):
            shifted_norm = transformed_norm[shift:] + transformed_norm[:shift]
            score = point_distance(reference_norm, shifted_norm)
            if score < best_score:
                best_score = score
                best = (reverse, shift)

    return best


def align_direct_delta_points(
    reference_points: list[tuple[float, float]],
    donor_roman_points: list[tuple[float, float]],
    donor_italic_points: list[tuple[float, float]],
    end_points: list[int],
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    reference_contours = split_contours(reference_points, end_points)
    donor_roman_contours = split_contours(donor_roman_points, end_points)
    donor_italic_contours = split_contours(donor_italic_points, end_points)

    aligned_roman: list[tuple[float, float]] = []
    aligned_italic: list[tuple[float, float]] = []

    for reference_contour, donor_roman_contour, donor_italic_contour in zip(
        reference_contours,
        donor_roman_contours,
        donor_italic_contours,
    ):
        reverse, shift = best_contour_transform(reference_contour, donor_roman_contour)
        aligned_roman.extend(apply_contour_transform(donor_roman_contour, reverse, shift))
        aligned_italic.extend(apply_contour_transform(donor_italic_contour, reverse, shift))

    return aligned_roman, aligned_italic


def interpolate(value_a: float, value_b: float, t: float) -> float:
    return value_a + (value_b - value_a) * t


def interpolate_points(
    points_a: list[tuple[float, float]],
    points_b: list[tuple[float, float]],
    t: float,
) -> list[tuple[float, float]]:
    return [
        (interpolate(ax, bx, t), interpolate(ay, by, t))
        for (ax, ay), (bx, by) in zip(points_a, points_b)
    ]


def apply_slant(
    points: list[tuple[float, float]],
    italic_angle: float,
    slant_height: float,
) -> list[tuple[float, float]]:
    shear = -math.tan(math.radians(italic_angle))
    return [
        (x + shear * (y - slant_height), y)
        for x, y in points
    ]


def set_simple_glyph(
    font: TTFont,
    glyph_name: str,
    points: list[tuple[float, float]],
    end_points: list[int],
    flags: bytes,
) -> None:
    glyph = deepcopy(font["glyf"][glyph_name])
    glyph.coordinates = GlyphCoordinates(points)
    glyph.endPtsOfContours = end_points
    glyph.flags = flags
    glyph.recalcBounds(font["glyf"])
    font["glyf"][glyph_name] = glyph


def build_method_map(
    glide_roman: FamilyConfig,
    roman_dir: Path,
    donor_dir: Path,
    direct_delta_denylist: set[str] | None = None,
) -> dict[str, str]:
    direct_delta_denylist = direct_delta_denylist or set()
    glide_regular = TTFont(roman_dir / glide_roman.master_files_by_weight()[400])
    glide_black = TTFont(roman_dir / glide_roman.master_files_by_weight()[900])
    circular_regular = TTFont(donor_dir / DONOR_ROMAN_FILES[400])
    circular_black = TTFont(donor_dir / DONOR_ROMAN_FILES[900])
    circular_regular_italic = TTFont(donor_dir / DONOR_ITALIC_FILES[400])
    circular_black_italic = TTFont(donor_dir / DONOR_ITALIC_FILES[900])

    for font in (
        glide_regular,
        glide_black,
        circular_regular,
        circular_black,
        circular_regular_italic,
        circular_black_italic,
    ):
        decompose_composites(font)

    common = (
        set(glide_regular.getGlyphOrder())
        & set(glide_black.getGlyphOrder())
        & set(circular_regular.getGlyphOrder())
        & set(circular_black.getGlyphOrder())
        & set(circular_regular_italic.getGlyphOrder())
        & set(circular_black_italic.getGlyphOrder())
    )

    method_by_glyph: dict[str, str] = {}
    for glyph_name in sorted(common):
        if glyph_name in direct_delta_denylist:
            method_by_glyph[glyph_name] = "slant_fallback"
            continue

        sig_gr400 = glyph_signature(glide_regular, glyph_name)
        sig_gr900 = glyph_signature(glide_black, glyph_name)
        sig_cr400 = glyph_signature(circular_regular, glyph_name)
        sig_ci400 = glyph_signature(circular_regular_italic, glyph_name)
        sig_cr900 = glyph_signature(circular_black, glyph_name)
        sig_ci900 = glyph_signature(circular_black_italic, glyph_name)

        donor_direct = sig_cr400 == sig_ci400 == sig_cr900 == sig_ci900 and sig_cr400 is not None
        glide_match = sig_gr400 == sig_cr400 and sig_gr900 == sig_cr900 and sig_gr400 is not None

        if donor_direct and glide_match:
            method_by_glyph[glyph_name] = "direct_delta"
        else:
            method_by_glyph[glyph_name] = "slant_fallback"

    return method_by_glyph


def seed_italic_family(
    glide_roman: FamilyConfig,
    roman_dir: Path,
    donor_dir: Path,
    output_dir: Path,
    family_name: str,
    style_family_name: str,
    italic_angle: float,
    direct_delta_denylist: set[str] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, str]]:
    method_by_glyph = build_method_map(
        glide_roman,
        roman_dir,
        donor_dir,
        direct_delta_denylist=direct_delta_denylist,
    )

    donor_fonts = {
        "cr400": TTFont(donor_dir / DONOR_ROMAN_FILES[400]),
        "ci400": TTFont(donor_dir / DONOR_ITALIC_FILES[400]),
        "cr900": TTFont(donor_dir / DONOR_ROMAN_FILES[900]),
        "ci900": TTFont(donor_dir / DONOR_ITALIC_FILES[900]),
    }
    glide_endpoints = {
        "gr400": TTFont(roman_dir / glide_roman.master_files_by_weight()[400]),
        "gr900": TTFont(roman_dir / glide_roman.master_files_by_weight()[900]),
    }
    for font in donor_fonts.values():
        decompose_composites(font)
    for font in glide_endpoints.values():
        decompose_composites(font)

    italic_masters: list[dict[str, object]] = []
    report: list[dict[str, object]] = []
    min_weight = min(master.weight for master in glide_roman.masters)
    max_weight = max(master.weight for master in glide_roman.masters)

    output_dir.mkdir(parents=True, exist_ok=True)

    for roman_master in glide_roman.masters:
        roman_path = roman_dir / roman_master.filename
        seeded_font = TTFont(roman_path, recalcBBoxes=False, recalcTimestamp=False)
        decompose_composites(seeded_font)

        t = 0.0 if max_weight == min_weight else (roman_master.weight - min_weight) / (max_weight - min_weight)
        donor_xheight = interpolate(
            float(getattr(donor_fonts["ci400"]["OS/2"], "sxHeight", 480)),
            float(getattr(donor_fonts["ci900"]["OS/2"], "sxHeight", 500)),
            t,
        )
        slant_height = donor_xheight * 0.5

        direct_count = 0
        slant_count = 0

        for glyph_name in seeded_font.getGlyphOrder():
            if glyph_name == ".notdef":
                continue
            glyph = seeded_font["glyf"][glyph_name]
            if glyph.numberOfContours == 0:
                continue

            method = method_by_glyph.get(glyph_name, "slant_fallback")
            target_points, end_points, flags = glyph_coords(seeded_font, glyph_name)
            new_points = target_points

            donor_width_delta = 0.0
            if glyph_name in donor_fonts["cr400"]["hmtx"].metrics and glyph_name in donor_fonts["ci400"]["hmtx"].metrics:
                donor_width_delta_400 = donor_fonts["ci400"]["hmtx"][glyph_name][0] - donor_fonts["cr400"]["hmtx"][glyph_name][0]
                donor_width_delta_900 = donor_fonts["ci900"]["hmtx"][glyph_name][0] - donor_fonts["cr900"]["hmtx"][glyph_name][0]
                donor_width_delta = interpolate(float(donor_width_delta_400), float(donor_width_delta_900), t)

            if method == "direct_delta":
                gr400_points, _, _ = glyph_coords(glide_endpoints["gr400"], glyph_name)
                cr400_points, _, _ = glyph_coords(donor_fonts["cr400"], glyph_name)
                ci400_points, _, _ = glyph_coords(donor_fonts["ci400"], glyph_name)
                gr900_points, _, _ = glyph_coords(glide_endpoints["gr900"], glyph_name)
                cr900_points, _, _ = glyph_coords(donor_fonts["cr900"], glyph_name)
                ci900_points, _, _ = glyph_coords(donor_fonts["ci900"], glyph_name)
                aligned_cr400_points, aligned_ci400_points = align_direct_delta_points(
                    gr400_points,
                    cr400_points,
                    ci400_points,
                    end_points,
                )
                aligned_cr900_points, aligned_ci900_points = align_direct_delta_points(
                    gr900_points,
                    cr900_points,
                    ci900_points,
                    end_points,
                )
                delta_400 = [
                    (ix - rx, iy - ry)
                    for (rx, ry), (ix, iy) in zip(aligned_cr400_points, aligned_ci400_points)
                ]
                delta_900 = [
                    (ix - rx, iy - ry)
                    for (rx, ry), (ix, iy) in zip(aligned_cr900_points, aligned_ci900_points)
                ]
                delta = interpolate_points(delta_400, delta_900, t)
                new_points = [(x + dx, y + dy) for (x, y), (dx, dy) in zip(target_points, delta)]
                direct_count += 1
            else:
                new_points = apply_slant(target_points, italic_angle, slant_height)
                slant_count += 1

            set_simple_glyph(seeded_font, glyph_name, new_points, end_points, flags)
            advance_width = seeded_font["hmtx"][glyph_name][0]
            seeded_font["hmtx"][glyph_name] = (
                round(advance_width + donor_width_delta),
                seeded_font["glyf"][glyph_name].xMin,
            )

        style_name = roman_master.style_name if roman_master.style_name == "Regular" else roman_master.style_name
        italic_style_name = f"{style_name} Italic"
        italic_filename = (
            roman_master.filename.replace(".ttf", "Italic.ttf")
            if not roman_master.filename.endswith("Italic.ttf")
            else roman_master.filename
        )
        patch_italic_metadata(seeded_font, style_family_name, italic_style_name, roman_master.weight, italic_angle)
        output_path = output_dir / italic_filename
        seeded_font.save(output_path)

        italic_masters.append(
            {
                "filename": italic_filename,
                "style_name": italic_style_name,
                "weight": roman_master.weight,
            }
        )
        report.append(
            {
                "filename": italic_filename,
                "weight": roman_master.weight,
                "direct_delta_glyphs": direct_count,
                "slant_fallback_glyphs": slant_count,
                "slant_height": slant_height,
                "italic_angle": italic_angle,
            }
        )
        print(f"Saved: {output_path}")

    return italic_masters, report, method_by_glyph


def main() -> int:
    args = parse_args()
    roman_dir = Path(args.roman_dir).resolve()
    donor_dir = Path(args.donor_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest_out = Path(args.manifest_out).resolve()
    report_out = Path(args.report_out).resolve()
    direct_delta_denylist = {
        glyph_name.strip()
        for glyph_name in args.direct_delta_denylist.split(",")
        if glyph_name.strip()
    }

    roman_config = load_source_config(args.roman_manifest)
    glide_roman = roman_config.families.get("roman")
    if glide_roman is None or not glide_roman.masters:
        raise SystemExit("Roman manifest does not define a usable roman family.")

    italic_masters, report, method_by_glyph = seed_italic_family(
        glide_roman=glide_roman,
        roman_dir=roman_dir,
        donor_dir=donor_dir,
        output_dir=output_dir,
        family_name=args.family_name,
        style_family_name=args.style_family_name,
        italic_angle=args.italic_angle,
        direct_delta_denylist=direct_delta_denylist,
    )

    manifest_payload = {
        "family_name": args.family_name,
        "axis_maps": {
            axis_tag: [[inp, out] for inp, out in mappings]
            for axis_tag, mappings in roman_config.axis_maps.items()
        },
        "families": {
            "roman": {
                "default_style": glide_roman.default_style,
                "masters": [
                    {
                        "filename": master.filename,
                        "style_name": master.style_name,
                        "weight": master.weight,
                    }
                    for master in glide_roman.masters
                ],
            },
            "italic": {
                "default_style": "Italic",
                "masters": italic_masters,
            },
        },
    }
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest_payload, indent=2))
    print(f"Wrote manifest: {manifest_out}")

    report_payload = {
        "roman_manifest": str(Path(args.roman_manifest).resolve()),
        "donor_dir": str(donor_dir),
        "output_dir": str(output_dir),
        "direct_delta_denylist": sorted(direct_delta_denylist),
        "forced_slant_fallback_glyphs": sorted(
            glyph_name
            for glyph_name, method in method_by_glyph.items()
            if glyph_name in direct_delta_denylist and method == "slant_fallback"
        ),
        "weights": report,
    }
    report_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.write_text(json.dumps(report_payload, indent=2))
    print(f"Wrote report: {report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
