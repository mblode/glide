import Image from "next/image";
import { DownloadIcon, PencilIcon } from "blode-icons-react";
import { Button } from "@/components/ui/button";
import { Playground } from "@/components/playground";
import { WeightShowcase } from "@/components/weight-showcase";
import { CodeBlock } from "@/components/code-block";
import { cn } from "@/lib/utils";
import { siteConfig } from "@/lib/config";

function Section({
  id,
  children,
  bordered = true,
}: {
  id?: string;
  children: React.ReactNode;
  bordered?: boolean;
}) {
  return (
    <section
      id={id}
      className={cn(
        "scroll-mt-6",
        bordered &&
          "rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8"
      )}
    >
      {children}
    </section>
  );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-xs font-bold uppercase tracking-widest text-muted-foreground">
      {children}
    </h2>
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
        <p className="pl-11 text-sm leading-relaxed text-muted-foreground">
          {description}
        </p>
      )}
      {children && <div className="pl-11">{children}</div>}
    </div>
  );
}

export default function Home() {
  return (
    <main id="main-content">
      {/* Hero */}
      <section className="flex flex-col items-center gap-6 px-4 py-24 text-center sm:px-6 sm:py-40">
        <h1 className="animate-fade-up text-8xl font-black leading-[0.85] tracking-[-0.06em] text-display sm:text-9xl lg:text-[11rem]">
          Glide
        </h1>
        <p className="animate-fade-up-delay-1 max-w-md text-xl leading-relaxed text-muted-foreground sm:text-2xl">
          Variable font family crafted for UI.
        </p>
        <div className="animate-fade-up-delay-2 flex flex-wrap items-center justify-center gap-3">
          <Button asChild>
            <a href="#install">
              <DownloadIcon data-icon="inline-start" />
              Install
            </a>
          </Button>
          <Button variant="outline" asChild>
            <a href="#playground">
              <PencilIcon data-icon="inline-start" />
              Try it
            </a>
          </Button>
        </div>
      </section>

      <div className="mx-auto w-full max-w-5xl space-y-5 px-4 pb-8 sm:px-6">
        {/* Playground */}
        <Section id="playground">
          <div className="space-y-6">
            <SectionHeading>Playground</SectionHeading>
            <Playground />
          </div>
        </Section>

        {/* Weights */}
        <Section bordered={false}>
          <WeightShowcase />
        </Section>

        {/* Install */}
        <Section id="install">
          <div className="space-y-8">
            <SectionHeading>Install</SectionHeading>
            <InstallStep
              step={1}
              title="Download the font files"
              description="Download glide-variable.woff2 and glide-variable-italic.woff2 and place them in your project's public/ directory."
            />

            <InstallStep
              step={2}
              title="Configure the font in your root layout"
              description="In app/layout.tsx, import localFont and configure the Glide variable font:"
            >
              <CodeBlock filename="app/layout.tsx">{`import localFont from "next/font/local";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },
    { path: "../public/glide-variable-italic.woff2", style: "italic" },
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
<p className="font-sans font-black">Black (900)</p>
<p className="font-sans font-bold italic">Bold italic (700)</p>`}</CodeBlock>
            </InstallStep>
          </div>
        </Section>

        {/* Footer */}
        <footer className="flex flex-col items-center justify-center gap-2 pt-16 pb-8 text-muted-foreground text-sm">
          <div className="flex items-center gap-1">
            Crafted by
            <a
              className="flex items-center gap-2 rounded-full py-1.5 pr-2.5 pl-1.5 transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-full"
              href={siteConfig.links.author}
              rel="noopener noreferrer"
              target="_blank"
            >
              <Image
                alt="Avatar of Matthew Blode"
                className="rounded-full"
                height={20}
                src="/matthew-blode-profile.jpg"
                width={20}
              />
              Matthew Blode
            </a>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground/30">
            <span className="text-muted-foreground">
              v{siteConfig.version}
            </span>{" "}
            &bull;
            <a
              className="text-muted-foreground transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-lg"
              href={siteConfig.links.github}
              rel="noopener noreferrer"
              target="_blank"
            >
              GitHub
            </a>
          </div>
        </footer>
      </div>
    </main>
  );
}
