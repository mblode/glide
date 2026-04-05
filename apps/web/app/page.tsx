import Image from "next/image";
import { DownloadIcon, PencilIcon } from "blode-icons-react";
import { Button } from "@/components/ui/button";
import { InstallSection } from "@/components/install-section";
import { Playground } from "@/components/playground";
import { WeightShowcase } from "@/components/weight-showcase";
import { cn } from "@/lib/utils";
import { siteConfig } from "@/lib/config";

function Section({
  id,
  children,
  bordered = true,
}: {
  id?: string;
  children: React.ReactNode;
  bordered?: boolean;
}) {
  return (
    <section
      id={id}
      className={cn(
        "scroll-mt-6",
        bordered &&
          "rounded-2xl border border-border bg-card/50 p-6 backdrop-blur-sm sm:p-8"
      )}
    >
      {children}
    </section>
  );
}

function SectionHeading({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-lg font-bold tracking-tight">{children}</h2>
  );
}

export default function Home() {
  return (
    <main id="main-content">
      {/* Hero */}
      <section className="flex flex-col items-center gap-6 px-4 py-24 text-center sm:px-6 sm:py-40">
        <h1 className="text-8xl font-black leading-[0.85] tracking-[-0.06em] text-display sm:text-9xl lg:text-[11rem]">
          Glide
        </h1>
        <p className="max-w-md text-xl leading-relaxed text-muted-foreground sm:text-2xl">
          Variable font family crafted for UI.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button asChild>
            <a href="#install">
              <DownloadIcon data-icon="inline-start" />
              Install
            </a>
          </Button>
          <Button variant="outline" asChild>
            <a href="#playground">
              <PencilIcon data-icon="inline-start" />
              Try it
            </a>
          </Button>
        </div>
      </section>

      <div className="mx-auto w-full max-w-5xl space-y-5 px-4 pb-8 sm:px-6">
        {/* Playground */}
        <Section id="playground">
          <div className="space-y-6">
            <SectionHeading>Playground</SectionHeading>
            <Playground />
          </div>
        </Section>

        {/* Weights */}
        <Section bordered={false}>
          <WeightShowcase />
        </Section>

        {/* Install */}
        <Section id="install">
          <InstallSection />
        </Section>

        {/* Footer */}
        <footer className="flex flex-col items-center justify-center gap-2 pt-16 pb-8 text-muted-foreground text-sm">
          <div className="flex items-center gap-1">
            Crafted by
            <a
              className="flex items-center gap-2 rounded-full py-1.5 pr-2.5 pl-1.5 transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-full"
              href={siteConfig.links.author}
              rel="noopener noreferrer"
              target="_blank"
            >
              <Image
                alt="Avatar of Matthew Blode"
                className="rounded-full"
                height={20}
                src="/matthew-blode-profile.jpg"
                width={20}
              />
              Matthew Blode
            </a>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground/30">
            <span className="text-muted-foreground">
              v{siteConfig.version}
            </span>{" "}
            &bull;
            <a
              className="text-muted-foreground transition-colors hover:text-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:rounded-lg"
              href={siteConfig.links.github}
              rel="noopener noreferrer"
              target="_blank"
            >
              GitHub
            </a>
          </div>
        </footer>
      </div>
    </main>
  );
}
