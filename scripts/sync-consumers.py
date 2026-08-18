#!/usr/bin/env python3
"""Roll the canonical Glide binaries out to every consumer repo.

The files in ``fonts/``, ``fonts/static/`` and ``apps/web/lib/og-assets/`` are
the only sources of truth. Dozens of sibling repos vendor copies of them under
their own names. This script finds those copies by exact filename, compares
SHA-256, and replaces the stale ones. It never creates a file that a consumer
does not already have, and it never commits.

    python3 scripts/sync-consumers.py              # dry run, changes nothing
    python3 scripts/sync-consumers.py --apply      # write the stale copies
    python3 scripts/sync-consumers.py --verify     # exit non-zero on drift

Consumers are enumerated with ``git ls-files``, not a directory walk. That is
deliberate: mblode/burger tracks ``dist/`` on purpose (it is what npm and the
CDN serve), so a blanket "skip dist" rule would leave it permanently stale,
while every genuinely generated tree is gitignored and drops out for free.

Four failure modes here are silent, so each one gets an explicit check:

1. Tracked build output. Handled by the ``git ls-files`` rule above. Repos in
   POST_SYNC still need a build step afterwards to regenerate the rest of the
   tree, and their version labels are checked against apps/web/lib/config.ts.
2. Subsetted faces. Some repos ship a subset on the LCP path and keep the full
   face beside it as the source. Copying a canonical face over the subset puts
   the stripped bytes back on the critical path and nothing complains. The
   subset output directories in SUBSET_REPOS are never written; they are
   verified by font revision instead and reported for manual regeneration. A
   repo that subsets but is missing from that table is a hard failure.
3. Variable OG fonts. Satori cannot render a variable font, so OG assets are
   instanced to a fixed weight. Glide 4.0 added an ``opsz`` axis, so an
   instancing script that pins only ``wght`` leaves an fvar table behind and
   breaks OG rendering. Every og-assets TTF is checked for fvar.
4. Core Text registration on iOS. Done Bear's GlideFont.register() does
   ``guard let url = Bundle.main.url(...) else { continue }``, so a static whose
   filename or PostScript name drifts from the Swift `faces` array is not an
   error, it is a skipped iteration and a silent fall back to SF Pro. The face
   list is parsed out of the Swift and checked against both the bundled files
   and the name table of the canonical statics.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct
import subprocess
import sys


REPO = Path(__file__).resolve().parent.parent
CODE = REPO.parent.parent
CONFIG = REPO / "apps" / "web" / "lib" / "config.ts"

SCAN_ROOTS = (CODE / "mblode", CODE / "donebear")

# Directory names that never contain a consumer copy worth syncing. Build
# output is not listed: git tracking already decides that, and burger tracks
# dist/ deliberately.
PRUNE_NAMES = frozenset(
    {
        "node_modules",
        ".git",
        ".next",
        ".turbo",
        ".output",
        ".vercel",
        "worktrees",
        ".codex-worktrees",
    }
)
PRUNE_PATHS = ("donebear/pr-slices",)
# The pipeline repos and this one are sources, not consumers. Each is listed in
# full: prefix matching is anchored on a path separator, so
# "mblode/static-to-variable" does NOT cover "mblode/static-to-variable-glide".
# Leaving the latter off makes the sync try to overwrite the frozen 3.002
# baseline and the hash-pinned build/glide artifacts the Glide 4 contract
# depends on.
SOURCE_REPOS = (
    "mblode/glide",
    "mblode/static-to-variable",
    "mblode/static-to-variable-glide",
)

# Defence in depth: these never receive a sync no matter which repo they are in.
# A frozen baseline or a pinned build artifact is an input to a release contract,
# not a vendored copy of the font.
NEVER_WRITE = ("baseline-snapshot/", "build/glide/", "build/glide-4")

VARIABLE_NAMES = (
    "glide-variable.woff2",
    "glide-variable-italic.woff2",
    "glide-mono.woff2",
    "glide-variable.ttf",
    "glide-variable-italic.ttf",
    "glide-mono.ttf",
)
OG_NAMES = (
    "glide-400.ttf",
    "glide-600.ttf",
    "glide-italic-500.ttf",
    "glide-mono-400.ttf",
)

# Repos that ship a subset of a Glide face and keep the full face as its
# source. `out` is never written by this script; `src` is synced normally and
# `cmd` regenerates `out` from it afterwards.
SUBSET_REPOS = {
    "mblode/rubber-duck": {
        "src": "apps/web/assets/fonts",
        "out": "apps/web/app/fonts",
        "cmd": "node apps/web/scripts/subset-fonts.mjs",
    },
    "mblode/commandment": {
        "src": "apps/web/assets/fonts",
        "out": "apps/web/app/fonts",
        "cmd": "node apps/web/scripts/subset-fonts.mjs",
    },
    "mblode/convene": {
        "src": "apps/web/assets/fonts",
        "out": "apps/web/app/fonts",
        "cmd": "node apps/web/scripts/subset-fonts.mjs",
    },
    "mblode/taste-training": {
        "src": "apps/web/fonts",
        "out": "apps/web/app/fonts",
        "cmd": "apps/web/scripts/subset-fonts.sh",
    },
    "donebear/donebear": {
        "src": "apps/marketing-frontend/assets/fonts",
        "out": "apps/marketing-frontend/app/fonts",
        "cmd": "cd apps/marketing-frontend && node scripts/subset-fonts.mjs",
    },
}
SUBSET_SCRIPT = re.compile(r"(^|/)subset-fonts\.(mjs|js|sh|py)$")
# pyftsubset lives here on this machine and is not on the default PATH.
PYFTSUBSET_HINT = "~/Library/Python/3.9/bin"

# Repos that register the static faces with Core Text at launch. The Swift
# array holds both the bundle resource name and the PostScript name, and
# `guard let url ... else { continue }` swallows a filename miss, so a renamed
# static silently drops the app back to SF Pro with nothing logged.
IOS_REGISTRARS = {
    "donebear/donebear": {
        "swift": "apps/ios/Done Bear/DesignSystem/Tokens/GlideFont.swift",
        "fonts": "apps/ios/Done Bear/Resources/Fonts",
    },
}
IOS_FACES = re.compile(r"let faces = \[(.*?)\]", re.DOTALL)

# Repos whose tracked build output only refreshes when a build step runs, and
# the file carrying a human-readable Glide version that must be edited *before*
# that build (the build copies it verbatim).
POST_SYNC = {
    "mblode/burger": {
        "cmd": "npm run build:assets",
        "labels": ("src/index.html", "dist/index.html"),
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sources() -> dict[str, Path]:
    """Map consumer filename -> canonical path in this repo."""
    sources: dict[str, Path] = {}
    for name in VARIABLE_NAMES:
        sources[name] = REPO / "fonts" / name
    for name in OG_NAMES:
        sources[name] = REPO / "apps" / "web" / "lib" / "og-assets" / name
    for path in sorted((REPO / "fonts" / "static").glob("Glide*.ttf")):
        sources[path.name] = path
    missing = [name for name, path in sources.items() if not path.is_file()]
    if missing:
        raise AssertionError("canonical source missing: " + ", ".join(sorted(missing)))
    return sources


def consumer_key(name: str) -> str:
    """Consumer filename -> canonical filename.

    taste-training keeps its unsubsetted sources as ``glide-variable.full.woff2``
    so the served name stays free for the subset.
    """
    return name.replace(".full.", ".", 1)


def glide_version() -> str | None:
    match = re.search(r'version:\s*"([^"]+)"', CONFIG.read_text())
    return match.group(1) if match else None


def find_repos() -> list[Path]:
    """Every git repo under the scan roots, minus the sources and the noise."""
    repos: list[Path] = []
    stack = [root for root in SCAN_ROOTS if root.is_dir()]
    while stack:
        current = stack.pop()
        relative = current.relative_to(CODE).as_posix()
        if any(relative == path or relative.startswith(f"{path}/") for path in PRUNE_PATHS):
            continue
        if (current / ".git").exists():
            if not any(
                relative == repo or relative.startswith(f"{repo}/") for repo in SOURCE_REPOS
            ):
                repos.append(current)
            # A repo's own worktrees and vendored checkouts are not consumers.
            continue
        for child in current.iterdir():
            if child.is_dir() and not child.is_symlink() and child.name not in PRUNE_NAMES:
                stack.append(child)
    return sorted(repos)


def tracked_files(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"],
        capture_output=True,
        check=True,
    )
    return [
        entry
        for entry in result.stdout.decode().split("\0")
        # Frozen baselines and pinned build artifacts are release-contract
        # inputs, not vendored copies. They are filtered here, at the single
        # place file candidates enter, so no later code path can reach them.
        if entry and not entry.startswith(NEVER_WRITE)
    ]


def sfnt_tables(data: bytes) -> set[str]:
    """Table tags of an uncompressed sfnt (TTF/OTF). No fontTools needed."""
    if len(data) < 12:
        return set()
    count = struct.unpack(">H", data[4:6])[0]
    if len(data) < 12 + 16 * count:
        return set()
    return {data[12 + 16 * i : 16 + 16 * i].decode("latin-1") for i in range(count)}


def postscript_name(path: Path) -> str | None:
    """name ID 6. None if fontTools is unavailable or the font is unreadable."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    try:
        with TTFont(str(path), lazy=True) as font:
            return font["name"].getDebugName(6)
    except Exception:
        return None


