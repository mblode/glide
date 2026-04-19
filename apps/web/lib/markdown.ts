import { siteConfig } from "./config";

export const homepageMarkdown = `# Glide

Variable font family crafted for UI.

${siteConfig.description}

- Site: ${siteConfig.url}
- Download: ${siteConfig.url}/download
- Archive: ${siteConfig.downloadUrl}
- Source: ${siteConfig.links.github}
- Author: ${siteConfig.author.name} — ${siteConfig.author.url}

## Sections

- Playground — ${siteConfig.url}/#playground
- Weights — ${siteConfig.url}/#weights
- Install — ${siteConfig.url}/#install

## Weights

Glide ships in both roman and italic with weights from 400 to 900 as a variable font.
`;

export const downloadMarkdown = `# Download Glide

Glide ${siteConfig.version} — ${siteConfig.description}

- Archive: ${siteConfig.downloadUrl}
- All releases: ${siteConfig.links.github}/releases
- Source: ${siteConfig.links.github}

## Install
1. Download the zip archive from the URL above.
2. Unzip the archive.
3. Install the .woff2, .woff, .ttf, or .otf files you need.
`;

export const markdownByPath: Record<string, string> = {
  "/": homepageMarkdown,
  "/download": downloadMarkdown,
};
