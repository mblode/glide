import type { MetadataRoute } from "next";
import { siteConfig } from "@/lib/config";

// The date the page last changed in substance (the 4.0.15 release), not the
// build date: `new Date()` marks the URL as changed on every deploy, and Google
// then stops trusting lastmod for the site. Bump it with the next release that
// changes the specimen. No `priority`: Google ignores it.
const lastModified = new Date("2026-08-25");

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    // Single page: the glyph inspector moved into the homepage at #characters,
    // so /glyphs no longer exists and must not be advertised here.
    {
      url: siteConfig.url,
      lastModified,
    },
  ];
}
