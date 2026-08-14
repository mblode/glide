import type { MetadataRoute } from "next";
import { siteConfig } from "@/lib/config";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return [
    {
      url: siteConfig.url,
      lastModified,
      priority: 1,
    },
    {
      url: `${siteConfig.url}/glyphs`,
      lastModified,
      priority: 0.5,
    },
  ];
}
