import { createHash } from "node:crypto";
import { siteConfig } from "./config";

export const downloadSkill = [
  "# Download Glide",
  "",
  `Glide ${siteConfig.version} is served as individual variable font files (roman, italic, and mono).`,
  "",
  `- Variable roman: ${siteConfig.url}/glide-variable.woff2`,
  `- Variable italic: ${siteConfig.url}/glide-variable-italic.woff2`,
  `- Variable mono: ${siteConfig.url}/glide-mono-variable.woff2`,
  `- Static mono 400: ${siteConfig.url}/glide-mono.woff2`,
  `- Desktop bundle: ${siteConfig.url}/glide.zip`,
  `- Source and license: ${siteConfig.links.github}`,
  "",
  "Glide is licensed under the SIL Open Font License 1.1.",
  "",
  "## Steps",
  "1. For the web, GET the .woff2 URLs above (.ttf is at the same paths).",
  "2. For desktop use, GET glide.zip: TTF, both variable fonts, Glide Mono and",
  "   20 static weights, for Figma, Font Book and Adobe apps.",
  "",
].join("\n");

export const embedSkill = [
  "# Embed Glide on the web",
  "",
  "Glide ships as a variable woff2 file suitable for `@font-face`.",
  "",
  "```css",
  "@font-face {",
  '  font-family: "Glide";',
  '  src: url("/glide-variable.woff2") format("woff2-variations");',
  "  font-weight: 100 950;",
  "  font-style: normal;",
  "  font-display: swap;",
  "}",
  "",
  "@font-face {",
  '  font-family: "Glide";',
  '  src: url("/glide-variable-italic.woff2") format("woff2-variations");',
  "  font-weight: 100 950;",
  "  font-style: italic;",
  "  font-display: swap;",
  "}",
  "```",
  "",
].join("\n");

export function sha256(text: string): string {
  return createHash("sha256").update(text, "utf8").digest("hex");
}
