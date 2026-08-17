#!/usr/bin/env python3
"""Publish one immutable Glide 4 beta directory without moving aliases."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
RELEASE = "4.0.0-beta.1"
MANIFEST_NAME = f"glide-{RELEASE}-manifest.json"
VERSIONED_DIRECTORY = Path("apps/web/public") / RELEASE
PROTECTED_DIRECTORIES = (
    Path("apps/web/public/3.1.0"),
    Path("apps/web/public/3.002"),
    Path("fonts"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _tree_hashes(directory: Path) -> dict[str, str]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"missing or unsafe directory: {directory}")
    hashes: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"directory contains a symlink: {path}")
        if path.is_file():
            hashes[path.relative_to(directory).as_posix()] = sha256(path.read_bytes())
    return hashes


def _protected_snapshot(public_repo: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative in PROTECTED_DIRECTORIES:
        for path, digest in _tree_hashes(public_repo / relative).items():
            snapshot[(relative / path).as_posix()] = digest
    public = public_repo / "apps/web/public"
    for path in sorted(public.glob("glide-*")):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"public alias is missing or unsafe: {path}")
        snapshot[path.relative_to(public_repo).as_posix()] = sha256(path.read_bytes())
    return snapshot


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _load_manifest(path: Path) -> tuple[bytes, dict[str, Any]]:
    if path.name != MANIFEST_NAME:
        raise ValueError(f"beta manifest must be named {MANIFEST_NAME}")
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or unsafe beta manifest: {path}")
    data = path.read_bytes()
    manifest = json.loads(data)
    required = {
        "kind": "glide-beta-release",
        "channel": "beta",
        "version": "4.0.0",
        "releaseLabel": RELEASE,
        "fontRevision": "4.000",
        "family": "Glide 4 Beta",
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise ValueError(f"beta manifest has the wrong {key}")
    target = manifest.get("publishTarget", {})
    if target.get("versionedDirectory") != VERSIONED_DIRECTORY.as_posix():
        raise ValueError("beta manifest has the wrong versioned publish directory")
    expected_digest = manifest.get("manifestSha256")
    unsigned = dict(manifest)
    unsigned.pop("manifestSha256", None)
    if expected_digest != sha256(_canonical(unsigned)):
        raise ValueError("beta manifest self-hash is invalid")
    return data, manifest


def _verify_source(
    stage: Path, manifest_path: Path
) -> tuple[Path, dict[str, str]]:
    # Inspect the complete private stage so a symlink outside the versioned
    # subtree can't hide a second release input from the operator.
    _tree_hashes(stage)
    manifest_bytes, manifest = _load_manifest(manifest_path)
    source = stage / VERSIONED_DIRECTORY
    actual = _tree_hashes(source)
    manifest_name = manifest_path.name
    if actual.pop(manifest_name, None) != sha256(manifest_bytes):
        raise ValueError("staged beta manifest differs from the approved manifest")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("beta manifest has no artifacts")
    expected: dict[str, str] = {}
    for artifact in artifacts:
        relative = artifact.get("path")
        digest = artifact.get("sha256")
        size = artifact.get("size")
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise ValueError("beta manifest contains an invalid artifact")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or path.as_posix() in expected:
            raise ValueError(f"beta manifest contains an unsafe artifact: {relative}")
        source_path = source / path
        if not source_path.is_file() or source_path.is_symlink():
            raise ValueError(f"staged beta artifact is missing or unsafe: {relative}")
        data = source_path.read_bytes()
        if len(data) != size or sha256(data) != digest:
            raise ValueError(f"staged beta artifact differs from manifest: {relative}")
        expected[path.as_posix()] = digest
    if actual != expected:
        raise ValueError("staged beta directory has missing or unmanifested files")
    return source, expected | {manifest_name: sha256(manifest_bytes)}


def publish(
    *, public_repo: Path, stage: Path, manifest_path: Path, confirm_release: str
) -> Path:
    if confirm_release != RELEASE:
        raise ValueError(f"publishing requires --confirm-release {RELEASE}")
    if stage.is_symlink():
        raise ValueError(f"beta stage must not be a symlink: {stage}")
    if manifest_path.is_symlink():
        raise ValueError(f"beta manifest must not be a symlink: {manifest_path}")
    public_repo = public_repo.resolve()
    if not (public_repo / "AGENTS.md").is_file():
        raise ValueError(f"not a Glide public checkout: {public_repo}")
    before = _protected_snapshot(public_repo)
    source, expected = _verify_source(stage.absolute(), manifest_path.absolute())
    target = public_repo / VERSIONED_DIRECTORY
    if target.exists() or target.is_symlink():
        if target.is_symlink() or _tree_hashes(target) != expected:
            raise ValueError(f"immutable beta directory already differs: {target}")
        if _protected_snapshot(public_repo) != before:
            raise RuntimeError("beta verification changed a protected public asset")
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f"{RELEASE}-", dir=target.parent))
    destination_claimed = False
    try:
        shutil.copytree(source, temporary / "payload")
        if _tree_hashes(temporary / "payload") != expected:
            raise ValueError("copied beta bytes differ from the approved stage")
        try:
            (temporary / "payload").rename(target)
            destination_claimed = True
        except FileExistsError as error:
            raise ValueError(f"immutable beta directory already exists: {target}") from error
        temporary.rmdir()
        if _tree_hashes(target) != expected:
            raise ValueError("published beta bytes differ from the approved stage")
        if _protected_snapshot(public_repo) != before:
            raise RuntimeError("beta publication changed a protected public asset")
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        if destination_claimed:
            shutil.rmtree(target, ignore_errors=True)
        raise
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--confirm-release", required=True)
    parser.add_argument("--public-repo", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        target = publish(
            public_repo=args.public_repo,
            stage=args.stage,
            manifest_path=args.manifest,
            confirm_release=args.confirm_release,
        )
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f"Glide beta publish: BLOCKED · {error}\n")
    print(f"Glide beta publish: PASS · {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
