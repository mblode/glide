"use client";

import {
  Checkmark1Icon as CheckIcon,
  CopySimpleIcon as CopyIcon,
} from "blode-icons-react";
import { useCallback, useState } from "react";

import { CodeBlock } from "@/components/code-block";
import { asset, siteConfig } from "@/lib/config";
import { installPrompt } from "@/lib/install-prompt";
import {
  layoutSnippet,
  themeSnippet,
  usageSnippet,
} from "@/lib/install-snippets";
import { cn } from "@/lib/utils";

/**
 * A copy button with a visible label. The shared CopyButton in components/ui is
 * icon-only by contract, so it can't carry one.
 */
function CopyTextButton({
  content,
  label,
  className,
  title,
}: {
  content: string;
  label: string;
  className?: string;
  title?: string;
}) {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    if (isCopied) {
      return;
    }
    try {
      await navigator.clipboard.writeText(content);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 3000);
    } catch (error) {
      console.error("Error copying content", error);
    }
  }, [content, isCopied]);

  const Icon = isCopied ? CheckIcon : CopyIcon;

  return (
    <button
      type="button"
      className={cn(
        // `max-sm:h-11` matches the specimen and weight toggles: 1.5 lines of
        // padding is a 34px target, under the 44px a thumb needs.
        "inline-flex shrink-0 items-center gap-2 rounded-xl border border-border px-3 py-1.5 text-sm font-medium transition-colors hover:bg-secondary/25 max-sm:h-11",
        className,
      )}
      onClick={handleCopy}
      aria-label={isCopied ? "Copied" : label}
      title={title}
    >
      <Icon className="size-4" />
      <span>{label}</span>
    </button>
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

export function InstallSection() {
  return (
    <section aria-labelledby="install-heading" id="install">
      {/*
        Inter's usage block is an 8-column grid with the label in 1-2 and the
        content in 3-8. A proportional split beats the fixed label column the
        other rows use here, because at full width a 10rem label next to a
        2000px content area stops reading as a pair.
      */}
      <div className="grid gap-x-10 gap-y-6 border-border border-t px-[var(--row-padding)] py-[var(--row-padding-vertical)] lg:grid-cols-4">
        {/*
          `min-w-0` on both columns, not decoration. A grid item defaults to
          `min-width: auto`, which is its min-content width, and the code blocks
          below are `pre` with `white-space: pre`, so their min-content width is
          the longest line — around 610px. Without this the track was sized to
          that line at every viewport, the row ran wider than a phone, and the
          whole page scrolled sideways with the prose clipped at the right edge.
        */}
        <div className="flex min-w-0 flex-col items-start gap-3">
          <h2
            className="font-semibold text-lg tracking-tight"
            id="install-heading"
          >
            Install
          </h2>
          <CopyTextButton
            content={installPrompt}
            label="Copy prompt"
            title="Copy install instructions for a coding agent"
          />
        </div>

        <div className="min-w-0 space-y-8 lg:col-span-3">
          <p className="text-pretty text-sm text-muted-foreground">
            Glide is free under the{" "}
            <a
              className="font-medium text-foreground underline underline-offset-4 hover:text-primary"
              href={siteConfig.links.license}
              rel="noopener noreferrer"
              target="_blank"
            >
              SIL Open Font License 1.1
            </a>
            . For Figma and Font Book,{" "}
            <a
              className="font-medium text-foreground underline underline-offset-4 hover:text-primary"
              download="glide.zip"
              href={asset("/glide.zip")}
            >
              download Glide for desktop
            </a>{" "}
            (TTF). On macOS open Font Book and choose File → Add Fonts. On
            Windows, select the files, right-click, and install for all users.
          </p>

          <InstallStep step={1} title="Download the font files">
            <p className="text-sm leading-relaxed text-muted-foreground">
              Download{" "}
              <a
                className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
                download="glide-variable.woff2"
                href={asset("/glide-variable.woff2")}
              >
                glide-variable.woff2
              </a>{" "}
              and{" "}
              <a
                className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
                download="glide-variable-italic.woff2"
                href={asset("/glide-variable-italic.woff2")}
              >
                glide-variable-italic.woff2
              </a>{" "}
              and{" "}
              <a
                className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
                download="glide-mono.woff2"
                href={asset("/glide-mono.woff2")}
              >
                glide-mono.woff2
              </a>{" "}
              and put them in app/fonts/ next to your root layout.
            </p>
          </InstallStep>

          <InstallStep
            step={2}
            title="Configure the fonts in your root layout"
            description="In app/layout.tsx, import localFont and configure the Glide variable and Glide Mono fonts:"
          >
            <CodeBlock filename="app/layout.tsx">{layoutSnippet}</CodeBlock>
          </InstallStep>

          <InstallStep
            step={3}
            title="Map the CSS variables in Tailwind"
            description="In your global CSS file, map --font-glide to Tailwind's --font-sans and --font-glide-mono to --font-mono:"
          >
            <CodeBlock filename="app/globals.css">{themeSnippet}</CodeBlock>
          </InstallStep>

          <InstallStep
            step={4}
            title="Use it"
            description="Glide is now your default sans-serif font, and Glide Mono is your monospace font. Use font-sans with any weight from 100 to 950, and font-mono for code:"
          >
            <CodeBlock>{usageSnippet}</CodeBlock>
          </InstallStep>
        </div>
      </div>
    </section>
  );
}
