import copy
import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

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
        (self.upstream / "skills" / "upstream").mkdir(parents=True)
        (self.upstream / "skills" / "upstream" / "SKILL.md").write_text(
            "---\n"
            "name: upstream\n"
            "description: An upstream test skill.\n"
            "---\n"
            "Original body.\n"
        )
        (self.upstream / "LICENSE").write_text("Test license.\n")

        self.git("init", "-b", "main")
        self.git("config", "user.name", "Vendor Test")
        self.git("config", "user.email", "vendor@example.com")
        self.git("add", ".")
        self.git("commit", "-m", "Initial skill")
        self.write_manifest(self.revision())

    def git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=self.upstream,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def revision(self):
        return self.git("rev-parse", "HEAD")

    def write_manifest(self, revision, **extra):
        entry = {
            "repository": str(self.upstream),
            "branch": "main",
            "revision": revision,
            "source": "skills/upstream",
            "destination": "skills/local",
            "name": "local",
            "license": {
                "source": "LICENSE",
                "destination": "vendor/licenses/upstream.txt",
            },
            **extra,
        }
        (self.root / "vendor" / "skills.json").write_text(
            json.dumps({"version": 1, "skills": {"local": entry}}, indent=2) + "\n"
        )

    def vendor(self, *args, check=True):
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

    def manifest_entry(self):
        manifest = json.loads((self.root / "vendor" / "skills.json").read_text())
        return manifest["skills"]["local"]

    def test_sync_renames_skill_copies_license_and_checks(self):
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
        del manifest["skills"]["local"]["name"]
        cases.append(("manifest.skills.local is missing: name", manifest))

        manifest = copy.deepcopy(original)
        manifest["unexpected"] = True
        cases.append(("unknown fields", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["revision"] = "short"
        cases.append(("full Git object ID", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["destination"] = "../escape"
        cases.append(("safe relative path", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["name"] = "different"
        cases.append(("must match its manifest key", manifest))

        manifest = copy.deepcopy(original)
        manifest["skills"]["local"]["outputSha256"] = "0" * 64
        cases.append(("both lock hashes or neither", manifest))

        manifest = copy.deepcopy(original)
        duplicate = copy.deepcopy(manifest["skills"]["local"])
        duplicate["name"] = "other"
        duplicate["destination"] = "skills/other"
        manifest["skills"]["other"] = duplicate
        cases.append(("duplicates skill", manifest))

        for expected, invalid in cases:
            with self.subTest(expected=expected):
                manifest_path.write_text(json.dumps(invalid, indent=2) + "\n")
                result = self.vendor("check", check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)

    def test_manifest_is_validated_before_write(self):
        manifest_path = self.root / "vendor" / "skills.json"
        original = manifest_path.read_text()
        environment = os.environ.copy()
        environment["VENDOR_SKILLS_ROOT"] = str(self.root)
        environment["VENDOR_SKILLS_CACHE"] = str(self.cache)
        environment["VENDOR_SKILLS_SCRIPT"] = str(VENDOR_SKILLS)
        code = textwrap.dedent("""
            import json
            import os
            import runpy
            from pathlib import Path

            module = runpy.run_path(os.environ["VENDOR_SKILLS_SCRIPT"])
            path = Path(os.environ["VENDOR_SKILLS_ROOT"]) / "vendor" / "skills.json"
            manifest = json.loads(path.read_text())
            manifest["skills"]["local"]["destination"] = "../escape"
            module["write_manifest"](manifest)
            """)

        result = subprocess.run(
            ["python3", "-c", code],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("safe relative path", result.stderr)
        self.assertEqual(manifest_path.read_text(), original)

    def test_check_detects_output_and_recipe_drift(self):
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
        manifest["skills"]["local"]["branch"] = "next"
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

    def test_patch_cannot_change_local_name(self):
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

    def test_update_advances_revision_and_rebuilds(self):
        self.vendor("sync")
        skill = self.upstream / "skills" / "upstream" / "SKILL.md"
        updated = skill.read_text().replace("name: upstream", "name: renamed-upstream")
        skill.write_text(updated + "Upstream update.\n")
        self.git("add", ".")
        self.git("commit", "-m", "Update skill")
        updated_revision = self.revision()

        result = self.vendor("update")

        self.assertIn("updated local", result.stdout)
        self.assertEqual(self.manifest_entry()["revision"], updated_revision)
        vendored = (self.root / "skills" / "local" / "SKILL.md").read_text()
        self.assertIn("Upstream update.", vendored)
        self.assertIn("name: local", vendored)
        self.assertNotIn("name: renamed-upstream", vendored)
        self.vendor("check")

    def test_renamed_upstream_source_preserves_output_and_pin(self):
        self.vendor("sync")
        skill = self.root / "skills" / "local" / "SKILL.md"
        original_skill = skill.read_text()
        original_revision = self.manifest_entry()["revision"]
        (self.upstream / "skills" / "upstream").rename(
            self.upstream / "skills" / "renamed"
        )
        self.git("add", "-A")
        self.git("commit", "-m", "Rename skill directory")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("may have been renamed or removed", result.stderr)
        self.assertEqual(skill.read_text(), original_skill)
        self.assertEqual(self.manifest_entry()["revision"], original_revision)
        self.vendor("check")

    def test_failed_update_preserves_output_and_pinned_revision(self):
        self.vendor("sync")
        skill = self.root / "skills" / "local" / "SKILL.md"
        license_file = self.root / "vendor" / "licenses" / "upstream.txt"
        original_skill = skill.read_text()
        original_license = license_file.read_text()
        original_revision = self.manifest_entry()["revision"]

        upstream_skill = self.upstream / "skills" / "upstream" / "SKILL.md"
        upstream_skill.write_text(upstream_skill.read_text() + "Incomplete update.\n")
        (self.upstream / "LICENSE").unlink()
        self.git("add", "-A")
        self.git("commit", "-m", "Remove required license")

        result = self.vendor("update", check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(skill.read_text(), original_skill)
        self.assertEqual(license_file.read_text(), original_license)
        self.assertEqual(self.manifest_entry()["revision"], original_revision)
        self.vendor("check")


if __name__ == "__main__":
    unittest.main()
