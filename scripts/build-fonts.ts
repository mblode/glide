import { copyFileSync, existsSync, mkdirSync, writeFileSync } from "fs";
import { join } from "path";

const ROOT = new URL("..", import.meta.url).pathname;
const INPUT_ROMAN = join(ROOT, "cabinet/input/roman");
const INPUT_ITALIC = join(ROOT, "cabinet/input/italic");
const FONTS = join(ROOT, "fonts");
const WEB = join(ROOT, "fonts/web");

mkdirSync(FONTS, { recursive: true });
mkdirSync(WEB, { recursive: true });

function copy(src: string, dest: string, required = true) {
  if (existsSync(src)) {
    copyFileSync(src, dest);
    console.log(`  ✓ ${dest.replace(ROOT, "")}`);
  } else if (required) {
    console.warn(`  ✗ MISSING: ${src.replace(ROOT, "")}`);
  }
}

// Variable TTF → fonts/
copy(join(INPUT_ROMAN, "GlideVF.ttf"), join(FONTS, "glide-variable.ttf"));
copy(join(INPUT_ITALIC, "GlideVF.ttf"), join(FONTS, "glide-variable-italic.ttf"));

// Variable WOFF2 → fonts/web/
copy(join(INPUT_ROMAN, "GlideVF.woff2"), join(WEB, "glide-variable.woff2"));
copy(join(INPUT_ITALIC, "GlideVF.woff2"), join(WEB, "glide-variable-italic.woff2"));

// Static roman WOFF2 → fonts/web/
copy(join(INPUT_ROMAN, "Glide-Regular.woff2"), join(WEB, "glide-regular.woff2"));
copy(join(INPUT_ROMAN, "Glide-Medium.woff2"),  join(WEB, "glide-medium.woff2"));
copy(join(INPUT_ROMAN, "Glide-Bold.woff2"),    join(WEB, "glide-bold.woff2"));
copy(join(INPUT_ROMAN, "Glide-Black.woff2"),   join(WEB, "glide-black.woff2"));

// Static italic WOFF2 → fonts/web/ (warn if missing)
copy(join(INPUT_ITALIC, "Glide-Regular-Italic.woff2"), join(WEB, "glide-regular-italic.woff2"), false);
copy(join(INPUT_ITALIC, "Glide-Medium-Italic.woff2"),  join(WEB, "glide-medium-italic.woff2"),  false);
copy(join(INPUT_ITALIC, "Glide-Bold-Italic.woff2"),    join(WEB, "glide-bold-italic.woff2"),    false);
copy(join(INPUT_ITALIC, "Glide-Black-Italic.woff2"),   join(WEB, "glide-black-italic.woff2"),   false);

// Generate glide.css
const css = `/* Variable font usage:
:root { font-family: "Glide", sans-serif; }
@supports (font-variation-settings: normal) {
  :root { font-family: "GlideVariable", sans-serif; }
} */
@font-face {
  font-family: GlideVariable;
  font-style: normal;
  font-weight: 400 900;
  font-display: swap;
  src: url("glide-variable.woff2") format("woff2");
}
@font-face {
  font-family: GlideVariable;
  font-style: italic;
  font-weight: 400 900;
  font-display: swap;
  src: url("glide-variable-italic.woff2") format("woff2");
}

/* static fonts */
@font-face { font-family: "Glide"; font-style: normal; font-weight: 400; font-display: swap; src: url("glide-regular.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: italic; font-weight: 400; font-display: swap; src: url("glide-regular-italic.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: normal; font-weight: 500; font-display: swap; src: url("glide-medium.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: italic; font-weight: 500; font-display: swap; src: url("glide-medium-italic.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: normal; font-weight: 700; font-display: swap; src: url("glide-bold.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: italic; font-weight: 700; font-display: swap; src: url("glide-bold-italic.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: normal; font-weight: 900; font-display: swap; src: url("glide-black.woff2") format("woff2"); }
@font-face { font-family: "Glide"; font-style: italic; font-weight: 900; font-display: swap; src: url("glide-black-italic.woff2") format("woff2"); }
`;

writeFileSync(join(WEB, "glide.css"), css);
console.log(`  ✓ fonts/web/glide.css`);
