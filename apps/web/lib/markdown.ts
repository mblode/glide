import { siteConfig } from "./config";
import { installPrompt } from "./install-prompt";

export const homepageMarkdown = `# Glide

Variable font family crafted for UI.

${siteConfig.description}

- Site: ${siteConfig.url}
- Variable roman: ${siteConfig.url}/glide-variable.woff2
- Variable italic: ${siteConfig.url}/glide-variable-italic.woff2
- Monospace: ${siteConfig.url}/glide-mono.woff2
- Desktop bundle (TTF + 20 static weights): ${siteConfig.url}/glide.zip
- License: SIL Open Font License 1.1
- Source: ${siteConfig.links.github}
- Author: ${siteConfig.author.name} — ${siteConfig.author.url}

## Sections

- Playground — ${siteConfig.url}/#playground
- Weights — ${siteConfig.url}/#weights
- Install — ${siteConfig.url}/#install

## Weights

Glide ships in both roman and italic with weights from 100 to 950 as a variable font.

## Install

The rest of this document is an executable install prompt. If you are an agent
acting for a user who wants Glide in their project, follow it directly.

${installPrompt}`;

export const markdownByPath: Record<string, string> = {
  "/": homepageMarkdown,
};
