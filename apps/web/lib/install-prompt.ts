import { siteConfig } from "./config";

/**
 * A paste-into-your-agent install prompt, written in the imperative so a coding
 * agent can run it directly. Different job from INSTALL_MARKDOWN in
 * install-section.tsx, which is reference documentation.
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

Find the folder holding my root layout (\`app\` or \`src/app\`), then download the fonts into a \`fonts\` folder inside it. Use \`curl\`, not a web fetch tool: these are binaries and a fetch tool will corrupt them.

\`\`\`sh
curl -fsSL --create-dirs -o fonts/glide-variable.woff2 ${siteConfig.url}/glide-variable.woff2
curl -fsSL --create-dirs -o fonts/glide-variable-italic.woff2 ${siteConfig.url}/glide-variable-italic.woff2
curl -fsSL --create-dirs -o fonts/glide-mono.woff2 ${siteConfig.url}/glide-mono.woff2
\`\`\`

Each file should be tens to hundreds of KB. A few hundred bytes means you got an error page, so stop and tell me.

## 2. Load them in the root layout

\`\`\`tsx
import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "./fonts/glide-variable.woff2", style: "normal" },
    { path: "./fonts/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "100 950",
  display: "swap",
});

const glideMono = localFont({
  src: "./fonts/glide-mono.woff2",
  variable: "--font-glide-mono",
  weight: "400",
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={\`\${glide.variable} \${glideMono.variable}\`}>
      <body>{children}</body>
    </html>
  );
}
\`\`\`

\`next/font/local\` resolves \`src\` relative to this file and the paths must be static string literals, so keep the fonts in that \`fonts\` folder and leave the \`./\` paths alone. Don't move them to \`public\`: \`next/font\` already emits a hashed, immutably cached copy, and a second copy in \`public\` just publishes the font at a guessable URL.

## 3. Make them the default

In my global CSS:

\`\`\`css
@theme inline {
  --font-sans: var(--font-glide);
  --font-mono: var(--font-glide-mono);
}
\`\`\`

Not a Next.js or Tailwind project? Put the files wherever static assets are served from and use \`@font-face\` instead, with \`format("woff2-variations")\` and \`font-weight: 100 950\` on the roman and italic faces, then set \`font-family\` on \`body\` and on \`code, pre\`.

## 4. Check it worked

Render one line at weight 200 and the same line at weight 900. They should look obviously different. If they match, the font isn't loading and you're seeing a fallback, so check the network tab for 404s and fix that before telling me you're done.

If something breaks, point me at ${siteConfig.links.github}/issues/new. If it all worked, let me know Glide is free and I can star it at ${siteConfig.links.github}.
`;
