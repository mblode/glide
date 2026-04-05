"use client";

import {
  Checkmark1Icon as CheckIcon,
  CopySimpleIcon as CopyIcon,
} from "blode-icons-react";
import { cva } from "class-variance-authority";
import type { VariantProps } from "class-variance-authority";
import { AnimatePresence, motion } from "motion/react";
import { useCallback, useState } from "react";
import type { MouseEvent } from "react";

import { cn } from "@/lib/utils";

const copyButtonVariants = cva(
  "flex shrink-0 items-center justify-center rounded-md outline-none transition-[box-shadow,_color,_background-color,_border-color,_outline-color,_text-decoration-color,_fill,_stroke] focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg:not([class*='size-'])]:size-4 [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    defaultVariants: {
      size: "default",
      variant: "ghost",
    },
    variants: {
      size: {
        default: "size-9",
        lg: "size-10 rounded-md",
        sm: "size-8 rounded-md",
        xs: "size-7 rounded-md [&_svg:not([class*='size-'])]:size-3.5",
      },
      variant: {
        default:
          "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90",
        ghost:
          "hover:bg-accent hover:text-accent-foreground",
        outline:
          "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground",
      },
    },
  }
);

type CopyButtonProps = Omit<
  React.ComponentProps<"button">,
  "children"
> &
  VariantProps<typeof copyButtonVariants> & {
    content: string;
    delay?: number;
  };

const CopyButton = ({
  className,
  content,
  onClick,
  variant,
  size,
  delay = 3000,
  ...props
}: CopyButtonProps) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = useCallback(
    async (e: MouseEvent<HTMLButtonElement>) => {
      onClick?.(e);
      if (isCopied) return;
      try {
        await navigator.clipboard.writeText(content);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), delay);
      } catch (error) {
        console.error("Error copying content", error);
      }
    },
    [onClick, isCopied, content, delay]
  );

  const Icon = isCopied ? CheckIcon : CopyIcon;

  return (
    <button
      type="button"
      className={cn(copyButtonVariants({ className, size, variant }))}
      data-slot="copy-button"
      onClick={handleCopy}
      aria-label={isCopied ? "Copied" : "Copy code"}
      {...props}
    >
      <AnimatePresence mode="wait" initial={false}>
        <motion.span
          key={isCopied ? "check" : "copy"}
          data-slot="copy-button-icon"
          initial={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
          animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
          exit={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
          transition={{ type: "spring", duration: 0.2, bounce: 0 }}
        >
          <Icon />
        </motion.span>
      </AnimatePresence>
    </button>
  );
};

export { CopyButton };
