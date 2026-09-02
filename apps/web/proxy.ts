import { NextResponse, type NextRequest } from "next/server";
import { markdownByPath } from "@/lib/markdown";

// Parse Accept as media types, not a substring match: `text/markdown` inside a
// quality parameter or a wildcard entry must not trigger negotiation.
const wantsMarkdownFrom = (accept: string | null) =>
  (accept ?? "")
    .split(",")
    .map((part) => part.split(";")[0].trim().toLowerCase())
    .some((type) => type === "text/markdown" || type === "text/x-markdown");

export function proxy(request: NextRequest) {
  const wantsMarkdown = wantsMarkdownFrom(request.headers.get("accept"));

  if (!wantsMarkdown) {
    return NextResponse.next();
  }

  const pathname = request.nextUrl.pathname.replace(/\/+$/, "") || "/";
  const body = markdownByPath[pathname];

  if (!body) {
    return NextResponse.next();
  }

  const tokens = Math.ceil(body.length / 4);

  return new NextResponse(body, {
    status: 200,
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      Vary: "Accept",
      "x-markdown-tokens": String(tokens),
      "Cache-Control": "public, max-age=3600",
    },
  });
}

export const config = {
  matcher: ["/"],
};
