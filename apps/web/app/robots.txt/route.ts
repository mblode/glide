import { siteConfig } from "@/lib/config";

export const dynamic = "force-static";

export function GET() {
  // AI-open on purpose: crawl, index, ground and train are all permitted, so a
  // single `*` group states the whole policy. No `Content-Signal:` line: signals
  // are a reservation mechanism, so silence already means no restriction is
  // expressed, and an all-yes signal only adds an unknown-directive warning in
  // Search Console.
  const body = [
    "User-agent: *",
    "Allow: /",
    "",
    `Sitemap: ${siteConfig.url}/sitemap.xml`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
