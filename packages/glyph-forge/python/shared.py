"""Paths, weight mapping, seed lists, and font-loading helpers for glyph-forge.

Reads from packages/variable-gen reports; writes only inside packages/glyph-forge/.
Keep side-effect-free at import time so the CLIs can import cheaply.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fontTools.ttLib import TTFont

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = PACKAGE_ROOT / "public-cache" / "svg"
MANIFEST_PATH = PACKAGE_ROOT / "manifests" / "broken-glyphs.json"

VARIABLE_GEN_REPORTS = REPO_ROOT / "packages" / "variable-gen" / "reports"
TRIAGE_MANIFEST = (
    REPO_ROOT / "packages" / "variable-gen" / "manifests" / "circular-triage.json"
)

# Use the full variable-gen build, not fonts/*.ttf — the fonts/ TTFs are subset
# to ~472 glyphs for shipping; variable-gen's build has the full 744-glyph set we
# need for audit coverage of glyphs like amacron, Dcroat, etc.
VARIABLE_GEN_BUILD = REPO_ROOT / "packages" / "variable-gen" / "build"
GLIDE_ROMAN_TTF = VARIABLE_GEN_BUILD / "roman" / "glide-variable-vf.ttf"
GLIDE_ITALIC_TTF = VARIABLE_GEN_BUILD / "italic" / "glide-variable-italic-vf.ttf"

CIRCULAR_DIR = REPO_ROOT / "cabinet" / "Circular"
CIRCULAR_ROMAN_DIR = CIRCULAR_DIR / "Circular"
CIRCULAR_ITALIC_DIR = CIRCULAR_DIR / "Circular Italic"

Family = Literal["roman", "italic"]
CellSource = Literal["donor", "glide"]


@dataclass(frozen=True)
class CircularWeight:
    name: str
    wght: int


# Read from Circular OTF OS/2.usWeightClass — stays in sync with the donor files.
CIRCULAR_WEIGHTS: tuple[CircularWeight, ...] = (
    CircularWeight("Thin", 250),
    CircularWeight("Light", 300),
    CircularWeight("Regular", 400),
    CircularWeight("Book", 450),
    CircularWeight("Medium", 500),
    CircularWeight("Bold", 700),
    CircularWeight("Black", 900),
    CircularWeight("ExtraBlack", 950),
)

WGHT_VALUES: tuple[int, ...] = tuple(w.wght for w in CIRCULAR_WEIGHTS)


def circular_otf(family: Family, weight_name: str) -> Path:
    folder = CIRCULAR_ITALIC_DIR if family == "italic" else CIRCULAR_ROMAN_DIR
    suffix = f"{weight_name}Italic" if family == "italic" else weight_name
    return folder / f"Circular-{suffix}.otf"


def glide_vf(family: Family) -> Path:
    return GLIDE_ITALIC_TTF if family == "italic" else GLIDE_ROMAN_TTF


# Seed lists copied verbatim from the user's two planning messages.
# Each entry is either a Unicode character (resolved via cmap) or a glyph name
# (treated literally). Glyph names may have a leading "/" from the user's notation.
ITALIC_SEED: tuple[str, ...] = (
    # plain
    "X", "a", "e", "g", "s", "t", "u",
    # symbols + digits
    "%", "&", "'", "2", "3", "?",
    # latin-1 supplement
    "£", "¥", "ª", "«", "²", "´", "µ", "¸", "»",
    "¼", "½", "¾", "¿", "Ç", "Ð",
    # accented lowercase
    "æ", "ç", "è", "é", "ê", "ë", "í",
    "ù", "ú", "û", "ü", "ý",
    # latin extended-A/B
    "ā", "ă", "ą", "ď", "Đ",
    "ē", "ĕ", "ė", "ę", "ě",
    "ĝ", "ğ", "ġ", "ģ",
    "Ĩ", "ĩ", "Ĳ",
    "ľ", "Ľ", "ņ", "ŉ", "œ",
    "ś", "ŝ", "ş", "š",
    "Ţ", "ţ", "Ť", "ť", "Ŧ", "ŧ",
    "ũ", "ū", "ŭ", "ů", "Ű", "ű", "Ų", "ų",
    # IPA + extra
    "Ə", "ǽ", "ș", "ț", "ə",
    # spacing marks
    "ˇ", "˜", "˝",
    # greek
    "μ",
    # extended latin / misc
    "Ẋ", "‰",
    "₁", "₂", "₇", "€", "™",
    "Ⅽ", "Ⅾ", "Ⅿ",
    "↑",
    # ligatures
    "ﬀ", "ﬁ", "ﬂ", "ﬃ", "ﬄ",
    # slashed glyph names
    "/i.latn_TRK",
    "/two.numr", "/five.numr",
    "/two.dnom", "/five.dnom",
    "/a.ordn", "/c.ordn", "/d.ordn", "/e.ordn",
    "/r.ordn", "/s.ordn", "/t.ordn", "/u.ordn",
    "/percent.tf", "/two.tf", "/sterling.tf", "/yen.tf", "/Euro.tf",
    "/braceleft.case", "/braceright.case",
    "/guillemotleft.case", "/guillemotright.case",
    "/questiondown.case",
    "/G.ss01", "/Gcircumflex.ss01", "/Gbreve.ss01",
    "/Gdotaccent.ss01", "/Gcommaaccent.ss01",
    "/r.ss03", "/racute.ss03", "/rcommaaccent.ss03", "/rcaron.ss03",
    "/ampersand.ss04",
    "/quotedbl.ss08", "/quotesingle.ss08",
    "/three.ss08", "/five.ss08",
    "/sterling.ss08", "/yen.ss08",
    "/ordfeminine.ss08", "/Euro.ss08",
    "/uni2113.ss08", "/uni2165.ss08", "/uni2166.ss08",
    "/uni2167.ss08", "/uni2168.ss08",
    "/uni216E.ss08", "/uni216F.ss08",
    "/two.numr.ss08", "/five.numr.ss08",
    "/six.numr.ss08", "/seven.numr.ss08",
    "/a.ordn.ss08", "/c.ordn.ss08", "/d.ordn.ss08",
    "/r.ordn.ss08", "/s.ordn.ss08",
    "/t.ordn.ss08", "/u.ordn.ss08",
    "/three.tf.ss08", "/five.tf.ss08",
    "/sterling.tf.ss08", "/yen.tf.ss08",
    "/infinity.ss08",
    "/f_f", "/f_f_i", "/f_f_l", "/f_i", "/f_l",
    "/acute.uc", "/caron.uc", "/hungarumlaut.uc", "/caron.alt.uc",
)


ROMAN_SEED: tuple[str, ...] = (
    # plain
    "a", "e", "t",
    # symbols + digits
    "&", "2", "3", "6", "9", "?",
    # latin-1
    "²", "³", "µ", "½", "¾",
    "à", "á", "â", "ã", "ä", "å", "æ",
    "è", "é", "ê", "ë",
    # latin extended
    "ā", "ă", "ą",
    "ē", "ĕ", "ė", "ę", "ě",
    "ĸ", "ņ", "ŉ", "œ",
    "Ş", "ş", "ť", "ŧ",
    "ű", "Ų", "ų",
    # IPA
    "Ə", "ǽ", "ț", "ə",
    # marks
    "˜", "˝",
    # greek
    "μ", "π",
    # extras
    "₂", "₃", "₇", "€", "™",
    "Ⅷ", "Ⅿ",
    "↑",
    "ﬀ", "ﬂ",
    # slashed glyph names
    "/three.numr",
    "/a.ordn", "/d.ordn", "/e.ordn", "/m.ordn", "/n.ordn", "/r.ordn",
    "/zero.tf", "/two.tf", "/three.tf", "/six.tf", "/nine.tf", "/sterling.tf",
    "/guillemotright.case",
    # ss02 a-variants
    "/agrave.ss02", "/aacute.ss02", "/acircumflex.ss02", "/atilde.ss02",
    "/adieresis.ss02", "/aring.ss02", "/amacron.ss02", "/abreve.ss02",
    "/aogonek.ss02", "/aringacute.ss02",
    # ss03
    "/r.ss03", "/racute.ss03", "/rcommaaccent.ss03", "/rcaron.ss03",
    # ss04
    "/ampersand.ss04",
    # ss08
    "/two.ss08", "/three.ss08", "/six.ss08", "/nine.ss08",
    "/ordfeminine.ss08", "/onehalf.ss08", "/threequarters.ss08",
    "/uni2167.ss08", "/uni216E.ss08", "/uni216F.ss08",
    "/three.numr.ss08",
    "/a.ordn.ss08", "/d.ordn.ss08", "/e.ordn.ss08",
    "/m.ordn.ss08", "/n.ordn.ss08", "/r.ordn.ss08",
    "/two.tf.ss08", "/three.tf.ss08", "/six.tf.ss08", "/nine.tf.ss08",
    "/f_f", "/f_l",
    "/hungarumlaut.uc",
)


def normalise_name(raw: str) -> str:
    """User writes /agrave.ss02; canonicalise to agrave.ss02."""
    return raw.lstrip("/").strip()


@lru_cache(maxsize=32)
def load_font(path: Path) -> TTFont:
    return TTFont(path)


@lru_cache(maxsize=None)
def _cmap(path: Path) -> dict[int, str]:
    return load_font(path).getBestCmap()


def resolve_glyph_name(raw: str, font_path: Path) -> str | None:
    """Resolve a seed entry to a glyph name valid for the given font, or None."""
    canon = normalise_name(raw)
    if not canon:
        return None
    font = load_font(font_path)
    order = set(font.getGlyphOrder())
    # Direct name match first (covers /agrave.ss02, f_f_i, etc.).
    if canon in order:
        return canon
    # Single character → cmap lookup.
    if len(canon) == 1:
        glyph = _cmap(font_path).get(ord(canon))
        if glyph and glyph in order:
            return glyph
    return None


def feature_tags(glyph_name: str) -> list[str]:
    """Extract suffixes like ss02, ordn, tf, case, uc, numr, dnom, latn_TRK."""
    parts = glyph_name.split(".")
    if len(parts) <= 1:
        return []
    return [p for p in parts[1:] if p]


def glyph_unicode(glyph_name: str, font_path: Path) -> str | None:
    """Reverse-lookup a single Unicode codepoint for a glyph, if any."""
    cmap = _cmap(font_path)
    for cp, name in cmap.items():
        if name == glyph_name:
            return f"U+{cp:04X}"
    return None
