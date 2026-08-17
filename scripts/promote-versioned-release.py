#!/usr/bin/env python3
"""Transactionally promote a contracted immutable Glide 4 release to aliases."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "4.0.0"
ROOT_FILES = (
    "glide-variable.ttf",
    "glide-variable-italic.ttf",
    "glide-variable.woff2",
    "glide-variable-italic.woff2",
    "glide-4.0.0.zip",
)
MANIFEST = "release-manifest.json"
WEIGHTS = (
    "Thin",
    "ExtraLight",
    "Light",
    "Regular",
    "Medium",
    "SemiBold",
    "Bold",
    "ExtraBold",
    "Black",
    "ExtraBlack",
)
EXPECTED = {
    *ROOT_FILES,
    *(f"static/Glide-{weight}.ttf" for weight in WEIGHTS),
    *(f"static/Glide-{weight}Italic.ttf" for weight in WEIGHTS),
}
AUTHORITY = {
    "path": "reports/glide-4-authority/glide-4-six-master-authority-80851dd48adef143.json",
    "sha256": "80851dd48adef14314a26663d3b4918b1d3e91dcc99a910437713f37af53aff2",
}
DEFAULT_CONTRACT = {
    "schemaVersion": 1,
    "kind": "glide-public-promotion",
    "semanticVersion": VERSION,
    "fontRevision": "4.000",
    "authority": AUTHORITY,
    "protectedTrees": {},
}
SUPPORTED_RELEASES = {"4.0.0": "4.000", "4.0.1": "4.001"}
HEX = set("0123456789abcdef")
JOURNAL = ".glide-promotion-journal"


def _canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _confined(relative: str, label: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"{label} is not a confined relative path")
    return path


def _digest(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or set(value) - HEX:
        raise ValueError(f"{label} has invalid SHA-256")
    return value


def _load_contract(path: Path | None) -> dict[str, object]:
    if path is None:
        return DEFAULT_CONTRACT
    expected_root = ROOT / "release-contracts"
    if path.is_symlink() or not path.is_file() or path.parent.resolve() != expected_root.resolve():
        raise ValueError("promotion contract is missing, unsafe, or outside release-contracts")
    contract = json.loads(path.read_text(encoding="utf-8"))
    version = contract.get("semanticVersion")
    revision = SUPPORTED_RELEASES.get(version)
    if (
        contract.get("schemaVersion") != 1
        or contract.get("kind") != "glide-public-promotion"
        or revision is None
        or contract.get("fontRevision") != revision
        or path.name != f"glide-{version}.json"
    ):
        raise ValueError("promotion contract has the wrong release identity")
    authority = contract.get("authority", {})
    if not isinstance(authority, dict):
        raise ValueError("promotion contract has no authority binding")
    _confined(str(authority.get("path", "")), "authority path")
    _digest(authority.get("sha256"), "authority manifest")
    protected = contract.get("protectedTrees")
    required = {
        "apps/web/public/3.1.0",
        "apps/web/public/3.002",
        "apps/web/public/4.0.0",
    }
    if version == "4.0.1" and set(protected or {}) != required:
        raise ValueError("4.0.1 promotion must protect 3.1.0, 3.002, and 4.0.0")
    if not isinstance(protected, dict):
        raise ValueError("promotion contract protectedTrees must be an object")
    for relative, digest in protected.items():
        _confined(relative, "protected tree")
        _digest(digest, f"protected tree {relative}")
    return contract


def _write_journal(path: Path, phase: str) -> None:
    with path.open("w", encoding="utf-8") as stream:
        stream.write(phase + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    _sync_dir(path.parent)


def _sync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _replace(source: Path, target: Path) -> None:
    os.replace(source, target)
    _sync_dir(source.parent)
    if target.parent != source.parent:
        _sync_dir(target.parent)


def _recover(
    public: Path, fonts: Path, public_backup: Path, fonts_backup: Path, journal: Path
) -> None:
    if not journal.exists():
        return
    phase = journal.read_text(encoding="utf-8").strip()
    if phase == "committed":
        shutil.rmtree(public_backup, ignore_errors=True)
        shutil.rmtree(fonts_backup, ignore_errors=True)
        if public_backup.exists() or fonts_backup.exists():
            return
    else:
        if fonts_backup.exists():
            shutil.rmtree(fonts, ignore_errors=True)
            _replace(fonts_backup, fonts)
        if public_backup.exists():
            shutil.rmtree(public, ignore_errors=True)
            _replace(public_backup, public)
    journal.unlink()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_digest(relative: str) -> str:
    directory = ROOT / _confined(relative, "protected tree")
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f"protected tree is missing or unsafe: {relative}")
    files = {
        path.relative_to(ROOT).as_posix(): _sha256(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    if not files or any(path.is_symlink() for path in directory.rglob("*")):
        raise ValueError(f"protected tree is empty or unsafe: {relative}")
    return hashlib.sha256(_canonical(files)).hexdigest()


def _verify_protected(contract: dict[str, object]) -> None:
    protected = contract.get("protectedTrees", {})
    if not isinstance(protected, dict):
        raise ValueError("promotion contract protectedTrees must be an object")
    for relative, expected in protected.items():
        if _tree_digest(relative) != expected:
            raise ValueError(f"protected release tree changed: {relative}")


def _root_files(version: str) -> tuple[str, ...]:
    return (*ROOT_FILES[:-1], f"glide-{version}.zip")


def _expected(version: str) -> set[str]:
    root_files = _root_files(version)
    return {
        *root_files,
        *(f"static/Glide-{weight}.ttf" for weight in WEIGHTS),
        *(f"static/Glide-{weight}Italic.ttf" for weight in WEIGHTS),
    }


def _safe_source(path: Path, contract: dict[str, object] = DEFAULT_CONTRACT) -> Path:
    version = str(contract["semanticVersion"])
    authority = contract["authority"]
    expected = (ROOT / "apps" / "web" / "public" / version).resolve()
    if path.resolve() != expected or path.is_symlink() or not path.is_dir():
        raise ValueError(f"source must be immutable public {version}: {expected}")
    if any(item.is_symlink() for item in path.rglob("*")):
        raise ValueError("versioned source contains a symlink")
    for name in _root_files(version):
        if not (path / name).is_file():
            raise ValueError(f"versioned source is missing {name}")
    statics = sorted((path / "static").glob("*.ttf"))
    if len(statics) != 20:
        raise ValueError("versioned source must contain 20 static TTFs")
    manifest_path = path / MANIFEST
    if not manifest_path.is_file():
        raise ValueError("versioned source has no candidate manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    body = {key: value for key, value in manifest.items() if key != "manifestSha256"}
    calculated = hashlib.sha256(
        (json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    if (
        manifest.get("kind") != "glide-4-production-candidate"
        or manifest.get("version") != version
        or manifest.get("fontRevision") != contract["fontRevision"]
        or manifest.get("authority") != authority
        or manifest.get("manifestSha256") != calculated
    ):
        raise ValueError("versioned source manifest has the wrong identity")
    qa = manifest.get("qualityAssurance", {})
    if (
        qa.get("ots", {}).get("status") != "pass"
        or qa.get("fontbakery", {}).get("FAIL") != 0
    ):
        raise ValueError("versioned source quality gates did not pass")
    records = manifest.get("artifacts", [])
    expected = {Path(record["path"]) for record in records}
    actual = {
        item.relative_to(path)
        for item in path.rglob("*")
        if item.is_file() and item.relative_to(path).as_posix() != MANIFEST
    }
    if (
        len(records) != 25
        or actual != expected
        or {item.as_posix() for item in expected} != _expected(version)
    ):
        raise ValueError("versioned source differs from its 25-artifact inventory")
    for record in records:
        artifact = path / record["path"]
        if (
            artifact.stat().st_size != record["size"]
            or _sha256(artifact) != record["sha256"]
        ):
            raise ValueError(f"versioned artifact changed: {record['path']}")
    return path


def _prepare(
    source: Path,
    workspace: Path,
    contract: dict[str, object] = DEFAULT_CONTRACT,
) -> tuple[Path, Path]:
    version = str(contract["semanticVersion"])
    root_files = _root_files(version)
    public_new = workspace / "public"
    fonts_new = workspace / "fonts"
    shutil.copytree(ROOT / "apps" / "web" / "public", public_new)
    shutil.copytree(ROOT / "fonts", fonts_new)
    for name in root_files[:-1]:
        shutil.copy2(source / name, public_new / name)
    shutil.copy2(source / f"glide-{version}.zip", public_new / "glide.zip")
    for name in ("glide-variable.ttf", "glide-variable-italic.ttf"):
        shutil.copy2(source / name, fonts_new / name)
    for name in ("glide-variable.woff2", "glide-variable-italic.woff2"):
        shutil.copy2(source / name, fonts_new / name)
        shutil.copy2(source / name, fonts_new / "web" / name)
    static_new = fonts_new / "static"
    if static_new.exists():
        shutil.rmtree(static_new)
    shutil.copytree(source / "static", static_new)
    manifest = json.loads((source / MANIFEST).read_text(encoding="utf-8"))
    records = {record["path"]: record for record in manifest["artifacts"]}
    aliases = {
        public_new / "glide-variable.ttf": "glide-variable.ttf",
        public_new / "glide-variable-italic.ttf": "glide-variable-italic.ttf",
        public_new / "glide-variable.woff2": "glide-variable.woff2",
        public_new / "glide-variable-italic.woff2": "glide-variable-italic.woff2",
        public_new / "glide.zip": f"glide-{version}.zip",
        fonts_new / "glide-variable.ttf": "glide-variable.ttf",
        fonts_new / "glide-variable-italic.ttf": "glide-variable-italic.ttf",
        fonts_new / "glide-variable.woff2": "glide-variable.woff2",
        fonts_new / "glide-variable-italic.woff2": "glide-variable-italic.woff2",
        fonts_new / "web/glide-variable.woff2": "glide-variable.woff2",
        fonts_new / "web/glide-variable-italic.woff2": "glide-variable-italic.woff2",
    }
    aliases.update({path: f"static/{path.name}" for path in static_new.glob("*.ttf")})
    for path, relative in aliases.items():
        record = records[relative]
        if path.stat().st_size != record["size"] or _sha256(path) != record["sha256"]:
            raise ValueError(f"prepared alias differs from manifest: {path}")
    return public_new, fonts_new


def promote(
    source: Path, contract: dict[str, object] = DEFAULT_CONTRACT
) -> None:
    public = ROOT / "apps" / "web" / "public"
    fonts = ROOT / "fonts"
    public_backup = ROOT / ".glide-public-rollback"
    fonts_backup = ROOT / ".glide-fonts-rollback"
    journal = ROOT / JOURNAL
    _recover(public, fonts, public_backup, fonts_backup, journal)
    _verify_protected(contract)
    source = _safe_source(source, contract)
    version = str(contract["semanticVersion"])
    workspace = Path(tempfile.mkdtemp(prefix=f".glide-{version}-promote-", dir=ROOT))
    if public_backup.exists() or fonts_backup.exists():
        shutil.rmtree(workspace)
        raise ValueError("a previous promotion transaction needs recovery")
    try:
        public_new, fonts_new = _prepare(source, workspace, contract)
        _write_journal(journal, "prepared")
        _replace(public, public_backup)
        try:
            _replace(public_new, public)
            _verify_protected(contract)
            _write_journal(journal, "public-swapped")
            _replace(fonts, fonts_backup)
            try:
                _replace(fonts_new, fonts)
                _write_journal(journal, "committed")
            except BaseException:
                _replace(public, public_new)
                _replace(public_backup, public)
                raise
        except BaseException:
            if not public.exists() and public_backup.exists():
                _replace(public_backup, public)
            raise
        shutil.rmtree(public_backup, ignore_errors=True)
        shutil.rmtree(fonts_backup, ignore_errors=True)
        if public_backup.exists() or fonts_backup.exists():
            print("Glide 4.0 promotion: WARNING · committed; backup cleanup pending")
        else:
            journal.unlink()
    except BaseException:
        _recover(public, fonts, public_backup, fonts_backup, journal)
        raise
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--confirm-version", required=True)
    args = parser.parse_args()
    try:
        contract = _load_contract(args.contract)
        version = str(contract["semanticVersion"])
        if args.confirm_version != version:
            raise ValueError(f"promotion requires --confirm-version {version}")
        promote(args.source, contract)
    except (json.JSONDecodeError, OSError, ValueError) as error:
        parser.exit(2, f"Glide promotion: BLOCKED · {error}\n")
    print(f"Glide {version} promotion: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
