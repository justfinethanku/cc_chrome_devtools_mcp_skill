# Chrome DevTools MCP Skill

Give Claude Code eyes for your frontend: inspect rendered pages, capture network
requests, record performance traces, and automate Chrome interactions. This
plugin supplies instructions; the separate `chrome-devtools-mcp` server supplies
the tools. Even Mike Dion would be impressed.

## Features

- Browser automation with snapshots, element UIDs, forms, dialogs, and tabs.
- Performance traces and insight analysis, with lab and field data kept distinct.
- Request/response and console inspection.
- Accessibility-tree inspection and keyboard testing to investigate specific issues.
- Viewport, CPU, network, and media emulation.
- Screenshots and recordings for reviewing observed behavior.

The checked v1.12.0 server exposes 32 tools by default. Snapshots do not certify
WCAG compliance, request lists are not HAR exports, and Chrome emulation does
not test other browser engines. See [tool contracts](TOOLS.md) and
[measurement limits](METRICS.md).

## Prerequisites

Install Claude Code, a Chrome/Chromium browser on the MCP server host, and a
Node.js version supported by the server. The v1.12.0 npm package declares
`^20.19.0 || ^22.12.0 || >=23`; use a supported Node LTS release satisfying that
range. Verify prerequisites in your terminal:

```bash
claude --version
node --version
npm --version
```

