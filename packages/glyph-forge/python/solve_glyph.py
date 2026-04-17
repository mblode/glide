"""Automated strategy solver.

For each candidate strategy, simulate what the rendered glyph would look like at each
of the 8 target weights under that strategy, then score the simulation against the
donor at that weight. The best strategy is the one with the highest *worst-case*
projected void score (minimax), because what kills variable interpolation is a
single weight where the shape collapses — not the average.

Simulations are raster-space:

- **donor_copy**: proposed raster at master weights = donor itself (perfect). At
  in-between weights, proposed = alpha-blend of the bracketing donor masters. Score
  against donor at target weight — captures the "raster interpolation vs designer
  intent" gap, which is the real failure mode once we adopt donor outlines.

- **reference_fallback**: freeze a single reference master (Regular by default) and
  use it unchanged for every weight. Penalises extreme weights since the reference
  won't match at Thin or ExtraBlack.

- **weighted_fallback**: blend current glide raster toward the donor at the same
  weight with coefficient α. Captures "nudge the interpolation", not a full rewrite.
  We search α ∈ {0.3, 0.5, 0.7} and keep the best alpha per glyph.

No irregularity or drift in projections: raster-space sim has no access to vector
curve ops, and interpreting those metrics on synthetic rasters would be misleading.
Void alone is the right signal for "will this fix it?".
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Literal

import numpy as np
from fontTools.pens.recordingPen import RecordingPen

from render_glyph import _donor_font, _instanced_glide
from score_glyph import _raster, _record_ops
from shared import (
    CIRCULAR_WEIGHTS,
    MANIFEST_PATH,
    PACKAGE_ROOT,
    circular_otf,
    glide_vf,
    resolve_glyph_name,
)

# Glide master weights (not to be confused with Circular donor weights)
GLIDE_MASTER_WGHTS = (100, 400, 950)
# Bracket each target weight by the two Glide masters we interpolate between
TARGET_WGHTS = tuple(w.wght for w in CIRCULAR_WEIGHTS)

SOLVER_RESULTS_PATH = PACKAGE_ROOT / "manifests" / "solver-results.json"

CandidateName = Literal["donor_copy", "reference_fallback", "weighted_fallback"]


@dataclass
class CandidateProjection:
    strategy: CandidateName
    projectedWorst: float  # min void across weights
    projectedAvg: float
    worstWght: int | None
    perWeight: dict[int, float]
    params: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["perWeight"] = {str(k): round(v, 4) for k, v in d["perWeight"].items()}
        d["projectedWorst"] = round(d["projectedWorst"], 4)
        d["projectedAvg"] = round(d["projectedAvg"], 4)
        return d


@dataclass
class SolverVerdict:
    family: str
    glyph: str
    currentWorst: float | None
    currentWorstWght: int | None
    best: CandidateName | None
    bestProjected: float | None
    bestWorstWght: int | None
    gain: float | None  # best - current
    candidates: list[CandidateProjection]

    def to_dict(self) -> dict:
        return {
            "family": self.family,
            "glyph": self.glyph,
            "currentWorst": (
                round(self.currentWorst, 4) if self.currentWorst is not None else None
            ),
            "currentWorstWght": self.currentWorstWght,
            "best": self.best,
            "bestProjected": (
                round(self.bestProjected, 4)
                if self.bestProjected is not None
                else None
            ),
            "bestWorstWght": self.bestWorstWght,
            "gain": round(self.gain, 4) if self.gain is not None else None,
            "candidates": [c.to_dict() for c in self.candidates],
        }


@lru_cache(maxsize=4096)
def _donor_raster(family: str, glyph: str, wght: int) -> np.ndarray | None:
    weight_name = next((w.name for w in CIRCULAR_WEIGHTS if w.wght == wght), None)
    if weight_name is None:
        return None
    font = _donor_font(family, wght)
    name = resolve_glyph_name(glyph, circular_otf(family, weight_name))
    if name is None:
        return None
    ops = _record_ops(font, name)
    if ops is None:
        return None
    return _raster(ops, font)


@lru_cache(maxsize=4096)
def _glide_raster(family: str, glyph: str, wght: int) -> np.ndarray | None:
    font = _instanced_glide(family, wght)
    name = resolve_glyph_name(glyph, glide_vf(family))
    if name is None:
        return None
    ops = _record_ops(font, name)
    if ops is None:
        return None
    return _raster(ops, font)


def _void_against(proposed: np.ndarray, target: np.ndarray) -> float:
    t_area = target.sum()
    if t_area == 0:
        return 0.0 if proposed.sum() > 0 else 1.0
    diff = np.logical_xor(proposed, target).sum()
    return float(max(0.0, 1.0 - diff / t_area))


def _bracket(target: int, anchors: tuple[int, ...]) -> tuple[int, int, float]:
    """Return (lo, hi, t) where target = lo + t*(hi-lo)."""
    sorted_a = sorted(anchors)
    if target <= sorted_a[0]:
        return sorted_a[0], sorted_a[0], 0.0
    if target >= sorted_a[-1]:
        return sorted_a[-1], sorted_a[-1], 0.0
    for i in range(len(sorted_a) - 1):
        if sorted_a[i] <= target <= sorted_a[i + 1]:
            lo, hi = sorted_a[i], sorted_a[i + 1]
            t = (target - lo) / (hi - lo) if hi > lo else 0.0
            return lo, hi, t
    return sorted_a[0], sorted_a[-1], 0.0


def _raster_blend(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Alpha-blend two binary masks. Threshold at 0.5 to get a binary mask back."""
    blended = (1.0 - t) * a.astype(np.float32) + t * b.astype(np.float32)
    return blended > 0.5


