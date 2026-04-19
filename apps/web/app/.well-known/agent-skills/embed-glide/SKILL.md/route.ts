import { embedSkill } from "@/lib/agent-skills";

export const dynamic = "force-static";

export function GET() {
  return new Response(embedSkill, {
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
