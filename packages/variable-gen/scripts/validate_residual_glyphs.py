#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest_tools import expand_manifest

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = SCRIPT_DIR.parent
DEFAULT_MANIFEST = PACKAGE_DIR / "manifests/circular-triage.json"
DEFAULT_REPORT_DIR = PACKAGE_DIR / "reports/repair"
DEFAULT_OUTPUT = DEFAULT_REPORT_DIR / "tracked-residual-review.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate tracked residual glyphs and emit a compact review packet."
    )
    parser.add_argument(
        "--family",
        choices=("roman", "italic", "all"),
        default="all",
        help="Which family to validate.",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Path to the residual manifest JSON.",
    )
    parser.add_argument(
        "--report-dir",
        default=str(DEFAULT_REPORT_DIR),
        help="Directory containing repair reports.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown output path.",
    )
    parser.add_argument(
        "--max-area-drift",
        type=float,
        default=25.0,
        help="Fail when a tracked glyph exceeds this exact-master area drift percentage.",
    )
    parser.add_argument(
        "--min-segment-threshold",
        type=float,
        default=0.0,
        help="Optional minimum sampled segment threshold. Set above 0 to enforce.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def build_family_review(
    family_key: str,
    manifest: dict[str, object],
    report_dir: Path,
    max_area_drift: float,
    min_segment_threshold: float,
) -> tuple[list[str], dict[str, int], list[str]]:
    source_payload = load_json(report_dir / f"{family_key}-source-report.json")
    interpolatable_payload = load_json(report_dir / f"{family_key}-designspace-interpolatable.json")
    instance_payload = load_json(report_dir / f"{family_key}-instance-risk-report.json")
    validation_payload = load_json(report_dir / f"{family_key}-master-validation.json")

    source_index = {entry["glyph_name"]: entry for entry in source_payload["glyphs"]}
    tracked = manifest[family_key]["glyphs"]
    lines = [f"## {family_key.title()}", ""]
    counts = {
        "tracked": 0,
        "frozen": 0,
        "interpolatable": 0,
        "area_drift_failures": 0,
        "min_segment_failures": 0,
        "source_structure_failures": 0,
    }
    failures: list[str] = []

    for glyph_name in sorted(tracked):
        entry = source_index.get(glyph_name)
        manifest_entry = tracked[glyph_name]
        if not entry:
            failures.append(f"{family_key}:{glyph_name}: missing source report entry")
            continue

        counts["tracked"] += 1
        issues = interpolatable_payload.get(glyph_name, [])
        risky_weights = []
        min_segment = None
        for weight, payload in instance_payload.get("weights", {}).items():
            metrics = payload.get("risky_glyphs", {}).get(glyph_name)
            if not metrics:
                continue
            risky_weights.append(int(weight))
            value = metrics.get("min_segment_length")
            if value is not None:
                min_segment = value if min_segment is None else min(min_segment, value)

        area_diffs = []
        for weight, payload in validation_payload.get("weights", {}).items():
            value = payload.get("worst_area_diffs_pct", {}).get(glyph_name)
            if value is not None:
                area_diffs.append(float(value))
        max_area = max(area_diffs) if area_diffs else None

        source_path_order_issues = int(entry.get("source_path_order_issues") or 0)
        source_node_count_issues = int(entry.get("source_node_count_issues") or 0)
        source_start_issues = int(entry.get("source_start_issues") or 0)
        source_direction_issues = int(entry.get("source_direction_issues") or 0)
        source_structure_total = (
            source_path_order_issues
            + source_node_count_issues
            + source_start_issues
            + source_direction_issues
        )

        if entry.get("same_outline_across_masters"):
            counts["frozen"] += 1
            failures.append(f"{family_key}:{glyph_name}: exact-outline frozen")
        if issues:
            counts["interpolatable"] += 1
            failures.append(f"{family_key}:{glyph_name}: interpolatable={len(issues)}")
        if source_structure_total > 0:
            counts["source_structure_failures"] += 1
            failures.append(
                f"{family_key}:{glyph_name}: source structure "
                f"pathOrder={source_path_order_issues} "
                f"nodeCount={source_node_count_issues} "
                f"start={source_start_issues} "
                f"direction={source_direction_issues}"
            )
        if max_area is not None and max_area > max_area_drift:
            counts["area_drift_failures"] += 1
            failures.append(f"{family_key}:{glyph_name}: area drift {round(max_area, 2)}%")
        if min_segment_threshold > 0 and min_segment is not None and min_segment < min_segment_threshold:
            counts["min_segment_failures"] += 1
            failures.append(f"{family_key}:{glyph_name}: min segment {round(min_segment, 2)}")

        manifest_strategy = manifest_entry.get("strategy")
        source_strategy = entry.get("strategy")
        strategy_note = source_strategy
        if manifest_strategy and manifest_strategy != source_strategy:
            strategy_note = f"{source_strategy}->{manifest_strategy}"

        lines.append(
            "- "
            f"`{glyph_name}` strategy={strategy_note} class={entry['classification']} "
            f"group={entry.get('group_name') or manifest_entry.get('group_name')} "
            f"inherits={entry.get('inherits_from') or manifest_entry.get('inherits_from')} "
            f"brace={entry.get('generated_brace_weights', [])} "
            f"frozen={entry['same_outline_across_masters']} "
            f"interpolatable={len(issues)} "
            f"sourceAudit="
            f"{source_path_order_issues}/{source_node_count_issues}/{source_start_issues}/{source_direction_issues} "
            f"riskyWeights={risky_weights} "
            f"maxAreaDrift={None if max_area is None else round(max_area, 2)}"
        )

    lines.append("")
    lines.append(
        "- summary: "
        f"tracked={counts['tracked']} "
        f"frozen={counts['frozen']} "
        f"interpolatable={counts['interpolatable']} "
        f"sourceStructureFailures={counts['source_structure_failures']} "
        f"areaDriftFailures={counts['area_drift_failures']} "
        f"minSegmentFailures={counts['min_segment_failures']}"
    )
    lines.append("")
    return lines, counts, failures


def main() -> int:
    args = parse_args()
    manifest = expand_manifest(Path(args.manifest))
    report_dir = Path(args.report_dir)
    output_path = Path(args.output)

    selected = ["roman", "italic"] if args.family == "all" else [args.family]
    lines = ["# Tracked Residual Review", ""]
    all_failures: list[str] = []

    for family_key in selected:
        family_lines, _, failures = build_family_review(
            family_key=family_key,
            manifest=manifest,
            report_dir=report_dir,
            max_area_drift=args.max_area_drift,
            min_segment_threshold=args.min_segment_threshold,
        )
        lines.extend(family_lines)
        all_failures.extend(failures)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n")
    if all_failures:
        print("Residual validation failures:")
        for failure in all_failures:
            print(f"  - {failure}")
        print(f"review={output_path}")
        return 1
    print(f"review={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
