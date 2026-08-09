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
  src: [{ path: "../public/glide-mono.woff2", style: "normal" }],
  variable: "--font-glide-mono",
  weight: "400",
  display: "swap",
});

const title = "Glide Variable Font Family Crafted for UI";

export const metadata: Metadata = {
  /*
   * Includes the basePath (Rule 11), because Next joins metadataBase's
   * pathname onto every relative metadata URL.
   *
   * That is why the cards below point at files in `public/` rather than using
   * the `app/opengraph-image.png` convention. That convention prefixes the
   * basePath onto the URL it generates, metadataBase then prefixes it a second
   * time, and the card 404s at /glide/glide/opengraph-image.png: the shape this
   * zone shipped for months. A file-convention image also outranks
   * `openGraph.images`, so declaring the right URL here is not enough on its
   * own; the file has to leave `app/`. Keep these root-relative and let
   * metadataBase supply the /glide.
   */
  metadataBase: new URL(siteConfig.url),
  title: {
    default: title,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  authors: [siteConfig.author],
  creator: siteConfig.author.name,
  openGraph: {
    type: "website",
    url: siteConfig.url,
    title,
    description: siteConfig.description,
    // One site, 33 paths: the product name is already in og:title, so this is
    // the only slot left to say who made it. See zone-conventions.md Rule 9.
    siteName: siteConfig.author.name,
    images: [{ url: "/opengraph-image.png", width: 1200, height: 630, alt: title }],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description: siteConfig.description,
    creator: "@mattblode",
    images: ["/twitter-image.png"],
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
