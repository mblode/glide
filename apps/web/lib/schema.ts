import { siteConfig } from "@/lib/config";

/**
 * Stable `@id` anchors, so this zone's nodes resolve into one graph instead of
 * several disconnected snippets.
 *
 * The Person, Organization and WebSite ids belong to blode.co and are only ever
 * referenced, never redefined here. blode.co/glide is a path on blode.co behind
 * a rewrite, not a site of its own: redefining them would publish a second
 * Matthew Blode and a second website on one domain. Contract:
 * blode-co/apps/web/.claude/knowledge/zone-conventions.md
 */
const host = "https://blode.co";

export const schemaId = {
  breadcrumb: `${siteConfig.url}/#breadcrumb`,
  font: `${siteConfig.url}/#font`,
  organization: `${host}/#organization`,
  person: `${host}/#person`,
  webPage: `${siteConfig.url}/#webpage`,
  website: `${host}/#website`,
} as const;

export const siteGraph = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@id": schemaId.webPage,
      "@type": "WebPage",
      about: { "@id": schemaId.font },
      breadcrumb: { "@id": schemaId.breadcrumb },
      description: siteConfig.description,
      inLanguage: "en-US",
      isPartOf: { "@id": schemaId.website },
      name: siteConfig.name,
      url: siteConfig.url,
    },
    /*
     * A typeface, not an app. SoftwareApplication would additionally require
     * `offers` plus one of `aggregateRating` or `review` for Google's Software
     * App rich result, and its review guidelines forbid ratings we author about
     * our own work, so that type could only ever fail validation.
     */
    {
      "@id": schemaId.font,
      "@type": "CreativeWork",
      author: { "@id": schemaId.person },
      description: siteConfig.description,
      isAccessibleForFree: true,
      isPartOf: { "@id": schemaId.website },
      license: "https://openfontlicense.org",
      name: "Glide Variable Font",
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "USD",
      },
      publisher: { "@id": schemaId.organization },
      url: siteConfig.url,
      version: siteConfig.version,
    },
    {
      "@id": schemaId.breadcrumb,
      "@type": "BreadcrumbList",
      itemListElement: [
        /*
         * "Matthew Blode", not "Home", and it must stay identical to the
         * visible trail in <ZoneBreadcrumb>: Google treats a mismatch between
         * the two as a markup error.
         */
        {
          "@type": "ListItem",
          item: `${host}/`,
          name: siteConfig.author.name,
          position: 1,
        },
        {
          "@type": "ListItem",
          item: `${host}/projects`,
          name: "Projects",
          position: 2,
        },
        {
          "@type": "ListItem",
          item: siteConfig.url,
          name: siteConfig.name,
          position: 3,
        },
      ],
    },
  ],
};
