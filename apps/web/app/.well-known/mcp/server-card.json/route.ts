import { siteConfig } from "@/lib/config";

export const dynamic = "force-static";

export function GET() {
  const card = {
    $schema:
      "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/well-known/server-card.schema.json",
    serverInfo: {
      name: `${siteConfig.name} WebMCP`,
      version: siteConfig.version,
      title: `${siteConfig.name} — ${siteConfig.description}`,
      publisher: {
        name: siteConfig.author.name,
        url: siteConfig.author.url,
      },
    },
    transport: {
      type: "webmcp",
      url: siteConfig.url,
    },
    capabilities: {
      tools: {
        listChanged: false,
      },
    },
    tools: [
      {
        name: "download_glide",
        description: `Returns the URL for the Glide ${siteConfig.version} font archive.`,
      },
      {
        name: "open_playground",
        description: "Scrolls the page to the Glide interactive playground.",
      },
    ],
  };

  return new Response(JSON.stringify(card, null, 2), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