# Use the donor's three Thin-equivalent, Regular, ExtraBlack weights as the
# synthetic "glide masters" we'd get from donor_copy. These are the two anchors
# closest to Glide's 100 / 400 / 950: Circular has Thin 250, Regular 400, ExtraBlack 950.
DONOR_MASTER_WGHTS = (250, 400, 950)


def simulate_donor_copy(family: str, glyph: str) -> CandidateProjection | None:
    """Simulate a glide rebuilt from donor masters. Use donor at 250/400/950 as our
    master anchors; blend between them in raster-space for every target weight."""
    # Preload anchor rasters
    anchors: dict[int, np.ndarray] = {}
    for w in DONOR_MASTER_WGHTS:
        r = _donor_raster(family, glyph, w)
        if r is None:
            return None
        anchors[w] = r

    per_weight: dict[int, float] = {}
    for target in TARGET_WGHTS:
        target_raster = _donor_raster(family, glyph, target)
        if target_raster is None:
            continue
        if target in anchors:
            proposed = anchors[target]
        else:
            lo, hi, t = _bracket(target, DONOR_MASTER_WGHTS)
            if lo == hi:
                proposed = anchors[lo]
            else:
                proposed = _raster_blend(anchors[lo], anchors[hi], t)
        per_weight[target] = _void_against(proposed, target_raster)

    if not per_weight:
        return None
    worst = min(per_weight.values())
    worst_wght = min(per_weight.items(), key=lambda kv: kv[1])[0]
    avg = sum(per_weight.values()) / len(per_weight)
    return CandidateProjection(
        strategy="donor_copy",
        projectedWorst=worst,
        projectedAvg=avg,
        worstWght=worst_wght,
        perWeight=per_weight,
    )


def simulate_reference_fallback(
    family: str, glyph: str
) -> CandidateProjection | None:
    """Freeze the *current* Glide Regular (wght 400) master as all three masters —
    produces a static glyph whose rendered shape is identical at every weight.

    Validation is independent: the simulated raster (glide@400) is scored against
    the donor designed for the target weight, which of course diverges at the
    extremes. This captures reference_fallback's real trade-off: safe at Regular,
    visibly wrong at Thin and ExtraBlack."""
    ref = _glide_raster(family, glyph, 400)
    if ref is None:
        return None

    per_weight: dict[int, float] = {}
    for target in TARGET_WGHTS:
        target_raster = _donor_raster(family, glyph, target)
        if target_raster is None:
            continue
        per_weight[target] = _void_against(ref, target_raster)

    if not per_weight:
        return None
    worst = min(per_weight.values())
    worst_wght = min(per_weight.items(), key=lambda kv: kv[1])[0]
    avg = sum(per_weight.values()) / len(per_weight)
    return CandidateProjection(
        strategy="reference_fallback",
        projectedWorst=worst,
        projectedAvg=avg,
        worstWght=worst_wght,
        perWeight=per_weight,
        params={"referenceWght": 400.0},
    )


