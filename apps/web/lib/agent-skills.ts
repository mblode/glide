import { createHash } from "node:crypto";
import { siteConfig } from "./config";

export const downloadSkill = [
  "# Download Glide",
  "",
  `Glide ${siteConfig.version} is served as individual variable font files (roman and italic) plus a static monospace.`,
  "",
  `- Variable roman: ${siteConfig.url}/glide-variable.woff2`,
  `- Variable italic: ${siteConfig.url}/glide-variable-italic.woff2`,
  `- Monospace: ${siteConfig.url}/glide-mono.woff2`,
  `- Source and license: ${siteConfig.links.github}`,
  "",
  "## Steps",
  "1. GET the font file URLs above (.ttf is also available at the same paths).",
  "2. Install the .woff2 or .ttf files you need.",
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