def font_revision(path: Path) -> float | None:
    """head.fontRevision, which survives subsetting. None if unreadable."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    try:
        with TTFont(str(path), lazy=True) as font:
            return round(float(font["head"].fontRevision), 5)
    except Exception:
        return None


class RepoPlan:
    def __init__(self, repo: Path):
        self.repo = repo
        self.name = repo.relative_to(CODE).as_posix()
        self.current: list[str] = []
        # (path in repo, absolute target, canonical source, old sha, new sha)
        self.stale: list[tuple[str, Path, Path, str, str]] = []
        self.held: list[str] = []
        self.notes: list[str] = []
        self.errors: list[str] = []

    @property
    def touched(self) -> bool:
        return bool(self.stale or self.notes or self.errors)


def plan_repo(repo: Path, sources: dict[str, Path]) -> RepoPlan:
    plan = RepoPlan(repo)
    subset = SUBSET_REPOS.get(plan.name)
    files = tracked_files(repo)

    if any(SUBSET_SCRIPT.search(entry) for entry in files) and subset is None:
        plan.errors.append(
            "has a subset-fonts script but no SUBSET_REPOS entry; syncing it "
            "would overwrite the subset with the full face"
        )

    out_prefix = f"{subset['out']}/" if subset else None
    for entry in files:
        name = entry.rsplit("/", 1)[-1]
        source = sources.get(consumer_key(name))
        if source is None:
            continue
        target = repo / entry
        if out_prefix and entry.startswith(out_prefix):
            plan.held.append(entry)
            continue
        want = source.read_bytes()
        have = target.read_bytes()
        if have == want:
            plan.current.append(entry)
        else:
            plan.stale.append((entry, target, source, sha256(have), sha256(want)))

    plan.errors += check_og_fvar(repo, files)
    plan.errors += check_ios(plan, sources)
    if subset:
        plan.notes += check_subset(plan, subset, sources)
    plan.notes += check_labels(plan)
    return plan


def check_og_fvar(repo: Path, files: list[str]) -> list[str]:
    """Satori cannot render a variable font; an instanced OG asset has no fvar."""
    errors = []
    for entry in files:
        name = entry.rsplit("/", 1)[-1]
        if not name.endswith(".ttf"):
            continue
        if "/og-assets/" not in f"/{entry}" and not name.startswith("og-"):
            continue
        if "fvar" in sfnt_tables((repo / entry).read_bytes()):
            errors.append(f"{entry} still has an fvar table; Satori will throw on it")
    return errors


def check_ios(plan: RepoPlan, sources: dict[str, Path]) -> list[str]:
    """Every face GlideFont.swift asks for must exist, by that exact name.

    Core Text registration takes the resource filename and every call site
    takes the PostScript name from the same string, so both have to agree with
    the shipped binary. A mismatch is not an error at runtime, it is a `continue`.
    """
    registrar = IOS_REGISTRARS.get(plan.name)
    if registrar is None:
        return []
    swift = plan.repo / registrar["swift"]
    if not swift.is_file():
        return [f"{registrar['swift']} is missing; the iOS face list cannot be checked"]
    block = IOS_FACES.search(swift.read_text())
    if block is None:
        return [f"{registrar['swift']} no longer declares a `faces` array to check"]

    errors = []
    for face in re.findall(r'"([^"]+)"', block.group(1)):
        name = f"{face}.ttf"
        bundled = plan.repo / registrar["fonts"] / name
        source = sources.get(name)
        if source is None:
            errors.append(f"{registrar['swift']} wants {name}, which fonts/static/ does not ship")
            continue
        if not bundled.is_file():
            errors.append(
                f"{registrar['fonts']}/{name} is missing; "
                "CTFontManagerRegisterFontsForURL will skip it silently"
            )
            continue
        actual = postscript_name(source)
        if actual is not None and actual != face:
            errors.append(
                f"fonts/static/{name} has PostScript name {actual!r}, but the app "
                f"asks for {face!r}; every Font.glide call site will fall back to SF Pro"
            )
    return errors


def check_subset(plan: RepoPlan, subset: dict, sources: dict[str, Path]) -> list[str]:
    """Compare font revisions, since subset bytes never match the source bytes."""
    notes = []
    unreadable = False
    for entry in plan.held:
        name = entry.rsplit("/", 1)[-1]
        source = sources.get(consumer_key(name))
        if source is None:
            continue
        want = font_revision(source)
        have = font_revision(plan.repo / entry)
        if want is None or have is None:
            unreadable = True
        elif want != have:
            notes.append(f"{entry} is subset from revision {have}, canonical is {want}")
    if unreadable:
        notes.append(
            f"could not read font revisions ({len(plan.held)} subset files unverified) "
            "-- install fontTools and brotli to check them"
        )
    if notes or any(entry.startswith(f"{subset['src']}/") for entry, *_ in plan.stale):
        notes.append(f"regenerate the subset: {subset['cmd']} (pyftsubset: {PYFTSUBSET_HINT})")
    return notes


def check_labels(plan: RepoPlan) -> list[str]:
    """Tracked build output needs a build, and its version label needs editing first."""
    post = POST_SYNC.get(plan.name)
    if post is None:
        return []
    notes = []
    version = glide_version()
    for label in post["labels"]:
        path = plan.repo / label
        if not path.is_file():
            continue
        found = set(re.findall(r"Glide (\d+\.\d+\.\d+)", path.read_text()))
        if version and found and version not in found:
            notes.append(f"{label} still says Glide {', '.join(sorted(found))}, not {version}")
    notes.append(
        f"tracked build output: edit the version label first, then run {post['cmd']!r} "
        "(it copies src/index.html verbatim)"
    )
    return notes


def report(plans: list[RepoPlan], apply: bool) -> None:
    for plan in plans:
        if not plan.touched:
            continue
        print(f"\n{plan.name}")
        for entry, _, _, old, new in plan.stale:
            verb = "wrote " if apply else "update"
            print(f"  {verb} {entry}  {old[:12]} -> {new[:12]}")
        for note in plan.notes:
            print(f"  warn   {note}")
        for error in plan.errors:
            print(f"  FAIL   {error}")
        if plan.current:
            print(f"  ok     {len(plan.current)} already current")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write the stale copies")
    mode.add_argument(
        "--verify",
        action="store_true",
        help="check for drift only; exits non-zero if any consumer is stale",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="the default: report what would change and write nothing",
    )
    args = parser.parse_args()

    try:
        sources = canonical_sources()
    except AssertionError as error:
        print(f"FAIL {error}")
        return 1

    repos = find_repos()
    plans = [plan_repo(repo, sources) for repo in repos]

    if args.apply:
        for plan in plans:
            # Skip a repo that failed a check. Its errors describe exactly the
            # damage a blind copy would do -- overwriting a subset with the full
            # face, for one -- so writing first and reporting afterwards means
            # the FAIL prints after the harm is already done.
            if plan.errors:
                continue
            for _, target, source, _old, _new in plan.stale:
                target.write_bytes(source.read_bytes())

    report(plans, args.apply)

    stale = sum(len(plan.stale) for plan in plans)
    current = sum(len(plan.current) for plan in plans)
    held = sum(len(plan.held) for plan in plans)
    errors = [f"{plan.name}: {error}" for plan in plans for error in plan.errors]
    attention = [plan for plan in plans if plan.notes]

    print()
    print(f"ok   {len(repos)} repos scanned, {len(sources)} canonical files")
    print(f"ok   {current} consumer files already current")
    print(f"ok   {held} subset outputs held back (never overwritten)")
    if args.apply:
        print(f"ok   {stale} files replaced -- re-run to confirm it converges to zero")
    elif stale:
        print(f"FAIL {stale} consumer files are stale -- re-run with --apply")
    else:
        print("ok   0 consumer files are stale")

    if attention:
        print("\nneeds a human:")
        for plan in attention:
            print(f"  {plan.name}")
            for note in plan.notes:
                print(f"    - {note}")

    if errors:
        print()
        for error in errors:
            print(f"FAIL {error}")
        return 1
    if args.verify and stale:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
