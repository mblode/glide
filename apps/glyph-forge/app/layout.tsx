import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Glyph Forge — Glide audit",
  description: "Internal tool. Visual audit loupe over Glide variable font interpolation against the Circular donor.",
  robots: { index: false, follow: false },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="min-h-dvh antialiased">{children}</body>
    </html>
  );
}
