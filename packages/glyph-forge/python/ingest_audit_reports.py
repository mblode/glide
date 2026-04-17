"""Build manifests/broken-glyphs.json from variable-gen reports + user seed lists.

Output is the union of three origins so nothing gets dropped:
  1. variable-gen audit JSON (severity-scored)
  2. Hardcoded ITALIC_SEED / ROMAN_SEED from shared.py (user-flagged)
  3. circular-triage.json (existing repair strategies)
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from shared import (
    ITALIC_SEED,
    MANIFEST_PATH,
    ROMAN_SEED,
    TRIAGE_MANIFEST,
    VARIABLE_GEN_REPORTS,
    Family,
    feature_tags,
    glide_vf,
    glyph_unicode,
    resolve_glyph_name,
)

AUDIT_JSON = {
    "roman": VARIABLE_GEN_REPORTS / "audit" / "roman" / "roman-variable-audit.json",
    "italic": VARIABLE_GEN_REPORTS / "audit" / "italic" / "italic-variable-audit.json",
}


@dataclass
class BrokenGlyph:
    name: str
    family: Family
    features: list[str]
    sources: list[str]
    auditVerdict: str
    unicode: str | None = None
    severityScore: int | None = None
    existingStrategy: str | None = None
    priority: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Keep required fields (name, family, features, sources, auditVerdict) even
        # when empty; drop optional fields when unset so the JSON is compact.
        required = {"name", "family", "features", "sources", "auditVerdict"}
        return {k: v for k, v in d.items() if k in required or v not in (None, [], "")}


@dataclass
class Accumulator:
    by_name: dict[str, BrokenGlyph] = field(default_factory=dict)

    def upsert(self, glyph: BrokenGlyph) -> None:
        existing = self.by_name.get(glyph.name)
        if existing is None:
            self.by_name[glyph.name] = glyph
            return
        # Merge sources.
        for src in glyph.sources:
            if src not in existing.sources:
                existing.sources.append(src)
        # Fill gaps — don't overwrite existing truthy fields.
        for attr in (
            "unicode",
            "severityScore",
            "existingStrategy",
            "priority",
            "notes",
        ):
            if getattr(existing, attr) in (None, "") and getattr(glyph, attr):
                setattr(existing, attr, getattr(glyph, attr))
        # Take the more severe verdict.
        existing.auditVerdict = _more_severe(existing.auditVerdict, glyph.auditVerdict)


VERDICT_ORDER = ["unknown", "low", "medium", "high", "blocker", "tracked"]


def _more_severe(a: str, b: str) -> str:
    return max(a, b, key=lambda v: VERDICT_ORDER.index(v) if v in VERDICT_ORDER else -1)


def severity_to_verdict(score: int | None) -> str:
    if score is None or score <= 0:
        return "unknown"
    if score < 50:
        return "low"
    if score < 200:
        return "medium"
    if score < 500:
        return "high"
    return "blocker"


def load_triage() -> dict[str, dict[str, dict[str, Any]]]:
    if not TRIAGE_MANIFEST.exists():
        return {"roman": {}, "italic": {}}
    with TRIAGE_MANIFEST.open() as f:
        raw = json.load(f)
    return {
        "roman": raw.get("roman", {}).get("glyphs", {}),
        "italic": raw.get("italic", {}).get("glyphs", {}),
    }


def load_audit_summary(family: Family) -> dict[str, int]:
    path = AUDIT_JSON[family]
    if not path.exists():
        print(f"warn: audit report missing at {path}", file=sys.stderr)
        return {}
    with path.open() as f:
        data = json.load(f)
    summary = data.get("glyph_issue_summary", {})
    return {
        name: entry.get("severity_score", 0)
        for name, entry in summary.items()
        if entry.get("severity_score", 0) > 0
    }


def ingest_family(family: Family, seed: tuple[str, ...], triage: dict[str, Any]) -> list[BrokenGlyph]:
    acc = Accumulator()
    font_path = glide_vf(family)

    # 1. Audit report — severity-ranked.
    audit = load_audit_summary(family)
    for name, score in audit.items():
        resolved = resolve_glyph_name(name, font_path)
        if resolved is None:
            continue
        acc.upsert(
            BrokenGlyph(
                name=resolved,
                family=family,
                features=feature_tags(resolved),
                sources=["audit"],
                auditVerdict=severity_to_verdict(score),
                severityScore=score,
                unicode=glyph_unicode(resolved, font_path),
            )
        )

    # 2. User seed list — guaranteed to be included.
    for raw in seed:
        resolved = resolve_glyph_name(raw, font_path)
        if resolved is None:
            print(f"warn: seed glyph {raw!r} not found in {family} font", file=sys.stderr)
            continue
        acc.upsert(
            BrokenGlyph(
                name=resolved,
                family=family,
                features=feature_tags(resolved),
                sources=["user_seed"],
                auditVerdict="unknown",
                unicode=glyph_unicode(resolved, font_path),
            )
        )

    # 3. Triage manifest — overlay strategy + notes + priority.
    for name, cfg in triage.items():
        resolved = resolve_glyph_name(name, font_path) or name
        if resolved not in acc.by_name:
            # If triage has a glyph not in audit or seed, still include it if it exists.
            real = resolve_glyph_name(name, font_path)
            if real is None:
                continue
            acc.upsert(
                BrokenGlyph(
                    name=real,
                    family=family,
                    features=feature_tags(real),
                    sources=["audit"],  # triage implies an audit-tracked glyph
                    auditVerdict="tracked",
                    unicode=glyph_unicode(real, font_path),
                )
            )
        entry = acc.by_name[resolved]
        entry.existingStrategy = cfg.get("strategy")
        entry.priority = cfg.get("priority")
        note = cfg.get("notes")
        if note:
            entry.notes = note

    return sorted(acc.by_name.values(), key=lambda g: (g.family, g.name))


def main() -> int:
    triage = load_triage()
    glyphs: list[BrokenGlyph] = []
    glyphs.extend(ingest_family("italic", ITALIC_SEED, triage["italic"]))
    glyphs.extend(ingest_family("roman", ROMAN_SEED, triage["roman"]))

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        json.dump([g.to_dict() for g in glyphs], f, indent=2, ensure_ascii=False)

    by_family: dict[str, int] = {}
    by_verdict: dict[str, int] = {}
    for g in glyphs:
        by_family[g.family] = by_family.get(g.family, 0) + 1
        by_verdict[g.auditVerdict] = by_verdict.get(g.auditVerdict, 0) + 1

    print(f"wrote {MANIFEST_PATH.relative_to(MANIFEST_PATH.parents[2])}: {len(glyphs)} glyphs")
    print(f"  by family: {by_family}")
    print(f"  by verdict: {by_verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
