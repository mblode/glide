import { siteConfig } from "@/lib/config";

export const dynamic = "force-static";

export function GET() {
  const catalog = {
    linkset: [
      {
        anchor: siteConfig.url,
        "service-doc": [
          {
            href: siteConfig.links.github,
            type: "text/html",
            title: "Glide source and documentation",
          },
        ],
        "service-desc": [
          {
            href: `${siteConfig.links.github}/releases`,
            type: "text/html",
            title: "Glide releases",
          },
        ],
        status: [
          {
            href: siteConfig.url,
            type: "text/html",
            title: "Glide website",
          },
        ],
      },
      {
        anchor: `${siteConfig.url}/download`,
        describedby: [
          {
            href: `${siteConfig.links.github}/blob/main/README.md`,
            type: "text/markdown",
          },
        ],
        item: [
          {
            href: siteConfig.downloadUrl,
            type: "application/zip",
            title: `Glide ${siteConfig.version} font archive`,
          },
        ],
      },
    ],
  };

  return new Response(JSON.stringify(catalog, null, 2), {
    headers: {
      "Content-Type": "application/linkset+json; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