Check the actual Chrome binary's `--version` on the server host. If it is not
automatically detected, set `--executablePath` as described in
[configuration examples](GUIDE.md#configuration-examples).

Setup was checked on November 6, 2026 with Claude Code 2.1.318, Node.js 22.22.2,
and `chrome-devtools-mcp@1.12.0` on Linux. This audit verified isolated plugin
installation, MCP registration, initialization, and tool discovery. It did not
launch Chrome or execute browser workflows; the audit host has no Chrome binary
on its command path. The workflow JSON examples passed the discovered input
schemas. These checks do not guarantee browser startup on your machine.

## Installation

### Install with the plugin manager

Run these commands in your terminal:

```bash
claude plugin marketplace add https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill
claude plugin install cc_chrome_devtools_mcp_skill@cc_chrome_devtools_mcp_skill-plugin-marketplace
claude plugin details cc_chrome_devtools_mcp_skill
```

The details should show one skill and zero bundled MCP servers. Configure the
server separately in the next step. Restart Claude Code after installation to
load the skill into your session.

### Register the MCP server

For this skill to work across projects, register the server at user scope:

```bash
claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@1.12.0 --isolated=true
claude mcp get chrome-devtools
```

The result should identify `npx`, the pinned package version, and the isolation
flag. The CLI manages the configuration in `~/.claude.json`; do not create
`~/.claude/mcp_settings.json`. For a shared project registration, use
`--scope project` from that project's root; this writes `.mcp.json` and requires
project approval in Claude Code. The default `local` scope is specific to the
current project and is not the same as user scope.

If `chrome-devtools` is already registered, inspect it with `claude mcp get`
before updating it; do not overwrite an existing attachment or custom binary
configuration blindly. See [Claude Code MCP scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes).

The package version is pinned to the version used for the examples. To upgrade,
review upstream releases, update the package argument, and recheck tool discovery
and schemas. `@latest` changes independently of this skill.

When MCP launches Chrome, `--isolated=true` creates a temporary profile that is
cleaned up after the browser closes. It does not redact browser data or isolate
an attached browser. Read [security considerations](SKILL.md#security-considerations)
before using accounts or exporting captures.

### Verify the connection

Restart Claude Code, open `/mcp`, and check that `chrome-devtools` connects. Ask
Claude to list available pages, open a test page, and take a snapshot. The browser
starts on first browser tool use, so a successful connection or tools listing
does not prove Chrome can launch. Record the returned page ID for later calls.

### Optional: install as a manual skill

Use this instead of plugin installation. Clone the repository:

```bash
git clone https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill
```

Create the user skills directory before copying:

```bash
mkdir -p ~/.claude/skills
cp -r cc_chrome_devtools_mcp_skill ~/.claude/skills/
```

For one project, run the following from that project's root, replacing
`/PATH/TO/cc_chrome_devtools_mcp_skill` with the cloned repository path:

```bash
mkdir -p .claude/skills
cp -r /PATH/TO/cc_chrome_devtools_mcp_skill .claude/skills/
```

Copy the whole package, including its supporting Markdown files. Register the
MCP server separately as described above, then restart Claude Code.

## Usage

Give Claude a URL and a concrete task, for example:

- "Trace the loading performance of https://example.com and explain the slowest insight."
- "Inspect the login form's labels and keyboard focus behavior."
- "Find failed API requests in this test checkout flow."
- "Test this page at a 390 by 844 mobile viewport."
- "Fill and submit the contact form using the test account."

Use `list_pages` or `new_page` to obtain a numeric `pageId`; most tools in this
version require it. Element UIDs come from a fresh `take_snapshot` call.
`wait_for` takes an array of strings. Emulation uses the single `emulate` tool.
See [workflows](WORKFLOWS.md) for complete call sequences.

## Connect to existing Chrome instance

Attachment gives MCP access to that browser's existing tabs, cookies, and sessions.
`--isolated=true` does not create a temporary profile when attaching. For a separate
test browser on Linux, create a fresh profile before enabling remote debugging:

```bash
CHROME_TEST_PROFILE="$(mktemp -d "${TMPDIR:-/tmp}/chrome-devtools-test.XXXXXX")"
printf 'Test profile: %s\n' "$CHROME_TEST_PROFILE"
google-chrome --remote-debugging-address=127.0.0.1 --remote-debugging-port=9222 --user-data-dir="$CHROME_TEST_PROFILE"
```

Replace `google-chrome` with your actual executable if needed. This Linux
launcher was checked with an argument-recording stub, not a real browser.
Chrome 136 and later require a non-default user data directory for these debugging
switches. Keep the debugging port on loopback and use test accounts. After closing
the browser, remove the printed test profile directory if you no longer need it;
MCP does not clean up an externally launched browser's profile.

Use the attachment configuration in [the configuration guide](GUIDE.md#configuration-examples).
See [the upstream connection guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md#connecting-to-a-running-chrome-instance)
and [Chrome's debugging requirements](https://developer.chrome.com/blog/remote-debugging-port).

## Documentation

- [SKILL.md](SKILL.md): Compact task entrypoint and security guidance.
- [GUIDE.md](GUIDE.md): Configuration flags, captures, and troubleshooting.
- [TOOLS.md](TOOLS.md): Versioned tool inputs and constraints.
- [WORKFLOWS.md](WORKFLOWS.md): Performance, network, accessibility, automation,
  tab management, and emulation procedures.
- [METRICS.md](METRICS.md): Core Web Vitals thresholds and measurement limits.

## Plugin structure and validation

This repository ships one instruction skill. Claude Code loads the root
[SKILL.md](SKILL.md); its supporting Markdown files stay beside it so both
marketplace and manual skill installs use the same content.

The entrypoint links to supporting documents for conditional reading, so routine
browser tasks do not load the full setup and example guide. This follows
[Claude Code's supporting-file guidance](https://code.claude.com/docs/en/skills#add-supporting-files).
Reading every reference still loads its full content; this changes the default
instruction payload, not the external MCP server or browser speed.

[plugin.json](.claude-plugin/plugin.json) owns plugin metadata and the release
version. [marketplace.json](.claude-plugin/marketplace.json) maps the published
plugin name to this repository root and reads its metadata from that manifest.
Bump the version in `plugin.json` when releasing an update.

Configure the MCP server separately. The external `chrome-devtools-mcp` process
supplies tools and manages the Chrome connection,
as described in [Prerequisites](#prerequisites).

For local packaging checks, run these from the repository root:

```bash
claude plugin validate .
claude --plugin-dir . plugin details cc_chrome_devtools_mcp_skill
```

The details should show one skill, `cc_chrome_devtools_mcp_skill`, and zero bundled
MCP servers. See the official [manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
and [component loading rules](https://code.claude.com/docs/en/plugins/components#skills).

### Automated package tests

With Python 3.9+ and Claude Code installed, run from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The suite checks direct loading from an arbitrarily named checkout, local
marketplace discovery and installation, the installed skill inventory and file
contents, manual-copy reference availability, and rejection of invalid metadata.
It creates temporary home and Claude configuration directories and removes them
after each test. It runs plugin management commands only; no model calls, MCP
server or Chrome session are started. A missing Claude CLI fails the installation
tests; set `CLAUDE_BIN` if its executable has a different name or path.

These checks cover this instruction package. They do not verify the external
MCP server's tools, browser behavior or the accuracy of every workflow example.

## Contributing

Report issues or propose changes in [the GitHub repository](https://github.com/justfinethanku/cc_chrome_devtools_mcp_skill).
When updating examples, check the published server's live schemas as well as the
package installation tests.

## License

MIT. See [LICENSE](LICENSE).

## Author

[Jonathan Edwards](https://github.com/justfinethanku).
