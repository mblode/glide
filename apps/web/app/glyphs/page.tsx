import type { Metadata } from "next";
import Link from "next/link";

import { GlyphSet } from "@/components/glyph-set";
import { Button } from "@/components/ui/button";
import { siteConfig } from "@/lib/config";

export const metadata: Metadata = {
  title: "Glyph set",
  description:
    "Browse every encoded glyph in Glide Variable, with a live weight slider for roman and italic.",
  alternates: {
    canonical: `${siteConfig.url}/glyphs`,
  },
};

export default function GlyphsPage() {
  return (
    <main id="main-content" className="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6">
      <div className="mb-10 space-y-4">
        <Button variant="outline" size="sm" asChild>
          <Link href="/">← Back</Link>
        </Button>
        <h1 className="text-4xl font-black tracking-[-0.04em] sm:text-5xl">
          Glyph set
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Every encoded character in the shipped Glide Variable webfont. Scrub
          the weight axis and switch roman or italic to check outlines across
          the family.
        </p>
      </div>

      <section className="rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8">
        <GlyphSet />
      </section>
    </main>
  );
}
