"""Package behavior tests. Run with Python 3 and a locally installed Claude CLI."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
# Public install identity: deliberately independent of the checkout directory.
PLUGIN = "cc_chrome_devtools_mcp_skill"
PAYLOAD = ("SKILL.md", "README.md", "TOOLS.md", "WORKFLOWS.md", "METRICS.md")


class PackageTests(unittest.TestCase):
    def test_manual_install_keeps_supporting_documents_resolvable(self):
        with tempfile.TemporaryDirectory(prefix="devtools-manual-") as folder:
            installed = Path(folder) / ".claude" / "skills" / PLUGIN
            shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns(
                ".git", "__pycache__"))
            for name in PAYLOAD:
                with self.subTest(document=name):
                    content = (installed / name).read_text(encoding="utf-8")
                    self.assertTrue(content.strip(), f"Empty installed document: {name}")
                    # Follow relative Markdown file links after relocation.
                    # Fragment validity and upstream URLs belong to docs checks.
                    for target in re.findall(r"\]\(([^\s)]+)\)", content):
                        url = urlsplit(target)
                        if not url.scheme and not url.netloc and url.path:
                            path = installed / unquote(url.path)
                            self.assertTrue(path.is_file(), f"{name}: missing {target}")


class ClaudeInstallationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.claude = shutil.which(os.environ.get("CLAUDE_BIN", "claude"))
        if not cls.claude:
            raise RuntimeError("Install Claude Code or set CLAUDE_BIN; installation tests require it")

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="devtools-install-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.package = self.base / "arbitrary-checkout-name"
        shutil.copytree(ROOT, self.package, ignore=shutil.ignore_patterns(
            ".git", "__pycache__"))
        home = self.base / "home"
        home.mkdir()
        self.config = home / ".claude"
        # Do not inherit model credentials, plugins, MCP configuration or hooks.
        self.env = {key: os.environ[key] for key in (
            "PATH", "SystemRoot", "WINDIR", "PATHEXT", "TMPDIR", "TEMP", "TMP"
        ) if key in os.environ}
        self.env.update({
            "HOME": str(home),
            "USERPROFILE": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "CLAUDE_CONFIG_DIR": str(self.config),
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
            "NO_COLOR": "1",
        })
        self.manifest = json.loads(
            (self.package / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.marketplace = json.loads(
            (self.package / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))

    def cli(self, *arguments, success=True):
        result = subprocess.run(
            [self.claude, *map(str, arguments)], cwd=self.base, env=self.env,
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def assert_inventory(self, text):
        self.assertIn(f"({PLUGIN}) {self.manifest['version']}", text)
        self.assertIn(self.manifest["description"], text)
        self.assertRegex(text, rf"(?m)^\s*Skills \(1\)\s+{PLUGIN}\s*$")
        for component in ("Agents", "Hooks", "MCP servers", "LSP servers"):
            self.assertRegex(text, rf"(?m)^\s*{component} \(0\)\s*$")

    def test_manifests_validate_with_real_cli(self):
        for path in (self.package, self.package / ".claude-plugin/plugin.json"):
            with self.subTest(path=path.name):
                report = json.loads(self.cli("plugin", "validate", path, "--json").stdout)
                self.assertTrue(report["success"], report)

    def test_direct_load_uses_published_identity_and_loads_one_skill(self):
        details = self.cli("--plugin-dir", self.package, "plugin", "details", PLUGIN)
        self.assert_inventory(details.stdout)

    def test_marketplace_install_delivers_metadata_and_complete_payload(self):
        marketplace = self.marketplace["name"]
        plugin_id = f"{PLUGIN}@{marketplace}"
        self.cli("plugin", "marketplace", "add", self.package)
        listing = json.loads(self.cli("plugin", "list", "--json", "--available").stdout)
        available = [p for p in listing["available"] if p["pluginId"] == plugin_id]
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0].get("description"), self.manifest["description"])
        self.cli("plugin", "install", plugin_id)
        installed = json.loads(self.cli("plugin", "list", "--json").stdout)
        matching = [p for p in installed if p["id"] == plugin_id]
        self.assertEqual(len(matching), 1)
        record = matching[0]
        self.assertTrue(record["enabled"])
        self.assertEqual(record["version"], self.manifest["version"])
        installed_path = Path(record["installPath"]).resolve()
        self.assertTrue(installed_path.is_relative_to(self.config.resolve()), record)
        for name in PAYLOAD:
            with self.subTest(document=name):
                self.assertTrue((installed_path / name).is_file(), f"Missing installed {name}")
                self.assertEqual((installed_path / name).read_bytes(),
                                 (self.package / name).read_bytes())
        self.assert_inventory(self.cli("plugin", "details", PLUGIN).stdout)

    def test_invalid_manifest_is_rejected(self):
        manifest = self.package / ".claude-plugin/plugin.json"
        manifest.write_text("{invalid JSON", encoding="utf-8")
        result = self.cli("plugin", "validate", manifest, "--json", success=False)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)["success"])


if __name__ == "__main__":
    unittest.main()
