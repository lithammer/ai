import copy
import json
import os
import runpy
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VENDOR_SKILLS = REPOSITORY_ROOT / "scripts" / "vendor-skills"


class VendorSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        temporary = Path(self.temporary.name)
        self.root = temporary / "consumer"
        self.upstream = temporary / "upstream"
        self.cache = temporary / "cache"
        self.root.mkdir()
        (self.root / "vendor").mkdir()

        self.write_upstream_skill("upstream", "Original body.\n")
        self.write_upstream_skill("sibling", "Sibling body.\n")
        (self.upstream / "LICENSE").write_text("Test license.\n")

        self.git("init", "-b", "main")
        self.git("config", "user.name", "Vendor Test")
        self.git("config", "user.email", "vendor@example.com")
        self.git("add", ".")
        self.git("commit", "-m", "Initial skills")
        self.write_manifest(self.revision())

    def write_upstream_skill(self, name: str, body: str):
        directory = self.upstream / "skills" / name
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: An upstream test skill.\n---\n{body}"
        )

    def git(self, *args: str):
        return subprocess.run(
            ["git", *args],
            cwd=self.upstream,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def revision(self):
        return self.git("rev-parse", "HEAD")

    def write_manifest(self, revision: str, **extra: object):
        entry = {
            "repository": "upstream",
            "source": "skills/upstream",
            "license": {
                "source": "LICENSE",
                "destination": "vendor/licenses/upstream.txt",
            },
            **extra,
        }
        manifest = {
            "version": 2,
            "repositories": {
                "upstream": {
                    "url": str(self.upstream),
                    "branch": "main",
                    "revision": revision,
                }
            },
            "skills": {"local": entry},
        }
        (self.root / "vendor" / "skills.json").write_text(
            json.dumps(manifest, indent=2) + "\n"
        )

    def add_sibling(self, *, source: str = "skills/sibling"):
        manifest_path = self.root / "vendor" / "skills.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["skills"]["sibling"] = {
            "repository": "upstream",
            "source": source,
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    def vendor(self, *args: str, check: bool = True):
        environment = os.environ.copy()
        environment["VENDOR_SKILLS_ROOT"] = str(self.root)
        environment["VENDOR_SKILLS_CACHE"] = str(self.cache)
        return subprocess.run(
            [str(VENDOR_SKILLS), *args],
            text=True,
            capture_output=True,
            env=environment,
            check=check,
        )

    def load_vendor_module(self):
        previous_root = os.environ.get("VENDOR_SKILLS_ROOT")
        previous_cache = os.environ.get("VENDOR_SKILLS_CACHE")
        os.environ["VENDOR_SKILLS_ROOT"] = str(self.root)
        os.environ["VENDOR_SKILLS_CACHE"] = str(self.cache)
        try:
            return runpy.run_path(str(VENDOR_SKILLS))
        finally:
            if previous_root is None:
                os.environ.pop("VENDOR_SKILLS_ROOT", None)
            else:
                os.environ["VENDOR_SKILLS_ROOT"] = previous_root
            if previous_cache is None:
                os.environ.pop("VENDOR_SKILLS_CACHE", None)
            else:
                os.environ["VENDOR_SKILLS_CACHE"] = previous_cache

    def manifest(self):
        return json.loads((self.root / "vendor" / "skills.json").read_text())

    def manifest_entry(self, name: str = "local"):
        return self.manifest()["skills"][name]

    def repository_entry(self):
        return self.manifest()["repositories"]["upstream"]

    def snapshot_tree(self, path: Path):
        return {
            child.relative_to(path): child.read_bytes()
            for child in path.rglob("*")
            if child.is_file()
        }

    def test_sync_derives_local_name_copies_license_and_checks(self):
        self.vendor("sync")

        skill = (self.root / "skills" / "local" / "SKILL.md").read_text()
        self.assertIn("name: local", skill)
        self.assertNotIn("name: upstream", skill)
        license_file = self.root / "vendor" / "licenses" / "upstream.txt"
        self.assertEqual(license_file.read_text(), "Test license.\n")
        self.assertEqual(license_file.stat().st_mode & 0o777, 0o644)
        self.assertIn("recipeSha256", self.manifest_entry())
        self.assertIn("outputSha256", self.manifest_entry())
        self.vendor("check")

    def test_manifest_rejects_invalid_schema(self):
        manifest_path = self.root / "vendor" / "skills.json"
        original = json.loads(manifest_path.read_text())
        cases = []

        manifest = copy.deepcopy(original)
        manifest["version"] = 1
        cases.append(("manifest.version must be 2", manifest))

        manifest = copy.deepcopy(original)
        manifest["unexpected"] = True
        cases.append(("unknown fields", manifest))

        manifest = copy.deepcopy(original)
        manifest["repositories"]["upstream"]["revision"] = "short"
        cases.append(("full Git object ID", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["repository"] = "missing"
        cases.append(("repository is unknown", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["source"] = "../escape"
        cases.append(("safe relative path", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["destination"] = "skills/local"
        cases.append(("unknown fields", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["outputSha256"] = "0" * 64
        cases.append(("both lock hashes or neither", manifest))

        manifest = copy.deepcopy(original)
        overlapping = {
            "repository": "upstream",
            "source": "skills/sibling",
            "license": {
                "source": "LICENSE",
                "destination": "vendor/licenses/upstream.txt/NOTICE",
            },
        }
        manifest["skills"]["sibling"] = overlapping
        cases.append(("overlaps skill", manifest))

        manifest = copy.deepcopy(original)
        manifest["repositories"]["unused"] = copy.deepcopy(
            manifest["repositories"]["upstream"]
        )
        cases.append(("repositories are unused", manifest))

        for expected, invalid in cases:
            with self.subTest(expected=expected):
                manifest_path.write_text(json.dumps(invalid, indent=2) + "\n")
                result = self.vendor("check", check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

    def test_check_detects_output_and_repository_recipe_drift(self):
        self.vendor("sync")
        skill = self.root / "skills" / "local" / "SKILL.md"
        skill.write_text(skill.read_text() + "Local edit.\n")

        output_check = self.vendor("check", check=False)
        self.assertNotEqual(output_check.returncode, 0)
        self.assertIn("vendored output drifted", output_check.stderr)

        refused_sync = self.vendor("sync", check=False)
        self.assertNotEqual(refused_sync.returncode, 0)
        self.assertIn("rerun with --force", refused_sync.stderr)
        self.assertIn("Local edit.", skill.read_text())

        self.vendor("sync", "--force")
        manifest_path = self.root / "vendor" / "skills.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["repositories"]["upstream"]["branch"] = "next"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        recipe_check = self.vendor("check", check=False)
        self.assertNotEqual(recipe_check.returncode, 0)
        self.assertIn("manifest or patches changed", recipe_check.stderr)

    def test_patch_is_applied(self):
        patch = self.root / "vendor" / "patches" / "local.patch"
        patch.parent.mkdir()
        patch.write_text(
            "--- a/SKILL.md\n"
            "+++ b/SKILL.md\n"
            "@@ -2,4 +2,4 @@\n"
            " name: local\n"
            " description: An upstream test skill.\n"
            " ---\n"
            "-Original body.\n"
            "+Patched body.\n"
        )
        self.write_manifest(self.revision(), patches=["vendor/patches/local.patch"])

        self.vendor("sync")

        skill = (self.root / "skills" / "local" / "SKILL.md").read_text()
        self.assertIn("Patched body.", skill)
        self.vendor("check")

    def test_patch_cannot_change_derived_local_name(self):
        self.vendor("sync")
        skill = self.root / "skills" / "local" / "SKILL.md"
        original_skill = skill.read_text()
        patch = self.root / "vendor" / "patches" / "rename.patch"
        patch.parent.mkdir()
        patch.write_text(
            "--- a/SKILL.md\n"
            "+++ b/SKILL.md\n"
            "@@ -1,4 +1,4 @@\n"
            " ---\n"
            "-name: local\n"
            "+name: changed\n"
            " description: An upstream test skill.\n"
            " ---\n"
        )
        manifest_path = self.root / "vendor" / "skills.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["skills"]["local"]["patches"] = ["vendor/patches/rename.patch"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        result = self.vendor("sync", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected local name 'local'", result.stderr)
        self.assertEqual(skill.read_text(), original_skill)

    def test_update_does_not_fall_back_from_branch_to_tag(self):
        self.vendor("update")
        manifest_path = self.root / "vendor" / "skills.json"
        skill_path = self.root / "skills" / "local" / "SKILL.md"
        license_path = self.root / "vendor" / "licenses" / "upstream.txt"
        original_manifest = manifest_path.read_text()
        original_skill = skill_path.read_text()
        original_license = license_path.read_text()
        self.git("tag", "main")
        self.git("branch", "-m", "main", "renamed-main")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("couldn't find remote ref refs/heads/main", result.stderr)
        self.assertEqual(manifest_path.read_text(), original_manifest)
        self.assertEqual(skill_path.read_text(), original_skill)
        self.assertEqual(license_path.read_text(), original_license)
        self.vendor("sync")

    def test_manifest_install_failure_restores_repository_outputs(self):
        self.add_sibling()
        self.vendor("sync")
        manifest_path = self.root / "vendor" / "skills.json"
        local_path = self.root / "skills" / "local"
        sibling_path = self.root / "skills" / "sibling"
        license_path = self.root / "vendor" / "licenses" / "upstream.txt"
        original_manifest_bytes = manifest_path.read_bytes()
        original_manifest = self.manifest()
        original_local = self.snapshot_tree(local_path)
        original_sibling = self.snapshot_tree(sibling_path)
        original_license = license_path.read_bytes()

        for name in ("upstream", "sibling"):
            skill = self.upstream / "skills" / name / "SKILL.md"
            skill.write_text(skill.read_text() + f"Updated {name}.\n")
        (self.upstream / "LICENSE").write_text("Updated license.\n")
        self.git("add", ".")
        self.git("commit", "-m", "Update repository outputs")
        real_replace = Path.replace

        for error_type in (OSError, KeyboardInterrupt):
            with self.subTest(error_type=error_type.__name__):
                module = self.load_vendor_module()
                in_memory_manifest = module["load_manifest"]()
                failed = False

                def fail_manifest_install(
                    path: Path,
                    target: Path,
                    error: type[OSError | KeyboardInterrupt] = error_type,
                ) -> Path:
                    nonlocal failed
                    if (
                        not failed
                        and path.name == "skills.json"
                        and Path(target) == manifest_path
                    ):
                        failed = True
                        raise error("manifest install failed")
                    return real_replace(path, target)

                with (
                    mock.patch.object(Path, "replace", new=fail_manifest_install),
                    self.assertRaises(error_type),
                ):
                    module["command_update"](in_memory_manifest, force=False)

                self.assertEqual(in_memory_manifest, original_manifest)
                self.assertEqual(manifest_path.read_bytes(), original_manifest_bytes)
                self.assertEqual(self.snapshot_tree(local_path), original_local)
                self.assertEqual(self.snapshot_tree(sibling_path), original_sibling)
                self.assertEqual(license_path.read_bytes(), original_license)
                self.assertEqual(list(self.root.glob(".vendor-skills-recovery-*")), [])

    def test_failed_restoration_keeps_recovery_files(self):
        module = self.load_vendor_module()
        managed = self.root / "managed"
        staged = self.root / "staged"
        managed.mkdir()
        staged.mkdir()
        first = managed / "first"
        second = managed / "second"
        first.write_text("old first\n")
        second.write_text("old second\n")
        staged_first = staged / "first"
        staged_second = staged / "second"
        staged_first.write_text("new first\n")
        staged_second.write_text("new second\n")
        real_replace = Path.replace

        def fail_install_and_restore(path: Path, target: Path) -> Path:
            if path == staged_second:
                raise OSError("install failed")
            if path.name == "1" and path.parent.name.startswith(
                ".vendor-skills-recovery-"
            ):
                raise OSError("restore failed")
            return real_replace(path, target)

        with (
            mock.patch.object(Path, "replace", new=fail_install_and_restore),
            self.assertRaises(module["VendorError"]) as raised,
        ):
            module["replace_paths"]([(staged_first, first), (staged_second, second)])

        self.assertIn("recovery files kept at", str(raised.exception))
        recovery = list(self.root.glob(".vendor-skills-recovery-*"))
        self.assertEqual(len(recovery), 1)
        recovered = sorted(
            path.read_text() for path in recovery[0].iterdir() if path.is_file()
        )
        self.assertEqual(recovered, ["old first\n", "old second\n"])
        shutil.rmtree(recovery[0])

    def test_update_advances_shared_revision_and_rebuilds_all_siblings(self):
        self.add_sibling()
        self.vendor("sync")
        for name in ("upstream", "sibling"):
            skill = self.upstream / "skills" / name / "SKILL.md"
            skill.write_text(skill.read_text() + f"Updated {name}.\n")
        self.git("add", ".")
        self.git("commit", "-m", "Update skills")
        updated_revision = self.revision()

        result = self.vendor("update")

        self.assertIn("updated upstream", result.stdout)
        self.assertEqual(self.repository_entry()["revision"], updated_revision)
        local = (self.root / "skills" / "local" / "SKILL.md").read_text()
        sibling = (self.root / "skills" / "sibling" / "SKILL.md").read_text()
        self.assertIn("Updated upstream.", local)
        self.assertIn("Updated sibling.", sibling)
        self.assertIn("name: local", local)
        self.assertIn("name: sibling", sibling)
        self.vendor("check")

    def test_missing_license_preserves_output_and_shared_pin(self):
        self.vendor("sync")
        manifest_path = self.root / "vendor" / "skills.json"
        skill_path = self.root / "skills" / "local" / "SKILL.md"
        license_path = self.root / "vendor" / "licenses" / "upstream.txt"
        original_manifest = manifest_path.read_text()
        original_skill = skill_path.read_text()
        original_license = license_path.read_text()

        upstream_skill = self.upstream / "skills" / "upstream" / "SKILL.md"
        upstream_skill.write_text(upstream_skill.read_text() + "Incomplete update.\n")
        (self.upstream / "LICENSE").unlink()
        self.git("add", "-A")
        self.git("commit", "-m", "Remove required license")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manifest_path.read_text(), original_manifest)
        self.assertEqual(skill_path.read_text(), original_skill)
        self.assertEqual(license_path.read_text(), original_license)
        self.vendor("check")

    def test_failed_sibling_patch_preserves_group_outputs_and_pin(self):
        patch = self.root / "vendor" / "patches" / "sibling.patch"
        patch.parent.mkdir()
        patch.write_text(
            "--- a/SKILL.md\n"
            "+++ b/SKILL.md\n"
            "@@ -5 +5 @@\n"
            "-Sibling body.\n"
            "+Patched sibling.\n"
        )
        self.add_sibling()
        manifest_path = self.root / "vendor" / "skills.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["skills"]["sibling"]["patches"] = ["vendor/patches/sibling.patch"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.vendor("sync")
        local_path = self.root / "skills" / "local" / "SKILL.md"
        sibling_path = self.root / "skills" / "sibling" / "SKILL.md"
        license_path = self.root / "vendor" / "licenses" / "upstream.txt"
        original_manifest = manifest_path.read_text()
        original_local = local_path.read_text()
        original_sibling = sibling_path.read_text()
        original_license = license_path.read_text()

        upstream_skill = self.upstream / "skills" / "upstream" / "SKILL.md"
        upstream_skill.write_text(upstream_skill.read_text() + "Incomplete update.\n")
        sibling_source = self.upstream / "skills" / "sibling" / "SKILL.md"
        sibling_source.write_text(
            sibling_source.read_text().replace("Sibling body.", "Changed sibling.")
        )
        self.git("add", ".")
        self.git("commit", "-m", "Break sibling patch")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manifest_path.read_text(), original_manifest)
        self.assertEqual(local_path.read_text(), original_local)
        self.assertEqual(sibling_path.read_text(), original_sibling)
        self.assertEqual(license_path.read_text(), original_license)
        self.vendor("check")

    def test_failed_sibling_update_preserves_group_outputs_and_pin(self):
        self.add_sibling()
        self.vendor("sync")
        manifest_path = self.root / "vendor" / "skills.json"
        local_path = self.root / "skills" / "local" / "SKILL.md"
        sibling_path = self.root / "skills" / "sibling" / "SKILL.md"
        license_path = self.root / "vendor" / "licenses" / "upstream.txt"
        original_manifest = manifest_path.read_text()
        original_local = local_path.read_text()
        original_sibling = sibling_path.read_text()
        original_license = license_path.read_text()

        upstream_skill = self.upstream / "skills" / "upstream" / "SKILL.md"
        upstream_skill.write_text(upstream_skill.read_text() + "Incomplete update.\n")
        sibling_source = self.upstream / "skills" / "sibling"
        for child in sibling_source.iterdir():
            child.unlink()
        sibling_source.rmdir()
        self.git("add", "-A")
        self.git("commit", "-m", "Remove sibling")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("may have been renamed or removed", result.stderr)
        self.assertEqual(manifest_path.read_text(), original_manifest)
        self.assertEqual(local_path.read_text(), original_local)
        self.assertEqual(sibling_path.read_text(), original_sibling)
        self.assertEqual(license_path.read_text(), original_license)
        self.vendor("check")

    def test_selected_sync_and_check_ignore_unselected_drift(self):
        self.add_sibling()
        self.vendor("sync")
        sibling = self.root / "skills" / "sibling" / "SKILL.md"
        sibling.write_text(sibling.read_text() + "Sibling edit.\n")

        self.vendor("check", "local")
        self.vendor("sync", "local")

        self.assertIn("Sibling edit.", sibling.read_text())
        full_check = self.vendor("check", check=False)
        self.assertNotEqual(full_check.returncode, 0)
        self.assertIn("sibling: vendored output drifted", full_check.stderr)

    def test_update_rejects_skill_names(self):
        result = self.vendor("update", "local", check=False)

        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments: local", result.stderr)


if __name__ == "__main__":
    unittest.main()
