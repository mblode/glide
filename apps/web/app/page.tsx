import Link from "next/link";

import { InstallSection } from "@/components/install-section";
import { Playground } from "@/components/playground";
import { Button } from "@/components/ui/button";
import { WeightShowcase } from "@/components/weight-showcase";
import { ZoneBreadcrumb } from "@/components/zone-breadcrumb";
import { asset, siteConfig } from "@/lib/config";
import { cn } from "@/lib/utils";

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
        bordered && "rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8",
      )}
    >
      {children}
    </section>
  );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return <h2 className="text-lg font-bold tracking-tight">{children}</h2>;
}

export default function Home() {
  return (
    <main id="main-content">
      {/*
        Root page only, and it must read identically to the BreadcrumbList in
        lib/schema.ts. See blode-co/apps/web/.claude/knowledge/zone-conventions.md.
      */}
      <div className="mx-auto w-full max-w-5xl px-4 pt-6 sm:px-6">
        <ZoneBreadcrumb product={siteConfig.name} />
      </div>

      {/* Hero */}
      <section className="flex flex-col items-center gap-6 px-4 py-24 text-center sm:px-6 sm:py-40">
        <h1 className="text-8xl font-black leading-[0.85] tracking-[-0.06em] text-display sm:text-9xl lg:text-[11rem]">
          Glide
        </h1>
        <p className="max-w-[40ch] text-xl text-pretty text-muted-foreground sm:text-2xl">
          Variable font family crafted for UI.
        </p>
        <p className="max-w-[48ch] text-pretty text-sm text-muted-foreground">
          Free under the SIL Open Font License. Variable 100–950, roman, italic,
          and mono.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button asChild>
            <Link href="#install">Download</Link>
          </Button>
          <Button variant="outline" asChild>
            <a href="#playground">Try it</a>
          </Button>
        </div>
      </section>

      <div className="mx-auto w-full max-w-5xl space-y-8 px-4 pb-8 sm:px-6">
        {/* Playground */}
        <Section id="playground">
          <div className="space-y-6">
            <SectionHeading>Playground</SectionHeading>
            <Playground />
          </div>
        </Section>

        {/* Weights */}
        <Section id="weights" bordered={false}>
          <div className="space-y-6">
            <WeightShowcase />
            <p className="text-pretty text-sm text-muted-foreground">
              Only three of these are drawn: Thin, Regular, and Extra Black. The rest
              are interpolated.{" "}
              <Link className="underline underline-offset-4 hover:text-foreground" href="/glyphs">
                Browse every glyph
              </Link>
              .
            </p>
          </div>
        </Section>

        {/* Install */}
        <Section id="install">
          <InstallSection />
        </Section>

        {/*
          Footer. blode.co and blode.co/projects are this same origin behind a
          rewrite, so both are internal links: same tab, and no
          rel="noopener noreferrer", which only means something cross-origin. The
          projects link is the edge back to the hub, without which this zone is a
          dead end for crawlers and readers. See
          blode-co/apps/web/.claude/knowledge/zone-conventions.md.
        */}
        <footer className="flex flex-col items-center justify-center gap-2 pt-16 pb-8 text-muted-foreground text-sm">
          <div className="flex items-center gap-1">
            Crafted by
            <a
              className="flex items-center gap-2 rounded-full py-1.5 pr-2.5 pl-1.5 transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-full"
              href={siteConfig.links.author}
              rel="author"
            >
              {/*
                Decorative: the link is already labelled "Matthew Blode" by its
                own text, so any alt here makes the accessible name announce the
                name twice.
              */}
              <img
                alt=""
                className="rounded-full"
                height={20}
                src={asset("/avatar-sm.png")}
                width={20}
              />
              Matthew Blode
            </a>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-x-2 gap-y-1">
            <span>v{siteConfig.version}</span>
            <span aria-hidden="true">·</span>
            <a
              className="hover:text-foreground focus-visible:rounded-lg focus-visible:ring-2 focus-visible:ring-ring"
              href={siteConfig.links.github}
              rel="noopener noreferrer"
              target="_blank"
            >
              GitHub
            </a>
            <span aria-hidden="true">·</span>
            <a
              className="hover:text-foreground focus-visible:rounded-lg focus-visible:ring-2 focus-visible:ring-ring"
              href={siteConfig.links.license}
              rel="noopener noreferrer"
              target="_blank"
            >
              OFL 1.1
            </a>
            <span aria-hidden="true">·</span>
            <Link
              className="hover:text-foreground focus-visible:rounded-lg focus-visible:ring-2 focus-visible:ring-ring"
              href="/glyphs"
            >
              Glyphs
            </Link>
          </div>
        </footer>
      </div>
    </main>
  );
}
