#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
import json
import sys
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from copy import deepcopy

from fontTools import varLib
from fontTools.designspaceLib import (
    AxisDescriptor,
    DesignSpaceDocument,
    InstanceDescriptor,
    SourceDescriptor,
)
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.subset import Options, Subsetter
from fontTools.otlLib.builder import buildStatTable as _buildStatTable
from fontTools.ttLib import TTFont
from fontTools.ttLib.woff2 import compress as compress_woff2

from italic_variable_kerning import build_variable_italic_gpos_sources
from source_manifest import MasterSpec, load_source_config, select_masters


SEVERE_ISSUES = {
    "missing",
    "node_count",
    "path_count",
    "open_path",
}
MODERATE_ISSUES = {
    "contour_order",
    "node_incompatibility",
    "nothing",
    "underweight",
    "overweight",
    "wrong_start_point",
}

@dataclass
class FamilySummary:
    family_key: str
    default_style: str
    sources: list[str]
    common_glyphs: int
    dropped_by_source: dict[str, int]
    decomposed_by_source: dict[str, int]
    compatibility_glyphs: int
    compatibility_issue_types: dict[str, int]
    compatibility_severity: dict[str, int]
    ttf_output: str
    woff2_output: str
    output_glyphs: int
    skipped_glyphs: int
    varying_glyphs: int
    frozen_glyphs: int
    fvar_axes: list[dict[str, float | str]]
    build_log: str
    compatibility_report: str

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build roman and italic variable fonts from static TTF masters."
    )
    parser.add_argument(
        "--manifest",
        help="Optional JSON source manifest describing roman/italic master sets.",
    )
    parser.add_argument(
        "--sample-dir",
        default="build/work/fontlab-ready",
        help="Directory containing the static TTF masters.",
    )
    parser.add_argument(
        "--output-dir",
        default="build/work/output",
        help="Directory for final TTF and WOFF2 outputs.",
    )
    parser.add_argument(
        "--normalized-dir",
        default="build/work/normalized",
        help="Directory for normalized sources and generated designspaces.",
    )
    parser.add_argument(
        "--reports-dir",
        default="build/work/reports",
        help="Directory for compatibility/build reports.",
    )
    parser.add_argument(
        "--italic-kerning-donor-dir",
        default="src/donors/circular",
        help="Directory containing the Circular italic donor fonts for exact kerning matching.",
    )
    parser.add_argument(
        "--skip-italic",
        action="store_true",
        help="Only build the roman variable font.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing normalized sources and outputs.",
    )
    parser.add_argument(
        "--two-master",
        action="store_true",
        help="Build with only book/black masters per family.",
    )
    return parser.parse_args()


def load_font(path: Path) -> TTFont:
    return TTFont(path, recalcBBoxes=False, recalcTimestamp=False)


def common_glyph_order(fonts: Iterable[TTFont]) -> list[str]:
    fonts = list(fonts)
    base_order = fonts[0].getGlyphOrder()
    common = set(base_order)
    for font in fonts[1:]:
        common &= set(font.getGlyphOrder())
    return [glyph_name for glyph_name in base_order if glyph_name in common]


def subset_to_glyphs(font: TTFont, glyph_names: list[str]) -> None:
    options = Options()
    options.glyph_names = True
    options.hinting = False
    options.layout_closure = False
    subsetter = Subsetter(options=options)
    subsetter.populate(glyphs=glyph_names)
    subsetter.subset(font)


def decompose_composites(font: TTFont) -> int:
    glyf = font["glyf"]
    decomposed = 0
    for glyph_name in font.getGlyphOrder():
        glyph = glyf[glyph_name]
        if not glyph.isComposite():
            continue
        recording_pen = DecomposingRecordingPen(font.getGlyphSet())
        font.getGlyphSet()[glyph_name].draw(recording_pen)
        tt_pen = TTGlyphPen(None)
        recording_pen.replay(tt_pen)
        new_glyph = tt_pen.glyph()
        if new_glyph.numberOfContours >= 0:
            new_glyph.recalcBounds(glyf)
        glyf[glyph_name] = new_glyph
        decomposed += 1
    return decomposed


