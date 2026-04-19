"use client";

import { useEffect } from "react";
import { siteConfig } from "@/lib/config";

type ToolDefinition = {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  execute: (args: unknown) => Promise<unknown>;
};

type ModelContext = {
  provideContext: (context: { tools: ToolDefinition[] }) => void | Promise<void>;
};

declare global {
  interface Navigator {
    modelContext?: ModelContext;
  }
}

export function WebMcp() {
  useEffect(() => {
    const modelContext = navigator.modelContext;
    if (!modelContext) return;

    const tools: ToolDefinition[] = [
      {
        name: "download_glide",
        description: `Returns the download URL for the Glide ${siteConfig.version} font archive.`,
        inputSchema: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        execute: async () => ({
          version: siteConfig.version,
          url: siteConfig.downloadUrl,
          releases: `${siteConfig.links.github}/releases`,
        }),
      },
      {
        name: "open_playground",
        description: "Scrolls to the Glide interactive playground on this page.",
        inputSchema: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        execute: async () => {
          const el = document.getElementById("playground");
          if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "start" });
            return { scrolled: true };
          }
          return { scrolled: false };
        },
      },
    ];

    void modelContext.provideContext({ tools });
  }, []);

  return null;
}
