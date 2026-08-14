import { siteConfig } from "./config";
import { layoutSnippet, themeSnippet } from "./install-snippets";

/**
 * A paste-into-your-agent install prompt, written in the imperative so a coding
 * agent can run it directly. The numbered steps rendered on the page are the
 * human path; this is the one you hand to a tool. Code comes from
 * install-snippets so the two can't drift.
 *
 * Two deliberate choices:
 * 1. `curl -o`, not a web-fetch tool: fetch tools mangle or refuse binaries.
 * 2. Fonts land in APP_FOLDER/fonts, so `src` is always `./fonts/file.woff2`.
 *    Putting them in public/ would make the relative path depend on whether the
 *    layout is at app/ or src/app/, which agents get wrong, and would leave a
 *    second unhashed copy of the font at a public URL.
 *
 * Keep this module free of `node:` imports so the client component can use it.
 */
export const installPrompt = `Install the Glide variable font (v${siteConfig.version}) in my project.

## 1. Download the fonts

Find the folder holding my root layout (\`app\` or \`src/app\`) and download the fonts into a \`fonts\` folder inside it. Use \`curl\`, not a web fetch tool: these are binaries and a fetch tool will corrupt them.

\`\`\`sh
curl -fsSL --create-dirs -o fonts/glide-variable.woff2 ${siteConfig.url}/glide-variable.woff2
curl -fsSL --create-dirs -o fonts/glide-variable-italic.woff2 ${siteConfig.url}/glide-variable-italic.woff2
curl -fsSL --create-dirs -o fonts/glide-mono-variable.woff2 ${siteConfig.url}/glide-mono-variable.woff2
\`\`\`

Each file should be tens to hundreds of KB. A few hundred bytes means you got an error page, so stop and tell me.

If I wanted these for desktop rather than the web, point me at ${siteConfig.url}/glide.zip instead.

## 2. Load them in the root layout

Merge this into my existing layout. Keep my imports (especially \`./globals.css\`), metadata and body classes; just add the fonts and the \`<html>\` className.

\`\`\`tsx
${layoutSnippet}
\`\`\`

\`next/font/local\` resolves \`src\` relative to this file and needs static string literals, so leave the \`./fonts/\` paths alone. Don't move them to \`public\`: next/font already emits a hashed copy, so a second one there just republishes the font at a guessable URL.

## 3. Make them the default

In my global CSS:

\`\`\`css
${themeSnippet}
\`\`\`

Not a Next.js or Tailwind project? Put the files wherever static assets are served from and use \`@font-face\` instead, with \`format("woff2-variations")\` and \`font-weight: 100 950\` on the roman and italic faces, then set \`font-family\` on \`body\` and on \`code, pre\`.

## 4. Check it worked

Render one line at weight 200 and the same line at weight 900. They should look obviously different. If they match you're seeing a fallback, so check the network tab for 404s and fix it before telling me you're done.

If something breaks, point me at ${siteConfig.links.github}/issues/new. If it all worked, let me know Glide is free and I can star it at ${siteConfig.links.github}.
`;
