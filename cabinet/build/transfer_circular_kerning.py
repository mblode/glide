#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
import json
from copy import deepcopy
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

from source_manifest import load_source_config


DONOR_ROMAN_FILES = {
    400: "lineto-circular-book.ttf",
    500: "lineto-circular-medium.ttf",
    700: "lineto-circular-bold.ttf",
    900: "lineto-circular-black.ttf",
}

DONOR_ITALIC_FILES = {
    400: "lineto-circular-bookItalic.ttf",
    500: "lineto-circular-mediumItalic.ttf",
    700: "lineto-circular-boldItalic.ttf",
    900: "lineto-circular-blackItalic.ttf",
}


def iter_pairpos_subtables(font: TTFont):
    if "GPOS" not in font:
        return
    lookup_list = getattr(font["GPOS"].table, "LookupList", None)
    if lookup_list is None:
        return

    for lookup in lookup_list.Lookup:
        if lookup.LookupType == 2:
            for subtable in lookup.SubTable:
                yield lookup, subtable
        elif lookup.LookupType == 9:
            for subtable in lookup.SubTable:
                if getattr(subtable, "ExtensionLookupType", None) != 2:
                    continue
                yield lookup, subtable.ExtSubTable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy Circular donor kerning into Glide masters and write a review report."
    )
    parser.add_argument(
        "--manifest",
        default="build/work/manifests/glide-root-plus-seeded-italic.json",
        help="Manifest describing the Glide master sets.",
    )
    parser.add_argument(
        "--target-dir",
        default="build/work/sources/glide-root-derived",
        help="Directory containing the Glide source masters to update.",
    )
    parser.add_argument(
        "--donor-dir",
        default="src/donors/circular",
        help="Directory containing the Circular donor fonts.",
    )
    parser.add_argument(
        "--report-out",
        default="build/work/reports/kerning-transfer-review.json",
        help="Path to write the kerning transfer and review report.",
    )
    parser.add_argument(
        "--skip-italic-transfer",
        action="store_true",
        help="Only write the roman review report without modifying italic masters.",
    )
    parser.add_argument(
        "--italic-donor-weight",
        type=int,
        default=400,
        help="Circular italic weight to use as the canonical kerning source for all Glide italic masters.",
    )
    return parser.parse_args()


def pair_stats(font: TTFont) -> dict[str, int]:
    stats = {
        "lookups": 0,
        "subtables": 0,
        "pairs": 0,
        "class_defs": 0,
    }
    counted_lookups: set[int] = set()
    for lookup, subtable in iter_pairpos_subtables(font) or ():
        lookup_id = id(lookup)
        if lookup_id not in counted_lookups:
            counted_lookups.add(lookup_id)
            stats["lookups"] += 1
        stats["subtables"] += 1
        format_type = getattr(subtable, "Format", None)
        if format_type == 1:
            for pair_set in subtable.PairSet:
                stats["pairs"] += len(pair_set.PairValueRecord)
        elif format_type == 2:
            if getattr(subtable, "ClassDef1", None):
                stats["class_defs"] += len(subtable.ClassDef1.classDefs)
            if getattr(subtable, "ClassDef2", None):
                stats["class_defs"] += len(subtable.ClassDef2.classDefs)
            for class1_record in subtable.Class1Record:
                stats["pairs"] += len(class1_record.Class2Record)
    return stats


def normalize_pairpos_gpos(font: TTFont) -> None:
    if "GPOS" not in font or font["GPOS"].table.LookupList is None:
        return

    glyph_order = {glyph_name: index for index, glyph_name in enumerate(font.getGlyphOrder())}

    for lookup in font["GPOS"].table.LookupList.Lookup:
        if lookup.LookupType not in (2, 9):
            continue

        normalized_subtables = []
        if lookup.LookupType == 2:
            paired_subtables = [(subtable, subtable) for subtable in lookup.SubTable]
        else:
            paired_subtables = [
                (subtable, subtable.ExtSubTable)
                for subtable in lookup.SubTable
                if getattr(subtable, "ExtensionLookupType", None) == 2
            ]

        for container, subtable in paired_subtables:
            coverage = list(getattr(getattr(subtable, "Coverage", None), "glyphs", []) or [])
            if not coverage:
                normalized_subtables.append((container, subtable))
                continue

            sort_keys = sorted(range(len(coverage)), key=lambda idx: glyph_order.get(coverage[idx], 10**9))
            if getattr(subtable, "Format", None) == 1:
                subtable.Coverage.glyphs = [coverage[idx] for idx in sort_keys]
                subtable.PairSet = [subtable.PairSet[idx] for idx in sort_keys]
            elif getattr(subtable, "Format", None) == 2:
                subtable.Coverage.glyphs = [coverage[idx] for idx in sort_keys]

            normalized_subtables.append((container, subtable))

        normalized_subtables.sort(
            key=lambda item: glyph_order.get(item[1].Coverage.glyphs[0], 10**9)
            if getattr(getattr(item[1], "Coverage", None), "glyphs", None)
            else 10**9,
        )
        lookup.SubTable = [container for container, _ in normalized_subtables]


