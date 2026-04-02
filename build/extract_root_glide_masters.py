#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from font_metadata import WEIGHT_NAMES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract static Glide roman checkpoints from src/glide-variable.ttf."
    )
    parser.add_argument(
        "--input",
        default="src/glide-variable.ttf",
        help="Path to the root Glide variable TTF.",
    )
    parser.add_argument(
        "--output-dir",
        default="build/work/sources/glide-root-derived",
        help="Directory for extracted static TTF checkpoints.",
    )
    parser.add_argument(
        "--manifest",
        default="build/work/manifests/glide-root-derived.json",
        help="Path to write a source manifest for the extracted masters.",
    )
    parser.add_argument(
        "--family-name",
        default="Glide",
        help="Family name to store in the source manifest.",
    )
    parser.add_argument(
        "--source-family-name",
        default="Glide Root Source",
        help="Family name to write into the extracted static masters.",
    )
    parser.add_argument(
        "--weights",
        default="400,500,700,900",
        help="Comma-separated weight values to extract.",
    )
    return parser.parse_args()


def set_name_record(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    for platform_id, plat_enc_id, lang_id in ((3, 1, 0x409), (1, 0, 0)):
        name_table.setName(value, name_id, platform_id, plat_enc_id, lang_id)


def patch_static_metadata(font: TTFont, family_name: str, style_name: str, weight: int) -> None:
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
    os2.usWeightClass = weight
    post.italicAngle = 0.0
    if weight == 400:
        os2.fsSelection |= 0x40
    elif weight == 700:
        head.macStyle |= 0x01
        os2.fsSelection |= 0x20


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    weights = [int(weight.strip()) for weight in args.weights.split(",") if weight.strip()]

    if not input_path.exists():
        raise SystemExit(f"Variable font not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    masters: list[dict[str, object]] = []

    for weight in weights:
        style_name = WEIGHT_NAMES.get(weight, f"W{weight}")
        filename = f"glide-root-{style_name.lower()}.ttf"
        output_path = output_dir / filename

        static_font = instantiateVariableFont(TTFont(input_path), {"wght": weight})
        patch_static_metadata(static_font, args.source_family_name, style_name, weight)
        static_font.save(output_path)

        masters.append(
            {
                "filename": filename,
                "style_name": style_name,
                "weight": weight,
            }
        )
        print(f"Saved: {output_path}")

    manifest = {
        "family_name": args.family_name,
        "families": {
            "roman": {
                "default_style": "Regular",
                "masters": masters,
            }
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
