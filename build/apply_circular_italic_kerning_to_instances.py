#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont

from italic_variable_kerning import pair_value
from transfer_circular_kerning import (
    DONOR_ITALIC_FILES,
    normalize_pairpos_gpos,
    pair_stats,
    subset_donor_for_target,
)


INSTANCE_FILES = {
    400: "glide-cli-italic-variable-Regular.ttf",
    500: "glide-cli-italic-variable-Medium.ttf",
    700: "glide-cli-italic-variable-Bold.ttf",
    900: "glide-cli-italic-variable-Black.ttf",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply matching Circular italic donor kerning to generated Glide italic instances."
    )
    parser.add_argument(
        "--instances-dir",
        default="build/work/output/instances-italic",
        help="Directory containing generated Glide italic static instances.",
    )
    parser.add_argument(
        "--output-dir",
        default="build/work/output/instances-italic-exact",
        help="Directory for exact-match italic compare instances.",
    )
    parser.add_argument(
        "--donor-dir",
        default="src/donors/circular",
        help="Directory containing Circular donor fonts.",
    )
    parser.add_argument(
        "--report-out",
        default="build/work/reports/italic-instance-exact-kerning.json",
        help="Path to write the exact-match instance report.",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    instances_dir = (repo_root / args.instances_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    donor_dir = (repo_root / args.donor_dir).resolve()
    report_out = (repo_root / args.report_out).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {
        "instances_dir": str(instances_dir),
        "output_dir": str(output_dir),
        "donor_dir": str(donor_dir),
        "weights": [],
    }

    for weight, filename in INSTANCE_FILES.items():
        instance_path = instances_dir / filename
        if not instance_path.exists():
            raise SystemExit(f"Instance not found: {instance_path}")

        donor_path = donor_dir / DONOR_ITALIC_FILES[weight]
        output_path = output_dir / filename
        shutil.copy2(instance_path, output_path)

        target_font = TTFont(output_path, recalcBBoxes=False, recalcTimestamp=False)
        donor_font = TTFont(donor_path, recalcBBoxes=False, recalcTimestamp=False)
        donor_subset = subset_donor_for_target(donor_font, target_font)

        if "GPOS" in donor_subset:
            target_font["GPOS"] = donor_subset["GPOS"]
            normalize_pairpos_gpos(target_font)
        if "kern" in target_font:
            del target_font["kern"]
        target_font.save(output_path)

        reloaded = TTFont(output_path, recalcBBoxes=False, recalcTimestamp=False)
        to_value = pair_value(reloaded, "T", "o")

        report["weights"].append(
            {
                "weight": weight,
                "instance": str(output_path),
                "donor": str(donor_path),
                "pair_stats": pair_stats(reloaded),
                "To": to_value,
            }
        )
        print(f"Saved: {output_path} (To={to_value})")

    report_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.write_text(json.dumps(report, indent=2))
    print(f"Wrote report: {report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
