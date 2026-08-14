import { ArrowLeftIcon } from "blode-icons-react";
import type { Metadata } from "next";
import Link from "next/link";

import { GlyphSet } from "@/components/glyph-set";
import { Button } from "@/components/ui/button";
import { siteConfig } from "@/lib/config";

export const metadata: Metadata = {
  title: "Glyphs",
  description:
    "Inspect every encoded glyph in Glide Variable against cap height, x-height, and baseline.",
  alternates: {
    canonical: `${siteConfig.url}/glyphs`,
  },
};

export default async function GlyphsPage({
  searchParams,
}: {
  searchParams: Promise<{ g?: string }>;
}) {
  const { g } = await searchParams;

  return (
    <main
      id="main-content"
      className="flex min-h-dvh flex-col lg:h-dvh lg:overflow-hidden"
    >
      <div className="flex items-center gap-3 border-b border-border px-4 py-3 sm:px-6">
        <Button variant="outline" size="sm" asChild>
          <Link href="/">
            <ArrowLeftIcon aria-hidden="true" data-icon="inline-start" />
            Home
          </Link>
        </Button>
        <h1 className="text-lg font-semibold tracking-tight">Glyphs</h1>
      </div>
      <GlyphSet initialName={g} />
    </main>
  );
}
