import Link from "next/link";

import { GlyphSet } from "@/components/glyph-set";
import { InstallSection } from "@/components/install-section";
import { Specimen } from "@/components/specimen";
import { Button } from "@/components/ui/button";
import { WeightShowcase } from "@/components/weight-showcase";
import { ZoneBreadcrumb } from "@/components/zone-breadcrumb";
import { asset, siteConfig } from "@/lib/config";

export default function Home() {
  return (
    <main id="main-content">
      {/*
        Root page only, and it must read identically to the BreadcrumbList in
        lib/schema.ts. See blode-co/apps/web/.claude/knowledge/zone-conventions.md.
      */}
      <div className="px-[var(--row-padding)] pt-6">
        <ZoneBreadcrumb product={siteConfig.name} />
      </div>

      {/* Hero */}
      <section className="flex flex-col items-start gap-8 px-[var(--row-padding)] py-[var(--row-padding-vertical)]">
        {/*
          Sized off the viewport the way Inter's title is (~14vw there), scaled
          up because "Glide" is five characters against their twenty-six and
          would otherwise sit marooned in the measure. The clamp floor keeps it
          a headline rather than a hazard on a phone, and the negative margin is
          side-bearing compensation so the G sits on the row's gutter.
        */}
        <h1 className="ml-[-0.015em] text-[clamp(5rem,24vw,26rem)] font-black leading-[0.85] tracking-[-0.04em] text-display">
          Glide
        </h1>
        {/* Inter sets its lede at ~29px/1.5 against a ~28em measure. */}
        <p className="max-w-[28em] text-[clamp(1.25rem,2.2vw,1.85rem)] text-pretty leading-[1.5]">
          Variable font family crafted for UI.
        </p>
        <p className="max-w-[48ch] text-pretty text-muted-foreground">
          Free under the SIL Open Font License. Variable 100–950, roman, italic,
          and mono.
        </p>
        <div className="flex flex-wrap items-center gap-3">
          <Button asChild>
            <Link href="#install">Download</Link>
          </Button>
        </div>
      </section>

      {/*
        Full-bleed on purpose: the specimen is the argument for the typeface, so
        it gets the whole measure rather than the reading column below.
      */}
      <Specimen />

      {/* Full-bleed for the same reason as the specimen: the type is the argument. */}
      <WeightShowcase />

      <GlyphSet />

      <InstallSection />

      <div className="border-border border-t px-[var(--row-padding)]">
        {/*
          Footer. blode.co and blode.co/projects are this same origin behind a
          rewrite, so both are internal links: same tab, and no
          rel="noopener noreferrer", which only means something cross-origin. The
          projects link is the edge back to the hub, without which this zone is a
          dead end for crawlers and readers. See
          blode-co/apps/web/.claude/knowledge/zone-conventions.md.
        */}
        <footer className="flex flex-col items-start gap-2 py-[var(--row-padding-vertical)] text-muted-foreground text-sm">
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
              {/*
                Sized in `em` so it tracks the footer's type instead of pinning
                to 20px while the fluid root scales everything around it. The
                width/height attributes stay to reserve layout before it loads.
              */}
              <img
                alt=""
                className="size-[1.6em] rounded-full"
                height={20}
                src={asset("/avatar-sm.png")}
                width={20}
              />
              Matthew Blode
            </a>
          </div>
          <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
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
          </div>
        </footer>
      </div>
    </main>
  );
}
