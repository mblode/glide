import Image from "next/image";
import { DownloadIcon, PencilIcon } from "blode-icons-react";
import { Button } from "@/components/ui/button";
import { Playground } from "@/components/playground";
import { CodeBlock } from "@/components/code-block";
import { siteConfig } from "@/lib/config";

const weights = [
  { weight: 400, name: "Regular" },
  { weight: 500, name: "Medium" },
  { weight: 600, name: "Semibold" },
  { weight: 700, name: "Bold" },
  { weight: 800, name: "Extrabold" },
  { weight: 900, name: "Black" },
] as const;

function Section({
  id,
  children,
}: {
  id?: string;
  children: React.ReactNode;
}) {
  return (
    <section
      id={id}
      className="scroll-mt-6 rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8"
    >
      {children}
    </section>
  );
}

function WeightRow({
  weight,
  name,
  italic = false,
}: {
  weight: number;
  name: string;
  italic?: boolean;
}) {
  return (
    <div className="grid items-baseline gap-2 border-t border-border py-4 first:border-t-0 first:pt-0 sm:grid-cols-[140px_1fr] sm:gap-4">
      <div className="text-sm text-muted-foreground tabular-nums">
        <span className="block font-semibold text-foreground">{name}</span>
        {weight}
      </div>
      <p
        className="text-2xl leading-snug tracking-tight sm:text-3xl"
        style={{ fontWeight: weight, fontStyle: italic ? "italic" : "normal" }}
      >
        The quick brown fox jumps over the lazy dog.
      </p>
    </div>
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
    <div className="mx-auto w-full max-w-5xl px-4 py-8 sm:px-6 sm:py-12">
      <main id="main-content" className="space-y-5">
        {/* Hero */}
        <section className="flex flex-col items-center gap-6 rounded-2xl border border-border bg-card/50 px-6 py-16 text-center backdrop-blur-sm sm:py-24">
          <h1 className="text-7xl font-black leading-[0.9] tracking-[-0.06em] sm:text-8xl lg:text-9xl">
            Glide
          </h1>
          <p className="max-w-lg text-lg leading-relaxed text-muted-foreground">
            A variable sans-serif typeface supporting weights from 400 to 900 in
            both roman and italic styles.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
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

        {/* Playground */}
        <Section id="playground">
          <Playground />
        </Section>

        {/* Roman weights */}
        <Section>
          <div>
            {weights.map((w) => (
              <WeightRow key={w.weight} weight={w.weight} name={w.name} />
            ))}
          </div>
        </Section>

        {/* Italic weights */}
        <Section>
          <div>
            {weights.map((w) => (
              <WeightRow
                key={w.weight}
                weight={w.weight}
                name={`${w.name} Italic`}
                italic
              />
            ))}
          </div>
        </Section>

        {/* Install */}
        <Section id="install">
          <div className="space-y-8">
            <InstallStep
              step={1}
              title="Download the font files"
              description="Download the font files and place them in your project's public/ directory."
            >
              <div className="flex flex-wrap gap-3">
                <Button variant="outline" size="sm" asChild>
                  <a
                    href="https://ui.blode.co/glide-variable.woff2"
                    download="glide-variable.woff2"
                  >
                    <DownloadIcon data-icon="inline-start" />
                    glide-variable.woff2
                  </a>
                </Button>
                <Button variant="outline" size="sm" asChild>
                  <a
                    href="https://ui.blode.co/glide-variable-italic.woff2"
                    download="glide-variable-italic.woff2"
                  >
                    <DownloadIcon data-icon="inline-start" />
                    glide-variable-italic.woff2
                  </a>
                </Button>
              </div>
            </InstallStep>

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
              className="flex items-center gap-2 rounded-full py-1.5 pr-2.5 pl-1.5 transition-colors hover:text-foreground"
              href={siteConfig.links.author}
              rel="noopener noreferrer"
              target="_blank"
            >
              <Image
                alt="Avatar of Matthew Blode"
                className="rounded-full"
                height={20}
                src="/matthew-blode-profile.jpg"
                unoptimized
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
              className="text-muted-foreground transition-colors hover:text-foreground"
              href={siteConfig.links.github}
              rel="noopener noreferrer"
              target="_blank"
            >
              GitHub
            </a>
          </div>
        </footer>
      </main>
    </div>
  );
}
