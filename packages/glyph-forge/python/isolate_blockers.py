"""Unblock the variable-font build by neutralising three specific glyphs whose
topology confuses fontmake's cu2qu stage.

Two operations, each auto-backed up:

1. For `emacron` and `gdotaccent`: strip their intermediate brace layers from
   `glide-variable.glyphs`. They'll interpolate linearly between Thin/Regular/
   ExtraBlack across the wght axis — a regression on those braces but the whole
   font compiles again.

2. For `emacron`, `gdotaccent`, and `uni021B`: set their triage strategy to
   `reference_fallback` in `circular-triage.json` (freezes all three masters to
   the Regular outline, cu2qu-trivial).

Both steps write `.bak` alongside the mutated files. Run the repair afterwards
and the build should succeed. These three glyphs will look identical at every
weight (acceptable — they were already on the broken list and wouldn't be
fixable without hand-editing in Glyphs.app).
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import glyphsLib

from shared import REPO_ROOT, TRIAGE_MANIFEST

GLYPHS_SOURCE = REPO_ROOT / "glide-variable.glyphs"

# Glyphs to neutralise: (strip_braces?, force_reference_fallback?, flatten_outlines?)
# flatten_outlines=True means copy the Regular master's paths to Thin and ExtraBlack
# so all three masters become byte-identical — trivially cu2qu-compatible.
BLOCKERS = {
    "emacron": (True, True, True),
    "gdotaccent": (True, True, True),
    "uni021B": (False, True, True),
}


def modify_glyphs_source(dry_run: bool) -> int:
    """Strip brace layers AND flatten outlines across masters in one .glyphs save."""
    font = glyphsLib.load(GLYPHS_SOURCE)

    # Identify the 3 main master IDs we care about
    master_ids = [m.id for m in font.masters]  # order: Thin, Regular, ExtraBlack

    strip_count = 0
    flatten_count = 0

    for name, (strip, _, flatten) in BLOCKERS.items():
        g = font.glyphs[name]
        if g is None:
            print(f"warn: {name} not in source", file=sys.stderr)
            continue

        # 1. Strip brace layers
        if strip:
            to_remove = []
            for L in g.layers:
                try:
                    coord = L.attributes.get("coordinates") if hasattr(L, "attributes") and L.attributes else None
                except Exception:
                    coord = None
                if coord:
                    to_remove.append(L)
            if to_remove and not dry_run:
                for L in to_remove:
                    g.layers.remove(L)
            if to_remove:
                strip_count += 1
                print(f"  {name}: stripped {len(to_remove)} brace layer(s)")

        # 2. Flatten outlines — copy Regular master's paths to Thin and ExtraBlack
        if flatten:
            regular_layer = None
            for L in g.layers:
                if L.associatedMasterId == master_ids[1]:  # Regular
                    try:
                        if L.attributes and L.attributes.get("coordinates"):
                            continue
                    except Exception:
                        pass
                    regular_layer = L
                    break
            if regular_layer is None:
                print(f"  warn: {name} has no Regular master layer", file=sys.stderr)
                continue

            # Copy Regular's paths to Thin (master_ids[0]) and ExtraBlack (master_ids[2])
            for target_master_id, target_name in [
                (master_ids[0], "Thin"),
                (master_ids[2], "ExtraBlack"),
            ]:
                target_layer = None
                for L in g.layers:
                    if L.associatedMasterId == target_master_id:
                        try:
                            if L.attributes and L.attributes.get("coordinates"):
                                continue
                        except Exception:
                            pass
                        target_layer = L
                        break
                if target_layer is None:
                    print(f"  warn: {name} has no {target_name} master layer", file=sys.stderr)
                    continue
                if not dry_run:
                    # Deep copy Regular's paths into this layer
                    import copy
                    target_layer.paths = [copy.deepcopy(p) for p in regular_layer.paths]
                    # Also sync components so anchors/references stay aligned
                    target_layer.components = [copy.deepcopy(c) for c in regular_layer.components]
            flatten_count += 1
            print(f"  {name}: flattened Thin + ExtraBlack outlines to match Regular")

    print(f"\nmodify_glyphs_source: stripped braces on {strip_count}, flattened {flatten_count}")

    if dry_run or (strip_count == 0 and flatten_count == 0):
        return 0

    backup = GLYPHS_SOURCE.with_suffix(GLYPHS_SOURCE.suffix + ".bak")
    shutil.copy2(GLYPHS_SOURCE, backup)
    font.save(GLYPHS_SOURCE)
    print(f"  wrote {GLYPHS_SOURCE.name} (backup: {backup.name})")
    return 0


def force_reference_fallback(dry_run: bool) -> int:
    with TRIAGE_MANIFEST.open() as f:
        triage = json.load(f)
    roman = triage.setdefault("roman", {}).setdefault("glyphs", {})

    changes = []
    for name, (_, force, _) in BLOCKERS.items():
        if not force:
            continue
        prev = roman.get(name, {}).get("strategy")
        if prev == "reference_fallback":
            continue
        changes.append((name, prev))
        roman.setdefault(name, {})
        roman[name]["strategy"] = "reference_fallback"
        roman[name]["priority"] = "blocker"
        existing_notes = roman[name].get("notes", "")
        tag = "[isolate_blockers] cu2qu incompatibility; frozen to reference outline to unblock build"
        roman[name]["notes"] = f"{existing_notes}\n\n{tag}".strip() if existing_notes else tag
        # Drop any brace_weights that would re-introduce intermediate layers
        roman[name].pop("brace_weights", None)

    print(f"force_reference_fallback: {len(changes)} glyphs")
    for name, prev in changes:
        print(f"  {name}: {prev or '(new)'} → reference_fallback")

    if dry_run or not changes:
        return 0

    backup = TRIAGE_MANIFEST.with_suffix(".json.bak.isolate")
    shutil.copy2(TRIAGE_MANIFEST, backup)
    with TRIAGE_MANIFEST.open("w", encoding="utf-8") as f:
        json.dump(triage, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  wrote {TRIAGE_MANIFEST.name} (backup: {backup.name})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    rc1 = modify_glyphs_source(args.dry_run)
    rc2 = force_reference_fallback(args.dry_run)
    return max(rc1, rc2)


if __name__ == "__main__":
    sys.exit(main())
