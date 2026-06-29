import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import Script from "next/script";
import { JsonLd } from "@/components/json-ld";
import { WebMcp } from "@/components/web-mcp";
import { siteConfig } from "@/lib/config";
import "./globals.css";

const googleAnalyticsId = "G-32358W56XH";

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
      <body className="min-h-dvh bg-background text-foreground">
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "Organization",
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
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "Glide Variable Font",
            applicationCategory: "DesignApplication",
            operatingSystem: "All",
            description: siteConfig.description,
            url: siteConfig.url,
            author: {
              "@type": "Person",
              name: siteConfig.author.name,
              url: siteConfig.author.url,
            },
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
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${googleAnalyticsId}');
          `}
        </Script>
      </body>
    </html>
  );
}
