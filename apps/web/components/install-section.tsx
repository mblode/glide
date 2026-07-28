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

function SectionHeading({ children }: { children: React.ReactNode }) {
  return <h2 className="text-lg font-bold tracking-tight">{children}</h2>;
}

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
        "inline-flex shrink-0 items-center gap-2 rounded-xl border border-border px-3 py-1.5 text-sm font-medium transition-colors hover:bg-secondary/25",
        className
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
    <div className="space-y-8">
      <div className="flex items-center justify-between gap-3">
        <SectionHeading>Install</SectionHeading>
        <CopyTextButton
          content={installPrompt}
          label="Copy prompt"
          title="Copy install instructions for a coding agent"
        />
      </div>

      <p className="text-sm leading-relaxed text-pretty text-muted-foreground">
        For Figma and Font Book,{" "}
        <a
          className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
          download="glide.zip"
          href={asset("/glide.zip")}
        >
          download Glide for desktop
        </a>{" "}
        (TTF).
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
  );
}