def subset_donor_for_target(donor_font: TTFont, target_font: TTFont) -> TTFont:
    buffer = io.BytesIO()
    donor_font.save(buffer)
    donor_copy = TTFont(io.BytesIO(buffer.getvalue()))
    common_glyphs = sorted(set(donor_font.getGlyphOrder()) & set(target_font.getGlyphOrder()))
    if ".notdef" not in common_glyphs and ".notdef" in donor_font.getGlyphOrder():
        common_glyphs.insert(0, ".notdef")

    options = Options()
    options.glyph_names = True
    options.hinting = False
    options.retain_gids = False
    options.layout_closure = True
    subsetter = Subsetter(options=options)
    subsetter.populate(glyphs=common_glyphs)
    subsetter.subset(donor_copy)
    return donor_copy


def donor_path_for_weight(weight: int, italic: bool, donor_dir: Path) -> Path:
    mapping = DONOR_ITALIC_FILES if italic else DONOR_ROMAN_FILES
    filename = mapping.get(weight)
    if filename is None:
        raise KeyError(f"No donor file defined for weight {weight} ({'italic' if italic else 'roman'})")
    return donor_dir / filename


def transfer_italic_kerning(
    manifest_path: Path,
    target_dir: Path,
    donor_dir: Path,
    donor_weight: int,
) -> list[dict[str, object]]:
    config = load_source_config(manifest_path)
    family = config.families.get("italic")
    if family is None or not family.masters:
        raise SystemExit("Manifest does not define an italic family to transfer kerning into.")

    canonical_donor_path = donor_path_for_weight(donor_weight, italic=True, donor_dir=donor_dir)
    canonical_donor_font = TTFont(canonical_donor_path, recalcBBoxes=False, recalcTimestamp=False)
    transfers: list[dict[str, object]] = []
    for master in sorted(family.masters, key=lambda item: item.weight):
        target_path = target_dir / master.filename
        target_font = TTFont(target_path, recalcBBoxes=False, recalcTimestamp=False)
        donor_subset = subset_donor_for_target(canonical_donor_font, target_font)

        before = pair_stats(target_font)
        donor_stats = pair_stats(donor_subset)

        if "GPOS" in donor_subset:
            target_font["GPOS"] = deepcopy(donor_subset["GPOS"])
            normalize_pairpos_gpos(target_font)
        if "kern" in target_font:
            del target_font["kern"]
        target_font.save(target_path)

        reloaded = TTFont(target_path, recalcBBoxes=False, recalcTimestamp=False)
        after = pair_stats(reloaded)
        transfers.append(
            {
                "weight": master.weight,
                "target": str(target_path),
                "donor": str(canonical_donor_path),
                "common_glyphs": len(set(canonical_donor_font.getGlyphOrder()) & set(target_font.getGlyphOrder())),
                "before": before,
                "donor_subset": donor_stats,
                "after": after,
            }
        )
    return transfers


def review_roman(manifest_path: Path, target_dir: Path, donor_dir: Path) -> list[dict[str, object]]:
    config = load_source_config(manifest_path)
    family = config.families.get("roman")
    if family is None or not family.masters:
        return []

    reviews: list[dict[str, object]] = []
    for master in sorted(family.masters, key=lambda item: item.weight):
        target_path = target_dir / master.filename
        donor_path = donor_path_for_weight(master.weight, italic=False, donor_dir=donor_dir)
        target_font = TTFont(target_path, recalcBBoxes=False, recalcTimestamp=False)
        donor_font = TTFont(donor_path, recalcBBoxes=False, recalcTimestamp=False)
        donor_subset = subset_donor_for_target(donor_font, target_font)
        reviews.append(
            {
                "weight": master.weight,
                "target_path": str(target_path),
                "donor_path": str(donor_path),
                "common_glyphs": len(set(donor_font.getGlyphOrder()) & set(target_font.getGlyphOrder())),
                "target_only_glyphs": len(set(target_font.getGlyphOrder()) - set(donor_font.getGlyphOrder())),
                "donor_only_glyphs": len(set(donor_font.getGlyphOrder()) - set(target_font.getGlyphOrder())),
                "target": {
                    "path": str(target_path),
                    "pair_stats": pair_stats(target_font),
                },
                "donor_subset": {
                    "path": str(donor_path),
                    "pair_stats": pair_stats(donor_subset),
                },
                "decision": "kept_glide_roman_gpos",
            }
        )
    return reviews


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = (repo_root / args.manifest).resolve()
    target_dir = (repo_root / args.target_dir).resolve()
    donor_dir = (repo_root / args.donor_dir).resolve()
    report_path = (repo_root / args.report_out).resolve()

    italic_transfers = []
    if not args.skip_italic_transfer:
        italic_transfers = transfer_italic_kerning(
            manifest_path=manifest_path,
            target_dir=target_dir,
            donor_dir=donor_dir,
            donor_weight=args.italic_donor_weight,
        )

    roman_review = review_roman(
        manifest_path=manifest_path,
        target_dir=target_dir,
        donor_dir=donor_dir,
    )

    payload = {
        "manifest": str(manifest_path),
        "target_dir": str(target_dir),
        "donor_dir": str(donor_dir),
        "italic_donor_weight": args.italic_donor_weight,
        "italic_transfer": italic_transfers,
        "roman_review": roman_review,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote report: {report_path}")

    for item in italic_transfers:
        print(
            f"italic {item['weight']}: "
            f"{item['before']['pairs']} -> {item['after']['pairs']} pairs "
            f"(donor subset {item['donor_subset']['pairs']})"
        )

    for item in roman_review:
        print(
            f"roman {item['weight']}: "
            f"kept Glide GPOS {item['target']['pair_stats']['pairs']} pairs; "
            f"donor subset has {item['donor_subset']['pair_stats']['pairs']} pairs"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
