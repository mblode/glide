import { createHash } from "node:crypto";
import { siteConfig } from "./config";

export const downloadSkill = [
  "# Download Glide",
  "",
  `Glide ${siteConfig.version} is available as a zip archive containing variable and static fonts in roman and italic.`,
  "",
  `- Archive: ${siteConfig.downloadUrl}`,
  `- Releases: ${siteConfig.links.github}/releases`,
  `- License: see ${siteConfig.links.github}/blob/main/README.md`,
  "",
  "## Steps",
  "1. GET the archive URL above.",
  "2. Unzip the archive.",
  "3. Install the .woff2, .woff, .ttf, or .otf files you need.",
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
  "  font-weight: 100 900;",
  "  font-style: normal;",
  "  font-display: swap;",
  "}",
  "",
  "@font-face {",
  '  font-family: "Glide";',
  '  src: url("/glide-variable-italic.woff2") format("woff2-variations");',
  "  font-weight: 100 900;",
  "  font-style: italic;",
  "  font-display: swap;",
  "}",
  "```",
  "",
].join("\n");

export function sha256(text: string): string {
  return createHash("sha256").update(text, "utf8").digest("hex");
}
