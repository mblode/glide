import { NextResponse, type NextRequest } from "next/server";
import { markdownByPath } from "@/lib/markdown";

export function proxy(request: NextRequest) {
  const accept = request.headers.get("accept") ?? "";
  const wantsMarkdown = /\btext\/markdown\b/i.test(accept);

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
  matcher: ["/", "/download"],
};
