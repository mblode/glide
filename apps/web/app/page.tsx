import { DownloadIcon, PencilIcon } from "blode-icons-react";
import { Button } from "@/components/ui/button";
import { Playground } from "@/components/playground";
import { CodeBlock } from "@/components/code-block";

const weights = [
  { weight: 400, name: "Regular" },
  { weight: 500, name: "Medium" },
  { weight: 600, name: "Semibold" },
  { weight: 700, name: "Bold" },
  { weight: 800, name: "Extrabold" },
  { weight: 900, name: "Black" },
] as const;

const instances = [
  { weight: 400, name: "Regular" },
  { weight: 500, name: "Medium" },
  { weight: 700, name: "Bold" },
  { weight: 900, name: "Black" },
] as const;

function Section({
  label,
  title,
  id,
  children,
}: {
  label: string;
  title: string;
  id?: string;
  children: React.ReactNode;
}) {
  return (
    <section
      id={id}
      className="scroll-mt-6 rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8"
    >
      <div className="mb-6">
        <p className="text-xs font-medium tracking-widest text-muted-foreground uppercase">
          {label}
        </p>
        <h2 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">
          {title}
        </h2>
      </div>
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
      <div className="text-sm text-muted-foreground">
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
        <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-mint-soft font-bold text-mint tabular-nums text-sm">
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
          <span className="inline-flex items-center gap-2 rounded-full bg-mint-soft px-3 py-1.5 text-xs font-medium tracking-widest text-mint uppercase">
            Variable Font
          </span>
          <h1 className="text-7xl font-black leading-[0.9] tracking-[-0.06em] sm:text-8xl lg:text-9xl">
            Glide
          </h1>
          <p className="max-w-lg text-lg leading-relaxed text-muted-foreground">
            A variable sans-serif typeface supporting weights from 400 to 900 in
            both roman and italic styles. Two files, every weight.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Button render={<a href="#install" />}>
              <DownloadIcon data-icon="inline-start" />
              Install
            </Button>
            <Button variant="outline" render={<a href="#playground" />}>
              <PencilIcon data-icon="inline-start" />
              Try it
            </Button>
          </div>
        </section>

        {/* Playground */}
        <Section label="Playground" title="Type something" id="playground">
          <Playground />
        </Section>

        {/* Roman weights */}
        <Section label="Weights" title="400 to 900">
          <div>
            {weights.map((w) => (
              <WeightRow key={w.weight} weight={w.weight} name={w.name} />
            ))}
          </div>
        </Section>

        {/* Italic weights */}
        <Section label="Italic" title="400 to 900">
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

        {/* Named instances */}
        <Section label="Named Instances" title="Four checkpoints">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {instances.map((inst) => (
              <div
                key={inst.weight}
                className="rounded-xl border border-border bg-background p-5"
              >
                <div className="flex items-center justify-between text-xs font-medium tracking-widest text-muted-foreground uppercase">
                  <span>{inst.weight}</span>
                  <span>{inst.name}</span>
                </div>
                <p
                  className="mt-4 text-5xl leading-[0.92] tracking-[-0.07em]"
                  style={{ fontWeight: inst.weight }}
                >
                  Glide
                </p>
                <p
                  className="mt-3 text-base leading-snug tracking-tight text-muted-foreground"
                  style={{ fontWeight: inst.weight }}
                >
                  The quick brown fox jumps over the lazy dog.
                </p>
                <p
                  className="mt-2 text-base italic leading-snug tracking-tight text-muted-foreground"
                  style={{ fontWeight: inst.weight }}
                >
                  The quick brown fox jumps over the lazy dog.
                </p>
              </div>
            ))}
          </div>
        </Section>

        {/* Heading scale */}
        <Section label="Typography" title="Heading scale">
          <div className="space-y-4" role="presentation">
            <h3 className="text-5xl font-black leading-[1.1] tracking-tight sm:text-6xl">
              Heading 1
            </h3>
            <h4 className="text-4xl font-extrabold leading-[1.1] tracking-tight sm:text-5xl">
              Heading 2
            </h4>
            <h5 className="text-3xl font-bold leading-[1.1] tracking-tight">
              Heading 3
            </h5>
            <h6 className="text-2xl font-bold leading-[1.1] tracking-tight">
              Heading 4
            </h6>
            <p className="text-xl font-semibold leading-[1.1] tracking-tight">
              Heading 5
            </p>
            <p className="text-base font-semibold uppercase tracking-widest">
              Heading 6
            </p>
          </div>
        </Section>

        {/* Paragraph text */}
        <Section label="Body text" title="Paragraph specimens">
          <div className="space-y-5">
            <p className="max-w-2xl text-lg leading-relaxed text-muted-foreground">
              This is a standard paragraph with the Glide font. The font
              provides excellent readability at various sizes while maintaining a
              modern, clean aesthetic. The variable font technology ensures that
              characters remain crisp and balanced across different weights and
              sizes.
            </p>
            <p className="max-w-2xl text-base leading-relaxed text-muted-foreground">
              Glide is shipped as two variable font files: regular and italic.
              Each contains all weights in a single file, allowing for precise
              typography with minimal file size impact. This technology enables
              smooth transitions between font weights and provides greater
              design flexibility compared to traditional static font families.
            </p>
            <p className="max-w-2xl text-sm leading-relaxed text-muted-foreground/70">
              This is a smaller paragraph showing how Glide performs at reduced
              sizes. Even at smaller sizes, the font maintains its legibility
              and character, making it suitable for captions, footnotes, and
              secondary content.
            </p>
          </div>
        </Section>

        {/* Waterfall */}
        <Section label="Waterfall" title="Text to display range">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-xl border border-border bg-background p-5">
              <h3 className="mb-4 text-lg font-semibold tracking-tight">
                Roman
              </h3>
              {[64, 48, 32, 20, 14].map((size) => (
                <p
                  key={size}
                  className="border-t border-border py-3 first:border-t-0 first:pt-0"
                  style={{
                    fontSize: `${size}px`,
                    fontWeight: size >= 48 ? 700 : size >= 32 ? 500 : 400,
                    lineHeight: 1.1,
                    letterSpacing: "-0.04em",
                  }}
                >
                  {size >= 48
                    ? "Sphinx of black quartz"
                    : "Sphinx of black quartz, judge my vow."}
                </p>
              ))}
            </div>
            <div className="rounded-xl border border-border bg-background p-5">
              <h3 className="mb-4 text-lg font-semibold tracking-tight">
                Italic
              </h3>
              {[64, 48, 32, 20, 14].map((size) => (
                <p
                  key={size}
                  className="border-t border-border py-3 italic first:border-t-0 first:pt-0"
                  style={{
                    fontSize: `${size}px`,
                    fontWeight: size >= 48 ? 700 : size >= 32 ? 500 : 400,
                    lineHeight: 1.1,
                    letterSpacing: "-0.04em",
                  }}
                >
                  {size >= 48
                    ? "Sphinx of black quartz"
                    : "Sphinx of black quartz, judge my vow."}
                </p>
              ))}
            </div>
          </div>
        </Section>

        {/* Glyph coverage */}
        <Section label="Glyph coverage" title="ASCII set">
          <div className="space-y-5">
            <div>
              <p className="mb-2 text-xs font-medium tracking-widest text-muted-foreground uppercase">
                Roman
              </p>
              <p className="break-all text-lg leading-loose tracking-wide text-muted-foreground">
                {`!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\`abcdefghijklmnopqrstuvwxyz{|}~`}
              </p>
            </div>
            <div>
              <p className="mb-2 text-xs font-medium tracking-widest text-muted-foreground uppercase">
                Italic
              </p>
              <p className="break-all text-lg italic leading-loose tracking-wide text-muted-foreground">
                {`!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\`abcdefghijklmnopqrstuvwxyz{|}~`}
              </p>
            </div>
          </div>
        </Section>

        {/* Install */}
        <Section label="Getting started" title="Install Glide" id="install">
          <div className="space-y-8">
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
              <CodeBlock>{`{/* Roman */}
<p className="font-sans font-normal">Regular (400)</p>
<p className="font-sans font-medium">Medium (500)</p>
<p className="font-sans font-semibold">Semibold (600)</p>
<p className="font-sans font-bold">Bold (700)</p>
<p className="font-sans font-extrabold">Extrabold (800)</p>
<p className="font-sans font-black">Black (900)</p>

{/* Italic */}
<p className="font-sans italic">Regular italic (400)</p>
<p className="font-sans font-bold italic">Bold italic (700)</p>`}</CodeBlock>
            </InstallStep>

            <InstallStep
              step={5}
              title="Plain CSS alternative"
              description="Not using Next.js? Link the bundled stylesheet or add the @font-face declarations directly:"
            >
              <CodeBlock>{`<link rel="stylesheet" href="fonts/glide.css" />

<style>
  body {
    font-family: "Glide", system-ui, sans-serif;
  }
</style>`}</CodeBlock>
            </InstallStep>
          </div>
        </Section>

        {/* Technical details */}
        <Section label="Technical" title="Details">
          <div>
            {[
              ["Family", "Glide"],
              ["Designer", "Matthew Blode"],
              ["Styles", "Roman + Italic"],
              ["Weight range", "400 \u2013 900 (variable wght axis)"],
              [
                "Formats",
                "Variable TTF, WOFF2, WOFF \u2014 Static TTF, OTF, WOFF2, WOFF",
              ],
              [
                "Named instances",
                "Regular (400), Medium (500), Bold (700), Black (900)",
              ],
            ].map(([label, value]) => (
              <div
                key={label}
                className="grid items-baseline gap-2 border-t border-border py-4 first:border-t-0 first:pt-0 sm:grid-cols-[140px_1fr] sm:gap-4"
              >
                <span className="text-sm font-semibold">{label}</span>
                <span className="text-muted-foreground">{value}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* Footer */}
        <footer className="py-12 text-center text-sm text-muted-foreground">
          <p>
            <strong className="font-semibold text-foreground">Glide</strong> by
            Matthew Blode
          </p>
        </footer>
      </main>
    </div>
  );
}
