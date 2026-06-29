import type { NextConfig } from "next";

const linkHeader = [
  '</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json"',
  '</.well-known/agent-skills/index.json>; rel="https://agentskills.io/rel/index"; type="application/json"',
  '</.well-known/mcp/server-card.json>; rel="https://modelcontextprotocol.io/rel/server-card"; type="application/json"',
  '<https://github.com/mblode/glide>; rel="service-doc"',
  '<https://github.com/mblode/glide/releases>; rel="service-desc"',
].join(", ");

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: "/",
        headers: [{ key: "Link", value: linkHeader }],
      },
      {
        source: "/download",
        headers: [{ key: "Link", value: linkHeader }],
      },
    ];
  },
};

export default nextConfig;
