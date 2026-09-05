"use client";

import { useEffect, useState } from "react";

import { TrackedLink } from "@/components/tracked-link";
import { buttonVariants } from "@/components/ui/button";
import { asset, siteConfig } from "@/lib/config";
import { cn } from "@/lib/utils";

/*
  Page order, which is also the order the analytics put these sections in.
  Over 90 days of /glide sessions: 102 touched the specimen controls, 29 the
  glyph tiles, and 33 the hero download. The specimen is what people come to
  play with, so it leads; Install is last because it is the end of the page and
  the persistent Download button next to these links is the shortcut for anyone
  who does not want to read the steps.
*/
const sections = [
  { id: "playground", label: "Specimen" },
  { id: "weights", label: "Weights" },
  { id: "characters", label: "Characters" },
  { id: "install", label: "Install" },
] as const;

const BAR_HEIGHT = 56;

/**
 * Sticky section bar for the one-page specimen.
 *
 * It exists for the scroll data: half of /glide readers never reach the
 * install section (median depth 69%, and 81 of 277 page leaves happened before
 * 25%), so the download had to stop living only at the bottom of the page.
 */
export const SiteNav = () => {
  const [active, setActive] = useState("");

  useEffect(() => {
    const targets = sections
      .map((section) => document.getElementById(section.id))
      .filter((element) => element !== null);

    if (targets.length === 0) {
      return;
    }

    /*
      The band is the strip just below the bar. Whatever section crosses it is
      the one being read, which is what the highlight should follow: keying off
      "most visible" instead makes the label jump back to a tall section that
      still fills the viewport behind a short one.
    */
    const observer = new IntersectionObserver(
      (entries) => {
        const crossing = entries
          .filter((entry) => entry.isIntersecting)
          .sort(
            (a, b) => a.boundingClientRect.top - b.boundingClientRect.top
          );
        if (crossing.length > 0) {
          setActive(crossing[0].target.id);
        }
      },
      { rootMargin: `-${BAR_HEIGHT}px 0px -70% 0px` }
    );

    for (const target of targets) {
      observer.observe(target);
    }

    return () => observer.disconnect();
  }, []);

  /*
    The bar is opaque rather than a translucent blur. The rows it passes over
    are viewport-sized type in a flat palette, and a letter showing through the
    bar reads as a rendering fault rather than as depth.
  */
  return (
    <header className="sticky top-0 z-50 border-border border-b bg-background">
      <div className="flex h-14 items-center gap-2 px-[var(--row-padding)]">
        {/*
          `#top` is the document top in every browser without an element to
          match, so the wordmark needs no anchor of its own. It is not an `h1`:
          the hero keeps that.
        */}
        <a
          aria-label="Back to top"
          className="flex items-baseline gap-2 rounded-lg pr-2 font-bold text-base tracking-[-0.02em] focus-visible:ring-2 focus-visible:ring-ring"
          href="#top"
        >
          Glide
          <span className="font-normal text-muted-foreground text-xs tabular-nums">
            v{siteConfig.version}
          </span>
        </a>

        {/*
          Hidden on a phone, where the row only has space for the wordmark and
          the download, and where a font file is not installable anyway.
        */}
        <nav
          aria-label="Sections"
          className="ml-auto hidden items-center gap-1 md:flex"
        >
          {sections.map((section) => (
            <a
              aria-current={active === section.id ? "true" : undefined}
              className={cn(
                "rounded-lg px-2.5 py-1.5 text-sm transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring",
                active === section.id
                  ? "font-medium text-foreground"
                  : "text-muted-foreground"
              )}
              href={`#${section.id}`}
              key={section.id}
            >
              {section.label}
            </a>
          ))}
        </nav>

        <TrackedLink
          className={cn(
            buttonVariants({ size: "sm" }),
            "ml-auto md:ml-2 max-sm:h-10"
          )}
          download="glide.zip"
          href={asset("/glide.zip")}
          label="download-desktop"
          location="nav"
        >
          Download
        </TrackedLink>
      </div>
    </header>
  );
};
