"""The guide must measure the same optical coordinate as the enlarged glyph."""
import importlib.util
from pathlib import Path

from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("font_metadata", ROOT / "scripts/update-font-metadata.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_x_height_passes_both_axis_coordinates_to_the_font():
    class Glyph:
        def draw(self, pen):
            pen.moveTo((0, 0))
            pen.lineTo((100, 525))
            pen.closePath()

    class Font:
        def getBestCmap(self):
            return {ord("x"): "x"}

        def getGlyphSet(self, *, location):
            assert location == {"wght": 950, "opsz": 14}
            return {"x": Glyph()}

    assert MODULE._x_height(Font(), 950, 14) == 525


def test_shipped_metadata_matches_independent_roman_and_italic_text_bounds():
    with TTFont(ROOT / "fonts/glide-variable.ttf") as roman, \
         TTFont(ROOT / "fonts/glide-variable-italic.ttf") as italic, \
         TTFont(ROOT / "fonts/glide-mono.ttf") as mono:
        generated = MODULE._metrics(roman, mono, italic)
        assert "export const GLIDE_TEXT_OPSZ = 14;" in generated
        assert "export const GLIDE_ITALIC_X_HEIGHT_STOPS" in generated
        assert generated == (ROOT / "apps/web/lib/font-metrics.ts").read_text()
