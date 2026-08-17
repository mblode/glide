from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/publish-glide-beta.py"
SPEC = importlib.util.spec_from_file_location("publish_glide_beta", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PublishGlideBetaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.public = root / "public"
        self.stage = root / "stage"
        self.manifest = root / MODULE.MANIFEST_NAME
        (self.public / "AGENTS.md").parent.mkdir(parents=True)
        (self.public / "AGENTS.md").write_text("test\n")
        protected = {
            "apps/web/public/3.1.0/asset.ttf": b"three-one",
            "apps/web/public/3.002/asset.ttf": b"rollback",
            "apps/web/public/glide-variable.ttf": b"alias",
            "fonts/glide-variable.ttf": b"canonical",
        }
        for relative, data in protected.items():
            path = self.public / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.protected = {
            relative: digest(data) for relative, data in protected.items()
        }
        versioned = self.stage / MODULE.VERSIONED_DIRECTORY
        (versioned / "static").mkdir(parents=True)
        artifacts = {
            "glide-variable.ttf": b"roman",
            "static/Glide4Beta-Regular.ttf": b"static",
        }
        for relative, data in artifacts.items():
            path = versioned / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        manifest = {
            "kind": "glide-beta-release",
            "channel": "beta",
            "family": "Glide 4 Beta",
            "version": "4.0.0",
            "releaseLabel": MODULE.RELEASE,
            "fontRevision": "4.000",
            "publishTarget": {
                "versionedDirectory": MODULE.VERSIONED_DIRECTORY.as_posix()
            },
            "artifacts": [
                {"path": relative, "size": len(data), "sha256": digest(data)}
                for relative, data in artifacts.items()
            ],
        }
        manifest["manifestSha256"] = digest(MODULE._canonical(manifest))
        payload = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        self.manifest.write_text(payload)
        (versioned / self.manifest.name).write_text(payload)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def assert_protected_unchanged(self) -> None:
        for relative, expected in self.protected.items():
            self.assertEqual(digest((self.public / relative).read_bytes()), expected)

    def test_publishes_only_the_immutable_beta_directory(self) -> None:
        target = MODULE.publish(
            public_repo=self.public,
            stage=self.stage,
            manifest_path=self.manifest,
            confirm_release=MODULE.RELEASE,
        )
        self.assertEqual(target, self.public.resolve() / MODULE.VERSIONED_DIRECTORY)
        self.assertEqual(
            MODULE._tree_hashes(target),
            MODULE._tree_hashes(self.stage / MODULE.VERSIONED_DIRECTORY),
        )
        self.assert_protected_unchanged()

    def test_identical_existing_release_is_idempotent(self) -> None:
        arguments = {
            "public_repo": self.public,
            "stage": self.stage,
            "manifest_path": self.manifest,
            "confirm_release": MODULE.RELEASE,
        }
        MODULE.publish(**arguments)
        MODULE.publish(**arguments)
        self.assert_protected_unchanged()

    def test_rejects_existing_release_with_different_bytes(self) -> None:
        target = self.public / MODULE.VERSIONED_DIRECTORY
        target.mkdir(parents=True)
        (target / "unexpected.ttf").write_bytes(b"different")
        with self.assertRaisesRegex(ValueError, "already differs"):
            MODULE.publish(
                public_repo=self.public,
                stage=self.stage,
                manifest_path=self.manifest,
                confirm_release=MODULE.RELEASE,
            )
        self.assertEqual((target / "unexpected.ttf").read_bytes(), b"different")
        self.assert_protected_unchanged()

    def test_rejects_symlink_and_wrong_confirmation(self) -> None:
        with self.assertRaisesRegex(ValueError, "confirm-release"):
            MODULE.publish(
                public_repo=self.public,
                stage=self.stage,
                manifest_path=self.manifest,
                confirm_release="4.0.0",
            )
        artifact = self.stage / MODULE.VERSIONED_DIRECTORY / "glide-variable.ttf"
        artifact.unlink()
        artifact.symlink_to(self.manifest)
        with self.assertRaisesRegex(ValueError, "symlink"):
            MODULE.publish(
                public_repo=self.public,
                stage=self.stage,
                manifest_path=self.manifest,
                confirm_release=MODULE.RELEASE,
            )
        self.assert_protected_unchanged()

    def test_rejects_symlinked_stage_root(self) -> None:
        linked_stage = self.stage.parent / "linked-stage"
        linked_stage.symlink_to(self.stage, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "stage must not be a symlink"):
            MODULE.publish(
                public_repo=self.public,
                stage=linked_stage,
                manifest_path=self.manifest,
                confirm_release=MODULE.RELEASE,
            )
        self.assert_protected_unchanged()


if __name__ == "__main__":
    unittest.main()
