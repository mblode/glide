"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";

const VIEWS = [
  { id: "overview", label: "Overview" },
  { id: "tokens", label: "Tokens" },
  { id: "activity", label: "Activity" },
] as const;

type ViewId = (typeof VIEWS)[number]["id"];

const ROWS = [
  { name: "Save changes", weight: "400", style: "Button" },
  { name: "Search projects", weight: "400", style: "Field" },
  { name: "Primary action", weight: "600", style: "Button" },
  { name: "1,280 members", weight: "500", style: "Table" },
] as const;

export function UiSpecimen() {
  const [weight, setWeight] = useState(400);
  const [view, setView] = useState<ViewId>("overview");
  const [query, setQuery] = useState("");

  const rows = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      return ROWS;
    }
    return ROWS.filter((row) =>
      `${row.name} ${row.weight} ${row.style}`.toLowerCase().includes(q),
    );
  }, [query]);

  const previewStyle = {
    fontSize: "0.875rem",
    fontWeight: weight,
    fontFeatureSettings: '"tnum" 1, "liga" 1',
  } as const;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <h2 className="text-lg font-bold tracking-tight">In UI</h2>
          <p className="max-w-[48ch] text-pretty text-sm text-muted-foreground">
            The same face at 14px, in chrome you would actually ship.
          </p>
        </div>
        <div className="w-full space-y-2 sm:max-w-56">
          <div className="flex items-baseline justify-between">
            <Label htmlFor="ui-weight-slider">Weight</Label>
            <span className="text-sm font-medium tabular-nums" style={{ fontWeight: weight }}>
              {weight}
            </span>
          </div>
          <Slider
            id="ui-weight-slider"
            min={100}
            max={950}
            step={1}
            value={[weight]}
            onValueChange={([v]) => setWeight(v)}
          />
        </div>
      </div>

      <div
        className="space-y-4 rounded-xl border border-border bg-background/40 p-4"
        style={previewStyle}
      >
        <div role="radiogroup" aria-label="Specimen view" className="flex flex-wrap gap-1">
          {VIEWS.map((item) => (
            <Button
              key={item.id}
              type="button"
              size="xs"
              variant={view === item.id ? "default" : "outline"}
              role="radio"
              aria-checked={view === item.id}
              onClick={() => setView(item.id)}
            >
              {item.label}
            </Button>
          ))}
        </div>

        {view === "overview" && (
          <div className="space-y-4">
            <div className="max-w-xs space-y-2">
              <Label htmlFor="ui-search">Search</Label>
              <Input
                id="ui-search"
                name="ui-search"
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Filter rows"
                className="h-8 text-sm max-sm:text-base"
              />
            </div>
            {rows.length === 0 ? (
              <p className="text-muted-foreground">
                No rows match.{" "}
                <button
                  type="button"
                  className="underline underline-offset-4 hover:text-foreground"
                  onClick={() => setQuery("")}
                >
                  Clear search
                </button>
              </p>
            ) : (
              <div className="-mx-4 overflow-x-auto sm:mx-0">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="whitespace-nowrap py-2 pr-4 font-medium">Name</th>
                      <th className="whitespace-nowrap py-2 pr-4 font-medium">Weight</th>
                      <th className="whitespace-nowrap py-2 font-medium">Style</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map((row) => (
                      <tr key={row.name} className="border-b border-border last:border-b-0">
                        <td className="py-2 pr-4">{row.name}</td>
                        <td className="py-2 pr-4 tabular-nums">{row.weight}</td>
                        <td className="py-2 text-muted-foreground">{row.style}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {view === "tokens" && (
          <dl className="grid gap-3 sm:grid-cols-2">
            <div className="space-y-1">
              <dt className="text-muted-foreground">Font family</dt>
              <dd>Glide Variable</dd>
            </div>
            <div className="space-y-1">
              <dt className="text-muted-foreground">Weight axis</dt>
              <dd className="tabular-nums">100–950</dd>
            </div>
            <div className="space-y-1">
              <dt className="text-muted-foreground">Default size</dt>
              <dd className="tabular-nums">14px / 20px</dd>
            </div>
            <div className="space-y-1">
              <dt className="text-muted-foreground">Features</dt>
              <dd>liga, tnum, kern</dd>
            </div>
          </dl>
        )}

        {view === "activity" && (
          <ul role="list" className="space-y-3">
            <li className="flex justify-between gap-4">
              <span>Published v3.0.2</span>
              <span className="shrink-0 text-muted-foreground tabular-nums">2h ago</span>
            </li>
            <li className="flex justify-between gap-4">
              <span>Synced italic masters</span>
              <span className="shrink-0 text-muted-foreground tabular-nums">Yesterday</span>
            </li>
            <li className="flex justify-between gap-4">
              <span>Opened interpolation inspector</span>
              <span className="shrink-0 text-muted-foreground tabular-nums">3 days ago</span>
            </li>
          </ul>
        )}
      </div>
    </div>
  );
}
