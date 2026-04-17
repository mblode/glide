"""Bulk-stage solver winners into pending-triage-edits.json.

Use this to fill the triage queue for a whole bucket of glyphs in one go,
instead of clicking through 100+ loupes. You still review on /triage and
apply via `npm run apply`.

Selection options (combinable):
  --family FAM           Limit to roman or italic
  --min-gain N           Only stage glyphs where solver projects a gain of at least N (default 0.1)
  --names FILE           Explicit list — one glyph per line (leading '/' stripped).
  --source LABEL         Source tag stored on the edit (default: 'manual')
  --dry-run              Print what would be staged without writing

Safety:
- Skips glyphs that already have a pending edit (won't clobber manual review)
- Skips glyphs with no solver verdict or gain < min_gain
- --no-downgrade: never replace a more-comprehensive existing strategy with a
  lighter one (e.g. structural_fallback → weighted_fallback). Catches the case
  where the solver's raster simulation under-estimates what a vector strategy
  actually does for compatibility.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from shared import MANIFEST_PATH, PACKAGE_ROOT

# Rigour ordering — higher index means more comprehensive repair.
# Staging a lower-rigour strategy over a higher one is a potential regression.
STRATEGY_RIGOUR = {
    "manual_review": 0,
    "reference_fallback": 1,
    "weighted_fallback": 2,
    "inherit_base_contours": 3,
    "donor_copy": 4,
    "structural_fallback": 5,
    "rebuild_notdef": 6,
}

PENDING_PATH = PACKAGE_ROOT / "manifests" / "pending-triage-edits.json"
SOLVER_PATH = PACKAGE_ROOT / "manifests" / "solver-results.json"


def _load(path: Path):
    if not path.exists():
        return None
    with path.open() as f:
        return json.load(f)


def _read_names_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    out: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line.lstrip("/"))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=["roman", "italic"])
    parser.add_argument("--min-gain", type=float, default=0.1)
    parser.add_argument("--names", type=Path)
    parser.add_argument("--source", default="manual")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-downgrade",
        action="store_true",
        help="Skip glyphs whose existing triage strategy is more comprehensive than the solver winner.",
    )
    args = parser.parse_args()

    manifest = _load(MANIFEST_PATH) or []
    solver = _load(SOLVER_PATH) or {}
    pending = _load(PENDING_PATH) or []
    if not isinstance(pending, list):
        pending = []

    existing_keys = {f"{e['family']}/{e['glyph']}" for e in pending}

    name_filter: set[str] | None = None
    if args.names:
        names = _read_names_file(args.names)
        name_filter = set(names)
        print(f"filtering by {len(name_filter)} names from {args.names}")

    candidates = []
    downgrades_skipped = 0
    for entry in manifest:
        fam = entry["family"]
        name = entry["name"]
        if args.family and fam != args.family:
            continue
        if name_filter is not None and name not in name_filter:
            continue
        v = solver.get(f"{fam}/{name}")
        if v is None or v.get("best") is None or v.get("gain") is None:
            continue
        if v["gain"] < args.min_gain:
            continue
        if f"{fam}/{name}" in existing_keys:
            continue
        if args.no_downgrade:
            current_rigour = STRATEGY_RIGOUR.get(entry.get("existingStrategy") or "", -1)
            proposed_rigour = STRATEGY_RIGOUR.get(v["best"], -1)
            if current_rigour > proposed_rigour:
                downgrades_skipped += 1
                continue
        candidates.append((entry, v))

    if args.no_downgrade and downgrades_skipped:
        print(f"  (--no-downgrade) skipped {downgrades_skipped} glyphs where current strategy is more rigorous")

    print(f"would stage {len(candidates)} glyphs (min_gain={args.min_gain})")
    if not candidates:
        return 0

    # Summary by winner
    by_winner: dict[str, int] = {}
    for _, v in candidates:
        by_winner[v["best"]] = by_winner.get(v["best"], 0) + 1
    print("  by winner:", by_winner)

    for entry, v in candidates[:10]:
        print(
            f"    {entry['family']}/{entry['name']:26s} "
            f"{v['currentWorst']:.2f} → {v['bestProjected']:.2f}  ({v['best']})"
        )
    if len(candidates) > 10:
        print(f"    … {len(candidates) - 10} more")

    if args.dry_run:
        print("\n(dry-run, no writes)")
        return 0

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    for entry, v in candidates:
        edit = {
            "family": entry["family"],
            "glyph": entry["name"],
            "strategy": v["best"],
            "source": args.source,
            "notes": (
                f"Bulk-staged by solver: projected {int(v['bestProjected'] * 100)}"
                f" from {int(v['currentWorst'] * 100)} at wght {v['bestWorstWght']}"
                f" (gain +{int(v['gain'] * 100)})"
            ),
            "stagedAt": now,
            "previousStrategy": entry.get("existingStrategy"),
        }
        pending.append(edit)

    pending.sort(key=lambda e: (e["family"], e["glyph"]))
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PENDING_PATH.open("w", encoding="utf-8") as f:
        json.dump(pending, f, indent=2, ensure_ascii=False)
    print(f"\nwrote {len(pending)} total pending edits to {PENDING_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
