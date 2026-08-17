/**
 * The install code, in one place.
 *
 * These snippets appear on the page as CodeBlocks, inside the agent install
 * prompt, and in README.md. The first two import from here; README is checked
 * against them by scripts/check-install-docs.py, since markdown can't import.
 *
 * They had already drifted before this module existed: the prompt used the
 * string form of `src` for the mono font and imported ./globals.css, the page
 * used the array form and dropped the import.
 *
 * Keep this module free of `node:` imports so client components can use it.
 */

/** Fonts live next to the layout, so `src` is `./fonts/…` at any nesting depth. */
export const layoutSnippet = `import localFont from "next/font/local";
import "./globals.css";

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
}`;

export const themeSnippet = `@theme inline {
  --font-sans: var(--font-glide);
  --font-mono: var(--font-glide-mono);
}

html {
  font-optical-sizing: auto;
  font-kerning: normal;
}`;

export const usageSnippet = `<p className="font-sans font-normal">Regular (400)</p>
<p className="font-sans font-bold">Bold (700)</p>
<p className="font-sans font-black">Black (900)</p>
<p className="font-sans font-bold italic">Bold italic (700)</p>
<p className="tabular-nums">11:45 0123456789</p>
<p className="slashed-zero">0</p>
<code className="font-mono">const glide = "mono";</code>`;
