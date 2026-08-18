"use client";

import { CopyButton } from "@/components/ui/copy-button";

export function CodeBlock({
  children,
  filename,
}: {
  children: string;
  filename?: string;
}) {
  return (
    <div className="group relative min-w-0 rounded-xl border border-border bg-card">
      {filename && (
        <div className="truncate border-b border-border px-4 py-2 text-xs font-medium text-muted-foreground">
          {filename}
        </div>
      )}
      {/*
        `overscroll-x-contain` so swiping a snippet sideways on a phone scrolls
        the snippet and stops there, instead of chaining into the browser's
        back gesture. Parents of this block need `min-w-0` where they are grid
        or flex items: `white-space: pre` makes the longest line the min-content
        width, which otherwise widens the whole row rather than scrolling here.
      */}
      <pre className="overflow-x-auto overscroll-x-contain p-4 text-sm leading-relaxed">
        <code>{children}</code>
      </pre>
      {/*
        Hover reveals it on a mouse; a touch device has no hover, so the button
        stayed invisible and the snippet had no copy affordance at all on the
        phones this page is mostly read on.
      */}
      <CopyButton
        className="absolute right-3 top-3 opacity-0 transition-opacity duration-150 ease-out group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100 pointer-coarse:size-10 pointer-coarse:opacity-100"
        content={children}
        variant="outline"
        size="sm"
      />
    </div>
  );
}
