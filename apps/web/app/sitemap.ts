import type { MetadataRoute } from "next";
import { siteConfig } from "@/lib/config";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return [
    // Single page: the glyph inspector moved into the homepage at #characters,
    // so /glyphs no longer exists and must not be advertised here.
    {
      url: siteConfig.url,
      lastModified,
      priority: 1,
    },
  ];
}
