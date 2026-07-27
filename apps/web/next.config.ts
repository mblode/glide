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

const nextConfig: NextConfig = {
  assetPrefix: basePath,
  basePath,
  async headers() {
    return [
      {
        headers: [{ key: "Link", value: linkHeader }],
        source: "/",
      },
    ];
  },
  async redirects() {
    return [
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
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
