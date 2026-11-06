"""Package behavior tests. Run with Python 3 and a locally installed Claude CLI."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
# Public install identity: deliberately independent of the checkout directory.
PLUGIN = "cc_chrome_devtools_mcp_skill"
PAYLOAD = ("SKILL.md", "README.md", "GUIDE.md", "TOOLS.md", "WORKFLOWS.md", "METRICS.md")


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

    def register_inert_server(self, scope, marker):
        # mcp get may start the configured command. This process exits without
        # network, model calls, or a browser; its arguments identify the config.
        self.cli("mcp", "add", "--scope", scope, "chrome-devtools", "--",
                 sys.executable, "-c", "pass", marker)

    def test_plugin_update_and_uninstall_preserve_separate_mcp_registration(self):
        plugin_id = f"{PLUGIN}@{self.marketplace['name']}"
        self.cli("plugin", "marketplace", "add", self.package)
        self.cli("plugin", "install", plugin_id)
        endpoint = "--browserUrl=http://127.0.0.1:19222"
        self.register_inert_server("user", endpoint)
        manifest_path = self.package / ".claude-plugin/plugin.json"
        manifest = dict(self.manifest, version="99.0.0")
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.cli("plugin", "update", plugin_id)
        self.assertIn(f"({PLUGIN}) 99.0.0",
                      self.cli("plugin", "details", PLUGIN).stdout)
        for action in ("updated", "uninstalled"):
            with self.subTest(action=action):
                if action == "uninstalled":
                    self.cli("plugin", "uninstall", plugin_id)
                    self.assertEqual(json.loads(self.cli("plugin", "list", "--json").stdout), [])
                details = self.cli("mcp", "get", "chrome-devtools").stdout
                self.assertIn("Scope: User config", details)
                self.assertIn(endpoint, details)
        self.cli("mcp", "remove", "--scope", "user", "chrome-devtools")
        self.assertNotEqual(self.cli("mcp", "get", "chrome-devtools", success=False).returncode, 0)

    def test_scope_removal_reveals_next_registration_without_merging_flags(self):
        self.register_inert_server("user", "--isolated=true")
        self.register_inert_server("project", "--browserUrl=http://127.0.0.1:19222")
        self.register_inert_server("local", "--browserUrl=http://127.0.0.1:19223")
        local = self.cli("mcp", "get", "chrome-devtools").stdout
        self.assertIn("Scope: Local config", local)
        self.assertIn("--browserUrl=http://127.0.0.1:19223", local)
        self.assertNotIn("--isolated=true", local)
        self.cli("mcp", "remove", "--scope", "local", "chrome-devtools")
        # An unapproved project entry does not override an available user entry.
        pending = self.cli("mcp", "get", "chrome-devtools").stdout
        self.assertIn("Scope: User config", pending)
        self.assertIn("--isolated=true", pending)
        settings = self.config / "settings.json"
        settings.write_text(json.dumps({"enabledMcpjsonServers": ["chrome-devtools"]}),
                            encoding="utf-8")
        for scope, expected, absent in (
                ("project", "--browserUrl=http://127.0.0.1:19222", "--isolated=true"),
                ("user", "--isolated=true", "--browserUrl=")):
            with self.subTest(scope=scope):
                details = self.cli("mcp", "get", "chrome-devtools").stdout
                self.assertIn(f"Scope: {scope.capitalize()} config", details)
                self.assertIn(expected, details)
                self.assertNotIn(absent, details)
                self.cli("mcp", "remove", "--scope", scope, "chrome-devtools")
        self.assertNotEqual(self.cli("mcp", "get", "chrome-devtools", success=False).returncode, 0)

    def test_rejected_duplicate_and_wrong_scope_removal_preserve_registration(self):
        original = "--isolated=true"
        replacement = "--browserUrl=http://127.0.0.1:19224"
        self.register_inert_server("user", original)
        for arguments in (
                ("mcp", "add", "--scope", "user", "chrome-devtools", "--",
                 sys.executable, "-c", "pass", replacement),
                ("mcp", "remove", "--scope", "project", "chrome-devtools")):
            with self.subTest(operation=arguments):
                result = self.cli(*arguments, success=False)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                effective = self.cli("mcp", "get", "chrome-devtools").stdout
                self.assertIn("Scope: User config", effective)
                self.assertIn(original, effective)
                self.assertNotIn(replacement, effective)
        self.cli("mcp", "remove", "--scope", "user", "chrome-devtools")
        repeated = self.cli("mcp", "remove", "--scope", "user", "chrome-devtools",
                            success=False)
        self.assertNotEqual(repeated.returncode, 0)
        self.assertNotEqual(self.cli("mcp", "get", "chrome-devtools", success=False).returncode, 0)
        # Explicit replacement is the successful control after rejected retries.
        self.register_inert_server("user", replacement)
        effective = self.cli("mcp", "get", "chrome-devtools").stdout
        self.assertIn(replacement, effective)
        self.assertNotIn(original, effective)

    def test_truncated_project_config_can_be_repaired_without_losing_other_servers(self):
        self.register_inert_server("user", "--isolated=true")
        endpoint = "--browserUrl=http://127.0.0.1:19225"
        self.register_inert_server("project", endpoint)
        self.cli("mcp", "add", "--scope", "project", "unrelated-server", "--",
                 sys.executable, "-c", "pass", "unrelated-marker")
        (self.config / "settings.json").write_text(
            json.dumps({"enabledMcpjsonServers": ["chrome-devtools"]}), encoding="utf-8")
        project = self.base / ".mcp.json"
        intact = project.read_bytes()
        original = json.loads(intact)
        self.assertIn(endpoint, self.cli("mcp", "get", "chrome-devtools").stdout)
        # Model an interrupted file write, not an actual process-kill race.
        truncated = b'{"mcpServers":'
        project.write_bytes(truncated)
        rejected = self.cli("mcp", "remove", "--scope", "project", "chrome-devtools",
                            success=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(project.read_bytes(), truncated)
        fallback = self.cli("mcp", "get", "chrome-devtools").stdout
        self.assertIn("Scope: User config", fallback)
        self.assertIn("--isolated=true", fallback)
        self.assertNotIn(endpoint, fallback)
        # Restore the saved file before scoped removal; preserve the other entry.
        project.write_bytes(intact)
        self.assertIn(endpoint, self.cli("mcp", "get", "chrome-devtools").stdout)
        self.cli("mcp", "remove", "--scope", "project", "chrome-devtools")
        remaining = json.loads(project.read_text(encoding="utf-8"))["mcpServers"]
        self.assertNotIn("chrome-devtools", remaining)
        self.assertEqual(remaining["unrelated-server"],
                         original["mcpServers"]["unrelated-server"])
        self.assertIn("--isolated=true", self.cli("mcp", "get", "chrome-devtools").stdout)

    def test_invalid_local_update_is_diagnosable_and_repairable(self):
        plugin_id = f"{PLUGIN}@{self.marketplace['name']}"
        self.cli("plugin", "marketplace", "add", self.package)
        self.cli("plugin", "install", plugin_id)
        profile = self.base / "persistent-profile"
        profile.mkdir()
        sentinel = profile / "keep.txt"
        sentinel.write_bytes(b"synthetic profile data")
        marker = f"--userDataDir={profile}"
        self.register_inert_server("user", marker)
        manifest = self.package / ".claude-plugin/plugin.json"
        manifest.write_text('{"version":', encoding="utf-8")
        validation = self.cli("plugin", "validate", self.package, "--json", success=False)
        self.assertNotEqual(validation.returncode, 0)
        self.assertFalse(json.loads(validation.stdout)["success"])
        # Deliberately bypass validation to model updating from a broken checkout.
        # 2.1.319 reports success here; don't require that upstream defect forever.
        self.cli("plugin", "update", plugin_id, success=False)
        records = json.loads(self.cli("plugin", "list", "--json").stdout)
        self.assertEqual(len(records), 1, records)
        details = self.cli("plugin", "details", PLUGIN, success=False)
        if details.returncode:
            self.assertTrue(records[0].get("errors"), records)
        else:
            # A future atomic refusal may retain a usable previous installation.
            self.assert_inventory(details.stdout)
            self.assertFalse(records[0].get("errors"), records)
            for name in PAYLOAD:
                self.assertEqual((Path(records[0]["installPath"]) / name).read_bytes(),
                                 (ROOT / name).read_bytes())
        self.assertIn(marker, self.cli("mcp", "get", "chrome-devtools").stdout)

        manifest.write_text(json.dumps(dict(self.manifest, version="99.0.0")),
                            encoding="utf-8")
        guide = self.package / "GUIDE.md"
        guide.write_text(guide.read_text(encoding="utf-8") + "\nRecovery payload marker.\n",
                         encoding="utf-8")
        repaired = self.cli("plugin", "validate", self.package, "--json")
        self.assertTrue(json.loads(repaired.stdout)["success"])
        for operation in ("update", "update", "uninstall", "uninstall", "install", "install"):
            with self.subTest(operation=operation):
                result = self.cli("plugin", operation, plugin_id, success=False)
                records = json.loads(self.cli("plugin", "list", "--json").stdout)
                if operation == "uninstall":
                    # The repeated uninstall can fail; it must leave nothing installed.
                    self.assertEqual(records, [])
                else:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(len(records), 1, records)
                    self.assertEqual(records[0]["id"], plugin_id)
                    self.assertEqual(records[0]["version"], "99.0.0")
                    self.assertFalse(records[0].get("errors"), records)
                    self.assertIn(f"({PLUGIN}) 99.0.0",
                                  self.cli("plugin", "details", PLUGIN).stdout)
                    installed = Path(records[0]["installPath"])
                    for name in PAYLOAD:
                        self.assertEqual((installed / name).read_bytes(),
                                         (self.package / name).read_bytes())
                self.assertIn(marker, self.cli("mcp", "get", "chrome-devtools").stdout)
                self.assertEqual(sentinel.read_bytes(), b"synthetic profile data")


if __name__ == "__main__":
    unittest.main()
