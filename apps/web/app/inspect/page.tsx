import type { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { InterpolationInspector } from "@/components/interpolation-inspector";
import { siteConfig } from "@/lib/config";

export const metadata: Metadata = {
  title: "Interpolation inspector",
  description:
    "Visualise how Glide interpolates its weight axis from three masters (Thin, Regular, Extra Black) and where in-between weights drift.",
  // Without this the page inherits the layout's canonical, which points at the
  // home page, so a URL that is in the sitemap canonicalises away from itself.
  alternates: {
    canonical: `${siteConfig.url}/inspect`,
  },
};

export default function InspectPage() {
  return (
    <main id="main-content" className="mx-auto w-full max-w-5xl px-4 py-16 sm:px-6">
      <div className="mb-10 space-y-4">
        <Button variant="outline" size="sm" asChild>
          <Link href="/">← Back</Link>
        </Button>
        <h1 className="text-4xl font-black tracking-[-0.04em] sm:text-5xl">
          Interpolation inspector
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Sweep the weight axis and watch the three-master interpolation. Master
          positions are exact; the midpoints between them are where shape drift
          appears first.
        </p>
      </div>

      <section className="rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8">
        <InterpolationInspector />
      </section>
    </main>
  );
}
