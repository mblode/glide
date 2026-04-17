import { cn } from "@/lib/utils";
import type { AuditVerdict } from "@/lib/data";

const VERDICT_CLASS: Record<AuditVerdict, string> = {
  unknown: "bg-[--color-verdict-unknown]",
  low: "bg-[--color-verdict-low]",
  medium: "bg-[--color-verdict-medium]",
  high: "bg-[--color-verdict-high]",
  blocker: "bg-[--color-verdict-blocker]",
  tracked: "bg-[--color-verdict-tracked]",
};

export function VerdictDot({
  verdict,
  className,
}: {
  verdict: AuditVerdict;
  className?: string;
}) {
  return (
    <span
      aria-label={verdict}
      title={verdict}
      className={cn(
        "inline-block h-2 w-2 shrink-0 rounded-full",
        VERDICT_CLASS[verdict],
        className
      )}
    />
  );
}
