import type { Metadata } from "next";
import { siteConfig } from "@/lib/config";
import { DownloadPage } from "@/components/download-page";

export const metadata: Metadata = {
  title: "Download Glide Variable Font",
  description: `Download Glide ${siteConfig.version} — a variable sans-serif font family by Matthew Blode. Weights from 400 to 900 in roman and italic.`,
  openGraph: {
    type: "website",
    url: `${siteConfig.url}/download`,
    title: "Download Glide Variable Font",
    description: `Download Glide ${siteConfig.version} — a variable sans-serif font family by Matthew Blode.`,
    siteName: siteConfig.name,
  },
  twitter: {
    card: "summary_large_image",
    title: "Download Glide Variable Font",
    description: `Download Glide ${siteConfig.version} — a variable sans-serif font family by Matthew Blode.`,
  },
  alternates: {
    canonical: `${siteConfig.url}/download`,
  },
};

export default function Page() {
  return <DownloadPage />;
}
