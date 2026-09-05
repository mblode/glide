import { GlyphSet } from "@/components/glyph-set";
import { InstallSection } from "@/components/install-section";
import { Specimen } from "@/components/specimen";
import { TrackedLink } from "@/components/tracked-link";
import { buttonVariants } from "@/components/ui/button";
import { WeightShowcase } from "@/components/weight-showcase";
import { ZoneBreadcrumb } from "@/components/zone-breadcrumb";
import { asset, siteConfig } from "@/lib/config";
import { cn } from "@/lib/utils";

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
        {/*
          Editable, because people already try. Four sessions in the last 90
          days registered a dead click on this wordmark, which is what a click
          on inert text looks like: they had read "interactive editable text"
          and reached for the biggest word on the page rather than the specimen
          headline further down.

          It stays an `h1` and keeps its heading role: no `role="textbox"`
          here, unlike the specimen's `h3`. `contentEditable` is exposed as an
          editable state on top of the heading, so a screen reader still gets
          the page's main heading, and the server-rendered text is still
          "Glide" for anything that does not run scripts.

          `dangerouslySetInnerHTML` for the same reason the specimen uses it:
          React refuses to manage children under `contentEditable`, and the
          string is a constant, so nothing you type can be overwritten by a
          re-render.

          `max-w-full` with `break-words` because the row is a column flex with
          `items-start`, which sizes this to its own content: without the cap a
          typed word longer than "Glide" runs past the gutter and takes the
          whole page into a sideways scroll at 24vw a character.
        */}
        {/*
          No `aria-label`: it would replace the heading's accessible name with
          a description, and the name of this page's h1 should be "Glide".
          `contentEditable` already reports itself as editable on its own.
        */}
        <h1
          className="ml-[-0.015em] max-w-full break-words text-[clamp(5rem,24vw,26rem)] font-black leading-[0.85] tracking-[-0.04em] outline-none text-display"
          contentEditable
          dangerouslySetInnerHTML={{ __html: "Glide" }}
          spellCheck={false}
          suppressContentEditableWarning
        />
        {/* Inter sets its lede at ~29px/1.5 against a ~28em measure. */}
        <p className="max-w-[28em] text-[clamp(1.25rem,2.2vw,1.85rem)] text-pretty leading-[1.5]">
          Variable font family crafted for UI.
        </p>
        <p className="max-w-[48ch] text-pretty text-muted-foreground">
          Free under the SIL Open Font License. Variable 100–950, roman, italic,
          and mono.
        </p>
        {/*
          Two actions, because the page serves two arrivals. Of the 90 days of
          sessions that took a font, 30 took the desktop zip and 10 took a
          WOFF2, so the desktop bundle leads and the web install sits beside it.

          The primary is the file itself, not the jump to the install steps the
          old single button made. That jump converted well once clicked (27 of
          33 sessions went on to take a file), but it charged every designer a
          second click for a bundle they could have had on the first.
        */}
        <div className="flex flex-col items-start gap-3">
          <div className="flex flex-wrap items-center gap-3">
            <TrackedLink
              className={cn(buttonVariants({ size: "lg" }))}
              download="glide.zip"
              href={asset("/glide.zip")}
              label="download-desktop"
              location="hero"
            >
              Download Glide
            </TrackedLink>
            <TrackedLink
              className={cn(buttonVariants({ size: "lg", variant: "outline" }))}
              href="#install"
              label="install-web"
              location="hero"
            >
              Install for web
            </TrackedLink>
          </div>
          <p className="text-muted-foreground text-sm">
            The bundle is TTF, for Figma and Font Book. The web install uses
            WOFF2 and next/font.
          </p>
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
