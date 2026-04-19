import { siteConfig } from "@/lib/config";
import { downloadSkill, embedSkill, sha256 } from "@/lib/agent-skills";

export const dynamic = "force-static";

export function GET() {
  const body = {
    $schema:
      "https://raw.githubusercontent.com/cloudflare/agent-skills-discovery-rfc/main/schemas/v0.2.0/index.json",
    version: "0.2.0",
    publisher: {
      name: siteConfig.author.name,
      url: siteConfig.author.url,
    },
    skills: [
      {
        name: "download-glide",
        type: "instructions",
        description:
          "How to download and install the Glide variable font family.",
        url: `${siteConfig.url}/.well-known/agent-skills/download-glide/SKILL.md`,
        sha256: sha256(downloadSkill),
      },
      {
        name: "embed-glide",
        type: "instructions",
        description:
          "How to embed the Glide variable font on the web with @font-face.",
        url: `${siteConfig.url}/.well-known/agent-skills/embed-glide/SKILL.md`,
        sha256: sha256(embedSkill),
      },
    ],
  };

  return new Response(JSON.stringify(body, null, 2), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
