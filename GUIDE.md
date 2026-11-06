# Chrome DevTools setup and configuration guide

This package supplies instructions to Claude Code. Install and configure the
external MCP server separately. Setup and tool discovery were checked with
Claude Code 2.1.318, Node.js 22.22.2, and `chrome-devtools-mcp@1.12.0` on Linux
on November 6, 2026. Browser startup and end-to-end page interactions were not
verified on that audit host, which has no Chrome executable on its command path.

## Quick start

Follow [the README prerequisites and setup](README.md#prerequisites) for the
maintained installation procedure. The README covers plugin and manual skill
installation, registration scope, and verification. Avoid installing the same
skill through both paths.

After setup, ask for a specific page and task. Start by listing pages, then use
the returned `pageId` for page-targeted tools. See [tool inputs](TOOLS.md#tool-inputs)
and [task workflows](WORKFLOWS.md). Available tools and arguments depend on the
server version and category flags; this reference targets the default v1.12.0
inventory, not upstream development HEAD.

## Configuration options

Run the installed version's help before changing its flags:

```bash
npx -y chrome-devtools-mcp@1.12.0 --help
```

The examples pin the version used for validation. To upgrade, choose a released
version, review its release/security notes, update the package argument, and
check tool discovery and the changed schemas again.

| Option | Purpose |
| --- | --- |
| `--isolated=true` | Use a temporary profile when the server launches Chrome. Does not isolate an attached browser. |
| `--headless=true` | Launch Chrome without a visible window. Chrome must still be installed. |
| `--executablePath=PATH` | Select a Chrome/Chromium executable on the server host. |
| `--channel=stable` | Choose stable, beta, dev, or canary. |
| `--viewport=1920x1080` | Set launch viewport dimensions. |
| `--userDataDir=PATH` | Choose a persistent launch profile instead of a temporary profile. |
| `--browserUrl=URL` | Attach through an existing browser's HTTP debugging endpoint. |
| `--wsEndpoint=URL` | Attach through its WebSocket endpoint instead. |
| `--wsHeaders=JSON` | Pass headers to an already authenticated WebSocket endpoint. |
| `--proxyServer=URL` | Set a launch proxy. |
| `--logFile=PATH` | Write potentially sensitive debug logs. `NODE_DEBUG=*` enables verbose Node debugging. |
| `--no-usage-statistics` | Disable the server's usage statistics. |
| `--no-performance-crux` | Disable trace URL lookups against the CrUX API. |
| `--workspace=PATH` | Allow file tools to access a directory; repeat for multiple roots. |

The correct persistent-profile flag is `--userDataDir`; use the spelling in the
installed help. Connection and launch options serve different modes. Do not
combine attachment with expectations of temporary-profile cleanup.

## Configuration examples

These are MCP configuration objects. For Claude Code project scope, save one as
`.mcp.json` at the project root and approve it through Claude Code's normal MCP
flow. User and local scope are managed by `claude mcp add`; they are stored in
`~/.claude.json` (or the configured Claude config directory), not
`~/.claude/mcp_settings.json`. See [Claude Code's scope documentation](https://code.claude.com/docs/en/mcp#mcp-installation-scopes).

Launch an isolated headless test browser with a chosen viewport:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@1.12.0", "--isolated=true", "--headless=true", "--viewport=1920x1080"]
    }
  }
}
```

For custom binaries, add an `--executablePath=PATH` argument using the actual
path on the MCP server host. The configuration can initialize even when Chrome
is missing because browser startup is lazy; tool discovery alone does not prove
a browser can launch.

Attach to a separately launched test browser only after following
[the external-browser setup](README.md#connect-to-existing-chrome-instance):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@1.12.0", "--browserUrl=http://127.0.0.1:9222"]
    }
  }
}
```

## Captures and filesystem access

Paths are resolved on the MCP server, except uploads whose paths must be
available to the browser. Without negotiated MCP roots or explicit workspaces,
v1.12.0 file tools default to the OS temporary directory. Use a directory allowed
by the current roots/workspace configuration; create its parent first. Prefer a
specific artifact directory over broad filesystem access. A valid input schema
does not establish path permission or file availability.

Request lists are not HAR files. Use Chrome DevTools for native HAR export.
Snapshots expose the accessibility tree; they cannot certify WCAG compliance.
See [tool constraints](TOOLS.md#important-constraints) and
[measurement interpretation](METRICS.md#field-and-lab-data).

## Security considerations

Read [the complete security guidance](SKILL.md#security-considerations), including
profile lifecycle, untrusted page content, artifact redaction, and outbound data
settings. Temporary profiles do not hide browser data from the MCP client.
Attached browsers retain their existing sessions. A loopback debugging port can
be controlled by other local processes.

## Troubleshooting

- **Server missing:** run `claude mcp get chrome-devtools` from the intended
  project. Check registration scope, project approvals, and restart the session
  after configuration changes.
- **Server exits before discovery:** run the pinned package's `--help`, check
  Node compatibility and package access, and inspect `/mcp` in Claude Code.
- **Chrome launch fails:** verify the executable and its version on the server
  host. Supply `--executablePath` if discovery cannot find it. Inspect the actual
  error before changing OS permissions or sandbox settings.
- **Tool or argument rejected:** inspect the connected server's schema. Old
  examples use tab indexes, scalar waits, and separate emulation tools that do
  not match this version. Do not infer schemas from another release.
- **Capture write rejected:** check the server's allowed roots/workspaces and
  parent directory. Use a permitted path rather than disabling all restrictions.

See the [official upstream configuration guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md)
and [connection guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md)
for options beyond this package's tested setup.
