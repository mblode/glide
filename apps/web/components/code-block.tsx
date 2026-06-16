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
    <div className="group relative rounded-xl border border-border bg-card">
      {filename && (
        <div className="border-b border-border px-4 py-2 text-xs font-medium text-muted-foreground">
          {filename}
        </div>
      )}
      <pre className="overflow-x-auto p-4 text-sm leading-relaxed">
        <code>{children}</code>
      </pre>
      <CopyButton
        className="absolute right-3 top-3 opacity-0 transition-opacity duration-150 ease-out group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100"
        content={children}
        variant="outline"
        size="sm"
      />
    </div>
  );
}
