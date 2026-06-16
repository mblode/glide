"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { CodeBlock } from "@/components/code-block";
import { siteConfig } from "@/lib/config";

type OS = "macos" | "windows" | "linux";

const OS_LABELS: Record<OS, string> = {
  macos: "macOS",
  windows: "Windows",
  linux: "Linux",
};

const INSTALL_STEPS: Record<OS, React.ReactNode> = {
  macos: (
    <ol className="space-y-3 text-sm leading-relaxed text-muted-foreground">
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          1
        </span>
        Extract the Glide zip archive.
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          2
        </span>
        Open the{" "}
        <span className="font-medium text-foreground">Font Book</span>{" "}
        application.
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          3
        </span>
        In the main menu, select{" "}
        <span className="font-medium text-foreground">
          File → Add Fonts…
        </span>
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          4
        </span>
        Select{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          glide-variable.ttf
        </code>
        {" "}and{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          glide-variable-italic.ttf
        </code>
        {" "}and press{" "}
        <span className="font-medium text-foreground">Open</span>.
      </li>
      <li className="mt-2 text-xs text-muted-foreground/70">
        Alternatively, move or copy the font files directly into{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          ~/Library/Fonts/
        </code>
      </li>
    </ol>
  ),
  windows: (
    <ol className="space-y-3 text-sm leading-relaxed text-muted-foreground">
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          1
        </span>
        Extract the Glide zip archive.
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          2
        </span>
        Right-click{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          glide-variable.ttf
        </code>{" "}
        and select{" "}
        <span className="font-medium text-foreground">Install</span>{" "}
        (or{" "}
        <span className="font-medium text-foreground">
          Install for all users
        </span>
        ).
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          3
        </span>
        Repeat for{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          glide-variable-italic.ttf
        </code>
        .
      </li>
    </ol>
  ),
  linux: (
    <ol className="space-y-3 text-sm leading-relaxed text-muted-foreground">
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          1
        </span>
        Extract the Glide zip archive.
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          2
        </span>
        Copy the font files to{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          ~/.fonts/
        </code>{" "}
        or{" "}
        <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
          /usr/share/fonts/truetype/glide/
        </code>
        .
      </li>
      <li className="flex gap-3">
        <span className="flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-bold text-primary tabular-nums">
          3
        </span>
        Refresh the font cache:
      </li>
      <li className="pl-9">
        <CodeBlock>{`fc-cache -f -v`}</CodeBlock>
      </li>
    </ol>
  ),
};

export function DownloadPage() {
  const [os, setOs] = useState<OS>("macos");

  useEffect(() => {
    window.location.href = siteConfig.downloadUrl;
  }, []);

  return (
    <main id="main-content">
      <div className="mx-auto w-full max-w-2xl space-y-8 px-4 py-16 sm:px-6 sm:py-24">
        {/* Back link */}
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground focus-visible:rounded-lg focus-visible:ring-2 focus-visible:ring-ring"
        >
          ← Back to Glide
        </Link>

        {/* Hero */}
        <section className="space-y-4">
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Downloading Glide version {siteConfig.version}…
          </h1>
          <p className="break-all font-mono text-xs text-muted-foreground">
            {siteConfig.downloadUrl}
          </p>
          <div className="flex flex-wrap gap-3">
            <Button asChild>
              <a href={siteConfig.downloadUrl} download>
                Download again
              </a>
            </Button>
            <Button variant="outline" asChild>
              <a
                href={siteConfig.links.github}
                target="_blank"
                rel="noopener noreferrer"
              >
                Star on GitHub ★
              </a>
            </Button>
          </div>
          <p className="text-sm text-muted-foreground">
            Glide is open source. Star the repo on GitHub to support the
            project.
          </p>
        </section>

        <hr className="border-border" />

        {/* Installation instructions */}
        <section className="space-y-6">
          <div className="flex flex-wrap items-center gap-3">
            <h2 className="text-lg font-bold tracking-tight">
              Installation instructions
            </h2>
            <div className="flex items-center gap-1 rounded-xl border border-border bg-card/50 p-1">
              {(["macos", "windows", "linux"] as OS[]).map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => setOs(option)}
                  className={`rounded-lg px-3 py-1 text-sm font-medium transition-colors ${
                    os === option
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {OS_LABELS[option]}
                </button>
              ))}
            </div>
          </div>
          {INSTALL_STEPS[os]}
        </section>

        <hr className="border-border" />

        {/* Variable font files */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold tracking-tight">
            Variable font files
          </h2>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Glide ships as a variable font —{" "}
            <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
              glide-variable.ttf
            </code>
            {" "}(roman) and{" "}
            <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
              glide-variable-italic.ttf
            </code>
            {" "}(italic)
            . Variable fonts let you dial any weight from 100 (Thin)
            to 900 (Black) on a continuous axis, using a single file instead of
            separate files per weight. A static{" "}
            <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
              glide-mono.ttf
            </code>{" "}
            monospace is included too.
          </p>
          <p className="text-sm leading-relaxed text-muted-foreground">
            Variable font support is excellent in all modern desktop
            applications and browsers.
          </p>
        </section>

        <hr className="border-border" />

        {/* Web use */}
        <section className="space-y-4">
          <h2 className="text-lg font-bold tracking-tight">Web use</h2>
          <p className="text-sm leading-relaxed text-muted-foreground">
            For web projects, use the WOFF2 variable font files. Download{" "}
            <a
              className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
              href="/glide-variable.woff2"
              download="glide-variable.woff2"
            >
              glide-variable.woff2
            </a>
            {" "}and{" "}
            <a
              className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
              href="/glide-variable-italic.woff2"
              download="glide-variable-italic.woff2"
            >
              glide-variable-italic.woff2
            </a>
            {" "}and place them in your project&apos;s{" "}
            <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
              public/
            </code>{" "}
            directory, then add:
          </p>
          <CodeBlock filename="app/globals.css">{`@font-face {
  font-family: 'GlideVariable';
  src: url('/glide-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'GlideVariable';
  src: url('/glide-variable-italic.woff2') format('woff2');
  font-weight: 100 900;
  font-style: italic;
  font-display: swap;
}
:root {
  font-family: GlideVariable, sans-serif;
}`}</CodeBlock>
          <p className="text-sm text-muted-foreground">
            Using Next.js?{" "}
            <Link
              href="/#install"
              className="font-medium text-foreground underline underline-offset-4 transition-colors hover:text-primary"
            >
              See the Next.js installation guide
            </Link>{" "}
            for setup with{" "}
            <code className="rounded bg-primary/10 px-1.5 py-0.5 font-mono text-xs text-primary">
              next/font/local
            </code>{" "}
            and Tailwind.
          </p>
        </section>
      </div>
    </main>
  );
}
