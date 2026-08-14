import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { JsonLd } from "@/components/json-ld";
import { WebMcp } from "@/components/web-mcp";
import { siteConfig } from "@/lib/config";
import { siteGraph } from "@/lib/schema";
import "./globals.css";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },
    { path: "../public/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "100 950",
  display: "swap",
});

const glideMono = localFont({
  src: [{ path: "../public/glide-mono-variable.woff2", style: "normal" }],
  variable: "--font-glide-mono",
  weight: "100 700",
  display: "swap",
});

const title = "Glide Variable Font Family Crafted for UI";

export const metadata: Metadata = {
  /*
   * Includes the basePath (Rule 11). Only correct because the card is a
   * generated `opengraph-image.tsx` route: Next does not prefix those with
   * `basePath`, so `metadataBase` supplies `/glide` exactly once. Against the
   * static PNG this replaced (and against `app/opengraph-image.png`), the two
   * stacked into `/glide/glide/opengraph-image.png` — the shape this zone
   * shipped for months.
   */
  metadataBase: new URL(siteConfig.url),
  title: {
    default: title,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  authors: [siteConfig.author],
  creator: siteConfig.author.name,
  // No `images` here: `app/opengraph-image.tsx` is the card. Next reuses it for
  // `twitter:image` too when there is no `twitter-image` file.
  openGraph: {
    type: "website",
    /*
     * No `url` here. It is not per-page, so /glyphs inherited the zone root
     * and every share of it collapsed onto the home page. It cannot be fixed
     * per page either: a child declaring `openGraph: { url }` replaces this
     * whole object and loses `siteName` with it. Absent beats wrong, since
     * consumers fall back to the URL they fetched and `alternates.canonical`
     * is already per-page. See zone-conventions.md Rule 9.
     */
    title,
    description: siteConfig.description,
    // One site, 33 paths: the product name is already in og:title, so this is
    // the only slot left to say who made it. See zone-conventions.md Rule 9.
    siteName: siteConfig.author.name,
  },
  twitter: {
    card: "summary_large_image",
    title,
    description: siteConfig.description,
    creator: "@mattblode",
  },
  alternates: {
    canonical: siteConfig.url,
  },
  verification: {
    google: "mFwyBIbXTaKK4uF_NA0MzVWFyY40hPgBjFObg3rje04",
  },
  other: {
    "apple-mobile-web-app-title": "Glide",
  },
};

export const viewport: Viewport = {
  themeColor: "#fbb6cd",
  colorScheme: "light",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${glide.variable} ${glideMono.variable} antialiased`}>
      <head>
        <link href={process.env.NEXT_PUBLIC_POSTHOG_HOST} rel="preconnect" />
      </head>
      <body className="min-h-dvh bg-background text-foreground">
        <JsonLd data={siteGraph} />
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-background focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:shadow-lg focus:ring-2 focus:ring-ring"
        >
          Skip to content
        </a>
        {children}
        <WebMcp />
      </body>
    </html>
  );
}