def simulate_weighted_fallback(
    family: str, glyph: str, alphas: tuple[float, ...] = (0.3, 0.5, 0.7)
) -> CandidateProjection | None:
    """Nudge *each Glide master outline* toward the matching-weight donor master,
    then interpolate the nudged masters in raster space for target weights.

    This is independent of the validation target (donor at target weight). At
    target weights that coincide with Glide master weights (400), the nudged
    master is directly scored. At in-between targets, the bracketing nudged
    masters are raster-blended.

    Glide masters are at wght 100 / 400 / 950. The nearest donor anchors are
    Thin 250 / Regular 400 / ExtraBlack 950 — those are the nudge targets."""
    # Glide master raster at each glide-axis weight
    glide_masters = {
        100: _glide_raster(family, glyph, 250),  # nearest donor below 100 doesn't exist;
        # use the donor's Thin (250) as the proxy reference for "thin end"
        400: _glide_raster(family, glyph, 400),
        950: _glide_raster(family, glyph, 950),
    }
    # Donor anchors used as nudge targets for each Glide master
    donor_anchors = {
        100: _donor_raster(family, glyph, 250),
        400: _donor_raster(family, glyph, 400),
        950: _donor_raster(family, glyph, 950),
    }
    if any(v is None for v in glide_masters.values()) or any(
        v is None for v in donor_anchors.values()
    ):
        return None

    best: CandidateProjection | None = None
    for a in alphas:
        # Nudge each master toward its donor anchor
        nudged = {
            w: _raster_blend(glide_masters[w], donor_anchors[w], a)
            for w in glide_masters
        }

        per_weight: dict[int, float] = {}
        for target in TARGET_WGHTS:
            donor_at_target = _donor_raster(family, glyph, target)
            if donor_at_target is None:
                continue
            # Interpolate between Glide master weights (100, 400, 950) to reach target
            lo, hi, t = _bracket(target, (100, 400, 950))
            if lo == hi:
                proposed = nudged[lo]
            else:
                proposed = _raster_blend(nudged[lo], nudged[hi], t)
            per_weight[target] = _void_against(proposed, donor_at_target)

        if not per_weight:
            continue
        worst = min(per_weight.values())
        worst_wght = min(per_weight.items(), key=lambda kv: kv[1])[0]
        avg = sum(per_weight.values()) / len(per_weight)
        candidate = CandidateProjection(
            strategy="weighted_fallback",
            projectedWorst=worst,
            projectedAvg=avg,
            worstWght=worst_wght,
            perWeight=per_weight,
            params={"alpha": a},
        )
        if best is None or candidate.projectedWorst > best.projectedWorst:
            best = candidate
    return best


def solve(family: str, glyph: str, current: dict | None) -> SolverVerdict:
    """Run all candidates, pick the best by projected worst-case, compute gain."""
    candidates: list[CandidateProjection] = []
    for sim in (
        simulate_donor_copy,
        simulate_reference_fallback,
        simulate_weighted_fallback,
    ):
        c = sim(family, glyph)
        if c is not None:
            candidates.append(c)

    current_worst = None
    current_worst_wght = None
    if current:
        cw = current.get("worstComposite")
        current_worst = cw if isinstance(cw, (int, float)) else None
        current_worst_wght = current.get("worstWght")

    if candidates:
        winner = max(candidates, key=lambda c: c.projectedWorst)
        gain = (
            winner.projectedWorst - current_worst
            if current_worst is not None
            else None
        )
        return SolverVerdict(
            family=family,
            glyph=glyph,
            currentWorst=current_worst,
            currentWorstWght=current_worst_wght,
            best=winner.strategy,
            bestProjected=winner.projectedWorst,
            bestWorstWght=winner.worstWght,
            gain=gain,
            candidates=candidates,
        )
    return SolverVerdict(
        family=family,
        glyph=glyph,
        currentWorst=current_worst,
        currentWorstWght=current_worst_wght,
        best=None,
        bestProjected=None,
        bestWorstWght=None,
        gain=None,
        candidates=[],
    )


def build(limit: int | None, only_seed: bool) -> int:
    if not MANIFEST_PATH.exists():
        print("error: run ingest first", file=sys.stderr)
        return 1
    with MANIFEST_PATH.open() as f:
        glyphs = json.load(f)
    glyph_scores_path = PACKAGE_ROOT / "manifests" / "glyph-scores.json"
    current_scores: dict = {}
    if glyph_scores_path.exists():
        with glyph_scores_path.open() as f:
            current_scores = json.load(f)

    if only_seed:
        glyphs = [g for g in glyphs if "user_seed" in g["sources"]]
    if limit:
        glyphs = glyphs[:limit]

    results: dict[str, dict] = {}
    start = time.monotonic()
    improvements = 0

    for i, entry in enumerate(glyphs):
        family, name = entry["family"], entry["name"]
        key = f"{family}/{name}"
        current = current_scores.get(key)
        verdict = solve(family, name, current)
        results[key] = verdict.to_dict()
        if (
            verdict.gain is not None
            and verdict.gain > 0.1
        ):
            improvements += 1
        if (i + 1) % 50 == 0:
            el = time.monotonic() - start
            print(
                f"  {i + 1}/{len(glyphs)} solved, {improvements} with gain > 0.1 "
                f"({el:.1f}s)",
                file=sys.stderr,
            )

    SOLVER_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SOLVER_RESULTS_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=0, ensure_ascii=False)

    elapsed = time.monotonic() - start
    print(
        f"done: {len(results)} glyphs solved, {improvements} with projected gain > 0.1 "
        f"in {elapsed:.1f}s"
    )
    print(f"wrote {SOLVER_RESULTS_PATH.relative_to(PACKAGE_ROOT.parent)}")
    # summary by winning strategy
    winners: dict[str, int] = {}
    for v in results.values():
        b = v["best"] or "none"
        winners[b] = winners.get(b, 0) + 1
    print("winners:", winners)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only-seed", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    return build(limit=args.limit, only_seed=args.only_seed)


if __name__ == "__main__":
    sys.exit(main())
