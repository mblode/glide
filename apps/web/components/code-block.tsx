"use client";

import { useState } from "react";
import { CheckIcon, CopyIcon } from "blode-icons-react";

export function CodeBlock({
  children,
  filename,
}: {
  children: string;
  filename?: string;
}) {
  const [copied, setCopied] = useState(false);

  function copy() {
    navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

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
      <button
        type="button"
        onClick={copy}
        className="absolute right-3 top-3 rounded-lg border border-border bg-background p-1.5 opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100"
        aria-label="Copy code"
      >
        {copied ? (
          <CheckIcon size={14} className="text-mint" />
        ) : (
          <CopyIcon size={14} className="text-muted-foreground" />
        )}
      </button>
    </div>
  );
}
