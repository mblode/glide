import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";

const glide = localFont({
  src: [
    { path: "../public/glide-variable.woff2", style: "normal" },
    { path: "../public/glide-variable-italic.woff2", style: "italic" },
  ],
  variable: "--font-glide",
  weight: "400 900",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Glide — Variable Font Family Crafted for UI",
  description:
    "Glide is a variable sans-serif font family by Matthew Blode. Weights from 400 to 900 in roman and italic.",
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
    <html lang="en" className={`${glide.variable} antialiased`}>
      <body className="min-h-dvh bg-background text-foreground">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-background focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:shadow-lg focus:ring-2 focus:ring-ring"
        >
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