def normalize_family(
    family_key: str,
    masters: list[MasterSpec],
    sample_dir: Path,
    normalized_dir: Path,
    force: bool,
) -> tuple[list[Path], int, dict[str, int], dict[str, int]]:
    source_paths = [sample_dir / master.filename for master in masters]
    fonts = [load_font(path) for path in source_paths]
    common_order = common_glyph_order(fonts)
    common_set = set(common_order)
    dropped_by_source = {
        master.filename: len(set(font.getGlyphOrder()) - common_set)
        for master, font in zip(masters, fonts)
    }
    normalized_paths: list[Path] = []
    decomposed_by_source: dict[str, int] = {}

    for master, source_path in zip(masters, source_paths):
        output_path = normalized_dir / f"{family_key}-{source_path.name}"
        normalized_paths.append(output_path)
        if output_path.exists() and not force:
            font = load_font(output_path)
            decomposed_by_source[master.filename] = sum(
                1
                for glyph_name in font.getGlyphOrder()
                if font["glyf"][glyph_name].isComposite()
            )
            continue

        font = load_font(source_path)
        subset_to_glyphs(font, common_order)
        decomposed_count = decompose_composites(font)
        subset_to_glyphs(font, common_order)
        font.save(output_path)
        decomposed_by_source[master.filename] = decomposed_count

    return normalized_paths, len(common_order), dropped_by_source, decomposed_by_source


def run_interpolatable_report(font_paths: list[Path], report_path: Path) -> tuple[int, dict[str, int], dict[str, int]]:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "fontTools.varLib.interpolatable",
        *[str(path) for path in font_paths],
        "--json",
        "--output",
        str(report_path),
    ]
    # Exit code 1 means issues were found; the JSON report is still valid.
    completed = __import__("subprocess").run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.stderr:
        report_path.with_suffix(".stderr.txt").write_text(completed.stderr)
    if completed.stdout:
        report_path.with_suffix(".stdout.txt").write_text(completed.stdout)

    if not report_path.exists():
        return 0, {}, {}

    data = json.loads(report_path.read_text())
    issue_types = Counter()
    severity = Counter()
    for issues in data.values():
        for issue in issues:
            issue_type = issue.get("type", "unknown")
            issue_types[issue_type] += 1
            if issue_type in SEVERE_ISSUES:
                severity["severe"] += 1
            elif issue_type in MODERATE_ISSUES:
                severity["moderate"] += 1
            else:
                severity["cosmetic"] += 1

    return len(data), dict(issue_types), dict(severity)


def build_designspace(
    family_name: str,
    default_style: str,
    masters: list[MasterSpec],
    source_paths: list[Path],
    designspace_path: Path,
    axis_map: list[tuple[float, float]] | None,
) -> None:
    document = DesignSpaceDocument()

    axis = AxisDescriptor()
    axis.name = "Weight"
    axis.tag = "wght"
    axis.minimum = float(min(master.weight for master in masters))
    axis.maximum = float(max(master.weight for master in masters))
    axis.default = 400.0

    if axis_map:
        axis.map = [(float(inp), float(out)) for inp, out in axis_map]

    document.addAxis(axis)

    for index, (master, source_path) in enumerate(zip(masters, source_paths)):
        source = SourceDescriptor()
        source.path = str(source_path)
        source.name = master.style_name
        source.familyName = family_name
        source.styleName = master.style_name
        source.location = {"Weight": float(master.weight)}
        source.copyLib = index == 0
        source.copyInfo = index == 0
        source.copyFeatures = index == 0
        source.copyGroups = index == 0
        document.addSource(source)

    instance_specs = [
        ("Regular", 400),
        ("Medium", 500),
        ("Bold", 700),
        ("Black", 900),
    ]
    for style_name, weight in instance_specs:
        if weight < axis.minimum or weight > axis.maximum:
            continue
        instance = InstanceDescriptor()
        instance.familyName = family_name
        if default_style == "Italic":
            instance.styleName = f"{style_name} Italic"
            instance.styleMapStyleName = "italic" if weight == 400 else "bold italic"
        else:
            instance.styleName = style_name
            instance.styleMapStyleName = "regular" if weight == 400 else "bold"
        instance.styleMapFamilyName = family_name
        instance.postScriptFontName = (
            f"{family_name.replace(' ', '')}-{instance.styleName.replace(' ', '')}"
        )
        instance.location = {"Weight": float(weight)}
        document.addInstance(instance)

    document.write(designspace_path)


