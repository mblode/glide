import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import { JsonLd } from "@/components/json-ld";
import { WebMcp } from "@/components/web-mcp";
import { siteConfig } from "@/lib/config";
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

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: "Glide Variable Font Family Crafted for UI",
  description: siteConfig.description,
  openGraph: {
    type: "website",
    url: siteConfig.url,
    title: "Glide Variable Font Family Crafted for UI",
    description: siteConfig.description,
    siteName: siteConfig.name,
  },
  twitter: {
    card: "summary_large_image",
    title: "Glide Variable Font Family Crafted for UI",
    description: siteConfig.description,
  },
  alternates: {
    canonical: siteConfig.url,
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
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "Person",
            name: siteConfig.author.name,
            url: siteConfig.author.url,
          }}
        />
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "WebSite",
            name: siteConfig.name,
            url: siteConfig.url,
          }}
        />
        {/*
          A typeface, not an app. SoftwareApplication would additionally require
          `offers` plus one of `aggregateRating` or `review` for Google's Software
          App rich result, and its review guidelines forbid ratings we author
          about our own work, so that type could only ever fail validation.
        */}
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            name: "Glide Variable Font",
            description: siteConfig.description,
            url: siteConfig.url,
            version: siteConfig.version,
            author: {
              "@type": "Person",
              name: siteConfig.author.name,
              url: siteConfig.author.url,
            },
            isAccessibleForFree: true,
            license: "https://openfontlicense.org",
            offers: {
              "@type": "Offer",
              price: "0",
              priceCurrency: "USD",
            },
          }}
        />
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
