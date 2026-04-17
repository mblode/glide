import type { Family } from "@/lib/data";
import { Button } from "@/components/ui/button";

export function ExportButton({
  family,
  name,
}: {
  family: Family;
  name: string;
}) {
  const href = `/api/export/${family}/${encodeURIComponent(name)}`;
  return (
    <Button asChild variant="outline" size="sm">
      <a
        href={href}
        download={`glyph-forge-${family}-${name}.html`}
        title="Download self-contained HTML of this loupe (inlined SVGs, print-friendly)"
      >
        ↓ Export
      </a>
    </Button>
  );
}