def prepare_build_sources(
    family_key: str,
    source_paths: list[Path],
    normalized_dir: Path,
    strip_gpos: bool,
    force: bool,
) -> list[Path]:
    if not strip_gpos:
        return source_paths

    build_paths: list[Path] = []
    for source_path in source_paths:
        build_path = normalized_dir / f"{family_key}-build-{source_path.name}"
        build_paths.append(build_path)
        if build_path.exists() and not force:
            continue
        font = load_font(source_path)
        if "GPOS" in font:
            del font["GPOS"]
        font.save(build_path)
    return build_paths


def set_name_record(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    for platform_id, plat_enc_id, lang_id in ((3, 1, 0x409), (1, 0, 0)):
        name_table.setName(value, name_id, platform_id, plat_enc_id, lang_id)


def patch_metadata(font: TTFont, family_name: str, default_style: str, italic: bool) -> None:
    full_name = f"{family_name} {default_style}"
    postscript_name = f"{family_name.replace(' ', '')}-{default_style.replace(' ', '')}"

    set_name_record(font, 1, family_name)
    set_name_record(font, 2, default_style)
    set_name_record(font, 4, full_name)
    set_name_record(font, 6, postscript_name)
    set_name_record(font, 16, family_name)
    set_name_record(font, 17, default_style)

    head = font["head"]
    os2 = font["OS/2"]
    post = font["post"]

    head.macStyle &= ~0x3
    os2.fsSelection &= ~0x41
    os2.usWeightClass = 400
    if italic:
        head.macStyle |= 0x02
        os2.fsSelection |= 0x01
        post.italicAngle = -12.0
    else:
        os2.fsSelection |= 0x40
        post.italicAngle = 0.0


def count_frozen_glyphs(font: TTFont) -> int:
    """Count glyphs with no variation deltas in the gvar table.

    A glyph is "frozen" (rendered identically at all axis positions) when it
    has no entry in gvar or its gvar entry contains no variation tuples.
    """
    gvar = font.get("gvar")
    if gvar is None:
        return len(font.getGlyphOrder())
    frozen = 0
    for glyph_name in font.getGlyphOrder():
        variations = gvar.variations.get(glyph_name)
        if not variations:
            frozen += 1
    return frozen


def build_stat_table(font: TTFont, italic: bool) -> None:
    """Add an OpenType STAT table with weight axis values and italic flag."""
    axes = [
        {
            "tag": "wght",
            "name": "Weight",
            "values": [
                {"name": "Regular", "value": 400, "flags": 0x0002},  # elidable
                {"name": "Medium", "value": 500},
                {"name": "Bold", "value": 700},
                {"name": "Black", "value": 900},
            ],
        },
    ]
    locations = None
    if italic:
        # Mark the entire font as italic via a STAT location.
        axes.append(
            {
                "tag": "ital",
                "name": "Italic",
            }
        )
        locations = [{"name": "Italic", "location": {"ital": 1.0}}]
    _buildStatTable(font, axes, locations=locations, elidedFallbackName=2)


def save_variable_font(
    family_key: str,
    family_name: str,
    default_style: str,
    designspace_path: Path,
    output_dir: Path,
    reports_dir: Path,
    italic: bool,
    gpos_source_path: Path | None = None,
) -> tuple[Path, Path, int, int, int, list[dict[str, float | str]], Path]:
    log_path = reports_dir / f"{family_key}-build.log"
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
        variable_font, *_ = varLib.build(str(designspace_path))

    if gpos_source_path is not None:
        gpos_source_font = TTFont(gpos_source_path)
        if "GPOS" in gpos_source_font:
            variable_font["GPOS"] = deepcopy(gpos_source_font["GPOS"])

    build_log = stdout_buffer.getvalue() + stderr_buffer.getvalue()
    log_path.write_text(build_log)

    if "GDEF" in variable_font and not hasattr(variable_font["GDEF"].table, "MarkGlyphSetsDef"):
        variable_font["GDEF"].table.MarkGlyphSetsDef = None

    patch_metadata(variable_font, family_name, default_style, italic)
    build_stat_table(variable_font, italic)

    ttf_path = output_dir / f"glide-cli-{family_key}-variable.ttf"
    woff2_path = output_dir / f"glide-cli-{family_key}-variable.woff2"
    variable_font.save(ttf_path)
    woff2_output_path = woff2_path
    try:
        compress_woff2(str(ttf_path), str(woff2_path))
    except ImportError as exc:
        woff2_output_path = None
        with log_path.open("a") as log_file:
            log_file.write(f"\nSkipping WOFF2 compression: {exc}\n")

    saved_font = TTFont(ttf_path)
    glyph_count = len(saved_font.getGlyphOrder())
    frozen = count_frozen_glyphs(saved_font)
    varying_glyphs = glyph_count - frozen
    axes = [
        {
            "tag": axis.axisTag,
            "minimum": axis.minValue,
            "default": axis.defaultValue,
            "maximum": axis.maxValue,
        }
        for axis in saved_font["fvar"].axes
    ]
    return (
        ttf_path,
        woff2_output_path,
        glyph_count,
        frozen,
        varying_glyphs,
        axes,
        log_path,
    )


def build_family(
    family_key: str,
    family_name: str,
    default_style: str,
    masters: list[MasterSpec],
    sample_dir: Path,
    normalized_dir: Path,
    output_dir: Path,
    reports_dir: Path,
    force: bool,
    italic: bool,
    axis_map: list[tuple[float, float]] | None,
    italic_kerning_donor_dir: Path,
) -> FamilySummary:
    normalized_paths, common_count, dropped_by_source, decomposed_by_source = normalize_family(
        family_key=family_key,
        masters=masters,
        sample_dir=sample_dir,
        normalized_dir=normalized_dir,
        force=force,
    )

    report_path = reports_dir / f"{family_key}-compat.json"
    compatibility_glyphs, issue_types, severity = run_interpolatable_report(
        normalized_paths,
        report_path,
    )

    designspace_path = normalized_dir / f"{family_key}.designspace"
    if italic:
        build_paths, _ = build_variable_italic_gpos_sources(
            source_paths=normalized_paths,
            donor_dir=italic_kerning_donor_dir,
            build_dir=normalized_dir / "italic-variable-kern",
            master_weights=[master.weight for master in masters],
            force=force,
        )
        gpos_source_path = None
    else:
        build_paths = prepare_build_sources(
            family_key=family_key,
            source_paths=normalized_paths,
            normalized_dir=normalized_dir,
            strip_gpos=False,
            force=force,
        )
        gpos_source_path = None
    build_designspace(
        family_name=family_name,
        default_style=default_style,
        masters=masters,
        source_paths=build_paths,
        designspace_path=designspace_path,
        axis_map=axis_map,
    )

    (
        ttf_path,
        woff2_path,
        output_glyphs,
        skipped_glyphs,
        varying_glyphs,
        axes,
        log_path,
    ) = save_variable_font(
        family_key=family_key,
        family_name=family_name,
        default_style=default_style,
        designspace_path=designspace_path,
        output_dir=output_dir,
        reports_dir=reports_dir,
        italic=italic,
        gpos_source_path=gpos_source_path,
    )

    return FamilySummary(
        family_key=family_key,
        default_style=default_style,
        sources=[master.filename for master in masters],
        common_glyphs=common_count,
        dropped_by_source=dropped_by_source,
        decomposed_by_source=decomposed_by_source,
        compatibility_glyphs=compatibility_glyphs,
        compatibility_issue_types=issue_types,
        compatibility_severity=severity,
        ttf_output=str(ttf_path),
        woff2_output="" if woff2_path is None else str(woff2_path),
        output_glyphs=output_glyphs,
        skipped_glyphs=skipped_glyphs,
        varying_glyphs=varying_glyphs,
        frozen_glyphs=skipped_glyphs,
        fvar_axes=axes,
        build_log=str(log_path),
        compatibility_report=str(report_path),
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    config = load_source_config(args.manifest)
    sample_dir = (repo_root / args.sample_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    normalized_dir = (repo_root / args.normalized_dir).resolve()
    reports_dir = (repo_root / args.reports_dir).resolve()
    italic_kerning_donor_dir = (repo_root / args.italic_kerning_donor_dir).resolve()

    if not sample_dir.exists():
        raise SystemExit(f"Sample directory not found: {sample_dir}")

    normalized_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    roman_family = config.families.get("roman")
    if roman_family is None or not roman_family.masters:
        raise SystemExit("Source config does not define a usable roman family.")
    roman_masters = select_masters(roman_family, args.two_master)

    italic_family = config.families.get("italic")
    italic_masters = select_masters(italic_family, args.two_master) if italic_family else []
    weight_axis_map = list(config.axis_maps.get("wght", ())) or None

    summaries: list[FamilySummary] = []
    summaries.append(
        build_family(
            family_key="roman",
            family_name=config.family_name,
            default_style=roman_family.default_style,
            masters=roman_masters,
            sample_dir=sample_dir,
            normalized_dir=normalized_dir,
            output_dir=output_dir,
            reports_dir=reports_dir,
            force=args.force,
            italic=False,
            axis_map=weight_axis_map,
            italic_kerning_donor_dir=italic_kerning_donor_dir,
        )
    )

    if not args.skip_italic and italic_masters:
        summaries.append(
            build_family(
                family_key="italic",
                family_name=config.family_name,
                default_style=italic_family.default_style,
                masters=italic_masters,
                sample_dir=sample_dir,
                normalized_dir=normalized_dir,
                output_dir=output_dir,
                reports_dir=reports_dir,
                force=args.force,
                italic=True,
                axis_map=weight_axis_map,
                italic_kerning_donor_dir=italic_kerning_donor_dir,
            )
        )

    summary_path = reports_dir / "summary.json"
    summary_payload = {
        "manifest": None if args.manifest is None else str(Path(args.manifest).resolve()),
        "family_name": config.family_name,
        "mode": "two-master" if args.two_master else "four-master",
        "sample_dir": str(sample_dir),
        "output_dir": str(output_dir),
        "families": [asdict(summary) for summary in summaries],
    }
    summary_path.write_text(json.dumps(summary_payload, indent=2))

    print(f"Wrote summary: {summary_path}")
    for summary in summaries:
        print(
            f"{summary.family_key}: glyphs={summary.output_glyphs}, "
            f"varying={summary.varying_glyphs}, frozen={summary.frozen_glyphs}, "
            f"compat_glyphs={summary.compatibility_glyphs}"
        )
        print(f"  ttf:   {summary.ttf_output}")
        print(f"  woff2: {summary.woff2_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
