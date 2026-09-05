import type { NextConfig } from "next";

import { basePath } from "./lib/config";

// Link header values are never basePath-prefixed by Next, so the zone prefix is
// applied explicitly here. Note these `.well-known` routes now live under
// /glide rather than the host root, so rel-based discovery via this header is
// the only way agents will find them.
const linkHeader = [
  `<${basePath}/.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json"`,
  `<${basePath}/.well-known/agent-skills/index.json>; rel="https://agentskills.io/rel/index"; type="application/json"`,
  `<${basePath}/.well-known/mcp/server-card.json>; rel="https://modelcontextprotocol.io/rel/server-card"; type="application/json"`,
  '<https://github.com/mblode/glide>; rel="service-doc"',
  '<https://github.com/mblode/glide/releases>; rel="service-desc"',
].join(", ");

const isDev = process.env.NODE_ENV === "development";

// The PostHog ingestion host, set per Vercel project to our reverse proxy
// (https://r.blode.co). posthog-js lazy-loads chunks from it, so it belongs in
// script-src as well as connect-src.
const posthogOrigin = process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "";

// The Glide woff2 files are served from this app's own public/, so font-src
// never needs a third-party origin.
const contentSecurityPolicy = [
  "default-src 'self'",
  // 'unsafe-inline' covers Next's bootstrap and the JSON-LD block. Dev also
  // needs 'unsafe-eval' for React Refresh; production must not have it.
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""} ${posthogOrigin}`,
  `connect-src 'self' ${posthogOrigin}`,
  "img-src 'self' data:",
  "style-src 'self' 'unsafe-inline'",
  "font-src 'self'",
  "worker-src 'self' blob:",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  "upgrade-insecure-requests",
].join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy", value: contentSecurityPolicy },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=(), payment=()",
  },
  { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
  { key: "Cross-Origin-Resource-Policy", value: "same-origin" },
];

const nextConfig: NextConfig = {
  assetPrefix: basePath,
  basePath,
  // Next adds `x-powered-by: Next.js` by default; it is fingerprinting for free.
  poweredByHeader: false,
  async headers() {
    // Every matching rule applies in array order and a later value wins per
    // header key, so the catch-all comes first and per-route rules after it.
    //
    // `/:path*`, not `/(.*)`. Next prefixes basePath onto the source, and
    // `/glide/(.*)` needs the separator, so it misses the zone root: the one
    // URL blode.co actually links to. `/:path*` matches `/glide` as well.
    return [
      {
        headers: securityHeaders,
        source: "/:path*",
      },
      // The share card is fetched by other origins, so it opts out of the
      // same-origin CORP the catch-all sets.
      {
        headers: [
          { key: "Cross-Origin-Resource-Policy", value: "cross-origin" },
        ],
        source: "/opengraph-image",
      },
      {
        headers: [{ key: "Link", value: linkHeader }],
        source: "/",
      },
    ];
  },
  async redirects() {
    return [
      /*
        Both pages were retired into the homepage: /inspect became /glyphs, and
        /glyphs became the glyph grid in the `#characters` row. The old
        /inspect rule still pointed at /glyphs, so it 301'd onto a 404, and
        both paths were still taking hits. They now land on the section that
        replaced them.
      */
      {
        destination: "/#characters",
        permanent: true,
        source: "/glyphs",
      },
      {
        destination: "/#characters",
        permanent: true,
        source: "/inspect",
      },
      {
        basePath: false,
        destination: "https://blode.co/glide",
        has: [{ type: "host" as const, value: "glide.blode.co" }],
        permanent: true,
        source: "/",
      },
      {
        // The old subdomain stays attached to this Vercel project, so the 301 to
        // the canonical subdirectory has to happen here. It cannot be a
        // Cloudflare Redirect Rule: every blode.co DNS record is "DNS only", so
        // no traffic passes through Cloudflare's proxy for a rule to fire on.
        //
        // basePath: false so `source` matches the raw incoming path instead of
        // being prefixed to /glide/:path*.
        //
        // No loop: blode.co/glide proxies to glide.zone.blode.co, whose host
        // does not match this rule, so that request falls through to the app.
        basePath: false,
        destination: "https://blode.co/glide/:path*",
        has: [{ type: "host" as const, value: "glide.blode.co" }],
        permanent: true,
        source: "/:path*",
      },
    ];
  },
};

export default nextConfig;
