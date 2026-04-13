"use client";

import {
  Checkmark1Icon as CheckIcon,
  CopySimpleIcon as CopyIcon,
} from "blode-icons-react";
import { useCallback, useState } from "react";

import { CodeBlock } from "@/components/code-block";
import { ENABLE_ITALIC } from "@/lib/flags";

function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-lg font-bold tracking-tight">{children}</h2>
  );
}

function InstallStep({
  step,
  title,
  description,
  children,
}: {
  step: number;
  title: string;
  description?: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-sm font-bold text-primary tabular-nums">
          {step}
        </span>
        <h3 className="text-lg font-bold tracking-tight">{title}</h3>
      </div>
      {description && (
        <p className="text-sm leading-relaxed text-muted-foreground sm:pl-11">
          {description}
        </p>
      )}
      {children && <div className="sm:pl-11">{children}</div>}
    </div>
  );
}

const INSTALL_MARKDOWN = `# Install Glide

## 1. Download the font files

Download [glide-variable.woff2](https://glide.blode.co/glide-variable.woff2)${ENABLE_ITALIC ? " and [glide-variable-italic.woff2](https://glide.blode.co/glide-variable-italic.woff2)" : ""} and place them in your project's public/ directory.

## 2. Configure the font in your root layout

In app/layout.tsx, import localFont and configure the Glide variable font:

\`\`\`tsx
import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },${ENABLE_ITALIC ? '\n    { path: "../public/glide-variable-italic.woff2", style: "italic" },' : ""}
  ],
  variable: "--font-glide",
  weight: "400 900",
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={glide.variable}>{children}</body>
    </html>
  );
}
\`\`\`

## 3. Map the CSS variable in Tailwind

In your global CSS file, map --font-glide to Tailwind's --font-sans so font-sans uses Glide:

\`\`\`css
@theme inline {
  --font-sans: var(--font-glide);
}
\`\`\`

## 4. Use it

Glide is now your default sans-serif font. Use font-sans with any weight from 400 to 900:

\`\`\`tsx
<p className="font-sans font-normal">Regular (400)</p>
<p className="font-sans font-bold">Bold (700)</p>
<p className="font-sans font-black">Black (900)</p>${ENABLE_ITALIC ? '\n<p className="font-sans font-bold italic">Bold italic (700)</p>' : ""}
\`\`\`
`;

export function InstallSection() {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    if (isCopied) return;
    try {
      await navigator.clipboard.writeText(INSTALL_MARKDOWN);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 3000);
    } catch (error) {
      console.error("Error copying content", error);
    }
  }, [isCopied]);

  const Icon = isCopied ? CheckIcon : CopyIcon;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <SectionHeading>Install</SectionHeading>
        <button
          type="button"
          className="inline-flex items-center gap-2 rounded-xl border border-border px-3 py-1.5 text-sm font-medium transition-colors hover:bg-secondary/25"
          onClick={handleCopy}
          aria-label={isCopied ? "Copied" : "Copy as markdown"}
        >
          <Icon className="size-[16px]" />
          <span>{isCopied ? "Copied" : "Copy as markdown"}</span>
        </button>
      </div>

      <InstallStep
        step={1}
        title="Download the font files"
      >
        <p className="text-sm leading-relaxed text-muted-foreground">
          Download{" "}
          <a
            className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
            download="glide-variable.woff2"
            href="/glide-variable.woff2"
          >
            glide-variable.woff2
          </a>
          {ENABLE_ITALIC && (
            <>
              {" "}and{" "}
              <a
                className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
                download="glide-variable-italic.woff2"
                href="/glide-variable-italic.woff2"
              >
                glide-variable-italic.woff2
              </a>
            </>
          )}{" "}
          and place them in your project&apos;s public/ directory.
        </p>
      </InstallStep>

      <InstallStep
        step={2}
        title="Configure the font in your root layout"
        description="In app/layout.tsx, import localFont and configure the Glide variable font:"
      >
        <CodeBlock filename="app/layout.tsx">{`import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },${ENABLE_ITALIC ? '\n    { path: "../public/glide-variable-italic.woff2", style: "italic" },' : ""}
  ],
  variable: "--font-glide",
  weight: "400 900",
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={glide.variable}>{children}</body>
    </html>
  );
}`}</CodeBlock>
      </InstallStep>

      <InstallStep
        step={3}
        title="Map the CSS variable in Tailwind"
        description="In your global CSS file, map --font-glide to Tailwind's --font-sans so font-sans uses Glide:"
      >
        <CodeBlock filename="app/globals.css">{`@theme inline {
  --font-sans: var(--font-glide);
}`}</CodeBlock>
      </InstallStep>

      <InstallStep
        step={4}
        title="Use it"
        description="Glide is now your default sans-serif font. Use font-sans with any weight from 400 to 900:"
      >
        <CodeBlock>{`<p className="font-sans font-normal">Regular (400)</p>
<p className="font-sans font-bold">Bold (700)</p>
<p className="font-sans font-black">Black (900)</p>${ENABLE_ITALIC ? '\n<p className="font-sans font-bold italic">Bold italic (700)</p>' : ""}`}</CodeBlock>
      </InstallStep>
    </div>
  );
}
