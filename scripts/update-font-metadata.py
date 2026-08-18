#!/usr/bin/env python3
"""Regenerate specimen metadata from the canonical Roman variable font."""

from __future__ import annotations

import argparse
import json
import unicodedata
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


REPO = Path(__file__).resolve().parent.parent


def _character(codepoint: int) -> str:
    if codepoint <= 0xFFFF:
        return f"\\u{codepoint:04x}"
    return f"\\u{{{codepoint:x}}}"


def _charset(font: TTFont) -> str:
    entries = [
        (codepoint, glyph_name)
        for codepoint, glyph_name in sorted((font.getBestCmap() or {}).items())
        if not unicodedata.category(chr(codepoint)).startswith("C")
    ]
    rows = [
        "/** Encoded printable codepoints from glide-variable.ttf cmap. Regenerated when the font ships. */",
        "export type CharsetEntry = {",
        "  cp: number;",
        "  hex: string;",
        "  name: string;",
        "  char: string;",
        "};",
        "",
        "export const CHARSET: readonly CharsetEntry[] = [",
    ]
    for codepoint, glyph_name in entries:
        rows.append(
            f'  {{ cp: {codepoint}, hex: "{codepoint:04X}", '
            f'name: {json.dumps(glyph_name)}, char: "{_character(codepoint)}" }},'
        )
    rows.extend(
        [
            "];",
            "",
            "export const DEFAULT_GLYPH =",
            '  CHARSET.find((entry) => entry.name === "A") ?? CHARSET[0];',
            "",
            "export function findGlyph(id: string | undefined | null): CharsetEntry {",
            "  if (!id) {",
            "    return DEFAULT_GLYPH;",
            "  }",
            "  const q = id.trim();",
            "  if (!q) {",
            "    return DEFAULT_GLYPH;",
            "  }",
            "  const lower = q.toLowerCase();",
            '  const hex = lower.replace(/^u\\+/, "");',
            "  return (",
            "    CHARSET.find((entry) => entry.name === q) ??",
            "    CHARSET.find((entry) => entry.name.toLowerCase() === lower) ??",
            "    CHARSET.find((entry) => entry.hex.toLowerCase() === hex) ??",
            "    CHARSET.find((entry) => entry.char === q) ??",
            "    DEFAULT_GLYPH",
            "  );",
            "}",
            "",
        ]
    )
    return "\n".join(rows)


def _x_height(font: TTFont, weight: float | None = None) -> int:
    """Top of `x`, optionally at one weight on a variable font.

    `getGlyphSet(location=...)` interpolates the single glyph without instancing
    the whole font: measured at 0.004s against 0.79s for three stops.
    """
    location = None if weight is None else {"wght": weight}
    glyph_set = font.getGlyphSet(location=location)
    pen = BoundsPen(glyph_set)
    glyph_set[font.getBestCmap()[ord("x")]].draw(pen)
    return round(pen.bounds[3])


def _metrics(font: TTFont, mono: TTFont) -> str:
    head = font["head"]
    os2 = font["OS/2"]
    hhea = font["hhea"]
    # Stops at the drawn masters. Interpolation between them is linear, so three
    # points describe the whole axis exactly.
    wght = next(a for a in font["fvar"].axes if a.axisTag == "wght")
    stops = [
        (round(w), _x_height(font, w))
        for w in (wght.minValue, wght.defaultValue, wght.maxValue)
    ]
    return "\n".join(
        [
            "/** OS/2 + hhea values from the shipped glide-variable.ttf. */",
            "export const GLIDE_METRICS = {",
            f"  unitsPerEm: {head.unitsPerEm},",
            f"  capHeight: {os2.sCapHeight},",
            f"  ascender: {hhea.ascent},",
            f"  descender: {hhea.descent},",
            "} as const;",
            "",
            "/**",
            " * x-height by weight. Glide's x-height rises across the weight axis",
            " * while cap height stays at a constant "
            f"{os2.sCapHeight}, so anything drawing an",
            " * x-height guide must interpolate rather than use the single OS/2",
            " * value, which describes the default master only.",
            " */",
            "export const GLIDE_X_HEIGHT_STOPS = [",
            *[f"  [{weight}, {value}]," for weight, value in stops],
            "] as const satisfies readonly (readonly [number, number])[];",
            "",
            "/**",
            " * Glide Mono is single-weight, so its x-height does not vary and it",
            " * needs constants rather than stops. Anything drawing metric guides",
            " * must switch on the family: the proportional stops do not apply.",
            " */",
            "export const GLIDE_MONO_METRICS = {",
            f"  capHeight: {mono['OS/2'].sCapHeight},",
            f"  xHeight: {_x_height(mono)},",
            "} as const;",
            "",
        ]
    )


def _write(path: Path, contents: str, *, check: bool) -> None:
    if check:
        if not path.is_file() or path.read_text() != contents:
            raise SystemExit(f"stale generated font metadata: {path.relative_to(REPO)}")
        return
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(contents)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=REPO / "fonts/glide-variable.ttf")
    parser.add_argument("--mono", type=Path, default=REPO / "fonts/glide-mono.ttf")
    parser.add_argument(
        "--charset", type=Path, default=REPO / "apps/web/lib/charset.ts"
    )
    parser.add_argument(
        "--metrics", type=Path, default=REPO / "apps/web/lib/font-metrics.ts"
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    font = TTFont(args.font, lazy=True)
    mono = TTFont(args.mono, lazy=True)
    cmap_count = len(font.getBestCmap() or {})
    printable_count = sum(
        not unicodedata.category(chr(codepoint)).startswith("C")
        for codepoint in (font.getBestCmap() or {})
    )
    _write(args.charset, _charset(font), check=args.check)
    _write(args.metrics, _metrics(font, mono), check=args.check)
    mono.close()
    font.close()
    action = "verified" if args.check else "updated"
    print(f"{action} specimen metadata: {printable_count}/{cmap_count} printable cmap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
